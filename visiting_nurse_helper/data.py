"""visiting_nurse_helper/data.py

症状ごとの疾患候補データ。実際の運用では外部JSONファイルに切り出す想定だが、
まずはPythonコード内に直接定義して、models.pyの動作確認をしやすくしている。
"""
from __future__ import annotations

from .models import EscalationRule, RiskCondition, Symptom

FEVER = Symptom(
    name="発熱",
    risk_conditions=[
        RiskCondition(
            name="腹膜炎",
            base_urgency="経過観察",
            key_signs=["腹部緊満感", "反跳痛", "筋性防御"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(
                    type="sign_count", min_severity="軽度", min_count=2, urgency="直ちに受診・緊急要請"
                ),
            ],
        ),
        RiskCondition(
            name="CV・CVポート関連感染",
            base_urgency="医師へ報告",
            key_signs=["挿入部の発赤", "挿入部の腫脹", "排膿"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="腫瘍熱",
            base_urgency="経過観察",
            key_signs=[],
            escalation_rules=[],
        ),
    ],
)

FATIGUE = Symptom(
    name="倦怠感",
    risk_conditions=[
        RiskCondition(
            name="心不全増悪",
            base_urgency="経過観察",
            key_signs=["労作時息切れ", "下腿浮腫", "体重増加(短期間)"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="貧血",
            base_urgency="経過観察",
            key_signs=["眼瞼結膜蒼白", "動悸", "立ちくらみ", "低体温"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="中等度", urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="電解質異常",
            base_urgency="経過観察",
            key_signs=["意識レベル低下", "筋力低下", "食思不振"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="敗血症性ショック疑い",
            base_urgency="経過観察",
            key_signs=["低体温", "頻脈", "血圧低下", "意識レベル低下"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="甲状腺機能低下症",
            base_urgency="経過観察",
            key_signs=["低体温", "浮腫(非圧痕性)", "徐脈", "体重増加(緩徐)"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="低血糖",
            base_urgency="経過観察",
            key_signs=["冷汗", "振戦", "意識レベル低下", "低体温"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="低栄養",
            base_urgency="経過観察",
            key_signs=["低体温", "褥瘡の悪化", "体重減少", "食思不振"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
    ],
)

# --- 呼吸苦 ---
DYSPNEA = Symptom(
    name="呼吸苦",
    risk_conditions=[
        RiskCondition(
            name="心不全増悪",
            base_urgency="経過観察",
            key_signs=["起坐呼吸", "下腿浮腫", "頸静脈怒張", "体重急増(数日で2kg以上)"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="気胸",
            base_urgency="経過観察",
            key_signs=["突然発症の胸痛", "患側呼吸音減弱", "皮下気腫"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="肺炎",
            base_urgency="経過観察",
            key_signs=["発熱を伴う呼吸苦", "喀痰の性状変化(膿性・血性)", "患側呼吸音の異常(捻髪音・水泡音)"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="肺塞栓症疑い",
            base_urgency="経過観察",
            key_signs=["突然発症の呼吸苦", "片側性の下腿腫脹・疼痛", "頻脈"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="中等度", min_count=2, urgency="直ちに受診・緊急要請"),
            ],
        ),
    ],
)

# --- 疼痛(腹痛) ---
ABDOMINAL_PAIN = Symptom(
    name="疼痛(腹痛)",
    risk_conditions=[
        RiskCondition(
            name="腹膜炎",
            base_urgency="経過観察",
            key_signs=["反跳痛", "筋性防御", "腹部全体の激痛", "発熱", "腸蠕動音減弱・消失"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="胆嚢炎疑い",
            base_urgency="経過観察",
            key_signs=["Murphy徴候陽性", "右季肋部痛", "発熱", "嘔気・嘔吐"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="虫垂炎疑い",
            base_urgency="経過観察",
            key_signs=["右下腹部への痛みの移動", "反跳痛", "発熱", "腰筋徴候陽性"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="腸閉塞疑い",
            base_urgency="経過観察",
            key_signs=["腹部膨満", "嘔吐(便臭様)", "排ガス・排便停止", "腸蠕動音亢進(金属音様)"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
    ],
)

# --- 嘔吐・下痢 ---
VOMITING_DIARRHEA = Symptom(
    name="嘔吐・下痢",
    risk_conditions=[
        RiskCondition(
            name="感染性胃腸炎",
            base_urgency="経過観察",
            key_signs=["水様下痢", "嘔吐", "発熱", "腹痛"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="脱水症",
            base_urgency="経過観察",
            key_signs=["皮膚ツルゴール低下", "口腔粘膜乾燥", "尿量減少", "頻脈", "意識レベル低下"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="消化管出血疑い",
            base_urgency="経過観察",
            key_signs=["黒色便・タール便", "吐血", "血便", "頻脈", "血圧低下"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="イレウス徴候(嘔吐由来)",
            base_urgency="経過観察",
            key_signs=["便臭様の嘔吐", "腹部膨満", "排ガス・排便停止"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="直ちに受診・緊急要請"),
            ],
        ),
    ],
)

# --- 皮膚トラブル ---
SKIN_TROUBLE = Symptom(
    name="皮膚トラブル",
    risk_conditions=[
        RiskCondition(
            name="褥瘡の悪化",
            base_urgency="経過観察",
            key_signs=["褥瘡評価"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="single_sign", min_severity="中等度", urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="スキン-テア",
            base_urgency="経過観察",
            key_signs=["皮膚の裂傷", "出血", "皮弁の欠損"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="蜂窩織炎",
            base_urgency="経過観察",
            key_signs=["熱感を伴う発赤の拡大", "腫脹", "局所の疼痛", "発熱"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="白癬疑い",
            base_urgency="経過観察",
            key_signs=["鱗屑を伴う環状の発赤", "掻痒感", "趾間の浸軟"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="疥癬疑い",
            base_urgency="経過観察",
            key_signs=["夜間増強する強い掻痒感", "指間・手関節屈側の線状皮疹", "同居者・スタッフの同様症状"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="帯状疱疹疑い",
            base_urgency="経過観察",
            key_signs=["一側性の帯状分布疹", "水疱形成", "神経痛様疼痛", "眼周囲・鼻背への皮疹"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="中等度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="とびひ(伝染性膿痂疹)疑い",
            base_urgency="経過観察",
            key_signs=["蜜色痂皮を伴う水疱・びらん", "急速な拡大", "掻痒感"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="水いぼ(伝染性軟属腫)疑い",
            base_urgency="経過観察",
            key_signs=["中心臍窩を伴う光沢のある丘疹", "多発", "軽度の掻痒感"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
    ],
)

# --- めまい ---
DIZZINESS = Symptom(
    name="めまい",
    risk_conditions=[
        RiskCondition(
            name="自律神経失調症",
            base_urgency="経過観察",
            key_signs=["浮動性めまい(フワフワする感じ)", "動悸・発汗を伴う"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="起立性低血圧",
            base_urgency="経過観察",
            key_signs=["立ちくらみ・眼前暗黒感", "立位で増悪し臥位で軽快する"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="良性発作性頭位めまい症",
            base_urgency="経過観察",
            key_signs=["回転性めまい(グルグル回る感じ)", "頭位変換で誘発され数十秒〜数分で軽快する"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="メニエール病",
            base_urgency="経過観察",
            key_signs=["回転性めまい(グルグル回る感じ)", "難聴・耳鳴りを伴う", "反復性で数十分〜数時間持続する"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="前庭神経炎",
            base_urgency="医師へ報告",
            key_signs=["回転性めまい(グルグル回る感じ)", "突発性の強い回転性めまいが数日持続する"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="脳梗塞・脳出血疑い(運動・感覚系)",
            base_urgency="経過観察",
            key_signs=[
                "麻痺・しびれを伴う",
                "構音障害(ろれつが回らない)を伴う",
                "複視を伴う",
                "歩行障害・失調を伴う",
                "感覚障害あり",
                "バレー徴候陽性",
                "MMT評価",
                "突然発症の頭痛を伴う",
            ],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="脳梗塞・脳出血疑い(高次機能・瞳孔系)",
            base_urgency="経過観察",
            key_signs=["高次機能障害あり", "瞳孔所見異常"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="脳腫瘍疑い(頭痛・嘔吐系)",
            base_urgency="経過観察",
            key_signs=[
                "持続する頭痛が増悪傾向にある",
                "朝方に増悪する頭痛を伴う",
                "嘔吐を伴う",
            ],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="脳腫瘍疑い(視野・意識障害系)",
            base_urgency="経過観察",
            key_signs=["視野異常を伴う", "急激な意識障害を伴う"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
    ],
)

# --- 胸痛 ---
CHEST_PAIN = Symptom(
    name="胸痛",
    risk_conditions=[
        RiskCondition(
            name="心筋梗塞疑い",
            base_urgency="経過観察",
            key_signs=[
                "持続する胸骨後部の激痛",
                "冷汗を伴う",
                "左肩・顎への放散痛",
                "嘔気・嘔吐を伴う",
                "突然発症の胸痛",
                "痛みが15分以上持続し安静でも軽快しない",
            ],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="大動脈解離疑い",
            base_urgency="経過観察",
            key_signs=["引き裂かれるような激痛", "背部へ移動する痛み", "左右の血圧差", "突然発症の激痛"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="気胸",
            base_urgency="経過観察",
            key_signs=["突然発症の胸痛", "患側呼吸音減弱", "皮下気腫"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="狭心症疑い",
            base_urgency="経過観察",
            key_signs=[
                "労作時に誘発される胸痛",
                "安静で軽快する",
                "数分以内に消失する",
                "痛みが15分以上持続し安静でも軽快しない",
            ],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="心膜炎疑い",
            base_urgency="経過観察",
            key_signs=["前傾姿勢で軽快する胸痛", "発熱を伴う", "深呼吸・体動で増悪する"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="逆流性食道炎",
            base_urgency="経過観察",
            key_signs=["食後に増悪する胸やけ", "夜間臥位で増悪する", "苦味・酸味の逆流感"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="肋間神経痛・筋骨格由来の胸痛",
            base_urgency="経過観察",
            key_signs=["体動・深呼吸で増悪する", "限局した圧痛点がある", "安静時は消失する"],
            escalation_rules=[],
        ),
    ],
)

# --- 頭痛 ---
HEADACHE = Symptom(
    name="頭痛",
    risk_conditions=[
        RiskCondition(
            name="緊張型頭痛",
            base_urgency="経過観察",
            key_signs=["両側性の締め付けられるような痛み", "ストレス・肩こりを伴う", "日常生活動作で増悪しない"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="片頭痛",
            base_urgency="経過観察",
            key_signs=["拍動性の片側性頭痛", "光過敏・音過敏を伴う", "悪心・嘔吐を伴う", "前兆(閃輝暗点)を伴う"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="くも膜下出血疑い",
            base_urgency="経過観察",
            key_signs=[
                "今まで経験したことのない激しい頭痛",
                "突然発症の頭痛(雷鳴頭痛)",
                "項部硬直",
                "意識レベル低下",
            ],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="髄膜炎疑い",
            base_urgency="経過観察",
            key_signs=["発熱を伴う頭痛", "項部硬直", "羞明(まぶしさ)", "意識レベル低下"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="脳出血・脳梗塞疑い(運動・感覚系)",
            base_urgency="経過観察",
            key_signs=[
                "麻痺・しびれを伴う",
                "構音障害(ろれつが回らない)を伴う",
                "複視を伴う",
                "歩行障害・失調を伴う",
                "感覚障害あり",
                "バレー徴候陽性",
                "MMT評価",
            ],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="脳出血・脳梗塞疑い(高次機能・瞳孔系)",
            base_urgency="経過観察",
            key_signs=["高次機能障害あり", "瞳孔所見異常"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="高血圧緊急症疑い",
            base_urgency="経過観察",
            key_signs=["血圧高値", "視覚障害を伴う", "嘔気・嘔吐を伴う"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="薬物乱用頭痛",
            base_urgency="経過観察",
            key_signs=["月15日以上の頭痛", "鎮痛薬の頻回使用", "明え方に増悪する"],
            escalation_rules=[],
        ),
    ],
)

# --- 浮腫 ---
EDEMA = Symptom(
    name="浮腫",
    risk_conditions=[
        RiskCondition(
            name="心不全増悪",
            base_urgency="経過観察",
            key_signs=["起坐呼吸", "下腿浮腫", "頸静脈怒張", "体重急増(数日で2kg以上)"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="腎不全・ネフローゼ症候群疑い",
            base_urgency="経過観察",
            key_signs=["全身性の浮腫(圧痕性)", "尿量減少", "泡立つ尿", "体重増加(短期間)"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="深部静脈血栓症(DVT)疑い",
            base_urgency="経過観察",
            key_signs=["片側性の下肢腫脹", "足背動脈触知不可", "熱感を伴う", "疼痛を伴う"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="肝硬変・低アルブミン血症",
            base_urgency="経過観察",
            key_signs=["腹水を伴う浮腫", "黄疸", "羽ばたき振戦", "腹壁静脈怒張"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="リンパ浮腫",
            base_urgency="経過観察",
            key_signs=["片側性の非圧痕性浮腫", "皮膚の硬化・肥厚", "リンパ節郭清・放射線治療の既往"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="廃用性浮腫",
            base_urgency="経過観察",
            key_signs=["長時間の同一体位", "下肢挙上で軽快する", "両側性の圧痕性浮腫"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="薬剤性浮腫",
            base_urgency="経過観察",
            key_signs=["降圧薬(Ca拮抗薬)の内服歴", "投薬開始後に浮腫が出現", "両側性の圧痕性浮腫"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="甲状腺機能低下症",
            base_urgency="経過観察",
            key_signs=["低体温", "浮腫(非圧痕性)", "徐脈", "体重増加(緩徐)"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="蜂窩織炎",
            base_urgency="経過観察",
            key_signs=["熱感を伴う発赤の拡大", "腫脹", "局所の疼痛", "発熱"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
    ],
)

# --- 排尿トラブル ---
URINARY_TROUBLE = Symptom(
    name="排尿トラブル",
    risk_conditions=[
        RiskCondition(
            name="尿路感染症(膀胱炎)",
            base_urgency="経過観察",
            key_signs=["頻尿", "排尿時痛", "尿混濁"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="腎盂腎炎疑い",
            base_urgency="経過観察",
            key_signs=["発熱を伴う", "側腹部・背部痛", "悪寒戦慄"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="尿閉",
            base_urgency="経過観察",
            key_signs=["排尿がまったくできない", "6時間以上排尿がない", "下腹部の膨満・疼痛を伴う"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="軽度", urgency="直ちに受診・緊急要請"),
            ],
        ),
        RiskCondition(
            name="尿路結石",
            base_urgency="経過観察",
            key_signs=["側腹部から鼠径部への激しい疝痛", "血尿", "悪心・嘔吐を伴う"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="前立腺肥大症",
            base_urgency="経過観察",
            key_signs=["尿勢低下", "夜間頻尿", "残尿感"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="神経因性膀胱",
            base_urgency="経過観察",
            key_signs=["尿失禁と尿閉を繰り返す", "残尿感が強い", "脊髄疾患・糖尿病の既往"],
            escalation_rules=[
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
        RiskCondition(
            name="尿失禁",
            base_urgency="経過観察",
            key_signs=["咳・くしゃみで漏れる", "我慢できず漏れる", "常時少量漏れる"],
            escalation_rules=[],
        ),
        RiskCondition(
            name="脱水による乏尿・無尿",
            base_urgency="経過観察",
            key_signs=["皮膚ツルゴール低下", "口腔粘膜乾燥", "尿量減少", "頻脈", "意識レベル低下"],
            escalation_rules=[
                EscalationRule(type="single_sign", min_severity="高度", urgency="直ちに受診・緊急要請"),
                EscalationRule(type="sign_count", min_severity="軽度", min_count=2, urgency="医師へ報告"),
            ],
        ),
    ],
)

# --- 全症状の一覧 ---
ALL_SYMPTOMS: dict[str, Symptom] = {
    FEVER.name: FEVER,
    FATIGUE.name: FATIGUE,
    DYSPNEA.name: DYSPNEA,
    ABDOMINAL_PAIN.name: ABDOMINAL_PAIN,
    VOMITING_DIARRHEA.name: VOMITING_DIARRHEA,
    SKIN_TROUBLE.name: SKIN_TROUBLE,
    DIZZINESS.name: DIZZINESS,
    CHEST_PAIN.name: CHEST_PAIN,
    HEADACHE.name: HEADACHE,
    EDEMA.name: EDEMA,
    URINARY_TROUBLE.name: URINARY_TROUBLE,
}