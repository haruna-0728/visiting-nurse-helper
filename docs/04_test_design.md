# Test Design（テスト設計）

## Document Information（文書情報）

| Item（項目） | Value（値） |
| --- | --- |
| Document ID（文書ID） | VNH-04 |
| Version（バージョン） | 0.2 |
| Status（ステータス） | Draft |
| Created Date（作成日） | 2026-09-14 |
| Last Updated（最終更新日） | 2026-09-14 |
| Owner（管理者） | haruna-0728 |

---

## Table of Contents（目次）

1. [Test Policy（テスト方針）](#1-test-policy)
2. [Test File List（テストファイル一覧）](#2-test-file-list)
3. [Test Design Pattern（テスト設計パターン）](#3-test-design-pattern)
4. [Running Tests（テストの実行方法）](#4-running-tests)

---

## 1. Test Policy（テスト方針）

各`RiskCondition`の緊急度判定ロジックについて、境界値（所見なし／単独所見／複数所見の組み合わせ）を中心にpytestで検証する。`scales.py`の各スケール変換関数についても、区分の境界値を網羅的にテストする。

---

## 2. Test File List（テストファイル一覧）

対応する11症状すべてについて、専用のデータテストファイルを整備している。

| ファイル | 対象 |
| --- | --- |
| `test_models.py` | Symptom / RiskCondition / EscalationRuleの基本ロジック |
| `test_data_fever.py` | 発熱データ |
| `test_data_fatigue.py` | 倦怠感データ |
| `test_data_dyspnea.py` | 呼吸苦データ |
| `test_data_abdominal_pain.py` | 疼痛（腹痛）データ |
| `test_data_vomiting_diarrhea.py` | 嘔吐・下痢データ |
| `test_data_skin_trouble.py` | 皮膚トラブルデータ |
| `test_data_dizziness.py` | めまいデータ |
| `test_data_chest_pain.py` | 胸痛データ |
| `test_data_headache.py` | 頭痛データ |
| `test_data_edema.py` | 浮腫データ |
| `test_data_urinary_trouble.py` | 排尿トラブルデータ |
| `test_scales.py` | JCS/GCS・NPUAP/DESIGN-R®・MMT・血圧の変換ロジック |

---

## 3. Test Design Pattern（テスト設計パターン）

各データテストファイルは、以下のパターンで構成する。

1. `RiskCondition`を名前で取得するヘルパー関数を用意する
2. 「所見なしで基準緊急度のまま」「単独所見での引き上げ」「複数所見の組み合わせでの引き上げ」「引き上げ条件を満たさないケース」を個別にテストする
3. `Symptom.evaluate()`を使い、複数の疾患候補にまたがる最終緊急度（`__overall__`）が正しく最大値を採用しているかを確認する

`test_scales.py`では、各スケールの区分の境界値（例：GCS合計点12点→中等度、13点→軽度）を1件ずつテストし、ラベル生成関数が値と説明文を含むかも確認する。

---

## 4. Running Tests（テストの実行方法）

```
pytest
```

全11症状のデータテスト・モデルテスト・スケールテストを合わせて137件以上のテストが全件PASSしていることを確認済みです（発熱・倦怠感・皮膚トラブルのテスト追加後の最新件数は、お手元の実行結果を反映してください）。
