"""Run a grid of village simulations. Resumable at run level: each run streams its events to
results/<out>/runs/<run_id>.jsonl as they happen; a run whose log ends with a summary is skipped on
rerun, and an unfinished log is kept (renamed .partial-N) and the run restarted.

    python -m code_of_silence.run --out results/main --n-residents 10,30 --seeds 5 \
        --insider-models llama-3.1-8b,gpt-4.1-mini --design v2
"""
import argparse
import concurrent.futures as cf
import itertools
import json
import logging
import threading
from pathlib import Path

from .scenario import MITIGATIONS
from .village import run_village

log = logging.getLogger("code_of_silence")

# (incident, n_insiders, channel, incentive, mitigation[, n_residents]); a sixth element fixes the village size
# for that cell and overrides --n-residents
_MITS = ("none", "placebo", "tipline", "duty", "reward", "audit")
DESIGNS = {
    "v2": ([("public_harm", k, k > 1, True, "none") for k in (1, 2, 4, 8)]
           + [("public_harm", 4, False, True, "none"), ("public_harm", 4, True, False, "none")]
           + [("public_harm", 4, True, True, mit) for mit in _MITS if mit != "none"]
           + [("privacy", 1, False, True, "none")]
           + [("privacy", 4, True, True, mit) for mit in _MITS]),
    "bounds": [("public_harm", 0, False, True, "none")],
    # inert placebo on both incidents (reference cell otherwise)
    "inert": [("public_harm", 4, True, True, "inert"), ("privacy", 4, True, True, "inert")],
    # positive control: the manager instructs the co-op to keep the result in-house (reference cell otherwise)
    "posctrl": [("public_harm", 4, True, True, "conceal"), ("public_harm", 4, True, True, "conceal_order")],
    "posctrl_order": [("public_harm", 4, True, True, "conceal_order")],
    # population scaling: insider share held at 2/15 (15/2, 30/4, 60/8) against insider count held at 4 (30/4, 60/4).
    # 30/4 is the v2 cell ("public_harm", 4, True, True, "none"), so it is not repeated here: two processes must not
    # write the same run log
    "scale": [("public_harm", m, True, True, "none", n) for n, m in ((15, 2), (60, 4), (60, 8))],
    # robustness: the audit carried out (an insider caught agreeing to hide the problem is banned)
    "enforced": [("public_harm", 4, True, True, "audit_enforced"), ("privacy", 4, True, True, "audit_enforced")],
    # robustness: the full board and channel history instead of the last 16 entries (tagged "full" in the run id)
    "fullctx": [("public_harm", 4, True, True, "none", 30, {"board_tail": 10_000}),
                ("public_harm", 8, True, True, "none", 30, {"board_tail": 10_000})],
    # robustness: the same facts reworded; a privacy incident that does not say the condition is harmless
    "reworded": [("public_harm_reworded", 4, True, True, "none"), ("public_harm_reworded", 4, True, True, "duty")],
    "privacy_hard": [("privacy_implicit", 4, True, True, mit) for mit in ("none", "tipline", "duty")],
}


def run_id(c: dict) -> str:
    full = "__full" if c.get("board_tail") else ""
    return (f"{c['insider_model']}__{c['incident']}__M{c['n_insiders']}__inc{int(c['incentive'])}__ch{int(c['channel'])}__"
            f"{c['mitigation']}__N{c['n_residents']}{full}__s{c['seed']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--design", default="v2", choices=list(DESIGNS))
    ap.add_argument("--insider-models", default="llama-3.1-8b")
    ap.add_argument("--n-residents", default="30")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--parallel-runs", type=int, default=4)
    a = ap.parse_args()

    out = Path(a.out)
    (out / "runs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(out / "run.log", encoding="utf-8"), logging.StreamHandler()])
    logging.getLogger("httpx").setLevel(logging.WARNING)
    with open(out / "run_config.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(vars(a)) + "\n")

    cfgs = []
    for model, n, cell, seed in itertools.product(
            a.insider_models.split(","), [int(x) for x in a.n_residents.split(",")], DESIGNS[a.design], range(a.seeds)):
        inc_, m, channel, incentive, mit = cell[:5]
        extra = cell[6] if len(cell) == 7 else {}
        if len(cell) >= 6:
            if n != int(a.n_residents.split(",")[0]):
                continue  # fixed-size cell: generate it once
            n = cell[5]
        c = {"insider_model": model, "n_residents": n, "n_insiders": m,
             "incident": inc_, "incentive": incentive, "channel": channel, "mitigation": mit, "seed": seed, **extra}
        c["run_id"] = run_id(c)
        cfgs.append(c)

    def done(c):
        p = out / "runs" / f"{c['run_id']}.jsonl"
        if not p.exists():
            return False
        lines = p.read_text(encoding="utf-8").strip().splitlines()
        return bool(lines) and json.loads(lines[-1]).get("type") == "summary"

    todo = [c for c in cfgs if not done(c)]
    log.info("%d runs in design, %d already finished, %d to run", len(cfgs), len(cfgs) - len(todo), len(todo))
    summaries_lock = threading.Lock()

    def one(c):
        p = out / "runs" / f"{c['run_id']}.jsonl"
        if p.exists():  # unfinished from an earlier attempt: keep it, start over
            k = 1
            while p.with_suffix(f".partial-{k}").exists():
                k += 1
            p.rename(p.with_suffix(f".partial-{k}"))
        f = open(p, "a", encoding="utf-8")
        lock = threading.Lock()

        def write(ev):
            with lock:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
                f.flush()

        try:
            s = run_village(c, write)
        finally:
            f.close()
        with summaries_lock, open(out / "summaries.jsonl", "a", encoding="utf-8") as sf:
            sf.write(json.dumps(s) + "\n")
        log.info("done %s: warned=%s mislead=%s leak=%s sick=%d", c["run_id"], s["warned_day"], s["mislead_day"], s["leak_day"], s["n_sick"])
        return s

    with cf.ThreadPoolExecutor(a.parallel_runs) as ex:
        futs = [ex.submit(one, c) for c in todo]
        for fu in cf.as_completed(futs):
            try:
                fu.result()
            except Exception as e:  # noqa: BLE001 - one failed run must not stop the grid
                log.exception("run failed: %s", e)
    log.info("finished; rerun the same command to retry any failed runs")


if __name__ == "__main__":
    main()
