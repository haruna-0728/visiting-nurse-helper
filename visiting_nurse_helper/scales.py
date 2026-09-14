"""visiting_nurse_helper/scales.py

意識レベル評価(JCS/GCS)、褥瘡評価(NPUAP/DESIGN-R)、MMT(徒手筋力検査)、
血圧を、内部の重症度(Severity)に変換するための定義。
画面表示にはスコアと臨床的な意味(ラベル)をそのまま使い、
判定ロジックにだけSeverityへの変換結果を渡す。
"""
from __future__ import annotations

from visiting_nurse_helper.models import Severity, SEVERITY_ORDER

# --- JCS(Japan Coma Scale) --------------------------------------------

JCS_OPTIONS: list[tuple[str, str, Severity]] = [
    ("0", "意識清明", "なし"),
    ("Ⅰ-1", "大体意識清明だが、今ひとつはっきりしない", "軽度"),
    ("Ⅰ-2", "見当識障害がある", "軽度"),
    ("Ⅰ-3", "自分の名前・生年月日が言えない", "軽度"),
    ("Ⅱ-10", "普通の呼びかけで容易に開眼する", "中等度"),
    ("Ⅱ-20", "大きな声または体を揺さぶることにより開眼する", "中等度"),
    ("Ⅱ-30", "痛み刺激を加えつつ呼びかけを繰り返すとかろうじて開眼する", "中等度"),
    ("Ⅲ-100", "痛み刺激に対し、払いのけるような動作をする", "高度"),
    ("Ⅲ-200", "痛み刺激で少し手足を動かしたり顔をしかめる", "高度"),
    ("Ⅲ-300", "痛み刺激に反応しない", "高度"),
]


def jcs_label(index: int) -> str:
    score, description, _ = JCS_OPTIONS[index]
    return f"JCS {score}: {description}"


def jcs_severity(index: int) -> Severity:
    return JCS_OPTIONS[index][2]


# --- GCS(Glasgow Coma Scale) --------------------------------------------

GCS_E_OPTIONS: list[tuple[int, str]] = [
    (4, "自発的に開眼"),
    (3, "呼びかけにより開眼"),
    (2, "痛み刺激により開眼"),
    (1, "開眼しない"),
]

GCS_V_OPTIONS: list[tuple[int, str]] = [
    (5, "見当識あり"),
    (4, "混乱した会話"),
    (3, "不適当な発語"),
    (2, "理解不能な音声"),
    (1, "発語なし"),
]

GCS_M_OPTIONS: list[tuple[int, str]] = [
    (6, "命令に従う"),
    (5, "痛み刺激部位に手をもってくる"),
    (4, "痛み刺激に対し四肢を屈曲する(逃避)"),
    (3, "痛み刺激に対し四肢を屈曲する(異常屈曲)"),
    (2, "痛み刺激に対し四肢を伸展する"),
    (1, "運動なし"),
]


def gcs_total_severity(total: int) -> Severity:
    if total >= 15:
        return "なし"
    elif total >= 13:
        return "軽度"
    elif total >= 9:
        return "中等度"
    return "高度"


def gcs_total_label(total: int) -> str:
    band_label = {
        "なし": "意識清明",
        "軽度": "軽度の意識障害",
        "中等度": "中等度の意識障害",
        "高度": "重度の意識障害",
    }[gcs_total_severity(total)]
    return f"GCS {total}点: {band_label}"

# --- NPUAP/EPUAP 褥瘡分類 -------------------------------------------------

NPUAP_OPTIONS: list[tuple[str, str, Severity]] = [
    ("DTI疑い", "圧迫による限局性の紫色または栗色の皮膚変色、または血疱", "中等度"),
    ("ステージⅠ", "消退しない発赤を伴う、通常骨突出部位の限局性の皮膚損傷", "軽度"),
    ("ステージⅡ", "真皮の部分欠損、赤色・ピンク色の創底を持つ浅い開放性潰瘍", "軽度"),
    ("ステージⅢ", "全層皮膚欠損、皮下脂肪は確認できるが骨・腱・筋肉は露出せず", "中等度"),
    ("ステージⅣ", "全層組織欠損、骨・腱・筋肉の露出を伴う", "高度"),
    ("判定不能", "潰瘍底が壊死組織やスラフで覆われ深さの評価ができない", "高度"),
]


def npuap_label(index: int) -> str:
    stage, description, _ = NPUAP_OPTIONS[index]
    return f"{stage}: {description}"


def npuap_severity(index: int) -> Severity:
    return NPUAP_OPTIONS[index][2]

# --- DESIGN-R(R)2020(褥瘡の経過記録用。合計点は判定ロジックには使用しない) --------

DESIGN_R_DEPTH_OPTIONS: list[tuple[str, str]] = [
    ("d0", "皮膚損傷・発赤なし"),
    ("d1", "持続する発赤"),
    ("d2", "真皮までの損傷"),
    ("D3", "皮下組織までの損傷"),
    ("D4", "皮下組織を超える損傷"),
    ("D5", "関節腔・体腔に至る損傷"),
    ("DDTI", "深部損傷褥瘡(DTI)疑い"),
    ("DU", "深さ判定不能"),
]

