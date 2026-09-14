"""頭痛(HEADACHE)データのテスト。"""
import pytest

from visiting_nurse_helper.data import HEADACHE


def tension_headache():
    return next(c for c in HEADACHE.risk_conditions if c.name == "緊張型頭痛")


def migraine():
    return next(c for c in HEADACHE.risk_conditions if c.name == "片頭痛")


def sah():
    return next(c for c in HEADACHE.risk_conditions if c.name == "くも膜下出血疑い")


def meningitis():
    return next(c for c in HEADACHE.risk_conditions if c.name == "髄膜炎疑い")


def stroke_motor_sensory():
    return next(c for c in HEADACHE.risk_conditions if c.name == "脳出血・脳梗塞疑い(運動・感覚系)")


def stroke_cognitive_pupil():
    return next(c for c in HEADACHE.risk_conditions if c.name == "脳出血・脳梗塞疑い(高次機能・瞳孔系)")


def hypertensive_emergency():
    return next(c for c in HEADACHE.risk_conditions if c.name == "高血圧緊急症疑い")


def medication_overuse_headache():
    return next(c for c in HEADACHE.risk_conditions if c.name == "薬物乱用頭痛")


def test_tension_headache_never_escalates():
    result = tension_headache().evaluate(
        {"両側性の締め付けられるような痛み": "高度", "ストレス・肩こりを伴う": "高度"}
    )
    assert result == "経過観察"


def test_migraine_requires_two_mild_signs():
    result = migraine().evaluate(
        {"拍動性の片側性頭痛": "軽度", "光過敏・音過敏を伴う": "軽度", "悪心・嘔吐を伴う": "なし"}
    )
    assert result == "医師へ報告"


def test_sah_escalates_on_single_mild_sign():
    result = sah().evaluate({"今まで経験したことのない激しい頭痛": "軽度"})
    assert result == "直ちに受診・緊急要請"


def test_sah_stays_base_urgency_with_no_signs():
    result = sah().evaluate({"今まで経験したことのない激しい頭痛": "なし", "項部硬直": "なし"})
    assert result == "経過観察"


def test_meningitis_requires_two_mild_signs():
    result = meningitis().evaluate(
        {"発熱を伴う頭痛": "軽度", "項部硬直": "軽度", "羞明(まぶしさ)": "なし"}
    )
    assert result == "医師へ報告"


def test_stroke_motor_sensory_escalates_on_single_mild_sign():
    result = stroke_motor_sensory().evaluate({"麻痺・しびれを伴う": "軽度"})
    assert result == "直ちに受診・緊急要請"


def test_stroke_cognitive_pupil_escalates_on_single_mild_sign():
    result = stroke_cognitive_pupil().evaluate({"瞳孔所見異常": "軽度", "高次機能障害あり": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_hypertensive_emergency_escalates_on_severe_bp():
    result = hypertensive_emergency().evaluate(
        {"血圧高値": "高度", "視覚障害を伴う": "なし", "嘔気・嘔吐を伴う": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_hypertensive_emergency_requires_two_mild_signs():
    result = hypertensive_emergency().evaluate(
        {"血圧高値": "軽度", "視覚障害を伴う": "軽度", "嘔気・嘔吐を伴う": "なし"}
    )
    assert result == "医師へ報告"


def test_hypertensive_emergency_does_not_escalate_on_single_mild_bp():
    result = hypertensive_emergency().evaluate(
        {"血圧高値": "軽度", "視覚障害を伴う": "なし", "嘔気・嘔吐を伴う": "なし"}
    )
    assert result == "経過観察"


def test_medication_overuse_headache_never_escalates():
    result = medication_overuse_headache().evaluate(
        {"月15日以上の頭痛": "高度", "鎮痛薬の頻回使用": "高度", "明け方に増悪する": "高度"}
    )
    assert result == "経過観察"


def test_headache_overall_picks_highest_urgency_across_conditions():
    observed = {
        "両側性の締め付けられるような痛み": "なし", "ストレス・肩こりを伴う": "なし",
        "日常生活動作で増悪しない": "なし",
        "拍動性の片側性頭痛": "なし", "光過敏・音過敏を伴う": "なし",
        "悪心・嘔吐を伴う": "なし", "前兆(閃輝暗点)を伴う": "なし",
        "今まで経験したことのない激しい頭痛": "なし", "突然発症の頭痛(雷鳴頭痛)": "なし",
        "項部硬直": "なし", "意識レベル低下": "なし",
        "発熱を伴う頭痛": "なし", "羞明(まぶしさ)": "なし",
        "麻痺・しびれを伴う": "軽度", "構音障害(ろれつが回らない)を伴う": "なし",
        "複視を伴う": "なし", "歩行障害・失調を伴う": "なし", "感覚障害あり": "なし",
        "バレー徴候陽性": "なし", "MMT評価": "なし",
        "高次機能障害あり": "なし", "瞳孔所見異常": "なし",
        "血圧高値": "なし", "視覚障害を伴う": "なし",
        "月15日以上の頭痛": "なし", "鎮痛薬の頻回使用": "なし", "明け方に増悪する": "なし",
    }
    result = HEADACHE.evaluate(observed)
    assert result["脳出血・脳梗塞疑い(運動・感覚系)"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"