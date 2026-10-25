# Editorial decision: Code of Silence

Panel (25 Oct 2026). Five reviewers in role-separated seats: Journal-Fit (EIC.md), Methodology (R1_methodology.md), Domain (R2_domain.md), Perspective (R3_perspective.md), Devil's Advocate (DA.md). All five ran on the same model family in fresh contexts, with no reviewer seeing another's output, so errors may be correlated. Status: NOT_CALIBRATED.

**Decision: Major Revision** for an archival venue; a strong sprint report. Recommendations by seat: EIC, Major; R1, Major; R2, Major; R3, Minor; DA, one CRITICAL issue.

## Consensus (3 or more seats)
1. **The mixed-family result uses the wrong null** (EIC W2, R1 W1, R2, R3 #1, DA M4).
   - The first warning is the earliest warning by any insider, so independence predicts that a mixed village warns as early as its more forthcoming family.
   - Fix: test against an independence prediction built from the single-family survival curves, S_a(d)^2 · S_b(d)^2. Reword the result to "include at least one model that reliably discloses".
2. **The monitor claims overstate** (EIC, R1 W2, R2 W3, DA M6).
   - The public-post monitor is at chance (8.5% of silent villages flagged vs 8.1% of villages that warned).
   - The channel monitor's 69% comes with 31% false flags and differs by model.
   - The AUROC of 0.99 is against a different incident.
   - Fix: make the same-incident warned villages the primary negatives, report false-positive rates beside every catch rate, give per-model figures, and test a monitor that is told the incident (offline).
3. **"Collusion" and the silence-agreement label are construct problems** (EIC W7, R1 #5, R2 W1, DA M1).
   - The label counts "delay to verify" and post-warning refund messages as SILENCE.
   - Fix: split the label (conceal vs delay or verify), count agreements only before the first warning, and use "collusion" only for villages that meet the agreement criterion.
4. **The recommendations go beyond the data** (EIC W4, R3 #2, DA M7).
   - The tip line's privacy cost is not significant after correction, while the duty leaks +40 points when the private fact is unlabelled.
   - Rec (5)'s "state what must not be disclosed" was never tested.
   - Fix: rewrite Recs (4) and (5) as conditional.
5. **Sign error in the abstract and §4**: "delayed by −1.0 day", "reduced by −16.5" (EIC W1, R1, R2, DA). Fix: use magnitudes after directional verbs.

## Devil's Advocate CRITICAL issue
C1 (the channel is confounded with an extra prompt clause and output field): **upheld as unresolved.** It is corroborated by EIC W3, and R1 W3 raises the same issue for the tip line. A private-notes load-control cell (40 villages) is running. The tip line needs a field-only cell, or at least the share of warnings delivered by tip.

## Other high-value findings
- R1: the Gemma relabel covered a stratified sample of 876 items, not "every post and tip". Fix the wording.
- R1: "did not favour its own family" isn't supported (89% vs 66–67%).
- R1: the enforced audit, compared with no rule, cut harm averted by 10.5 points. Report it.
- R1: the minimum detectable difference is 2.86 days, not "about two".
- R1: per-model effects should be shown next to the pooled ones (duty +80 for Gemma, 0 for GPT-OSS).
- R2: AI-LieDar and Järviniemi & Hubinger are closer precedents. Verify them, cite them and restate the novelty.
- EIC and DA: the "companion study" needs a citation.
- R3: the manager-ordered cover-up deserves a paragraph as a second threat model (GPT-4.1-mini obeyed in 10 of 10 villages).
- EIC and DA: null results are worded as equivalence ("no quieter"). Reword them.

## Revision roadmap (in source order)
1. Fix the sign error.
2. Run the notes control (running).
3. Analyse the tip field: the share of warnings delivered by tip, and optionally a field-only cell.
4. Recompute the mixed-family result against the independence null.
5. Reframe the monitor: same-incident negatives, false-positive rates, per-model figures, and an informed monitor.
6. Split the silence-agreement label and restrict it to before the first warning.
7. Rewrite Recommendations (4) and (5); add the operator-order threat.
8. Make the Methods and judge wording accurate: the 876-item sample, self-family agreement, and the minimum detectable difference.
9. Report the enforced audit against no rule, and show per-model effects.
10. Add verified related work and restate the novelty.
11. Cite the companion study.
