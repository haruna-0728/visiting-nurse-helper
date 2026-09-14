"""visiting_nurse_helper/app.py

訪問看護お助けツールの最小限のStreamlit画面。
症状を選び、観察した所見の程度を入力すると、疾患候補ごと/全体の緊急度を表示する。

起動方法:
    streamlit run visiting_nurse_helper/app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from visiting_nurse_helper.data import ALL_SYMPTOMS
from visiting_nurse_helper.models import SEVERITY_ORDER, Severity
from visiting_nurse_helper.scales import (
    DESIGN_R_DEPTH_OPTIONS,
    DESIGN_R_E_OPTIONS,
    DESIGN_R_G_OPTIONS,
    DESIGN_R_I_OPTIONS,
    DESIGN_R_N_OPTIONS,
    DESIGN_R_P_OPTIONS,
    DESIGN_R_S_OPTIONS,
    blood_pressure_severity,
    design_r_total,
    GCS_E_OPTIONS,
    GCS_M_OPTIONS,
    GCS_V_OPTIONS,
    JCS_OPTIONS,
    MMT_OPTIONS,
    NPUAP_OPTIONS,
    gcs_total_label,
    gcs_total_severity,
    jcs_label,
    jcs_severity,
    mmt_label,
    mmt_severity,
    npuap_label,
    npuap_severity,
)

SEVERITY_OPTIONS: list[Severity] = list(SEVERITY_ORDER.keys())

URGENCY_COLOR = {
    "経過観察": "🟢",
    "医師へ報告": "🟡",
    "直ちに受診・緊急要請": "🔴",
}

OVERALL_URGENCY_LABEL = {
    "経過観察": "経過観察が適切と考えられる状態です",
    "医師へ報告": "医師への報告が必要な状態です",
    "直ちに受診・緊急要請": "病院受診・緊急要請の必要性が高い状態です",
}

URGENCY_BORDER = {
    "経過観察": "#3DDC84",
    "医師へ報告": "#FFC857",
    "直ちに受診・緊急要請": "#FF5A5F",
}

SIGN_HELP: dict[str, str] = {
    "反跳痛": (
        "【観察方法】疼痛部位を避け、健常な部位からゆっくり深く圧迫し、"
        "指を離した瞬間に痛みが増強するかを確認します。\n\n"
        "【リスクの目安】陽性であれば腹膜刺激症状(腹膜炎)を疑う重要な所見です。"
    ),
    "筋性防御": (
        "【観察方法】触診時に反射的・持続的に腹壁が硬くなるかを確認します。"
        "「お腹の力を抜いて」と声をかけても解除されない場合を「不随意性」の"
        "真の筋性防御と判断します。声かけで解除される場合は単なる緊張です。\n\n"
        "【リスクの目安】不随意性であれば腹膜炎を疑う所見です。"
    ),
    "Murphy徴候陽性": (
        "【観察方法】仰臥位で右季肋部に指を当て、深呼吸してもらいます。"
        "吸気時に胆嚢が指に触れた瞬間、疼痛のため吸気が止まれば陽性です。"
        "左右差(左季肋部では止まらない)を確認すると信頼度が上がります。\n\n"
        "【リスクの目安】陽性であれば胆嚢炎を疑う所見です。"
    ),
    "腰筋徴候陽性": (
        "【観察方法】左側臥位にし、検者が右股関節を他動的に後方へ伸展させます。"
        "右下腹部の疼痛が増強すれば陽性です(自力での運動ではなく他動運動がポイント)。\n\n"
        "【リスクの目安】陽性であれば後腹膜位の虫垂炎を疑う所見です。"
    ),
    "起坐呼吸": (
        "【観察方法】臥位で呼吸が苦しく、座位・半座位になると呼吸が楽になるかを確認します。\n\n"
        "【リスクの目安】肺うっ血の進行を示唆し、心不全増悪を疑う重要な所見です。"
    ),
    "皮下気腫": (
        "【観察方法】皮下を触診し、雪を握るような握雪感(パリパリした感触)がないか確認します。\n\n"
        "【リスクの目安】緊張性気胸への移行を疑う所見で、軽度でも緊急性が高いとされます。"
    ),
    "黒色便・タール便": (
        "【観察方法】排便の性状を確認します。コールタールのようにつやがあり、"
        "ドロッとした粘り気のある真っ黒な便であるかを観察します(通常の黒っぽい便とは"
        "見た目・臭いが異なります)。\n\n"
        "【リスクの目安】上部消化管(胃・十二指腸など)からの出血を示唆する所見です。"
    ),
    "皮膚ツルゴール低下": (
        "【観察方法】前腕内側や手背の皮膚を指でつまみ上げ、離した後に元の状態に"
        "戻るまでの時間を確認します。つまんだ皮膚がすぐに戻らず、つまんだ形の"
        "しわが残る場合を「ツルゴール低下」とします。\n\n"
        "【リスクの目安】脱水の進行を示す所見です。"
    ),
    "夜間増強する強い掻痒感": (
        "【観察方法】掻痒感が日中より夜間・就寝時に強くなる傾向があるかを確認します。\n\n"
        "【注意】疥癬は見逃すと施設内・家庭内で感染が拡大するリスクがあります。"
        "疑いがある場合は、確定診断までの間、手袋・ガウンなどの接触予防策を徹底し、"
        "使用したリネン類は熱水洗濯(50℃以上・10分以上目安)するなど、"
        "標準予防策に加えた対応を検討してください。"
    ),
    "指間・手関節屈側の線状皮疹": (
        "【観察方法】指の間や手関節の内側(屈側)を中心に、線状に伸びる皮疹(疥癬トンネル)"
        "がないか確認します。\n\n"
        "【注意】疥癬は見逃すと施設内・家庭内で感染が拡大するリスクがあります。"
        "疑いがある場合は、確定診断までの間、手袋・ガウンなどの接触予防策を徹底し、"
        "使用したリネン類は熱水洗濯(50℃以上・10分以上目安)するなど、"
        "標準予防策に加えた対応を検討してください。"
    ),
    "一側性の帯状分布疹": (
        "【観察方法】発疹が体の正中線(中心線)を越えず、左右どちらか片側のみに"
        "出ているかを確認します。神経の走行(デルマトーム)に沿って帯状に分布している"
        "ことが特徴で、正中線を越える場合は帯状疱疹以外の可能性も考慮します。\n\n"
        "【リスクの目安】片側性・帯状分布は帯状疱疹に特徴的な所見です。"
    ),
    "眼周囲・鼻背への皮疹": (
        "【観察方法】鼻の付け根から鼻背にかけて皮疹が出ているかを確認します"
        "(Hutchinson徴候)。\n\n"
        "【リスクの目安】鼻背への皮疹は、眼球を支配する神経(鼻毛様体神経)も"
        "帯状疱疹ウイルスの影響を受けている可能性を示す所見で、"
        "角膜炎・視力低下などの眼合併症(眼帯状疱疹)のサインです。"
        "早期の眼科受診が特に重要になります。"
    ),
    "感覚障害あり": (
        "【評価方法】顔面・上肢・下肢の左右対称な部位を触れ、"
        "触覚・痛覚の左右差やしびれの分布を確認する。\n"
        "片側性(左右どちらか一側)に出現している場合は中枢性を疑う。"
    ),
    "高次機能障害あり": (
        "【評価方法】会話の受け答えで言葉が出にくい・理解できない(失語)、"
        "物や人の認識ができない(失認)、"
        "指示された動作がうまくできない(失行)などがないか観察する。\n"
        "普段との会話の様子との違いに注目する。"
    ),
    "瞳孔所見異常": (
        "【評価方法】ペンライトで両眼の瞳孔径・左右差・対光反射(光を当てたときの収縮)を確認する。\n"
        "瞳孔不同や対光反射の低下・消失は脳圧亢進や脳ヘルニアの徴候として重要。"
    ),
    "バレー徴候陽性": (
        "【評価方法】閉眼して両上肢を手掌を上に向けて前方に水平挙上し、"
        "その姿勢を保持してもらう(10秒程度)。\n"
        "麻痺側は回内しながら徐々に下降する(バレー徴候陽性)。"
        "下肢の場合は腹臥位で両膝を90度屈曲位に保持させ、"
        "麻痺側の下腿が下がってくるかを見る(下肢バレー徴候)。"
    ),
    "羽ばたき振戦": (
        "【観察方法】患者に両上肢を前方に伸展してもらい、手関節を背屈させた状態を"
        "保持してもらう(手のひらを相手に向けて「ストップ」のポーズに近い形)。\n"
        "その姿勢で、手や指が不規則に上下に羽ばたくような動き(振戦)が見られるかを確認する。\n\n"
        "【リスクの目安】肝性脳症の徴候の一つで、肝機能の悪化を示唆する重要な所見です。"
    ),
    "足背動脈触知不可": (
        "【観察方法】足の甲(足背)、母趾と第2趾の間から足首方向へなぞった位置にある"
        "足背動脈を触知する。健側(反対側の足)と比較し、左右差の有無を確認する。\n\n"
        "【リスクの目安】片側のみ触知が弱い・触知できない場合、深部静脈血栓症による"
        "血流障害や動脈閉塞を疑う所見です。"
    ),
    "項部硬直": (
        "【観察方法】仰臥位にした患者の後頭部を両手で支え、"
        "ゆっくりと頸部を前屈(顎を胸に近づける方向)させる。\n"
        "抵抗があり顎が胸につかない、または前屈により疼痛が誘発される場合を陽性とする。\n\n"
        "【リスクの目安】陽性であればくも膜下出血や髄膜炎など、"
        "髄膜刺激症状を疑う重要な所見です。"
    ),
}

CONDITION_GUIDANCE: dict[str, str] = {
    "イレウス徴候(嘔吐由来)": "腹部の症状(腹痛・腹部膨満・腸蠕動音など)も併せて観察してください。",
}

st.set_page_config(
    page_title="Visiting Nurse Helper | 訪問看護お助けツール",
    page_icon="🩺",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #9AA3B2;
        font-size: 0.95rem;
        margin-bottom: 1.4rem;
    }
    .result-card {
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        background-color: #1A1D26;
        border-left: 6px solid {border_color};
        margin-bottom: 1rem;
    }
    div[data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #2A2E3A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.error(
    "⚠️ 本アプリはPython学習用に作成した**ポートフォリオ(制作物サンプル)**です。\n\n"
    "実際の医療・看護現場での使用を想定したものではなく、"
    "疾患の判定ロジックも簡略化したサンプルデータに基づいています。\n\n"
    "**実際の患者の観察・報告・受診判断には絶対に使用しないでください。**"
)

st.markdown('<div class="main-header">🩺 Visiting Nurse Helper</div>', unsafe_allow_html=True)

# --- 症状の選択 -----------------------------------------------------------

with st.container(border=True):
    symptom_name = st.selectbox("🗂️ 患者が訴えている自覚症状を選んでください", list(ALL_SYMPTOMS.keys()))
    symptom = ALL_SYMPTOMS[symptom_name]

st.divider()
st.subheader("📋 観察した所見の程度を入力してください")

all_signs: list[str] = []
for condition in symptom.risk_conditions:
    for sign in condition.key_signs:
        if sign not in all_signs:
            all_signs.append(sign)

CONSCIOUSNESS_SIGN_NAME = "意識レベル低下"
PRESSURE_ULCER_SIGN_NAME = "褥瘡評価"
MMT_SIGN_NAME = "MMT評価"
BLOOD_PRESSURE_SIGN_NAME = "血圧高値"
SPECIAL_SIGN_NAMES = {CONSCIOUSNESS_SIGN_NAME, PRESSURE_ULCER_SIGN_NAME, MMT_SIGN_NAME, BLOOD_PRESSURE_SIGN_NAME}

normal_signs = [s for s in all_signs if s not in SPECIAL_SIGN_NAMES]

observed_signs: dict[str, Severity] = {}
if not all_signs:
    st.info("この症状には、個別に観察する所見が登録されていません。")
else:
    with st.container(border=True):
        if normal_signs:
            sign_filter = st.text_input(
                "🔍 所見名で絞り込み(空欄なら全件表示)",
                key=f"sign_filter_{symptom_name}",
            )
            filtered_signs = [s for s in normal_signs if sign_filter in s] if sign_filter else normal_signs

            if sign_filter and not filtered_signs:
                st.caption("一致する所見がありません。")

            cols = st.columns(3)
            for i, sign in enumerate(filtered_signs):
                with cols[i % 3]:
                    observed_signs[sign] = st.selectbox(
                        sign,
                        SEVERITY_OPTIONS,
                        key=f"sign_{symptom_name}_{sign}",
                        help=SIGN_HELP.get(sign),
                    )
            # フィルタで一時的に非表示になった所見も、判定には影響しないよう
            # 未表示分は「なし」として扱う
            for sign in normal_signs:
                if sign not in observed_signs:
                    observed_signs[sign] = "なし"

        if CONSCIOUSNESS_SIGN_NAME in all_signs:
            st.markdown(f"**{CONSCIOUSNESS_SIGN_NAME}**")
            scale_type = st.radio(
                "評価スケールを選択",
                ["JCS", "GCS"],
                horizontal=True,
                key=f"scale_type_{symptom_name}",
            )
            if scale_type == "JCS":
                jcs_index = st.selectbox(
                    "JCSスコア",
                    range(len(JCS_OPTIONS)),
                    format_func=jcs_label,
                    key=f"jcs_{symptom_name}",
                )
                observed_signs[CONSCIOUSNESS_SIGN_NAME] = jcs_severity(jcs_index)
            else:
                gcs_e_labels = {v: f"E{v}: {d}" for v, d in GCS_E_OPTIONS}
                gcs_v_labels = {v: f"V{v}: {d}" for v, d in GCS_V_OPTIONS}
                gcs_m_labels = {v: f"M{v}: {d}" for v, d in GCS_M_OPTIONS}

                gcs_cols = st.columns(3)
                with gcs_cols[0]:
                    e_score = st.selectbox(
                        "E(開眼)", [v for v, _ in GCS_E_OPTIONS],
                        format_func=lambda v: gcs_e_labels[v], key=f"gcs_e_{symptom_name}",
                    )
                with gcs_cols[1]:
                    v_score = st.selectbox(
                        "V(言語)", [v for v, _ in GCS_V_OPTIONS],
                        format_func=lambda v: gcs_v_labels[v], key=f"gcs_v_{symptom_name}",
                    )
                with gcs_cols[2]:
                    m_score = st.selectbox(
                        "M(運動)", [v for v, _ in GCS_M_OPTIONS],
                        format_func=lambda v: gcs_m_labels[v], key=f"gcs_m_{symptom_name}",
                    )
                total = e_score + v_score + m_score
                st.caption(f"E{e_score}V{v_score}M{m_score} = {gcs_total_label(total)}")
                observed_signs[CONSCIOUSNESS_SIGN_NAME] = gcs_total_severity(total)

        if PRESSURE_ULCER_SIGN_NAME in all_signs:
            st.markdown(f"**{PRESSURE_ULCER_SIGN_NAME}**")
            npuap_index = st.selectbox(
                "NPUAP/EPUAP分類(緊急度判定に使用)",
                range(len(NPUAP_OPTIONS)),
                format_func=npuap_label,
                key=f"npuap_{symptom_name}",
            )
            observed_signs[PRESSURE_ULCER_SIGN_NAME] = npuap_severity(npuap_index)

            st.caption("DESIGN-R®2020(経過記録用の参考値・判定には使用しません)")

            depth_labels = {code: f"{code}: {desc}" for code, desc in DESIGN_R_DEPTH_OPTIONS}
            depth_code = st.selectbox(
                "深さ(Depth)",
                [code for code, _ in DESIGN_R_DEPTH_OPTIONS],
                format_func=lambda c: depth_labels[c],
                key=f"design_r_depth_{symptom_name}",
            )

            design_r_cols = st.columns(3)
            option_groups = [
                ("滲出液(Exudate)", DESIGN_R_E_OPTIONS, "e"),
                ("大きさ(Size)", DESIGN_R_S_OPTIONS, "s"),
                ("炎症/感染(Inflammation)", DESIGN_R_I_OPTIONS, "i"),
                ("肉芽組織(Granulation)", DESIGN_R_G_OPTIONS, "g"),
                ("壊死組織(Necrotic tissue)", DESIGN_R_N_OPTIONS, "n"),
                ("ポケット(Pocket)", DESIGN_R_P_OPTIONS, "p"),
            ]
            selected_codes: dict[str, str] = {}
            selected_points: dict[str, int] = {}
            for idx, (label, options, key_prefix) in enumerate(option_groups):
                option_labels = {code: f"{code}: {desc}" for code, desc, _ in options}
                option_points = {code: pts for code, _, pts in options}
                with design_r_cols[idx % 3]:
                    chosen_code = st.selectbox(
                        label,
                        [code for code, _, _ in options],
                        format_func=lambda c, m=option_labels: m[c],
                        key=f"design_r_{key_prefix}_{symptom_name}",
                    )
                selected_codes[key_prefix] = chosen_code
                selected_points[key_prefix] = option_points[chosen_code]

            total_points = design_r_total(
                selected_points["e"], selected_points["s"], selected_points["i"],
                selected_points["g"], selected_points["n"], selected_points["p"],
            )
            code_string = (
                f"{depth_code}-"
                f"{selected_codes['e']}{selected_codes['s']}{selected_codes['i']}"
                f"{selected_codes['g']}{selected_codes['n']}{selected_codes['p']}"
            )
            st.caption(f"DESIGN-R®2020: {code_string} 合計{total_points}点(深さを除く6項目の合計)")

        if MMT_SIGN_NAME in all_signs:
            st.markdown(f"**{MMT_SIGN_NAME}(徒手筋力検査・左右差を確認)**")
            mmt_labels = {v: mmt_label(v) for v, _ in MMT_OPTIONS}
            mmt_cols = st.columns(2)
            with mmt_cols[0]:
                mmt_right = st.selectbox(
                    "右側の筋力",
                    [v for v, _ in MMT_OPTIONS],
                    format_func=lambda v: mmt_labels[v],
                    key=f"mmt_right_{symptom_name}",
                )
            with mmt_cols[1]:
                mmt_left = st.selectbox(
                    "左側の筋力",
                    [v for v, _ in MMT_OPTIONS],
                    format_func=lambda v: mmt_labels[v],
                    key=f"mmt_left_{symptom_name}",
                )
            mmt_diff = abs(mmt_right - mmt_left)
            st.caption(f"右{mmt_right}/左{mmt_left}(左右差{mmt_diff})")
            observed_signs[MMT_SIGN_NAME] = mmt_severity(mmt_right, mmt_left)

        if BLOOD_PRESSURE_SIGN_NAME in all_signs:
            st.markdown(f"**{BLOOD_PRESSURE_SIGN_NAME}(血圧の実測値)**")
            bp_cols = st.columns(2)
            with bp_cols[0]:
                systolic = st.number_input(
                    "収縮期血圧(mmHg)",
                    min_value=60, max_value=260, value=120, step=1,
                    key=f"bp_systolic_{symptom_name}",
                )
            with bp_cols[1]:
                diastolic = st.number_input(
                    "拡張期血圧(mmHg)",
                    min_value=30, max_value=180, value=80, step=1,
                    key=f"bp_diastolic_{symptom_name}",
                )
            bp_severity = blood_pressure_severity(int(systolic), int(diastolic))
            st.caption(f"血圧 {int(systolic)}/{int(diastolic)}mmHg: {bp_severity}")
            observed_signs[BLOOD_PRESSURE_SIGN_NAME] = bp_severity

st.divider()

# --- 判定結果の表示 ---------------------------------------------------------


def _render_result_card(condition_name: str, urgency: str) -> None:
    """1つの疾患候補分の結果カードを描画する(直ちに受診・医師へ報告用)。"""
    if urgency == "医師へ報告":
        st.markdown(
            f"""
            <div class="result-card" style="border-left-color: {URGENCY_BORDER[urgency]}; padding: 0.8rem 1.2rem;">
                <b>{condition_name}</b><br>
                🟡 疾患リスク中程度の所見です(否定はできません)
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:  # 直ちに受診・緊急要請
        display_name = condition_name if "疑い" in condition_name else f"{condition_name}疑い"
        guidance = CONDITION_GUIDANCE.get(condition_name)
        guidance_html = f'<div style="margin-top:0.4rem; color:#9AA3B2; font-size:0.85rem;">{guidance}</div>' if guidance else ""
        st.markdown(
            f"""
            <div class="result-card" style="border-left-color: {URGENCY_BORDER[urgency]}; padding: 0.8rem 1.2rem;">
                <b>{display_name}</b><br>
                🔴 可能性が高い所見です
                {guidance_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


if st.button("🔍 緊急度を判定する", type="primary", use_container_width=True):
    result = symptom.evaluate(observed_signs)
    overall = result.pop("__overall__")

    URGENCY_ORDER = {"直ちに受診・緊急要請": 0, "医師へ報告": 1, "経過観察": 2}
    result = dict(sorted(result.items(), key=lambda item: URGENCY_ORDER[item[1]]))

    st.subheader("判定結果")

    overall_color = URGENCY_BORDER[overall]
    st.markdown(
        f"""
        <div class="result-card" style="border-left-color: {overall_color};">
            <div style="font-size: 0.9rem; color: #9AA3B2;">全体の緊急度</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-top: 0.2rem;">
                {URGENCY_COLOR[overall]} {OVERALL_URGENCY_LABEL[overall]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 疾患候補ごとの内訳")

    urgent_items = [name for name, u in result.items() if u == "直ちに受診・緊急要請"]
    report_items = [name for name, u in result.items() if u == "医師へ報告"]
    observe_items = [name for name, u in result.items() if u == "経過観察"]

    if urgent_items:
        st.markdown(f"**🔴 直ちに受診・緊急要請({len(urgent_items)}件)**")
        for condition_name in urgent_items:
            _render_result_card(condition_name, "直ちに受診・緊急要請")

    if report_items:
        st.markdown(f"**🟡 医師へ報告({len(report_items)}件)**")
        for condition_name in report_items:
            _render_result_card(condition_name, "医師へ報告")

    if observe_items:
        with st.expander(f"⚪ 経過観察相当・所見に乏しいもの({len(observe_items)}件)"):
            for condition_name in observe_items:
                st.markdown(
                    f"""
                    <div class="result-card" style="border-left-color: #4A4F5C; padding: 0.8rem 1.2rem;">
                        <b>{condition_name}</b><br>
                        ⚪ 現時点では所見に乏しく、可能性は低い所見です(否定はできません)
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.caption(
        "※ これはポートフォリオ用のサンプル判定です。疾患を確定するものではなく、"
        "実際の観察・報告・受診判断の根拠として使用しないでください。"
    )