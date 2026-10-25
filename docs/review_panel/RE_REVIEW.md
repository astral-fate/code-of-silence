# Re-review (verification): Code of Silence?

Reviewer: verification seat (re-review mode, practical form). Date: 26 Oct 2026.
Inputs read: the five round-1 reports and EDITORIAL_DECISION.md; the revised `paper/main.pdf` (all 17 pages, via `pdftotext -layout`) and `main.tex`; the five `numbers*.tex` macro files; `results/v2/analysis/{numbers,monitor_views,channel_split}.json`; `results/v2_robust/analysis.json`; and the previous version (`git show HEAD:paper/main.tex`).
Yardstick: the round-1 reports themselves. No reviewer configuration cards exist, so the criteria were taken from each report's "Suggestion" field and from the decision letter's roadmap. Status: NOT_CALIBRATED. A single seat did this review on the same model family as round 1.

## Verdict

| Venue | Round 1 | Now | Condition |
|---|---|---|---|
| Apart sprint report (Tracks 2 and 3) | Strong, minor fixes | **Accept / submit**, after fixes F1 to F6 below (all rewording, about 15 minutes) | The red "TBD: agreement" must not ship (F6). |
| Archival (NeurIPS/ICML safety track, SaTML) | Major Revision | **Minor Revision** | Fill in the hand-label agreement. Label the notes contrasts exploratory or give them a Holm p. Ideally, label the private notes and add one more capable insider (EIC W6, still only partly addressed). |

The revision does more than patch the paper. It takes the DA's CRITICAL load confound seriously, and the load control overturns the old story: private notes delay warnings more than the shared channel does. The paper now tells this new story honestly in its title, abstract, RQ2, Discussion and Conclusion. The old claims have been removed from the main text: "silence lives in the channel", "mixing breaks silence", "did not favour its own family", the 62% gap, the "companion study", and "about two days". All sign errors are fixed with the `\A{}` magnitude macro. What remains is a handful of residual overclaims, and one stale passage where the old GPT-4.1-mini SILENCE/DISCLOSE shares sit beside the new 4-way relabel and contradict it.

## 1. Traceability matrix (Major and Critical items only)

Counts: **29 items. 24 Addressed, 5 Partly, 0 Not addressed.**

