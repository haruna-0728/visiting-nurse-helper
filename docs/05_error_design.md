# Error Design（エラー設計・簡易版）

## Document Information（文書情報）

| Item（項目） | Value（値） |
| --- | --- |
| Document ID（文書ID） | VNH-05 |
| Version（バージョン） | 0.1 |
| Status（ステータス） | Draft |
| Created Date（作成日） | 2026-09-14 |
| Owner（管理者） | haruna-0728 |
| Note（注記） | 本ツールは単一のStreamlit画面で完結し、外部APIやユーザーによる自由入力（フォーム送信等）をほとんど持たないため、簡易版として作成しています。 |

---

## Table of Contents（目次）

1. [Validation Errors（バリデーションエラー）](#1-validation-errors)
2. [Input Constraints（入力値の制約）](#2-input-constraints)
3. [Known Limitations（既知の制約事項）](#3-known-limitations)

---

## 1. Validation Errors（バリデーションエラー）

`models.py`では、Pydanticの`Literal`型により`Severity`（なし／軽度／中等度／高度）と`UrgencyLevel`（経過観察／医師へ報告／直ちに受診・緊急要請）の取りうる値を型レベルで固定している。定義外の値を渡した場合、`RiskCondition`や`EscalationRule`のインスタンス化時点でPydanticの`ValidationError`が送出される。

`EscalationRule`には`model_validator`によるチェックがあり、以下の場合に`ValueError`を送出する。

- `type="sign_count"`にもかかわらず`min_count`が指定されていない場合
- `type="single_sign"`にもかかわらず`min_count`が指定されている場合

`Symptom`には`field_validator`があり、`risk_conditions`が1件も存在しない場合に`ValueError`を送出する。

これらはいずれも`data.py`でのデータ定義段階のミスを早期に検知するためのものであり、アプリ実行時にエンドユーザーの入力によって発生するものではない。

---

## 2. Input Constraints（入力値の制約）

Streamlit画面上の入力は、以下のようにすべて選択式・数値範囲指定の入力欄で構成されており、不正な形式の値が入力される余地を設計上排除している。

| 入力項目 | 制約 |
| --- | --- |
| 通常の所見 | セレクトボックス（なし／軽度／中等度／高度）のみ選択可能 |
| JCS/GCSスコア | 定義済みの選択肢からのみ選択可能 |
| NPUAP/EPUAP分類・DESIGN-R® | 定義済みの選択肢からのみ選択可能 |
| MMT評価 | 0〜5点の選択肢からのみ選択可能 |
| 血圧（収縮期／拡張期） | `st.number_input`で最小値・最大値・刻み幅を指定（収縮期60〜260、拡張期30〜180） |

---

## 3. Known Limitations（既知の制約事項）

- 本ツールはポートフォリオ用のサンプルであり、入力値そのものの臨床的な妥当性（例：血圧の左右差が生理的にありえない組み合わせかどうか等）はチェックしていない。
- ネットワーク通信や外部APIを使用しないため、通信エラーやタイムアウトに関する設計は対象外である。
- 判定結果はあくまでサンプルロジックによる目安であり、エラーではなく免責事項（disclaimer）として、実際の受診判断への使用を禁止する注意書きを画面上部に常時表示している。
