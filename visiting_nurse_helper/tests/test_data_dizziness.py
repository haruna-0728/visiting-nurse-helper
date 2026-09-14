"""めまい(DIZZINESS)データのテスト。"""
import pytest

from visiting_nurse_helper.data import DIZZINESS


def autonomic_dysfunction():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "自律神経失調症")


def meniere_disease():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "メニエール病")


def vestibular_neuritis():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "前庭神経炎")


def stroke_motor_sensory():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "脳梗塞・脳出血疑い(運動・感覚系)")


def stroke_cognitive_pupil():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "脳梗塞・脳出血疑い(高次機能・瞳孔系)")


def brain_tumor_headache():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "脳腫瘍疑い(頭痛・嘔吐系)")


def brain_tumor_visual_consciousness():
    return next(c for c in DIZZINESS.risk_conditions if c.name == "脳腫瘍疑い(視野・意識障害系)")


def test_autonomic_dysfunction_never_escalates():
    result = autonomic_dysfunction().evaluate(
        {"浮動性めまい(フワフワする感じ)": "高度", "動悸・発汗を伴う": "高度"}
    )
    assert result == "経過観察"


def test_vestibular_neuritis_stays_at_base_urgency_with_no_signs():
    result = vestibular_neuritis().evaluate(
        {"回転性めまい(グルグル回る感じ)": "なし", "突発性の強い回転性めまいが数日持続する": "なし"}
    )
    assert result == "医師へ報告"


def test_meniere_escalates_when_two_mild_signs_present():
    result = meniere_disease().evaluate(
        {
            "回転性めまい(グルグル回る感じ)": "軽度",
            "難聴・耳鳴りを伴う": "軽度",
            "反復性で数十分〜数時間持続する": "なし",
        }
    )
    assert result == "医師へ報告"


def test_meniere_does_not_escalate_on_single_mild_sign():
    result = meniere_disease().evaluate(
        {
            "回転性めまい(グルグル回る感じ)": "軽度",
            "難聴・耳鳴りを伴う": "なし",
            "反復性で数十分〜数時間持続する": "なし",
        }
    )
    assert result == "経過観察"


def test_stroke_motor_sensory_escalates_on_single_mild_sign():
    result = stroke_motor_sensory().evaluate({"麻痺・しびれを伴う": "軽度"})
    assert result == "直ちに受診・緊急要請"


def test_stroke_motor_sensory_stays_base_urgency_with_no_signs():
    result = stroke_motor_sensory().evaluate({"麻痺・しびれを伴う": "なし", "MMT評価": "なし"})
    assert result == "経過観察"


def test_stroke_cognitive_pupil_escalates_on_single_mild_sign():
    result = stroke_cognitive_pupil().evaluate({"瞳孔所見異常": "軽度", "高次機能障害あり": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_brain_tumor_headache_requires_two_mild_signs():
    result = brain_tumor_headache().evaluate(
        {"持続する頭痛が増悪傾向にある": "軽度", "朝方に増悪する頭痛を伴う": "軽度", "嘔吐を伴う": "なし"}
    )
    assert result == "医師へ報告"


def test_brain_tumor_headache_does_not_escalate_on_single_mild_sign():
    result = brain_tumor_headache().evaluate(
        {"持続する頭痛が増悪傾向にある": "軽度", "朝方に増悪する頭痛を伴う": "なし", "嘔吐を伴う": "なし"}
    )
    assert result == "経過観察"


def test_brain_tumor_visual_consciousness_escalates_on_single_mild_sign():
    result = brain_tumor_visual_consciousness().evaluate(
        {"視野異常を伴う": "軽度", "急激な意識障害を伴う": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_dizziness_overall_picks_highest_urgency_across_conditions():
    observed = {
        "浮動性めまい(フワフワする感じ)": "なし", "動悸・発汗を伴う": "なし",
        "立ちくらみ・眼前暗黒感": "なし", "立位で増悪し臥位で軽快する": "なし",
        "回転性めまい(グルグル回る感じ)": "なし", "頭位変換で誘発され数十秒〜数分で軽快する": "なし",
        "難聴・耳鳴りを伴う": "なし", "反復性で数十分〜数時間持続する": "なし",
        "突発性の強い回転性めまいが数日持続する": "なし",
        "麻痺・しびれを伴う": "軽度", "構音障害(ろれつが回らない)を伴う": "なし",
        "複視を伴う": "なし", "歩行障害・失調を伴う": "なし", "感覚障害あり": "なし",
        "バレー徴候陽性": "なし", "MMT評価": "なし", "突然発症の頭痛を伴う": "なし",
        "高次機能障害あり": "なし", "瞳孔所見異常": "なし",
        "持続する頭痛が増悪傾向にある": "なし", "朝方に増悪する頭痛を伴う": "なし",
        "嘔吐を伴う": "なし", "視野異常を伴う": "なし", "急激な意識障害を伴う": "なし",
    }
    result = DIZZINESS.evaluate(observed)
    assert result["脳梗塞・脳出血疑い(運動・感覚系)"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"