| # | Seat / item | Round-1 ask (short) | Status | Anchor in revised paper (verified) | Residual |
|---|---|---|---|---|---|
| 1 | EIC W1 (Major) | Sign error: "delayed by −1.0" | Addressed | `text: Abstract "A shared private channel delayed the first warning by 1.0 day"`; `text: §4 RQ2 "delayed the first warning by 1.0 day [0.6, 1.4]"`; `text: §4 RQ3 "cut the gap averted by 16.5 points"`. All directional verbs use `\A{}`. | None |
| 2 | EIC W2 (Major) | Mixing tested against the wrong null; Rec (4) | Addressed | `text: §3.2 "independence predicts that a 2+2 village is still silent at day d with probability sqrt(S_a(d) S_b(d))"`; `text: §4 Mixed families "+0.1 [+0.0, +0.3]" / "+0.0 [-0.3, +0.6]"`; `text: §5 Rec (4) "Include at least one model that reliably discloses"` | "exactly" overclaims (F7) |
| 3 | EIC W3 (Major) | Channel confounded with output load; notes control | Addressed | `table: Table 1 "Private notes vs no field +1.8 [+1.5, +2.2]"`; `text: §3.2 "Private notes (load control) ... same place in the system prompt, an extra JSON field in the same position"` | Abstract's "not from coordination" is stronger than the design supports (F2). Notes contrasts are not placed in a Holm family (F8). |
| 4 | EIC W4 (Major) | Privacy-cost contradiction in Discussion | Addressed | `text: §5 "No rule's privacy cost on the labelled incident survived correction, but the duty and the tip line both leaked an unlabelled private fact heavily"` | None |
| 5 | EIC W6 (Major) | Effects concentrated in one small model; frontier relevance | Partly | `text: Abstract "mostly in the one model that often stayed silent"`; `text: App. A Lim. 6 "Few seeds, few hesitant models"` | No capable or frontier insider under stronger pressure. Lim. 6 misattributes the effects to Llama (F9). |
| 6 | EIC W7 (Major) | SILENCE label conflates delay with concealment | Addressed | `text: §3.3 "CONCEAL ... DELAY (proposes waiting, for example to verify, without proposing to hide it)"`; `text: §4 RQ2 "18% proposed concealment and 12% proposed waiting"` | The old 23%/55% SILENCE/DISCLOSE shares are still in RQ2 and contradict "mostly talk of disclosure" (F1). No verbatim CONCEAL vs DELAY examples. |
| 7 | R1 W1 (Major) | Mixed null: S_a·S_b, channel effect inside the mixture | Addressed | `text: §4 Mixed families`; `text: App. D "within the Gemma-3-12B and GPT-4.1-mini mixture, the channel delayed the first warning by 1.3 days [1.0, 1.6]"` | None |
| 8 | R1 W2 (Major) | Monitor: same-incident negatives, FPR, per-model, informed | Addressed | `text: §3.3 "the primary negatives are harm villages that warned by then"`; `text: §4 "flagged 8% [5–14] of silent villages and 8% [6–11] of warned ones"`; `table: Table 4 (per-model AUROC, FPR warned)` | The abstract mixes the binary monitor ("at chance") with the scored informed view (F3). The informed view's threshold is 1/10, so it flags every village with any score (macro `mv/informed/threshold` = 1). The threshold is still chosen in-sample. |
| 9 | R1 W3 (Major) | Tip-line effect confounded with an extra field | Addressed | `text: §4 RQ3 "Most tip-line warnings came only through the anonymous-tip field (27 of 39), but the field without the notice averted only +8.2 points [-0.7, +17.7]; the notice added +19.6"` | "averted only +8.2" carries a sign after a verb (cosmetic) |
| 10 | R1 W4 (Major) | Channel-on excess has no inference; lag vs persistent silence | Partly | `text: §4 RQ2 "+39.8, +17.0 and +16.2 points ... (descriptive)"` | Labelled descriptive, but there is no CI and no on-minus-off test. The day-1–2 lag is not separated out. The headline no longer rests on it. |
| 11 | R1 W5 (Major) | Agreement criterion: pre-warning, non-insider relabel, per model | Addressed | `text: §3.3 "at least two insiders sent CONCEAL messages before its first explicit warning"`; `text: §4 RQ2 "6 of 40 villages with no rule, nearly all Gemma-3-12B ... (associational, and largely a model difference)"` | The 4-way prompt is missing from App. F (F10) |
| 12 | R1 W6 (Major) | Judge self-preference claim; "every post" → 876 sample | Partly | `text: §3.1 "a stratified sample of 600 harm-incident and 276 privacy posts"`; `text: App. D "the data cannot tell the two apart"` | Relabel-based per-model rule estimates are not next to Table 2. Lim. 1 cites hand labels that do not exist yet (F6). |
| 13 | R1 W7 (Major) | Per-model estimates beside pooled ones | Addressed | `table: Table 1, Table 2, Table 4 per-model columns` | None |
| 14 | R2 W1 (Major) | "Collusion" reserved for the agreement criterion | Addressed | `text: §1 "use collusion only for villages in which at least two insiders endorse keeping the incident from residents ... and for the ordered cover-up"` | Morrison & Milliken (organisational silence) is still uncited. Optional. |
| 15 | R2 W2 (Major) | AI-LieDar, Järviniemi & Hubinger; "closest precedent" | Addressed | `text: §2 "conceal material facts when utility conflicts with truthfulness [36], and deceive auditors unprompted as a company assistant [16]"`; `text: §1 "The closest monitoring precedent is the omission attack"` | Ward et al. is still uncited (minor) |
| 16 | R2 W3 (Major) | Place against CoT monitoring; test an informed monitor | Addressed | `text: §2 "Monitors that read a model's private reasoning catch misbehaviour its actions hide [3]"`; `table: Table 4 "Informed: incident + public 0.81"` | None |
| 17 | R2 W4 (Major) | Mixed-family null | Addressed | As row 2 | Gemma insiders' own first posts are not reported (optional) |
| 18 | R3 W1 (Major) | Rec (4) → "include a forthcoming model" | Addressed | `text: §5 Rec (4)` | None |
| 19 | R3 W2 (Major) | Rec (5) relies on an untested safeguard | Addressed | `text: §5 Rec (5) "only behind a privacy filter or where private data are labelled; pairing a duty with a statement of what must not be disclosed is untested"` | None |
| 20 | R3 W3 (Major) | Operator-ordered silence as a second threat | Addressed | `text: §1 Threat model "We cover two threats: emergent ... and ordered silence"`; `text: §5 "Collusion where it is measured, and ordered silence"`; `text: §5 Rec (6)` | None |
| 21 | R3 W4 (Major) | Public-only routes; tiered reporting | Addressed | `text: App. A Lim. 4 "Public routes only"`; `text: App. A Future work "A route that reports to the council without posting"` | None |
| 22 | DA C1 (CRITICAL) | Channel vs load: load-matched control | Addressed | `table: Table 1`; `text: §4 RQ2 "The load control decides what that delay means"`; `text: §5 "A private place to write delays disclosure"` | Abstract and Conclusion overstate what follows from it (F2, F5) |
| 23 | DA M1 (Major) | "Is it collusion?" construct | Addressed | As rows 6 and 14; the salary null is reported (`text: §4 RQ1 "C1: +0.1 days [-0.4, +0.6]"`) | "mostly talk of disclosure" is not supported by the new labels (F1) |
| 24 | DA M2 (Major) | No-channel null worded as equivalence | Addressed | `text: §4 RQ2 "not detectably quieter ... the intervals do not rule out moderate excess silence"`; `text: §3.3 "2.9 days per model ... nulls are reported with intervals, not as equivalence"` | None |
| 25 | DA M3 (Major) | Effects carried by Gemma, the least reliably judged model | Partly | `table: Table 2 per model`; `text: App. D "The channel's effect on the gap averted ... was +10.2 under the relabel"` | The relabel replays of the notes and channel effects on warning day are not in the body |
| 26 | DA M4 (Major) | Mixed families | Addressed | As row 2 | None |
| 27 | DA M5 (Major) | Audit mechanism asserted; bans remove warners | Partly | `text: §4 RQ3 "cut the gap averted relative to no rule by 10.5 points [2.0, 18.2] ... partly because bans remove potential warners"` | "did not stop such agreements" understates it: there were twice as many as with no rule (F4). "The rules that worked tell an insider what to do" is still an untested mechanism, though now hedged ("may need"). |
| 28 | DA M6 (Major) | Monitor AUROC topic-confounded; Conclusion overclaims | Addressed | `text: §4 "Against privacy villages AUROC was higher, but topic alone can separate those"` | The new Conclusion's "can see the silence in public" overclaims, given that 45% of warned villages are flagged (F5) |
| 29 | DA M7 (Major) | Privacy-cost contradiction | Addressed | As row 4 | None |

