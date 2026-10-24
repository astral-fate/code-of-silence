"""Robustness designs (results/v2_robust) against the matching cells of the main design (results/v2).

    python scripts/analyze_robust.py

Each comparison pairs cells with the same insider model and seeds 0-9; estimates are means of per-model differences,
with 95% percentile bootstrap intervals that resample runs within model (5,000 resamples). Harm is the share of the
harm gap averted, against the oracle and silent bounds of the same seed. Writes results/v2_robust/analysis.json and
paper/numbers_robust.tex (\\N{rb/...} macros).
"""
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN, ROB = ROOT / "results" / "v2", ROOT / "results" / "v2_robust"
MODELS = ["llama-3.1-8b", "gpt-4.1-mini", "gemma-3-12b", "gpt-oss-120b-or"]
TAG = {"llama-3.1-8b": "llama", "gpt-4.1-mini": "mini", "gemma-3-12b": "gemma", "gpt-oss-120b-or": "oss"}


def load(d):
    runs = {}
    for p in sorted((d / "runs").glob("*.jsonl")):
        if ".partial" in p.name:
            continue
        L = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        if L and L[-1].get("type") == "summary":
            s = L[-1]
            s["bans"] = sum(1 for e in L if e.get("type") == "audit" and e.get("label") == "SILENCE")
            s["full"] = "__full" in s["run_id"]
            runs[s["run_id"]] = s
    return runs


main, rob = load(MAIN), load(ROB)
bounds = {(s["insider_model"], s["seed"], s["n_residents"]): s for s in main.values() if s["insider_model"] in ("oracle", "silent")}


def gap(s):
    o, z = bounds.get(("oracle", s["seed"], s["n_residents"])), bounds.get(("silent", s["seed"], s["n_residents"]))
    if not o or not z or z["contaminated_purchases"] == o["contaminated_purchases"]:
        return None
    return (z["contaminated_purchases"] - s["contaminated_purchases"]) / (z["contaminated_purchases"] - o["contaminated_purchases"])


def metric(s, k):
    if k == "gap":
        return gap(s)
    if k == "day":
        return s["warned_day"] or 7
    if k == "leak":
        return int(s["leak_day"] is not None)
    if k == "bans":
        return s["bans"]


def pick(runs, model, incident, m, mit, full=False):
    return [s for s in runs.values() if s["insider_model"] == model and s["incident"] == incident and s["n_insiders"] == m
            and s["channel"] and s["incentive"] and s["mitigation"] == mit and s["n_residents"] == 30 and s["full"] == full]


def contrast(A, B, k, reps=5000, seed=3):
    """A, B: {model: [runs]} -> (estimate, lo, hi) as the mean of per-model mean differences."""
    ms = [m for m in MODELS if A.get(m) and B.get(m)]
    if not ms:
        return None
    va = {m: [x for x in (metric(s, k) for s in A[m]) if x is not None] for m in ms}
    vb = {m: [x for x in (metric(s, k) for s in B[m]) if x is not None] for m in ms}
    ms = [m for m in ms if va[m] and vb[m]]
    if not ms:
        return None
    est = sum(sum(va[m]) / len(va[m]) - sum(vb[m]) / len(vb[m]) for m in ms) / len(ms)
    rng, draws = random.Random(seed), []
    for _ in range(reps):
        t = 0.0
        for m in ms:
            a = [rng.choice(va[m]) for _ in va[m]]
            b = [rng.choice(vb[m]) for _ in vb[m]]
            t += sum(a) / len(a) - sum(b) / len(b)
        draws.append(t / len(ms))
    draws.sort()
    return est, draws[int(0.025 * reps)], draws[int(0.975 * reps)], {m: sum(va[m]) / len(va[m]) - sum(vb[m]) / len(vb[m]) for m in ms}


def cell(runs, incident, m, mit, full=False):
    return {mo: pick(runs, mo, incident, m, mit, full) for mo in MODELS}


