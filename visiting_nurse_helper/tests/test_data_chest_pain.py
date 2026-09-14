"""胸痛(CHEST_PAIN)データのテスト。"""
import pytest

from visiting_nurse_helper.data import CHEST_PAIN


def mi():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "心筋梗塞疑い")


def aortic_dissection():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "大動脈解離疑い")


def pneumothorax():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "気胸")


def angina():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "狭心症疑い")


def pericarditis():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "心膜炎疑い")


def reflux_esophagitis():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "逆流性食道炎")


def musculoskeletal_pain():
    return next(c for c in CHEST_PAIN.risk_conditions if c.name == "肋間神経痛・筋骨格由来の胸痛")


def test_mi_escalates_on_single_mild_sign():
    result = mi().evaluate({"冷汗を伴う": "軽度"})
    assert result == "直ちに受診・緊急要請"


def test_mi_stays_base_urgency_with_no_signs():
    result = mi().evaluate({"冷汗を伴う": "なし", "突然発症の胸痛": "なし"})
    assert result == "経過観察"


def test_mi_escalates_when_angina_shared_sign_present():
    # 狭心症疑いと共有している「痛みが15分以上持続し安静でも軽快しない」が
    # 心筋梗塞疑い側の判定にも単独で作用することを確認
    result = mi().evaluate({"痛みが15分以上持続し安静でも軽快しない": "軽度"})
    assert result == "直ちに受診・緊急要請"


def test_aortic_dissection_escalates_on_single_mild_sign():
    result = aortic_dissection().evaluate({"引き裂かれるような激痛": "軽度"})
    assert result == "直ちに受診・緊急要請"


def test_pneumothorax_escalates_even_on_mild_single_sign():
    result = pneumothorax().evaluate(
        {"突然発症の胸痛": "なし", "患側呼吸音減弱": "なし", "皮下気腫": "軽度"}
    )
    assert result == "直ちに受診・緊急要請"


def test_angina_requires_two_mild_signs():
    result = angina().evaluate(
        {"労作時に誘発される胸痛": "軽度", "安静で軽快する": "軽度", "数分以内に消失する": "なし"}
    )
    assert result == "医師へ報告"


def test_angina_does_not_escalate_on_single_mild_sign():
    result = angina().evaluate(
        {"労作時に誘発される胸痛": "軽度", "安静で軽快する": "なし", "数分以内に消失する": "なし"}
    )
    assert result == "経過観察"


def test_pericarditis_requires_two_mild_signs():
    result = pericarditis().evaluate(
        {"前傾姿勢で軽快する胸痛": "軽度", "発熱を伴う": "軽度", "深呼吸・体動で増悪する": "なし"}
    )
    assert result == "医師へ報告"


def test_reflux_esophagitis_requires_two_mild_signs():
    result = reflux_esophagitis().evaluate(
        {"食後に増悪する胸やけ": "軽度", "夜間臥位で増悪する": "軽度", "苦味・酸味の逆流感": "なし"}
    )
    assert result == "医師へ報告"


def test_musculoskeletal_pain_never_escalates():
    result = musculoskeletal_pain().evaluate(
        {"体動・深呼吸で増悪する": "高度", "限局した圧痛点がある": "高度", "安静時は消失する": "高度"}
    )
    assert result == "経過観察"


def test_chest_pain_overall_picks_highest_urgency_across_conditions():
    observed = {
        "持続する胸骨後部の激痛": "なし", "冷汗を伴う": "軽度", "左肩・顎への放散痛": "なし",
        "嘔気・嘔吐を伴う": "なし", "突然発症の胸痛": "なし",
        "痛みが15分以上持続し安静でも軽快しない": "なし",
        "引き裂かれるような激痛": "なし", "背部へ移動する痛み": "なし",
        "左右の血圧差": "なし", "突然発症の激痛": "なし",
        "患側呼吸音減弱": "なし", "皮下気腫": "なし",
        "労作時に誘発される胸痛": "なし", "安静で軽快する": "なし", "数分以内に消失する": "なし",
        "前傾姿勢で軽快する胸痛": "なし", "発熱を伴う": "なし", "深呼吸・体動で増悪する": "なし",
        "食後に増悪する胸やけ": "なし", "夜間臥位で増悪する": "なし", "苦味・酸味の逆流感": "なし",
        "体動・深呼吸で増悪する": "なし", "限局した圧痛点がある": "なし", "安静時は消失する": "なし",
    }
    result = CHEST_PAIN.evaluate(observed)
    assert result["心筋梗塞疑い"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"