"""意識レベル評価(JCS/GCS)・褥瘡評価(NPUAP/DESIGN-R)・MMTのスケール変換のテスト。"""
import pytest

from visiting_nurse_helper.scales import (
    DESIGN_R_E_OPTIONS,
    DESIGN_R_P_OPTIONS,
    DESIGN_R_S_OPTIONS,
    JCS_OPTIONS,
    MMT_OPTIONS,
    NPUAP_OPTIONS,
    design_r_total,
    gcs_total_label,
    gcs_total_severity,
    jcs_label,
    jcs_severity,
    mmt_label,
    mmt_severity,
    npuap_label,
    npuap_severity,
    blood_pressure_label,
    blood_pressure_severity,
)


# --- JCS ---------------------------------------------------------------


def test_jcs_index0_is_severity_none():
    # インデックス0 = JCS "0"(意識清明)
    assert jcs_severity(0) == "なし"


def test_jcs_grade1_indices_are_mild():
    # インデックス1-3 = JCS Ⅰ桁(1, 2, 3)
    for i in (1, 2, 3):
        assert jcs_severity(i) == "軽度"


def test_jcs_grade2_indices_are_moderate():
    # インデックス4-6 = JCS Ⅱ桁(10, 20, 30)
    for i in (4, 5, 6):
        assert jcs_severity(i) == "中等度"


def test_jcs_grade3_indices_are_severe():
    # インデックス7-9 = JCS Ⅲ桁(100, 200, 300)
    for i in (7, 8, 9):
        assert jcs_severity(i) == "高度"


def test_jcs_label_contains_score_and_description():
    label = jcs_label(5)  # Ⅱ-20
    score, description, _ = JCS_OPTIONS[5]
    assert score in label
    assert description in label


# --- GCS ---------------------------------------------------------------


def test_gcs_total_15_is_severity_none():
    assert gcs_total_severity(15) == "なし"


def test_gcs_total_boundary_14_is_mild():
    # 軽度の上限境界
    assert gcs_total_severity(14) == "軽度"


def test_gcs_total_boundary_13_is_mild():
    # 軽度の下限境界
    assert gcs_total_severity(13) == "軽度"


def test_gcs_total_boundary_12_is_moderate():
    # 軽度→中等度に切り替わる境界
    assert gcs_total_severity(12) == "中等度"


def test_gcs_total_boundary_9_is_moderate():
    # 中等度の下限境界
    assert gcs_total_severity(9) == "中等度"


def test_gcs_total_boundary_8_is_severe():
    # 中等度→高度に切り替わる境界
    assert gcs_total_severity(8) == "高度"


def test_gcs_total_minimum_3_is_severe():
    assert gcs_total_severity(3) == "高度"


def test_gcs_total_label_contains_score_and_band():
    label = gcs_total_label(8)
    assert "8" in label
    assert "重度の意識障害" in label


# --- NPUAP/EPUAP 褥瘡分類 -------------------------------------------------


def test_npuap_dti_suspected_is_moderate():
    # インデックス0 = DTI疑い
    assert npuap_severity(0) == "中等度"


def test_npuap_stage1_is_mild():
    assert npuap_severity(1) == "軽度"


def test_npuap_stage2_is_mild():
    assert npuap_severity(2) == "軽度"


def test_npuap_stage3_is_moderate():
    assert npuap_severity(3) == "中等度"


def test_npuap_stage4_is_severe():
    assert npuap_severity(4) == "高度"


def test_npuap_unstageable_is_severe():
    # インデックス5 = 判定不能
    assert npuap_severity(5) == "高度"


def test_npuap_label_contains_stage_and_description():
    label = npuap_label(4)  # ステージⅣ
    stage, description, _ = NPUAP_OPTIONS[4]
    assert stage in label
    assert description in label


# --- DESIGN-R®2020 -------------------------------------------------------


def test_design_r_total_sums_six_items():
    # e0(0) + s6(6) + i1(1) + g3(3) + N3(3) + p0(0) = 13
    assert design_r_total(e=0, s=6, i=1, g=3, n=3, p=0) == 13


def test_design_r_total_all_zero_is_zero():
    assert design_r_total(e=0, s=0, i=0, g=0, n=0, p=0) == 0


def test_design_r_e_options_have_expected_max_points():
    # E6(多量)が最大点
    assert max(pts for _, _, pts in DESIGN_R_E_OPTIONS) == 6


def test_design_r_s_options_have_expected_max_points():
    # S15(100以上)が最大点
    assert max(pts for _, _, pts in DESIGN_R_S_OPTIONS) == 15


def test_design_r_p_options_have_expected_max_points():
    # P24(36以上)が最大点
    assert max(pts for _, _, pts in DESIGN_R_P_OPTIONS) == 24


# --- MMT(徒手筋力検査) ---------------------------------------------------


def test_mmt_both_normal_is_severity_none():
    assert mmt_severity(right_score=5, left_score=5) == "なし"


def test_mmt_single_score_boundary_4_is_mild():
    assert mmt_severity(right_score=4, left_score=4) == "軽度"


def test_mmt_single_score_boundary_3_is_moderate():
    assert mmt_severity(right_score=3, left_score=3) == "中等度"


def test_mmt_single_score_boundary_2_is_moderate():
    assert mmt_severity(right_score=2, left_score=2) == "中等度"


def test_mmt_single_score_boundary_1_is_severe():
    assert mmt_severity(right_score=1, left_score=1) == "高度"


def test_mmt_single_score_boundary_0_is_severe():
    assert mmt_severity(right_score=0, left_score=0) == "高度"


def test_mmt_diff_matches_score_severity_when_score_is_already_higher():
    # 右5/左4(差1): 点数側(軽度)と差側(軽度)が一致し、結果に矛盾がないことを確認
    assert mmt_severity(right_score=5, left_score=4) == "軽度"


def test_mmt_large_diff_escalates_beyond_score_alone():
    # 右5/左2(差3): 点数側だけなら中等度だが、
    # 左右差3(高度相当)により最終的に高度へ引き上げられる
    assert mmt_severity(right_score=5, left_score=2) == "高度"


def test_mmt_label_contains_score_and_description():
    label = mmt_label(3)
    _, description = next(opt for opt in MMT_OPTIONS if opt[0] == 3)
    assert "3" in label
    assert description in label


# --- 血圧 ------------------------------------------------------------


def test_blood_pressure_normal_is_severity_none():
    assert blood_pressure_severity(120, 80) == "なし"


def test_blood_pressure_systolic_boundary_140_is_mild():
    assert blood_pressure_severity(140, 80) == "軽度"


def test_blood_pressure_diastolic_boundary_90_is_mild():
    assert blood_pressure_severity(130, 90) == "軽度"


def test_blood_pressure_systolic_boundary_160_is_moderate():
    assert blood_pressure_severity(160, 80) == "中等度"


def test_blood_pressure_diastolic_boundary_100_is_moderate():
    assert blood_pressure_severity(130, 100) == "中等度"


def test_blood_pressure_systolic_boundary_180_is_severe():
    assert blood_pressure_severity(180, 80) == "高度"


def test_blood_pressure_diastolic_boundary_120_is_severe():
    assert blood_pressure_severity(130, 120) == "高度"


def test_blood_pressure_either_value_triggers_higher_severity():
    # 収縮期は正常域でも拡張期が高度域なら全体として高度
    assert blood_pressure_severity(110, 125) == "高度"


def test_blood_pressure_label_contains_values_and_severity():
    label = blood_pressure_label(190, 125)
    assert "190" in label
    assert "125" in label
    assert "高度" in label