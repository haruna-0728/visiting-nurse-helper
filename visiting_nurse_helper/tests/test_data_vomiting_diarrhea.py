"""嘔吐・下痢(VOMITING_DIARRHEA)データのテスト。"""
import pytest

from visiting_nurse_helper.data import VOMITING_DIARRHEA


def infectious_gastroenteritis():
    return next(c for c in VOMITING_DIARRHEA.risk_conditions if c.name == "感染性胃腸炎")


def dehydration():
    return next(c for c in VOMITING_DIARRHEA.risk_conditions if c.name == "脱水症")


def gi_bleeding():
    return next(c for c in VOMITING_DIARRHEA.risk_conditions if c.name == "消化管出血疑い")


def ileus_signs():
    return next(c for c in VOMITING_DIARRHEA.risk_conditions if c.name == "イレウス徴候(嘔吐由来)")


def test_gastroenteritis_stays_base_urgency_with_no_signs():
    result = infectious_gastroenteritis().evaluate(
        {"水様下痢": "なし", "嘔吐": "なし", "発熱": "なし", "腹痛": "なし"}
    )
    assert result == "経過観察"


def test_gastroenteritis_escalates_when_two_mild_signs_present():
    result = infectious_gastroenteritis().evaluate(
        {"水様下痢": "軽度", "嘔吐": "軽度", "発熱": "なし", "腹痛": "なし"}
    )
    assert result == "医師へ報告"


def test_gastroenteritis_does_not_escalate_on_single_mild_sign():
    result = infectious_gastroenteritis().evaluate(
        {"水様下痢": "軽度", "嘔吐": "なし", "発熱": "なし", "腹痛": "なし"}
    )
    assert result == "経過観察"


def test_dehydration_escalates_on_single_severe_sign():
    result = dehydration().evaluate(
        {"皮膚ツルゴール低下": "高度", "口腔粘膜乾燥": "なし", "尿量減少": "なし", "頻脈": "なし", "意識レベル低下": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_dehydration_escalates_when_two_mild_signs_present():
    result = dehydration().evaluate(
        {"皮膚ツルゴール低下": "軽度", "口腔粘膜乾燥": "軽度", "尿量減少": "なし", "頻脈": "なし", "意識レベル低下": "なし"}
    )
    assert result == "医師へ報告"


def test_gi_bleeding_escalates_even_on_mild_single_sign():
    result = gi_bleeding().evaluate(
        {"黒色便・タール便": "軽度", "吐血": "なし", "血便": "なし", "頻脈": "なし", "血圧低下": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_gi_bleeding_stays_base_urgency_with_no_signs():
    result = gi_bleeding().evaluate(
        {"黒色便・タール便": "なし", "吐血": "なし", "血便": "なし", "頻脈": "なし", "血圧低下": "なし"}
    )
    assert result == "経過観察"


def test_ileus_signs_requires_two_mild_signs():
    result = ileus_signs().evaluate(
        {"便臭様の嘔吐": "軽度", "腹部膨満": "軽度", "排ガス・排便停止": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_ileus_signs_does_not_escalate_on_single_mild_sign():
    result = ileus_signs().evaluate(
        {"便臭様の嘔吐": "軽度", "腹部膨満": "なし", "排ガス・排便停止": "なし"}
    )
    assert result == "経過観察"


def test_vomiting_diarrhea_overall_picks_highest_urgency_across_conditions():
    observed = {
        "水様下痢": "なし", "嘔吐": "なし", "発熱": "なし", "腹痛": "なし",
        "皮膚ツルゴール低下": "なし", "口腔粘膜乾燥": "なし", "尿量減少": "なし",
        "頻脈": "なし", "意識レベル低下": "なし",
        "黒色便・タール便": "軽度", "吐血": "なし", "血便": "なし", "血圧低下": "なし",
        "便臭様の嘔吐": "なし", "腹部膨満": "なし", "排ガス・排便停止": "なし",
    }
    result = VOMITING_DIARRHEA.evaluate(observed)
    assert result["消化管出血疑い"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"