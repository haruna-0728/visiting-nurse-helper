# 訪問看護お助けツール(ポートフォリオ用)

## ⚠️ 重要な注意事項

- 本プロジェクトはあくまで**ポートフォリオ(学習成果物)**であり、実際の医療・看護現場での使用を想定したものではありません。
- 本プロジェクトで使用するデータ(症状・疾患候補・患者情報等)は**すべて架空のもの**であり、実在の患者・医療機関とは一切関係ありません。
- 疾患候補や緊急度判定のロジックは、開発の学習を目的として簡略化したサンプルであり、医学的な正確性・網羅性を保証するものではありません。
- **実際の患者の観察・報告・受診判断には絶対に使用しないでください。**

## Document Information(文書情報)

| Item(項目) | Value(値) |
| --- | --- |
| Document ID(文書ID) | VNH-README |
| Version(バージョン) | 0.1 |
| Status(ステータス) | Draft |
| Created Date(作成日) | 2026-09-14 |
| Owner(管理者) | haruna-0728 |
| Related Documents(関連文書) | 01_requirements.md 〜 05_error_design.md(docsフォルダ配下) |

---

## Table of Contents(目次)

1. [Project Overview(プロジェクト概要)](#1-project-overview)
2. [Problem / Solution / Benefit Summary(問題・解決・効果の概要)](#2-problem--solution--benefit-summary)
3. [Feature Overview(機能概要)](#3-feature-overview)
4. [Directory Structure(ディレクトリ構成)](#4-directory-structure)
5. [Design Documents Index(設計書一覧)](#5-design-documents-index)
6. [Overall Design Policy(設計上の全体方針)](#6-overall-design-policy)
7. [Glossary(用語集)](#7-glossary)
8. [Document Owners and Reviewers(文書管理者・レビュアー一覧)](#8-document-owners-and-reviewers)
9. [Getting Started(セットアップ・テスト)](#9-getting-started)
10. [Screen Captures(画面キャプチャ)](#10-screen-captures)

---

## 1. Project Overview(プロジェクト概要)

訪問看護お助けツール(Visiting Nurse Helper)は、訪問看護師としての臨床経験を活かして開発した、患者の自覚症状・観察所見から疑うべき疾患候補と緊急度の目安を提示するWebアプリケーションです。

Python学習(Pydantic / pytest / Streamlit)の集大成として、医療IT系企業への就職活動用ポートフォリオとして作成しました。

**技術スタック**

- 言語:Python 3.13
- データモデル:Pydantic
- テスト:pytest
- 画面:Streamlit
- データ管理:Pythonコード内に直接定義(DB不使用)

---

## 2. Problem / Solution / Benefit Summary(問題・解決・効果の概要)

| Item(項目) | Summary(概要) | Detail Document(詳細文書) |
| --- | --- | --- |
| Current Problems(現在の課題) | 訪問看護の現場では、経験年数や専門知識の差によって、同じ所見を観察しても評価・重症度判断にばらつきが生じうる | [01_requirements.md](docs/01_requirements.md) |
| Development Purpose(開発目的) | 看護師としての臨床経験を活かし、観察した所見から疑うべき疾患候補と緊急度の目安を提示する学習用ツールを開発する | [01_requirements.md](docs/01_requirements.md) |
| Solution Approach(解決方針) | Symptom→RiskCondition→EscalationRuleの3階層モデルをPydanticで設計し、専門的な観察手技・臨床スケールを専用入力欄やツールチップで補助する | [02_architecture.md](docs/02_architecture.md) |
| System Functions(システム機能) | 11症状に対応した疾患候補の緊急度判定、専用スケール入力(JCS/GCS・NPUAP/DESIGN-R®・MMT・血圧)、所見の検索絞り込み、緊急度別の判定結果表示 | [03_screen_design.md](docs/03_screen_design.md) |
| Expected Benefits(期待効果) | 経験年数・専門知識に関わらず、誰が観察しても同じ基準で所見を評価し、重症度を判断できることを目指す | [01_requirements.md](docs/01_requirements.md) |
| Completion Criteria(完成判定基準) | 対応症状11種類すべてについて疾患候補データ・専用スケール・テストを実装し、pytest全件PASSを確認 | [04_test_design.md](docs/04_test_design.md) |

---

## 3. Feature Overview(機能概要)

### 対応している自覚症状(Symptom)

発熱、倦怠感、呼吸苦、疼痛(腹痛)、嘔吐・下痢、皮膚トラブル、めまい、胸痛、頭痛、浮腫、排尿トラブル

### このツールの特徴(元看護師としての工夫点)

臨床経験を活かし、疾患候補ごとに**必須の観察項目**と**評価方法の補足コメント(観察手順・判断基準)**を設定しています。これにより、経験年数や専門知識の差に関わらず、誰が観察しても同じ基準で所見を評価し、重症度を判断できることを目指しました。

- 反跳痛・Murphy徴候・腰筋徴候・バレー徴候・項部硬直・羽ばたき振戦・足背動脈触知など、専門的な観察手技には具体的な手順と陽性所見の目安をツールチップで表示
- 意識レベル(JCS/GCS)、褥瘡評価(NPUAP/DESIGN-R®)、MMT(徒手筋力検査・左右差)、血圧は、経験による解釈のブレが出やすい項目のため、それぞれ専用の入力スケールを用意し、内部的に統一された重症度に変換
- 疾患候補ごとの緊急度引き上げルール(EscalationRule)により、「疑われた時点で重篤化しうる」所見(腸閉塞・消化管出血・低血糖・心筋梗塞・くも膜下出血など)は早期に警告する設計
- 呼吸苦・胸痛の「気胸」、めまい・頭痛の「脳出血・脳梗塞疑い」のように、複数の自覚症状にまたがって現れる疾患候補は、症状ごとに観察の切り口を揃えて重複して収録
- 所見が多い症状では、検索での絞り込みや緊急度別の折りたたみ表示により、画面が長くなりすぎないよう配慮

詳細(画面構成・項目定義・操作フロー): [03_screen_design.md](docs/03_screen_design.md)

---

## 4. Directory Structure(ディレクトリ構成)

```
visiting_nurse_helper_project/
├── README.md
├── requirements.txt
├── docs/                                  … 設計書一式(下記5.参照)
└── visiting_nurse_helper/
    ├── models.py   … 中核データモデル(Symptom / RiskCondition / EscalationRule)とロジック(Pydantic)
    ├── data.py     … 症状ごとの疾患候補データ
    ├── scales.py   … 意識レベル(JCS/GCS)・褥瘡評価(NPUAP/DESIGN-R®)・MMT(徒手筋力検査)・血圧の変換ロジック
    ├── app.py      … Streamlitによる画面
    └── tests/
        ├── test_models.py                     … モデル・ロジックの基本テスト
        ├── test_data_fever.py                  … 発熱データのテスト
        ├── test_data_fatigue.py                … 倦怠感データのテスト
        ├── test_data_dyspnea.py                … 呼吸苦データのテスト
        ├── test_data_abdominal_pain.py         … 疼痛(腹痛)データのテスト
        ├── test_data_vomiting_diarrhea.py       … 嘔吐・下痢データのテスト
        ├── test_data_skin_trouble.py            … 皮膚トラブルデータのテスト
        ├── test_data_dizziness.py               … めまいデータのテスト
        ├── test_data_chest_pain.py              … 胸痛データのテスト
        ├── test_data_headache.py                … 頭痛データのテスト
        ├── test_data_edema.py                   … 浮腫データのテスト
        ├── test_data_urinary_trouble.py         … 排尿トラブルデータのテスト
        └── test_scales.py                       … JCS/GCS・NPUAP/DESIGN-R®・MMT・血圧のテスト
```

## 5. Design Documents Index(設計書一覧)

| File(ファイル名) | Document Name(文書名) | Status(ステータス) | Owner(担当者) |
| --- | --- | --- | --- |
| [01_requirements.md](docs/01_requirements.md) | 要件定義 | Draft | haruna-0728 |
| [02_architecture.md](docs/02_architecture.md) | アーキテクチャ設計 | Draft | haruna-0728 |
| [03_screen_design.md](docs/03_screen_design.md) | 画面設計 | Draft | haruna-0728 |
| [04_test_design.md](docs/04_test_design.md) | テスト設計 | Draft | haruna-0728 |
| [05_error_design.md](docs/05_error_design.md) | エラー設計(簡易版) | Draft | haruna-0728 |

> DB設計・API仕様は、本プロジェクトがDB・外部APIを使用しない構成のため対象外としています。

---

## 6. Overall Design Policy(設計上の全体方針)

- データはPythonコード内(`data.py`)に直接定義する(学習段階のため、外部DB・JSONへの切り出しは行わない)
- Symptom(自覚症状)→RiskCondition(疾患候補)→EscalationRule(緊急度引き上げルール)の3階層構造で判定ロジックを設計する
- 同一の疾患候補が複数の自覚症状にまたがる場合は、症状ごとに観察の切り口を揃えて重複して収録する
- 「疑われた時点で重篤化しうる」疾患は、軽度所見1つでも早期に最高緊急度まで引き上げる設計とする
- 経験による解釈のブレが出やすい項目は、選択式の所見ではなく臨床スケールに基づく専用入力欄を用意する
- 緊急度表示は、診断と受け取られる法令リスクを避けるため、マイルドな表現に統一する

詳細: [02_architecture.md](docs/02_architecture.md)

---

## 7. Glossary(用語集)

| Term(用語) | Definition(定義) |
| --- | --- |
| Severity(重症度) | なし/軽度/中等度/高度の4段階。所見の程度を表す内部値 |
| UrgencyLevel(緊急度) | 経過観察/医師へ報告/直ちに受診・緊急要請の3段階。疾患候補・症状全体の判定結果 |
| RiskCondition(疾患候補) | 1つの疾患候補と、判定に用いる観察ポイント・緊急度引き上げルールをまとめたモデル |
| EscalationRule(緊急度引き上げルール) | 所見の重症度・件数に応じて緊急度を引き上げる条件(single_sign / sign_count) |
| JCS / GCS | 意識レベルの評価スケール(Japan Coma Scale / Glasgow Coma Scale) |
| NPUAP/EPUAP・DESIGN-R® | 褥瘡の重症度分類・経過記録スケール |
| MMT | 徒手筋力検査(Manual Muscle Testing) |

---

## 8. Document Owners and Reviewers(文書管理者・レビュアー一覧)

| Role(役割) | Name(氏名) | Assigned Documents(担当文書) |
| --- | --- | --- |
| Document Owner(文書管理者) | haruna-0728 | All Documents(全文書) |
| Reviewer(レビュアー) | (記入欄) | (記入欄) |

---

## 9. Getting Started(セットアップ・テスト)

### セットアップ
pip install -r requirements.txt
streamlit run visiting_nurse_helper/app.py

起動後、ブラウザで表示されるURL(通常 `http://localhost:8501`)にアクセスしてください。

### テスト

全11症状のデータテスト・モデルテスト・スケールテストを含め、全件PASSすることを確認しています。詳細: [04_test_design.md](docs/04_test_design.md)

---

## 10. Screen Captures(画面キャプチャ)

準備中です。症状選択・所見入力・判定結果の各画面キャプチャを追加予定です。