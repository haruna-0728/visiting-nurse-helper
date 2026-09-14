"""浮腫(EDEMA)データのテスト。"""
import pytest

from visiting_nurse_helper.data import EDEMA


def heart_failure():
    return next(c for c in EDEMA.risk_conditions if c.name == "心不全増悪")


def renal_failure():
    return next(c for c in EDEMA.risk_conditions if c.name == "腎不全・ネフローゼ症候群疑い")


def dvt():
    return next(c for c in EDEMA.risk_conditions if c.name == "深部静脈血栓症(DVT)疑い")


def cirrhosis():
    return next(c for c in EDEMA.risk_conditions if c.name == "肝硬変・低アルブミン血症")


def lymphedema():
    return next(c for c in EDEMA.risk_conditions if c.name == "リンパ浮腫")


def disuse_edema():
    return next(c for c in EDEMA.risk_conditions if c.name == "廃用性浮腫")


def drug_induced_edema():
    return next(c for c in EDEMA.risk_conditions if c.name == "薬剤性浮腫")


def hypothyroidism():
    return next(c for c in EDEMA.risk_conditions if c.name == "甲状腺機能低下症")


def cellulitis():
    return next(c for c in EDEMA.risk_conditions if c.name == "蜂窩織炎")


def test_heart_failure_escalates_on_single_severe_sign():
    result = heart_failure().evaluate(
        {"起坐呼吸": "高度", "下腿浮腫": "なし", "頸静脈怒張": "なし", "体重急増(数日で2kg以上)": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_renal_failure_requires_two_mild_signs():
    result = renal_failure().evaluate(
        {"全身性の浮腫(圧痕性)": "軽度", "尿量減少": "軽度", "泡立つ尿": "なし", "体重増加(短期間)": "なし"}
    )
    assert result == "医師へ報告"


def test_dvt_escalates_on_single_mild_sign():
    result = dvt().evaluate(
        {"片側性の下肢腫脹": "軽度", "足背動脈触知不可": "なし", "熱感を伴う": "なし", "疼痛を伴う": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_dvt_stays_base_urgency_with_no_signs():
    result = dvt().evaluate(
        {"片側性の下肢腫脹": "なし", "足背動脈触知不可": "なし", "熱感を伴う": "なし", "疼痛を伴う": "なし"}
    )
    assert result == "経過観察"


def test_cirrhosis_requires_two_mild_signs():
    result = cirrhosis().evaluate(
        {"腹水を伴う浮腫": "軽度", "黄疸": "軽度", "羽ばたき振戦": "なし", "腹壁静脈怒張": "なし"}
    )
    assert result == "医師へ報告"


def test_lymphedema_never_escalates():
    result = lymphedema().evaluate(
        {"片側性の非圧痕性浮腫": "高度", "皮膚の硬化・肥厚": "高度", "リンパ節郭清・放射線治療の既往": "高度"}
    )
    assert result == "経過観察"


def test_disuse_edema_never_escalates():
    result = disuse_edema().evaluate(
        {"長時間の同一体位": "高度", "下肢挙上で軽快する": "高度", "両側性の圧痕性浮腫": "高度"}
    )
    assert result == "経過観察"


def test_drug_induced_edema_never_escalates():
    result = drug_induced_edema().evaluate(
        {"降圧薬(Ca拮抗薬)の内服歴": "高度", "投薬開始後に浮腫が出現": "高度", "両側性の圧痕性浮腫": "高度"}
    )
    assert result == "経過観察"


def test_hypothyroidism_requires_two_mild_signs():
    result = hypothyroidism().evaluate(
        {"低体温": "軽度", "浮腫(非圧痕性)": "軽度", "徐脈": "なし", "体重増加(緩徐)": "なし"}
    )
    assert result == "医師へ報告"


def test_cellulitis_escalates_on_single_severe_sign():
    result = cellulitis().evaluate(
        {"熱感を伴う発赤の拡大": "高度", "腫脹": "なし", "局所の疼痛": "なし", "発熱": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_edema_overall_picks_highest_urgency_across_conditions():
    observed = {
        "起坐呼吸": "なし", "下腿浮腫": "なし", "頸静脈怒張": "なし", "体重急増(数日で2kg以上)": "なし",
        "全身性の浮腫(圧痕性)": "なし", "尿量減少": "なし", "泡立つ尿": "なし", "体重増加(短期間)": "なし",
        "片側性の下肢腫脹": "軽度", "足背動脈触知不可": "なし", "熱感を伴う": "なし", "疼痛を伴う": "なし",
        "腹水を伴う浮腫": "なし", "黄疸": "なし", "羽ばたき振戦": "なし", "腹壁静脈怒張": "なし",
        "片側性の非圧痕性浮腫": "なし", "皮膚の硬化・肥厚": "なし", "リンパ節郭清・放射線治療の既往": "なし",
        "長時間の同一体位": "なし", "下肢挙上で軽快する": "なし", "両側性の圧痕性浮腫": "なし",
        "降圧薬(Ca拮抗薬)の内服歴": "なし", "投薬開始後に浮腫が出現": "なし",
        "低体温": "なし", "浮腫(非圧痕性)": "なし", "徐脈": "なし", "体重増加(緩徐)": "なし",
        "熱感を伴う発赤の拡大": "なし", "腫脹": "なし", "局所の疼痛": "なし", "発熱": "なし",
    }
    result = EDEMA.evaluate(observed)
    assert result["深部静脈血栓症(DVT)疑い"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"