The editorial decision's other high-value items are all **Addressed**:
- Companion study cited as [9].
- "did not favour" removed.
- Enforced audit vs no rule reported.
- MDE 2.9.
- 876-item sample described.
- Abstract robustness sentence removed.
- Null wording changed to detection language.

The R1 W9 misdirection measure is resolved by removing the +30.0 any-MISLEAD claim from the body.

## 2. Numbers spot-check (claimed vs found)

| # | Claim (location) | Claimed | Found | Verdict |
|---|---|---|---|---|
| 1 | Channel delay (Abstract, RQ2, Table 1) | 1.0 [0.6, 1.4] | analysis.json `channel_vs_nochannel/day` 0.975 [0.575, 1.375]; numbers.json C3 −0.975 | match |
| 2 | Notes delay (Abstract, Table 1) | +1.8 [+1.5, +2.2]; Gemma/Llama/mini/oss +2.8/+3.8/+0.7/+0.0 | 1.825 [1.475, 2.15]; per model 2.8/3.8/0.7/0.0 | match |
| 3 | Channel vs notes (Table 1, RQ2) | −0.9 [−1.3, −0.4]; gap +14.3 [+7.2, +21.5] | −0.85 [−1.275, −0.425]; 0.143 [0.072, 0.215] | match (−0.85 shown as −0.9; float is −0.8500000000000001) |
| 4 | Notes gap (Table 1, RQ2) | −30.5 [−36.0, −24.7] | −0.305 [−0.360, −0.247] | match |
| 5 | Duty / tip line (Abstract, Table 2) | +27.1 [+20.7, +33.8] / +27.9 [+20.2, +35.0]; Gemma 80.0/86.7 | 0.271 [0.207, 0.338] / 0.279 [0.202, 0.350]; 0.8/0.867 | match |
| 6 | Tip field, notice, tip-only (RQ3) | +8.2 [−0.7, +17.7]; +19.6 [+10.9, +27.9]; 27 of 39 | 0.082 [−0.007, 0.177]; 0.196 [0.109, 0.279]; macros 27/39 | match |
| 7 | Enforced vs none (RQ3) | 10.5 [2.0, 18.2], Llama 48.6; 79 bans in 31/40 | −0.105 [−0.182, −0.020]; Llama −0.486 | match (bounds correctly swapped under `\A`) |
| 8 | Mixed vs independence (§4) | 1.1 vs 1.0, +0.1 [+0.0, +0.3]; 2.3 vs 2.3, +0.0 [−0.3, +0.6] | obs 1.1, pred 1.0, [0.0, 0.3]; obs 2.3, pred 2.265, est 0.035 [−0.347, 0.600] | match |
| 9 | Agreement criterion (RQ2, PC, §5) | 6/40 none (6.5 vs 2.3); 34/40 order; 12/40 audit | channel_split.json: none 6 (Gemma 5, Llama 1), 6.5 vs 2.32; order 34; audit 12 | match |
| 10 | 4-way shares (RQ2) | 18% conceal, 12% delay of 4,019 | 0.182, 0.119, n 4019 (17 unlabelled) | match |
| 11 | Say–do gap (RQ2) | 84% of 1235 | say_do_gap 1039/1235 = 0.841 | match (format "1235" should be "1,235") |
| 12 | Scored monitor (§4, Table 4) | do 0.63, say 0.75, both 0.83, claims 0.79, informed 0.81 (0.71/0.62/0.75), FPR warned 9/31/41/49/45 | monitor_views.json informed 0.810, 0.706/0.619/0.753, 0.446; others as macros | match |
| 13 | Binary monitor (§4) | 8% [5–14] vs 8% [6–11]; 69% [62–76] vs 31% [26–36]; 88% order | macros `mon/*` | match (macros only; summary.json not re-opened) |
| 14 | Positive control (§4) | +3.9 [3.4, 4.3]; 64.5 [57.1, 71.1]; soft +0.4 (p = 0.14) | 3.875 [3.425, 4.275]; −0.645 [−0.711, −0.571]; 0.4, p 0.140 | match |
| 15 | Ordered compliance (§5) | mini 0/10, oss 1, Llama 2 | cell macros 0/1/2 (Gemma 0, not mentioned) | match |
| 16 | MDE, C3 Holm (§3.3, §4) | 2.9; p < 0.001 | 2.86; 0.0006 | match |
| 17 | Run counts (Abstract, §3.2) | 1,000 + 480 | `n/runs` 1,000; `rb/runs` 480 (tip field 40 + notes 40 + enforced 80 + full 80 + reworded 80 + implicit 120 + mixed 40) | match |
| 18 | Scale (App. D) | −0.2 [−0.5, −0.1], "Holm p ≥ 0.5" | est −0.2 [−0.5, −0.1], p_perm 0.12, Holm 0.54 | match, but the CI excludes 0 while p = 0.12. The bootstrap and permutation disagree; the CI is worth a footnote or should be dropped from the text. |