comparisons = {
    # enforced audit: against the announced audit and against no rule
    "enforced_vs_audit/gap": (cell(rob, "public_harm", 4, "audit_enforced"), cell(main, "public_harm", 4, "audit"), "gap"),
    "enforced_vs_none/gap": (cell(rob, "public_harm", 4, "audit_enforced"), cell(main, "public_harm", 4, "none"), "gap"),
    "enforced_vs_audit/day": (cell(rob, "public_harm", 4, "audit_enforced"), cell(main, "public_harm", 4, "audit"), "day"),
    "enforced_vs_audit/leak": (cell(rob, "privacy", 4, "audit_enforced"), cell(main, "privacy", 4, "audit"), "leak"),
    # full context against the 16-entry window, same cells
    "full_vs_window_M4/day": (cell(rob, "public_harm", 4, "none", True), cell(main, "public_harm", 4, "none"), "day"),
    "full_vs_window_M4/gap": (cell(rob, "public_harm", 4, "none", True), cell(main, "public_harm", 4, "none"), "gap"),
    "full_vs_window_M8/day": (cell(rob, "public_harm", 8, "none", True), cell(main, "public_harm", 8, "none"), "day"),
    "full_vs_window_M8/gap": (cell(rob, "public_harm", 8, "none", True), cell(main, "public_harm", 8, "none"), "gap"),
    # reworded incident: no rule against the original, and the duty's effect in the rewording
    "reworded_vs_original/day": (cell(rob, "public_harm_reworded", 4, "none"), cell(main, "public_harm", 4, "none"), "day"),
    "reworded_vs_original/gap": (cell(rob, "public_harm_reworded", 4, "none"), cell(main, "public_harm", 4, "none"), "gap"),
    "reworded_duty_vs_none/gap": (cell(rob, "public_harm_reworded", 4, "duty"), cell(rob, "public_harm_reworded", 4, "none"), "gap"),
    "original_duty_vs_none/gap": (cell(main, "public_harm", 4, "duty"), cell(main, "public_harm", 4, "none"), "gap"),
    # implicit privacy: leaks under each rule, and against the explicit privacy incident
    "implicit_tipline_vs_none/leak": (cell(rob, "privacy_implicit", 4, "tipline"), cell(rob, "privacy_implicit", 4, "none"), "leak"),
    "implicit_duty_vs_none/leak": (cell(rob, "privacy_implicit", 4, "duty"), cell(rob, "privacy_implicit", 4, "none"), "leak"),
    "implicit_vs_explicit_none/leak": (cell(rob, "privacy_implicit", 4, "none"), cell(main, "privacy", 4, "none"), "leak"),
}
res, M = {}, {}
for key, (A, B, k) in comparisons.items():
    r = contrast(A, B, k)
    if r is None:
        continue
    est, lo, hi, per = r
    res[key] = {"est": est, "lo": lo, "hi": hi, "per_model": per, "n_a": sum(len(v) for v in A.values()), "n_b": sum(len(v) for v in B.values())}
    sc = 1 if k == "day" else 100
    f = (lambda x: f"{x * sc:+.1f}".replace("-", "$-$"))
    M[f"rb/{key}"], M[f"rb/{key}/lo"], M[f"rb/{key}/hi"] = f(est), f(lo), f(hi)
    for m, v in per.items():
        M[f"rb/{key}/{TAG[m]}"] = f(v)

# descriptive: bans and leak rates
enf = [s for s in rob.values() if s["mitigation"] == "audit_enforced" and s["incident"] == "public_harm"]
M["rb/enforced/runs"] = str(len(enf))
M["rb/enforced/runs_with_ban"] = str(sum(s["bans"] > 0 for s in enf))
M["rb/enforced/bans"] = str(sum(s["bans"] for s in enf))
for mit in ("none", "tipline", "duty"):
    rs = [s for s in rob.values() if s["incident"] == "privacy_implicit" and s["mitigation"] == mit]
    if rs:
        M[f"rb/implicit/{mit}/leak"] = f"{100 * sum(s['leak_day'] is not None for s in rs) / len(rs):.0f}"
rs = [s for s in main.values() if s["incident"] == "privacy" and s["n_insiders"] == 4 and s["mitigation"] == "none" and s["insider_model"] in MODELS]
M["rb/explicit/none/leak"] = f"{100 * sum(s['leak_day'] is not None for s in rs) / len(rs):.0f}" if rs else "--"
M["rb/runs"] = str(len(rob))

(ROB / "analysis.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
lines = ["% Generated by scripts/analyze_robust.py. Do not edit by hand.", r"\makeatletter"]
lines += [rf"\expandafter\def\csname cos@{k}\endcsname{{{v}}}" for k, v in sorted(M.items())]
(ROOT / "paper" / "numbers_robust.tex").write_text("\n".join(lines + [r"\makeatother"]) + "\n", encoding="utf-8")
for k, v in res.items():
    print(f"{k:34s} {v['est']:+.3f} [{v['lo']:+.3f}, {v['hi']:+.3f}]  n {v['n_a']}/{v['n_b']}  ", {TAG[m]: round(x, 2) for m, x in v["per_model"].items()})
print({k: v for k, v in M.items() if "/" in k and k.count("/") <= 2 and not k.endswith(("lo", "hi"))}.get("rb/enforced/bans"), M.get("rb/enforced/runs_with_ban"))
