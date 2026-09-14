"""発熱(FEVER)データのテスト。"""
import pytest

from visiting_nurse_helper.data import FEVER


def peritonitis():
    return next(c for c in FEVER.risk_conditions if c.name == "腹膜炎")


def cv_port_infection():
    return next(c for c in FEVER.risk_conditions if c.name == "CV・CVポート関連感染")


def tumor_fever():
    return next(c for c in FEVER.risk_conditions if c.name == "腫瘍熱")


def test_peritonitis_escalates_on_single_severe_sign():
    result = peritonitis().evaluate({"腹部緊満感": "高度", "反跳痛": "なし", "筋性防御": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_peritonitis_escalates_when_two_mild_signs_present():
    result = peritonitis().evaluate({"腹部緊満感": "軽度", "反跳痛": "軽度", "筋性防御": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_peritonitis_does_not_escalate_on_single_mild_sign():
    result = peritonitis().evaluate({"腹部緊満感": "軽度", "反跳痛": "なし", "筋性防御": "なし"})
    assert result == "経過観察"


def test_cv_port_infection_base_urgency_is_report_with_no_signs():
    result = cv_port_infection().evaluate({"挿入部の発赤": "なし", "挿入部の腫脹": "なし", "排膿": "なし"})
    assert result == "医師へ報告"


def test_cv_port_infection_escalates_on_single_mild_sign():
    result = cv_port_infection().evaluate({"挿入部の発赤": "軽度", "挿入部の腫脹": "なし", "排膿": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_tumor_fever_never_escalates():
    # key_signsが空のため、どんな所見を渡しても判定に影響しない
    result = tumor_fever().evaluate({"腹部緊満感": "高度"})
    assert result == "経過観察"


def test_fever_overall_picks_highest_urgency_across_conditions():
    observed = {
        "腹部緊満感": "なし", "反跳痛": "なし", "筋性防御": "なし",
        "挿入部の発赤": "軽度", "挿入部の腫脹": "なし", "排膿": "なし",
    }
    result = FEVER.evaluate(observed)
    assert result["CV・CVポート関連感染"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"