No wrong numbers found. Every number in the text is generated from a macro.

## 3. New issues introduced by the revision

**N1. Stale old-label passage contradicts the new relabel (§4 RQ2, ¶2; §5 ¶1). Most serious.** "What the channel carries is mostly talk of disclosure: 23% ... keep the problem from residents and 55% to tell them" uses GPT-4.1-mini's old SILENCE label, which the paper itself now replaces because it lumps delay in with concealment. It glosses that label as "keep the problem from residents". Two sentences later, the DeepSeek relabel of 4,019 messages gives CONCEAL 18%, DELAY 12%, DISCLOSE **33%**, OTHER 37% (`channel_split.json`). Under the paper's own preferred labeller, the channel is *not* "mostly" disclosure talk: 33% disclose against 30% conceal or delay. Two message counts (4,034 vs 4,019) sit side by side without explanation. The Discussion inherits the problem: "peers' messages, mostly favouring disclosure".

**N2. The abstract overclaims the load-control inference.** "the delay comes from a private place to write, not from coordination among insiders". The design shows that a private field delays warnings and that sharing it partly offsets the delay. It cannot rule out that coordination adds some delay that peers' disclosure talk then offsets. RQ2's own wording ("so it is not explained by coordination") is the defensible form.

**N3. The abstract and Rec (1) conflate two monitors.** "A monitor reading only public posts was at chance; told what the insiders know, it nearly matched one that also read the private channel." The at-chance monitor is the binary one. The informed view (0.81) is a scored monitor, compared with the scored "both" view (0.83). The uninformed *scored* public view had AUROC 0.63, not chance. Rec (1) repeats the conflation: "uninformed, it was at chance".

