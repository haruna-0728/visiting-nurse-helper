"""根幹ロジック(EscalationRule / RiskCondition / Symptom)のテスト。"""
import pytest
from pydantic import ValidationError

from visiting_nurse_helper.data import FATIGUE, FEVER
from visiting_nurse_helper.models import EscalationRule, RiskCondition, Symptom


# --- EscalationRuleのバリデーション --------------------------------------


def test_sign_count_rule_requires_min_count():
    with pytest.raises(ValidationError):
        EscalationRule(type="sign_count", min_severity="軽度", urgency="医師へ報告")


def test_single_sign_rule_rejects_min_count():
    with pytest.raises(ValidationError):
        EscalationRule(
            type="single_sign", min_severity="軽度", urgency="医師へ報告", min_count=2
        )


# --- 腹膜炎(発熱の疾患候補)の判定 -----------------------------------------


def peritonitis():
    return next(c for c in FEVER.risk_conditions if c.name == "腹膜炎")


def test_peritonitis_stays_base_urgency_with_no_signs():
    condition = peritonitis()
    result = condition.evaluate({"腹部緊満感": "なし", "反跳痛": "なし", "筋性防御": "なし"})
    assert result == "経過観察"


def test_peritonitis_escalates_on_single_high_severity_sign():
    condition = peritonitis()
    result = condition.evaluate({"腹部緊満感": "高度", "反跳痛": "なし", "筋性防御": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_peritonitis_escalates_when_two_mild_signs_present():
    """1つ1つは軽度でも、2つ揃えば緊急度が上がる(組み合わせリスク)。"""
    condition = peritonitis()
    result = condition.evaluate({"腹部緊満感": "軽度", "反跳痛": "軽度", "筋性防御": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_peritonitis_does_not_escalate_on_single_mild_sign():
    condition = peritonitis()
    result = condition.evaluate({"腹部緊満感": "軽度", "反跳痛": "なし", "筋性防御": "なし"})
    assert result == "経過観察"


# --- CV感染(single_signのみで軽度から引き上げるケース) ---------------------


def test_cv_infection_escalates_even_on_mild_single_sign():
    condition = next(c for c in FEVER.risk_conditions if c.name == "CV・CVポート関連感染")
    result = condition.evaluate({"挿入部の発赤": "なし", "挿入部の腫脹": "なし", "排膿": "軽度"})
    assert result == "直ちに受診・緊急要請"


# --- Symptom全体での最終判定(最も高い緊急度が採用される) --------------------


def test_symptom_overall_picks_highest_urgency_across_conditions():
    observed = {
        # 腹膜炎の所見はなし(経過観察のまま)
        "腹部緊満感": "なし",
        "反跳痛": "なし",
        "筋性防御": "なし",
        # CV感染は排膿ありで緊急度MAX
        "挿入部の発赤": "なし",
        "挿入部の腫脹": "なし",
        "排膿": "軽度",
    }
    result = FEVER.evaluate(observed)
    assert result["腹膜炎"] == "経過観察"
    assert result["CV・CVポート関連感染"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"


def test_fatigue_symptom_evaluates_independently_of_fever():
    observed = {"労作時息切れ": "軽度", "下腿浮腫": "軽度", "体重増加(短期間)": "なし"}
    result = FATIGUE.evaluate(observed)
    assert result["心不全増悪"] == "医師へ報告"
    assert result["__overall__"] == "医師へ報告"


def test_symptom_requires_at_least_one_risk_condition():
    with pytest.raises(ValidationError):
        Symptom(name="テスト症状", risk_conditions=[])