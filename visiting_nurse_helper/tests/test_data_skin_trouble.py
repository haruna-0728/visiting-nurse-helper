"""皮膚トラブル(SKIN_TROUBLE)データのテスト。"""
import pytest

from visiting_nurse_helper.data import SKIN_TROUBLE


def pressure_ulcer():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "褥瘡の悪化")


def skin_tear():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "スキン-テア")


def cellulitis():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "蜂窩織炎")


def tinea():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "白癬疑い")


def scabies():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "疥癬疑い")


def shingles():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "帯状疱疹疑い")


def impetigo():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "とびひ(伝染性膿痂疹)疑い")


def molluscum():
    return next(c for c in SKIN_TROUBLE.risk_conditions if c.name == "水いぼ(伝染性軟属腫)疑い")


def test_pressure_ulcer_escalates_on_severe_stage():
    result = pressure_ulcer().evaluate({"褥瘡評価": "高度"})
    assert result == "直ちに受診・緊急要請"


def test_pressure_ulcer_escalates_on_moderate_stage():
    result = pressure_ulcer().evaluate({"褥瘡評価": "中等度"})
    assert result == "医師へ報告"


def test_pressure_ulcer_stays_base_urgency_on_mild_stage():
    result = pressure_ulcer().evaluate({"褥瘡評価": "軽度"})
    assert result == "経過観察"


def test_skin_tear_escalates_on_single_severe_sign():
    result = skin_tear().evaluate({"皮膚の裂傷": "高度", "出血": "なし", "皮弁の欠損": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_skin_tear_requires_two_mild_signs():
    result = skin_tear().evaluate({"皮膚の裂傷": "軽度", "出血": "軽度", "皮弁の欠損": "なし"})
    assert result == "医師へ報告"


def test_cellulitis_escalates_on_single_severe_sign():
    result = cellulitis().evaluate(
        {"熱感を伴う発赤の拡大": "高度", "腫脹": "なし", "局所の疼痛": "なし", "発熱": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_tinea_requires_two_mild_signs():
    result = tinea().evaluate({"鱗屑を伴う環状の発赤": "軽度", "掻痒感": "軽度", "趾間の浸軟": "なし"})
    assert result == "医師へ報告"


def test_scabies_escalates_on_single_mild_sign():
    result = scabies().evaluate(
        {"夜間増強する強い掻痒感": "軽度", "指間・手関節屈側の線状皮疹": "なし", "同居者・スタッフの同様症状": "なし"}
    )
    assert result == "医師へ報告"


def test_shingles_escalates_on_single_moderate_sign():
    result = shingles().evaluate(
        {"一側性の帯状分布疹": "中等度", "水疱形成": "なし", "神経痛様疼痛": "なし", "眼周囲・鼻背への皮疹": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_shingles_requires_two_mild_signs():
    result = shingles().evaluate(
        {"一側性の帯状分布疹": "軽度", "水疱形成": "軽度", "神経痛様疼痛": "なし", "眼周囲・鼻背への皮疹": "なし"}
    )
    assert result == "医師へ報告"


def test_impetigo_requires_two_mild_signs():
    result = impetigo().evaluate({"蜜色痂皮を伴う水疱・びらん": "軽度", "急速な拡大": "軽度", "掻痒感": "なし"})
    assert result == "医師へ報告"


def test_molluscum_requires_two_mild_signs():
    result = molluscum().evaluate({"中心臍窩を伴う光沢のある丘疹": "軽度", "多発": "軽度", "軽度の掻痒感": "なし"})
    assert result == "医師へ報告"


def test_skin_trouble_overall_picks_highest_urgency_across_conditions():
    observed = {
        "褥瘡評価": "なし",
        "皮膚の裂傷": "なし", "出血": "なし", "皮弁の欠損": "なし",
        "熱感を伴う発赤の拡大": "高度", "腫脹": "なし", "局所の疼痛": "なし", "発熱": "なし",
        "鱗屑を伴う環状の発赤": "なし", "掻痒感": "なし", "趾間の浸軟": "なし",
        "夜間増強する強い掻痒感": "なし", "指間・手関節屈側の線状皮疹": "なし", "同居者・スタッフの同様症状": "なし",
        "一側性の帯状分布疹": "なし", "水疱形成": "なし", "神経痛様疼痛": "なし", "眼周囲・鼻背への皮疹": "なし",
        "蜜色痂皮を伴う水疱・びらん": "なし", "急速な拡大": "なし",
        "中心臍窩を伴う光沢のある丘疹": "なし", "多発": "なし", "軽度の掻痒感": "なし",
    }
    result = SKIN_TROUBLE.evaluate(observed)
    assert result["蜂窩織炎"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"