# Architecture Design（アーキテクチャ設計）

## Document Information（文書情報）

| Item（項目） | Value（値） |
| --- | --- |
| Document ID（文書ID） | VNH-02 |
| Version（バージョン） | 0.1 |
| Status（ステータス） | Draft |
| Created Date（作成日） | 2026-09-14 |
| Owner（管理者） | haruna-0728 |

---

## Table of Contents（目次）

1. [Directory Structure（ディレクトリ構成）](#1-directory-structure)
2. [Layered Model（データモデルの階層構造）](#2-layered-model)
3. [Design Policy（設計上の全体方針）](#3-design-policy)
4. [Development Flow（開発フロー）](#4-development-flow)

---

## 1. Directory Structure（ディレクトリ構成）

```
visiting_nurse_helper_project/
├── README.md
├── requirements.txt
└── visiting_nurse_helper/
    ├── models.py   … 中核データモデル（Symptom / RiskCondition / EscalationRule）とロジック（Pydantic）
    ├── data.py     … 症状ごとの疾患候補データ
    ├── scales.py   … 意識レベル（JCS/GCS）・褥瘡評価（NPUAP/DESIGN-R®）・MMT・血圧の変換ロジック
    ├── app.py      … Streamlitによる画面
    └── tests/      … pytestによる各モジュールのテスト
```

---

## 2. Layered Model（データモデルの階層構造）

本ツールの中核は、以下の3階層構造である。

```
Symptom（自覚症状）
  └─ RiskCondition（疾患候補）
        └─ EscalationRule（緊急度引き上げルール）
```

- `Symptom`: 1つの自覚症状と、そこから考えられる疾患候補群を保持する。`evaluate()`は疾患候補ごとの緊急度と、全体の最終緊急度（`__overall__`）をまとめて返す。
- `RiskCondition`: 1つの疾患候補と、判定に用いる観察ポイント（`key_signs`）、基準緊急度（`base_urgency`）、緊急度引き上げルール一覧を保持する。`evaluate()`は自分の`key_signs`に含まれる所見のみを判定に使う（他の疾患候補向けの所見が混ざっても無視する）。
- `EscalationRule`: `single_sign`（いずれか1つの所見が閾値以上で発火）と`sign_count`（閾値以上の所見が指定件数以上で発火）の2種類のルールを持つ。

型定義（`Severity`, `UrgencyLevel`）はPydanticの`Literal`型で固定し、`SEVERITY_ORDER` / `URGENCY_ORDER`で重症度・緊急度の順序を比較可能にしている。

---

## 3. Design Policy（設計上の全体方針）

- データは`data.py`内にPythonコードとして直接定義する（学習段階のため、外部DB・JSONへの切り出しは行わない）。
- 同一の疾患候補（例：気胸、脳出血・脳梗塞疑い）が複数の自覚症状にまたがって現れる場合、症状ごとに観察の切り口をそろえて重複して収録する（`Symptom`間でのデータ共有は行わない）。
- 「疑われた時点で高確率入院・重篤化しうる」疾患（腸閉塞疑い、消化管出血疑い、低血糖、心筋梗塞疑いなど）は、`min_severity="軽度"`の`single_sign`ルールで早期に最高緊急度まで引き上げる設計とする。
- 経験による解釈のブレが出やすい項目（意識レベル、褥瘡評価、MMT、血圧）は、通常の所見選択（軽度〜高度）ではなく、`scales.py`に臨床スケールごとの専用変換関数を実装し、`app.py`側で専用入力欄として扱う。
- 疾患候補名に既に「疑い」を含む場合（例：脳梗塞・脳出血疑い（運動・感覚系））、画面側での「疑い」自動付与ロジックが二重表示を起こさないよう、名前中の存在チェックで判定する。
- 表現方針として、診断と受け取られる法令リスクを避けるため、緊急度表示は「経過観察」「医師へ報告」等の断定的な文言を避け、マイルドな表現（「疑い・可能性が高い」等）に統一する（内部の`UrgencyLevel`の値自体は変更しない）。

---

## 4. Development Flow（開発フロー）

Pydanticでデータモデルを設計 → pytestでロジックを検証 → Streamlitで画面化、という手順で開発した。

1. `models.py`でSymptom / RiskCondition / EscalationRuleの型とロジックを定義
2. `data.py`で症状ごとの疾患候補データを実装
3. `tests/`配下でpytestによる境界値テストを作成し、ロジックの正しさを検証
4. `scales.py`で専用スケール（JCS/GCS、NPUAP/DESIGN-R®、MMT、血圧）の変換ロジックを追加
5. `app.py`でStreamlit画面を実装し、専用入力欄・所見の絞り込み表示・判定結果の緊急度別グルーピングを行う
