"""倦怠感(FATIGUE)データのテスト。"""
import pytest

from visiting_nurse_helper.data import FATIGUE


def heart_failure():
    return next(c for c in FATIGUE.risk_conditions if c.name == "心不全増悪")


def anemia():
    return next(c for c in FATIGUE.risk_conditions if c.name == "貧血")


def electrolyte_imbalance():
    return next(c for c in FATIGUE.risk_conditions if c.name == "電解質異常")


def septic_shock():
    return next(c for c in FATIGUE.risk_conditions if c.name == "敗血症性ショック疑い")


def hypothyroidism():
    return next(c for c in FATIGUE.risk_conditions if c.name == "甲状腺機能低下症")


def hypoglycemia():
    return next(c for c in FATIGUE.risk_conditions if c.name == "低血糖")


def malnutrition():
    return next(c for c in FATIGUE.risk_conditions if c.name == "低栄養")


def test_heart_failure_escalates_on_single_severe_sign():
    result = heart_failure().evaluate(
        {"労作時息切れ": "高度", "下腿浮腫": "なし", "体重増加(短期間)": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_heart_failure_escalates_when_two_mild_signs_present():
    result = heart_failure().evaluate(
        {"労作時息切れ": "軽度", "下腿浮腫": "軽度", "体重増加(短期間)": "なし"}
    )
    assert result == "医師へ報告"


def test_anemia_escalates_on_single_moderate_sign():
    result = anemia().evaluate(
        {"眼瞼結膜蒼白": "中等度", "動悸": "なし", "立ちくらみ": "なし", "低体温": "なし"}
    )
    assert result == "医師へ報告"


def test_anemia_does_not_escalate_on_single_mild_sign():
    result = anemia().evaluate(
        {"眼瞼結膜蒼白": "軽度", "動悸": "なし", "立ちくらみ": "なし", "低体温": "なし"}
    )
    assert result == "経過観察"


def test_electrolyte_imbalance_escalates_on_single_mild_sign():
    result = electrolyte_imbalance().evaluate({"意識レベル低下": "軽度", "筋力低下": "なし", "食思不振": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_septic_shock_requires_two_mild_signs():
    result = septic_shock().evaluate(
        {"低体温": "軽度", "頻脈": "軽度", "血圧低下": "なし", "意識レベル低下": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_septic_shock_does_not_escalate_on_single_mild_sign():
    result = septic_shock().evaluate(
        {"低体温": "軽度", "頻脈": "なし", "血圧低下": "なし", "意識レベル低下": "なし"}
    )
    assert result == "経過観察"


def test_hypothyroidism_requires_two_mild_signs():
    result = hypothyroidism().evaluate(
        {"低体温": "軽度", "浮腫(非圧痕性)": "軽度", "徐脈": "なし", "体重増加(緩徐)": "なし"}
    )
    assert result == "医師へ報告"


def test_hypoglycemia_escalates_on_single_mild_sign():
    result = hypoglycemia().evaluate({"冷汗": "軽度", "振戦": "なし", "意識レベル低下": "なし", "低体温": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_malnutrition_requires_two_mild_signs():
    result = malnutrition().evaluate(
        {"低体温": "軽度", "褥瘡の悪化": "軽度", "体重減少": "なし", "食思不振": "なし"}
    )
    assert result == "医師へ報告"


def test_fatigue_overall_picks_highest_urgency_across_conditions():
    observed = {
        "労作時息切れ": "なし", "下腿浮腫": "なし", "体重増加(短期間)": "なし",
        "眼瞼結膜蒼白": "なし", "動悸": "なし", "立ちくらみ": "なし", "低体温": "軽度",
        "筋力低下": "なし", "食思不振": "なし", "意識レベル低下": "なし",
        "頻脈": "なし", "血圧低下": "なし",
        "浮腫(非圧痕性)": "なし", "徐脈": "なし", "体重増加(緩徐)": "なし",
        "冷汗": "軽度", "振戦": "なし",
        "褥瘡の悪化": "なし", "体重減少": "なし",
    }
    result = FATIGUE.evaluate(observed)
    assert result["低血糖"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"