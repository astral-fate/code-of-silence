"""results/<dir>/analysis/numbers.json (+ offline summary) -> paper/numbers.tex, so the paper never hard-codes a statistic.

    python scripts/make_macros.py results/v2

The paper reads every number through \\N{key}; a missing key prints as a bold ??key, so it cannot pass unnoticed.
Shares are printed in percentage points, days to one decimal.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / sys.argv[1] if len(sys.argv) > 1 else ROOT / "results" / "v2"
n = json.loads((out / "analysis" / "numbers.json").read_text(encoding="utf-8"))
M = {}

MODEL = {"llama-3.1-8b": "llama", "gpt-4.1-mini": "mini", "gemma-3-12b": "gemma", "gpt-oss-120b-or": "oss"}
DAYS = ("warnday", "warn_day")


def sgn(x, nd=1):
    s = f"{x:+.{nd}f}"
    return s.replace("-", "$-$")


def pfmt(p):
    if p is None:
        return "--"
    return "< 0.001" if p < 0.001 else f"= {p:.3f}" if p < 0.01 else f"= {p:.2f}"


def put_contrast(key, c, scale):
    if not c or c.get("estimate") is None:
        return
    M[f"{key}/est"] = sgn(c["estimate"] * scale)
    lo, hi = c.get("ci95") or (None, None)
    if lo is not None:
        M[f"{key}/lo"], M[f"{key}/hi"] = sgn(lo * scale), sgn(hi * scale)
    M[f"{key}/p"] = pfmt(c.get("p_perm"))
    for m, v in (c.get("per_model") or {}).items():
        if m in MODEL and isinstance(v, (int, float)):
            M[f"{key}/{MODEL[m]}"] = sgn(v * scale)


for k, c in n["contrasts"].items():
    put_contrast(k, c, 1 if k.endswith(DAYS) else 100)
for k, c in (n.get("robust_no_parse_fail") or {}).items():
    put_contrast(f"rob/{k}", c, 1 if k.endswith(DAYS) else 100)
for fam, ps in n.get("holm", {}).items():
    for k, p in ps.items():
        M[f"holm/{fam}/{k}"] = pfmt(p)

for m, d in n.get("C2_channel_off", {}).items():
    if m in MODEL:
        M[f"C2/{MODEL[m]}"] = sgn(d["excess_silence"] * 100)
        M[f"C2/{MODEL[m]}/lo"], M[f"C2/{MODEL[m]}/hi"] = (sgn(x * 100) for x in d["ci95"])
        M[f"C2/{MODEL[m]}/p"] = pfmt(d["p_one_sided"])

# silence with the channel on, against the same independence prediction (descriptive)
for m, d in n.get("dependence", {}).items():
    if m not in MODEL or not d.get("S1"):
        continue
    for k in (2, 4, 8):
        g = d.get(f"M{k}") or {}
        if g.get("observed") and g.get("predicted"):
            ex = sum(o - p for o, p in zip(g["observed"], g["predicted"])) / len(g["observed"])
            M[f"dep/{MODEL[m]}/M{k}"] = sgn(ex * 100)
            M[f"dep/{MODEL[m]}/M{k}/day6"] = f"{round(g['observed'][-1] * g['runs'])}"
    M[f"dep/{MODEL[m]}/S1/day6"] = f"{round(d['S1'][-1] * d['solo_runs'])}"

for b in ("oracle", "silent"):
    bd = n.get(f"bound_{b}") or {}
    if bd:
        M[f"bound/{b}/sick"] = f"{100 * bd['frac_sick']:.1f}"
        M[f"bound/{b}/cp"] = f"{bd['cp_per_res']:.2f}"

# per-cell descriptive values (warned villages of 10, mean residents sick, mean warning day)
for r in n.get("cells", []):
    if r["model"] not in MODEL or r["N"] != 30:
        continue
    key = f"cell/{MODEL[r['model']]}/{r['incident']}/M{r['M']}/ch{int(r['channel'])}/inc{int(r['incentive'])}/{r['rule']}"
    M[f"{key}/warned"] = str(r["warned"])
    M[f"{key}/day"] = f"{r['mean_warn_day']:.1f}"
    if r.get("any_leak") is not None:
        M[f"{key}/leak"] = str(r["any_leak"])
    M[f"{key}/runs"] = str(r["runs"])

M["n/runs"] = f"{n['n_runs']:,}"
M["placeholders"] = str(n.get("placeholder_posted_total", "--"))
M["placeholders/changed"] = str(n.get("runs_warned_day_changed_by_placeholders", "--"))
M["mde"] = f"{n.get('mde_warn_day_per_model', 0):.1f}"

# offline relabel and monitor (results/<dir>/offline/summary.json, written by offline_checks.py)
off = out / "offline" / "summary.json"
if off.exists():
    o = json.loads(off.read_text(encoding="utf-8"))
    for m, d in o.items():
        if m not in MODEL or not isinstance(d, dict):
            continue
        for k in ("false_reassure", "half_truth", "promote"):
            v = d.get(f"share_runs_pre_warning_{k}")
            if v is not None:
                M[f"off/{MODEL[m]}/pre/{k}"] = f"{100 * v:.0f}"
        if d.get("mean_cp_online"):
            M[f"off/{MODEL[m]}/cp_online"] = f"{d['mean_cp_online']:.1f}"
            M[f"off/{MODEL[m]}/cp_protect"] = f"{d['mean_cp_protect_counts']:.1f}"
            M[f"off/{MODEL[m]}/protect_share"] = f"{100 * (1 - d['mean_cp_protect_counts'] / d['mean_cp_online']):.0f}"
    for view, d in (o.get("monitor_all_models") or {}).items():
        v = "public" if view.endswith("public") else "channel"
        def put(key, r):
            M[f"mon/{v}/{key}"] = f"{100 * r['flag_rate']:.0f}"
            M[f"mon/{v}/{key}/ci"] = f"{100 * r['ci95'][0]:.0f}--{100 * r['ci95'][1]:.0f}"
            M[f"mon/{v}/{key}/n"] = str(r["n"])
        put("pc", d["positive_control_flag_rate"])
        put("privacy", d["fpr_privacy_hard_negatives"])
        for day in (2, 3):
            t = d.get(f"truth_no_warning_by_day{day}") or {}
            if t.get("tpr"):
                put(f"tpr{day}", t["tpr"])
            for fk, fv in t.items():
                if fk.startswith("fpr") and isinstance(fv, dict) and "flag_rate" in fv:
                    put(f"{fk}{day}", fv)

# channel labels, agreement criterion, second judge (analysis/numbers.json, from judge_offline.jsonl)
cl = n.get("channel_labels") or {}
tot = sum(v for k, v in cl.items() if k in ("SILENCE", "DISCLOSE", "OTHER"))
for k in ("SILENCE", "DISCLOSE", "OTHER"):
    if tot:
        M[f"chan/{k.lower()}"] = f"{100 * cl.get(k, 0) / tot:.0f}"
M["chan/n"] = f"{tot:,}"
for key, c in (n.get("collusion_criterion") or {}).items():
    m, mit = key.split("|")
    tag = "all" if m == "all" else MODEL.get(m)
    if tag:
        M[f"crit/{tag}/{mit}"] = f"{c['runs_with_2plus_endorsers']}"
        M[f"crit/{tag}/{mit}/runs"] = f"{c['runs']}"
        if c["runs"]:
            M[f"crit/{tag}/{mit}/share"] = f"{100 * c['runs_with_2plus_endorsers'] / c['runs']:.0f}"
        for w in ("with", "without"):
            if c.get(f"mean_warn_day_{w}") is not None:
                M[f"crit/{tag}/{mit}/day_{w}"] = f"{c[f'mean_warn_day_{w}']:.1f}"
sd = n.get("say_do_gap") or {}
if sd.get("share") is not None:
    M["saydo/share"] = f"{100 * sd['share']:.0f}"
    M["saydo/n"] = f"{sd['disclose_insider_days']:,}"
for inc, k in (n.get("second_judge_kappa") or {}).items():
    if k is not None:
        M[f"kappa/{inc}"] = f"{k:.2f}"
if n.get("second_judge_agreement") is not None:
    M["kappa/agreement"] = f"{100 * n['second_judge_agreement']:.0f}"

lines = ["% Generated by scripts/make_macros.py from results/analysis. Do not edit by hand.", r"\makeatletter",
         r"\providecommand{\N}[1]{\ifcsname cos@#1\endcsname\csname cos@#1\endcsname\else\textbf{??#1}\fi}"]
lines += [rf"\expandafter\def\csname cos@{k}\endcsname{{{v}}}" for k, v in sorted(M.items())]
lines += [r"\makeatother"]
(ROOT / "paper" / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(len(M), "macros -> paper/numbers.tex")
