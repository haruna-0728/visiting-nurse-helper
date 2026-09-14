"""呼吸苦(DYSPNEA)データのテスト。"""
import pytest

from visiting_nurse_helper.data import DYSPNEA


def heart_failure():
    return next(c for c in DYSPNEA.risk_conditions if c.name == "心不全増悪")


def pneumothorax():
    return next(c for c in DYSPNEA.risk_conditions if c.name == "気胸")


def pulmonary_embolism():
    return next(c for c in DYSPNEA.risk_conditions if c.name == "肺塞栓症疑い")


def test_heart_failure_stays_base_urgency_with_no_signs():
    result = heart_failure().evaluate(
        {"起坐呼吸": "なし", "下腿浮腫": "なし", "頸静脈怒張": "なし", "体重急増(数日で2kg以上)": "なし"}
    )
    assert result == "経過観察"


def test_heart_failure_escalates_on_single_severe_sign():
    result = heart_failure().evaluate(
        {"起坐呼吸": "高度", "下腿浮腫": "なし", "頸静脈怒張": "なし", "体重急増(数日で2kg以上)": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_heart_failure_does_not_escalate_on_single_mild_sign():
    result = heart_failure().evaluate(
        {"起坐呼吸": "なし", "下腿浮腫": "軽度", "頸静脈怒張": "なし", "体重急増(数日で2kg以上)": "なし"}
    )
    assert result == "経過観察"


def test_heart_failure_escalates_when_two_mild_signs_present():
    result = heart_failure().evaluate(
        {"起坐呼吸": "なし", "下腿浮腫": "軽度", "頸静脈怒張": "軽度", "体重急増(数日で2kg以上)": "なし"}
    )
    assert result == "医師へ報告"


def test_pneumothorax_escalates_even_on_mild_single_sign():
    result = pneumothorax().evaluate(
        {"突然発症の胸痛": "なし", "患側呼吸音減弱": "なし", "皮下気腫": "軽度"}
    )
    assert result == "直ちに受診・緊急要請"


def test_pulmonary_embolism_requires_two_moderate_signs():
    result = pulmonary_embolism().evaluate(
        {"突然発症の呼吸苦": "中等度", "片側性の下腿腫脹・疼痛": "中等度", "頻脈": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_pulmonary_embolism_does_not_escalate_on_single_moderate_sign():
    result = pulmonary_embolism().evaluate(
        {"突然発症の呼吸苦": "中等度", "片側性の下腿腫脹・疼痛": "なし", "頻脈": "なし"}
    )
    assert result == "経過観察"


def test_dyspnea_overall_picks_highest_urgency_across_conditions():
    observed = {
        "起坐呼吸": "なし", "下腿浮腫": "なし", "頸静脈怒張": "なし", "体重急増(数日で2kg以上)": "なし",
        "突然発症の胸痛": "なし", "患側呼吸音減弱": "なし", "皮下気腫": "軽度",
        "発熱を伴う呼吸苦": "なし", "喀痰の性状変化(膿性・血性)": "なし", "患側呼吸音の異常(捻髪音・水泡音)": "なし",
        "突然発症の呼吸苦": "なし", "片側性の下腿腫脹・疼痛": "なし", "頻脈": "なし",
    }
    result = DYSPNEA.evaluate(observed)
    assert result["気胸"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"