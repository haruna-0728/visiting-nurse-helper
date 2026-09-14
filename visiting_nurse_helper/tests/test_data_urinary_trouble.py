"""排尿トラブル(URINARY_TROUBLE)データのテスト。"""
import pytest

from visiting_nurse_helper.data import URINARY_TROUBLE


def cystitis():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "尿路感染症(膀胱炎)")


def pyelonephritis():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "腎盂腎炎疑い")


def urinary_retention():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "尿閉")


def urolithiasis():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "尿路結石")


def bph():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "前立腺肥大症")


def neurogenic_bladder():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "神経因性膀胱")


def urinary_incontinence():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "尿失禁")


def oliguria_from_dehydration():
    return next(c for c in URINARY_TROUBLE.risk_conditions if c.name == "脱水による乏尿・無尿")


def test_cystitis_requires_two_mild_signs():
    result = cystitis().evaluate({"頻尿": "軽度", "排尿時痛": "軽度", "尿混濁": "なし"})
    assert result == "医師へ報告"


def test_pyelonephritis_escalates_on_single_severe_sign():
    result = pyelonephritis().evaluate({"発熱を伴う": "高度", "側腹部・背部痛": "なし", "悪寒戦慄": "なし"})
    assert result == "直ちに受診・緊急要請"


def test_urinary_retention_escalates_on_single_mild_sign():
    result = urinary_retention().evaluate(
        {"排尿がまったくできない": "軽度", "6時間以上排尿がない": "なし", "下腹部の膨満・疼痛を伴う": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_urinary_retention_stays_base_urgency_with_no_signs():
    result = urinary_retention().evaluate(
        {"排尿がまったくできない": "なし", "6時間以上排尿がない": "なし", "下腹部の膨満・疼痛を伴う": "なし"}
    )
    assert result == "経過観察"


def test_urolithiasis_escalates_on_single_severe_sign():
    result = urolithiasis().evaluate(
        {"側腹部から鼠径部への激しい疝痛": "高度", "血尿": "なし", "悪心・嘔吐を伴う": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_urolithiasis_requires_two_mild_signs():
    result = urolithiasis().evaluate(
        {"側腹部から鼠径部への激しい疝痛": "軽度", "血尿": "軽度", "悪心・嘔吐を伴う": "なし"}
    )
    assert result == "医師へ報告"


def test_bph_never_escalates():
    result = bph().evaluate({"尿勢低下": "高度", "夜間頻尿": "高度", "残尿感": "高度"})
    assert result == "経過観察"


def test_neurogenic_bladder_requires_two_mild_signs():
    result = neurogenic_bladder().evaluate(
        {"尿失禁と尿閉を繰り返す": "軽度", "残尿感が強い": "軽度", "脊髄疾患・糖尿病の既往": "なし"}
    )
    assert result == "医師へ報告"


def test_urinary_incontinence_never_escalates():
    result = urinary_incontinence().evaluate(
        {"咳・くしゃみで漏れる": "高度", "我慢できず漏れる": "高度", "常時少量漏れる": "高度"}
    )
    assert result == "経過観察"


def test_oliguria_from_dehydration_escalates_on_single_severe_sign():
    result = oliguria_from_dehydration().evaluate(
        {"皮膚ツルゴール低下": "高度", "口腔粘膜乾燥": "なし", "尿量減少": "なし", "頻脈": "なし", "意識レベル低下": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_urinary_trouble_overall_picks_highest_urgency_across_conditions():
    observed = {
        "頻尿": "なし", "排尿時痛": "なし", "尿混濁": "なし",
        "発熱を伴う": "なし", "側腹部・背部痛": "なし", "悪寒戦慄": "なし",
        "排尿がまったくできない": "軽度", "6時間以上排尿がない": "なし", "下腹部の膨満・疼痛を伴う": "なし",
        "側腹部から鼠径部への激しい疝痛": "なし", "血尿": "なし", "悪心・嘔吐を伴う": "なし",
        "尿勢低下": "なし", "夜間頻尿": "なし", "残尿感": "なし",
        "尿失禁と尿閉を繰り返す": "なし", "残尿感が強い": "なし", "脊髄疾患・糖尿病の既往": "なし",
        "咳・くしゃみで漏れる": "なし", "我慢できず漏れる": "なし", "常時少量漏れる": "なし",
        "皮膚ツルゴール低下": "なし", "口腔粘膜乾燥": "なし", "尿量減少": "なし",
        "頻脈": "なし", "意識レベル低下": "なし",
    }
    result = URINARY_TROUBLE.evaluate(observed)
    assert result["尿閉"] == "直ちに受診・緊急要請"
    assert result["__overall__"] == "直ちに受診・緊急要請"