DESIGN_R_E_OPTIONS: list[tuple[str, str, int]] = [
    ("e0", "なし", 0),
    ("e1", "少量:毎日のドレッシング交換不要", 1),
    ("E3", "中等量:1日1回のドレッシング交換", 3),
    ("E6", "多量:1日2回以上のドレッシング交換", 6),
]

DESIGN_R_S_OPTIONS: list[tuple[str, str, int]] = [
    ("s0", "皮膚損傷なし", 0),
    ("s3", "4未満", 3),
    ("s6", "4以上16未満", 6),
    ("s8", "16以上36未満", 8),
    ("s9", "36以上64未満", 9),
    ("s12", "64以上100未満", 12),
    ("S15", "100以上", 15),
]

DESIGN_R_I_OPTIONS: list[tuple[str, str, int]] = [
    ("i0", "局所の炎症徴候なし", 0),
    ("i1", "局所の炎症徴候あり", 1),
    ("I3C", "臨界的定着疑い", 3),
    ("I3", "局所の明らかな感染徴候あり", 3),
    ("I9", "全身的影響あり", 9),
]

DESIGN_R_G_OPTIONS: list[tuple[str, str, int]] = [
    ("g0", "創閉鎖または創が浅いため評価不可", 0),
    ("g1", "良性肉芽が創面の90%以上", 1),
    ("g3", "良性肉芽が創面の50%以上90%未満", 3),
    ("G4", "良性肉芽が創面の10%以上50%未満", 4),
    ("G5", "良性肉芽が創面の10%未満", 5),
    ("G6", "良性肉芽が全くない", 6),
]

DESIGN_R_N_OPTIONS: list[tuple[str, str, int]] = [
    ("n0", "壊死組織なし", 0),
    ("N3", "柔らかい壊死組織あり", 3),
    ("N6", "硬く厚い密着した壊死組織あり", 6),
]

DESIGN_R_P_OPTIONS: list[tuple[str, str, int]] = [
    ("p0", "ポケットなし", 0),
    ("P6", "4未満", 6),
    ("P9", "4以上16未満", 9),
    ("P12", "16以上36未満", 12),
    ("P24", "36以上", 24),
]


def design_r_total(e: int, s: int, i: int, g: int, n: int, p: int) -> int:
    return e + s + i + g + n + p


# --- MMT(Manual Muscle Testing・徒手筋力検査) --------------------------

MMT_OPTIONS: list[tuple[int, str]] = [
    (5, "5: 強い抵抗にも打ち勝てる(正常)"),
    (4, "4: いくらかの抵抗に打ち勝てる(軽度低下)"),
    (3, "3: 重力に抗して動かせるが、抵抗には勝てない"),
    (2, "2: 重力を除けば動かせる"),
    (1, "1: 筋の収縮のみ見られ、関節は動かない"),
    (0, "0: まったく収縮なし"),
]


def mmt_label(score: int) -> str:
    return next(label for value, label in MMT_OPTIONS if value == score)


def _mmt_score_severity(score: int) -> Severity:
    if score <= 1:
        return "高度"
    elif score <= 3:
        return "中等度"
    elif score == 4:
        return "軽度"
    return "なし"


def _mmt_diff_severity(diff: int) -> Severity:
    if diff >= 3:
        return "高度"
    elif diff == 2:
        return "中等度"
    elif diff == 1:
        return "軽度"
    return "なし"


def mmt_severity(right_score: int, left_score: int) -> Severity:
    worse_score = min(right_score, left_score)
    diff = abs(right_score - left_score)

    score_severity = _mmt_score_severity(worse_score)
    diff_severity = _mmt_diff_severity(diff)

    return max([score_severity, diff_severity], key=lambda s: SEVERITY_ORDER[s])


def mmt_summary_label(right_score: int, left_score: int) -> str:
    diff = abs(right_score - left_score)
    severity = mmt_severity(right_score, left_score)
    return f"MMT 右{right_score}/左{left_score}(左右差{diff}): {severity}"


# --- 血圧 ------------------------------------------------------------

def blood_pressure_severity(systolic: int, diastolic: int) -> Severity:
    """収縮期血圧・拡張期血圧から、内部Severityを判定する。

    日本高血圧学会のガイドラインにおける血圧分類を参考にした区分。
    """
    if systolic >= 180 or diastolic >= 120:
        return "高度"
    elif systolic >= 160 or diastolic >= 100:
        return "中等度"
    elif systolic >= 140 or diastolic >= 90:
        return "軽度"
    return "なし"


def blood_pressure_label(systolic: int, diastolic: int) -> str:
    """画面表示用のラベル(例: '血圧 190/125mmHg: 高度')を作る。"""
    severity = blood_pressure_severity(systolic, diastolic)
    return f"血圧 {systolic}/{diastolic}mmHg: {severity}"