**N4. The Conclusion overclaims on two counts.**
- "delayed their warnings more than coordination did" implies coordination delayed warnings, which the results do not show (channel vs notes is −0.9 days).
- "a monitor that knows what they know can see the silence in public" ignores that at the 10%-privacy threshold the informed view also flags 45% of warned villages.

**N5. "Announcing an audit did not stop such agreements: they appeared in 12 of 40 audit villages" (RQ2).** With no rule the count is 6/40, so the audit cell has twice as many. "did not stop" understates a descriptive increase (Gemma 7, Llama 5). It is also post-treatment, so the passage should report it, not interpret it.

**N6. "warned exactly when independence predicts" (§4 Mixed families).** The Gemma+oss interval is [+0.0, +0.3], and the Gemma+mini upper bound is +0.6 days. "the quiet family did not hold back the forthcoming one" is a null stated as a fact, the same pattern the panel flagged in round 1.

**N7. Analysis plan vs reporting of the notes contrasts (§3.3).** "C3 channel on vs off at M = 4, and each against private notes", with "C1, C3 and C5 form a secondary Holm family". That puts the notes contrasts in a corrected family, but no Holm p is reported for them, and `analysis.json` has no p for them. Either report Holm p or call them exploratory. Their CIs exclude zero comfortably, so labelling them exploratory costs nothing.

**N8. Lim. 1 claims hand labels bound judge error, but the hand labels are pending** ("TBD: agreement" renders in red in §3.1). If the labels are not finished, both places must change.

