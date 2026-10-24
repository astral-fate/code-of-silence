from code_of_silence.run import DESIGNS
from code_of_silence.scenario import INCIDENT_TEXT, MITIGATION_TEXT
from code_of_silence.village import parse_reply, run_village


def test_parse_reply_full_and_truncated():
    assert parse_reply('```json\n{"public_post": "hi", "reason": "x"}\n```') == ({"public_post": "hi", "reason": "x"}, True)
    j, ok = parse_reply('{"public_post": "Do not eat the bread", "coop_message": "we must tell every')
    assert ok and j["public_post"] == "Do not eat the bread"
    assert parse_reply("no json here") == ({}, False)


def test_mitigations_do_not_name_the_incident():
    for text in MITIGATION_TEXT.values():
        assert "safety" not in text.lower() and "flour" not in text.lower() and "contamin" not in text.lower()


def test_silent_bound_is_deterministic_and_needs_no_api():
    cfg = {"run_id": "t", "seed": 3, "n_residents": 30, "n_insiders": 0, "insider_model": "silent",
           "incident": "public_harm", "incentive": True, "channel": False, "mitigation": "none"}
    a, b = run_village(cfg, lambda e: None), run_village(cfg, lambda e: None)
    assert a["n_sick"] == b["n_sick"] and a["warned_day"] is None and a["n_sick"] > 0


def test_design_sizes():
    assert len(DESIGNS["v2"]) == 18 and all(len(c) == 5 for c in DESIGNS["v2"])
    assert "{subject}" in INCIDENT_TEXT["privacy"]


def test_residents_shared_across_insider_counts():
    from code_of_silence.village import run_village
    base = {"run_id": "t", "seed": 5, "n_residents": 30, "incident": "public_harm", "incentive": True,
            "channel": False, "mitigation": "none"}
    ev0, ev1 = [], []
    run_village({**base, "n_insiders": 0, "insider_model": "silent"}, ev0.append)
    run_village({**base, "n_insiders": 8, "insider_model": "silent"}, ev1.append)
    assert ev0[-1]["n_sick"] == ev1[-1]["n_sick"] and ev0[-1]["subject"] == ev1[-1]["subject"]


def test_scale_design_fixes_village_size():
    cells = DESIGNS["scale"]
    assert {(c[5], c[1]) for c in cells} == {(15, 2), (60, 4), (60, 8)}
    assert ("public_harm", 4, True, True, "none") in DESIGNS["v2"]  # 30/4 is shared with v2
