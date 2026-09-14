"""疼痛(腹痛)(ABDOMINAL_PAIN)データのテスト。"""
import pytest

from visiting_nurse_helper.data import ABDOMINAL_PAIN


def peritonitis():
    return next(c for c in ABDOMINAL_PAIN.risk_conditions if c.name == "腹膜炎")


def appendicitis():
    return next(c for c in ABDOMINAL_PAIN.risk_conditions if c.name == "虫垂炎疑い")


def test_peritonitis_stays_base_urgency_with_no_signs():
    result = peritonitis().evaluate(
        {"反跳痛": "なし", "筋性防御": "なし", "腹部全体の激痛": "なし", "発熱": "なし"}
    )
    assert result == "経過観察"


def test_peritonitis_escalates_on_single_severe_sign():
    result = peritonitis().evaluate(
        {"反跳痛": "高度", "筋性防御": "なし", "腹部全体の激痛": "なし", "発熱": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_peritonitis_does_not_escalate_on_single_mild_sign():
    result = peritonitis().evaluate(
        {"反跳痛": "軽度", "筋性防御": "なし", "腹部全体の激痛": "なし", "発熱": "なし"}
    )
    assert result == "経過観察"


def test_peritonitis_escalates_when_two_mild_signs_present():
    result = peritonitis().evaluate(
        {"反跳痛": "軽度", "筋性防御": "軽度", "腹部全体の激痛": "なし", "発熱": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_appendicitis_escalates_when_two_signs_present():
    result = appendicitis().evaluate(
        {"右下腹部への痛みの移動": "軽度", "反跳痛": "なし", "発熱": "なし", "腰筋徴候陽性": "軽度"}
    )
    assert result == "医師へ報告"

def test_key_signs_filtering_ignores_unrelated_findings():
    # RiskCondition.evaluate()は自分のkey_signsに含まれる所見のみで判定する
    # 既存の制約が、新しい疾患候補を追加した後も保たれているかの回帰テスト
    result = appendicitis().evaluate(
        {"右下腹部への痛みの移動": "軽度", "起坐呼吸": "高度"}  # 呼吸苦の所見は無視されるはず
    )
    assert result == "経過観察"
def ileus():
    return next(c for c in ABDOMINAL_PAIN.risk_conditions if c.name == "腸閉塞疑い")


def test_ileus_stays_base_urgency_with_no_signs():
    result = ileus().evaluate(
        {"腹部膨満": "なし", "嘔吐(便臭様)": "なし", "排ガス・排便停止": "なし", "腸蠕動音亢進(金属音様)": "なし"}
    )
    assert result == "経過観察"


def test_ileus_escalates_on_single_mild_sign():
    # イレウスは疑われた段階で緊急度を引き上げる方針のため、
    # 所見が1つ・軽度でも即座に最高レベルになることを確認する
    result = ileus().evaluate(
        {"腹部膨満": "軽度", "嘔吐(便臭様)": "なし", "排ガス・排便停止": "なし", "腸蠕動音亢進(金属音様)": "なし"}
    )
    assert result == "直ちに受診・緊急要請"


def test_ileus_escalates_on_bowel_sound_sign_alone():
    result = ileus().evaluate(
        {"腹部膨満": "なし", "嘔吐(便臭様)": "なし", "排ガス・排便停止": "なし", "腸蠕動音亢進(金属音様)": "軽度"}
    )
    assert result == "直ちに受診・緊急要請"


def test_peritonitis_bowel_sound_absence_included_in_key_signs():
    # 腹膜炎に追加した「腸蠕動音減弱・消失」が正しくkey_signsとして
    # 機能しているかの確認(単独・高度で即時対応になる既存ルールの対象)
    result = peritonitis().evaluate(
        {"反跳痛": "なし", "筋性防御": "なし", "腹部全体の激痛": "なし", "発熱": "なし", "腸蠕動音減弱・消失": "高度"}
    )
    assert result == "直ちに受診・緊急要請"