**N9. Lim. 6 misattributes rule effects.** "most rule effects come from Gemma-3-12B and Llama-3.1-8B". Table 2 shows that for the duty and the tip line GPT-4.1-mini contributes more than Llama (16.7 vs 11.6 and 8.0).

**N10. Reproducibility gap.** Appendix F says its prompts are "Verbatim from ... offline_checks.py and monitor_views.py". It omits the 4-way CONCEAL/DELAY/DISCLOSE/OTHER prompt (`scripts/relabel_channel.py`), which now defines the paper's collusion criterion. Figure 1 still says "Offline judging: channel: silence, disclose, other" (`fig_arch.tex` l.42) and shows no notes field.

**N11. Minor.**
- "Every view did worse within a model than pooled": the "do" view for mini equals pooled (0.63).
- RQ3 "each averted about 28 points" vs the abstract's 27.1 and 27.9 (harmless).
- The binary and scored monitors use different samples (166/372 vs 137/263) without saying so.
- Figure 1 floats into Appendix C, leaving "B System architecture" empty in the text flow.
- Table 4 splits the Appendix E notice list.
- Notes cell and no-field cell: if they were run at different times or through different providers, say so in App. C (R1 W14 pattern). This needs checking; no text is proposed here.

**Stale-story sweep.**
- Absent from the revised text, confirmed by grep: "silence lives in the channel", "broke the silence", "companion study", "did not favour", "about two days", 62%, 55% agreement, "no quieter".
- Only the old SILENCE label survives, in N1 and Fig. 1.
- No development-history wording found.
- "fixed before any run was inspected" applies only to the binary monitor, which is accurate.

## 4. Format gates

| Gate | Result |
|---|---|
| Body ≤ 8 pages | **Pass.** The Conclusion ends on p. 8; References start p. 9. Exactly full, so replacements below are equal or shorter in length. |
| Abstract 150–250 words | **Pass.** 240 words (pdftotext count). F2/F3 change it by +3 words at most → 243. |
| Appendix "Limitations and Dual-Use/Ethical Considerations" | **Pass** (App. A, exact title) |
| LLM usage statement | **Pass** (App. G) |
| No `??` | **Pass** (none in the PDF text or `main.log`; no undefined references) |
| Placeholders | **Fail until filled:** `\res{agreement}` renders as red "TBD: agreement" in §3.1 (pending author labels), and Lim. 1 depends on it (F6) |

## 5. Ranked rewriting-only fixes (most valuable first)

**F1. RQ2 ¶2 and Discussion: remove the stale label shares (N1).** In `main.tex` §4 RQ2, replace:
> What the channel carries is mostly talk of disclosure: \N{chan/silence}\% of the \N{chan/n} labelled channel messages proposed or agreed to keep the problem from residents and \N{chan/disclose}\% to tell them; on \N{saydo/share}\% of the \N{saydo/n} insider-days up to the first warning with a message proposing disclosure, the same insider's public post was not an explicit warning. Of \N{split/n} channel messages, \N{split/share/conceal}\% proposed concealment and \N{split/share/delay}\% proposed waiting.

with:
> Of the \N{split/n} channel messages, \N{split/share/disclose}\% proposed telling residents, \N{split/share/conceal}\% concealment and \N{split/share/delay}\% waiting. On \N{saydo/share}\% of the 1,235 insider-days up to the first warning with a message proposing disclosure, the same insider's public post was not an explicit warning.

(This is shorter. Also make the `saydo/n` macro emit "1,235" or hard-code it as here.) In §5 ¶1, replace "perhaps because peers' messages, mostly favouring disclosure, prompt a warning" with "perhaps because peers' messages proposing disclosure prompt a warning".

**F2. Abstract: state the load-control inference at its defensible strength (N2).** Replace "the delay comes from a private place to write, not from coordination among insiders." with "a private place to write, not coordination among insiders, suffices to explain the delay." (+1 word.)

**F3. Abstract and Rec (1): separate the two monitors (N3).**
- Abstract: replace "A monitor reading only public posts was at chance; told what the insiders know, it nearly matched one that also read the private channel." with "A monitor reading only public posts was at chance; one also told what the insiders know (AUROC 0.81) nearly matched one reading the channel (0.83)." (+2 words.)
- Rec (1): replace "uninformed, it was at chance." with "uninformed, it did worst (AUROC 0.63)."

**F4. RQ2: report the audit agreement count as an increase (N5).** Replace "Announcing an audit did not stop such agreements: they appeared in \N{split/crit/audit} of \N{split/crit/audit/runs} audit villages." with "Under an announced audit they appeared in \N{split/crit/audit} of \N{split/crit/audit/runs} villages, twice as often (descriptive)."

**F5. Conclusion (N4).** Replace "A private place to write delayed their warnings more than coordination did, and a monitor that knows what they know can see the silence in public." with "A private place to write, read by others or not, delayed their warnings, and a monitor that knows what they know can see much of the silence in public."

**F6. Hand-label placeholder (N8).** If the labels arrive, fill in `\res{agreement}`. If they do not arrive before submission:
- §3.1: delete ", and the author hand-labels 150 posts and channel messages stratified by label, blind to condition and model (\res{agreement})".
- Lim. 1: replace "the cross-family relabel, $\kappa$ and hand labels bound this" with "the cross-family relabel and $\kappa$ bound this".

Do not ship red "TBD" text.

**F7. Mixed families: state the nulls as detection results (N6).**
- Replace "Villages mixing model families warned exactly when independence predicts." with "Villages mixing model families warned as independence predicts."
- Replace "and the quiet family did not hold back the forthcoming one." with "and the quiet family did not detectably hold back the forthcoming one."

Net change: 0 words.

**F8. Analysis plan: assign the notes contrasts a family (N7).** Replace "\textbf{C3} channel on vs off at $M=4$, and each against private notes." with "\textbf{C3} channel on vs off at $M=4$; contrasts with private notes are exploratory." (Alternatively, compute and report Holm p for them; that needs a script run, so it is outside rewriting-only.)

**F9. Lim. 6 (N9).** Replace "so most rule effects come from Gemma-3-12B and Llama-3.1-8B." with "so most rule effects come from Gemma-3-12B."

**F10. Appendix F and Figure 1 (N10). Appendix, no page cost.**
- After "Judge prompt, channel messages (offline)", add "Channel relabel prompt (offline, DeepSeek-V4.1-Flash)" with the verbatim `PROMPT` from `scripts/relabel_channel.py` (l.29–37).
- In `fig_arch.tex` l.42, replace `channel: \textsc{silence}, \textsc{disclose}, \textsc{other}` with `channel: \textsc{conceal}, \textsc{delay}, \textsc{disclose}, \textsc{other}`.

**F11. Monitoring paragraph (N11).** Replace "Every view did worse within a model than pooled" with "Within a model, views did no better than pooled".

**F12. RQ3 (cosmetic).** Replace "the field without the notice averted only \N{rb/tipfield_vs_none/gap} points" with "the field without the notice averted only \A{rb/tipfield_vs_none/gap} points".

The total body change from F1 to F12 is net shorter, so the 8-page body should still fit. Recompile and confirm that References still start on p. 9.

## 6. Optional (not rewriting-only; archival)

- Label the private notes with the 4-way prompt. This would turn the "private field substitutes for public disclosure" hypothesis (Lim. 3) into a measurement.
- Bootstrap the channel-on excess (R1 W4).
- Report the relabel-replay notes and channel effects on warning day in the body (DA M3).
- Add one more capable insider under the reference and notes cells (EIC W6).
- Report the Gemma insiders' own first explicit post in mixed vs Gemma-only villages (R2 W4).
