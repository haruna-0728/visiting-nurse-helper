"""visiting_nurse_helper/models.py

在宅・施設訪問看護お助けツールの中核となるデータモデル。

    Symptom(自覚症状) → RiskCondition(疾患候補) → EscalationRule(緊急度引き上げルール)

という3階層の構造で、観察した所見(S/Oデータ)から緊急度を判定する。
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, field_validator, model_validator

# --- 基本の型定義 -----------------------------------------------------

Severity = Literal["なし", "軽度", "中等度", "高度"]
UrgencyLevel = Literal["経過観察", "医師へ報告", "直ちに受診・緊急要請"]

# 比較用の順序(値が大きいほど重い)
SEVERITY_ORDER: dict[Severity, int] = {"なし": 0, "軽度": 1, "中等度": 2, "高度": 3}
URGENCY_ORDER: dict[UrgencyLevel, int] = {
    "経過観察": 0,
    "医師へ報告": 1,
    "直ちに受診・緊急要請": 2,
}


def _severity_score(value: Severity) -> int:
    return SEVERITY_ORDER[value]


def highest_urgency(levels: list[UrgencyLevel]) -> UrgencyLevel:
    """複数の緊急度の中から最も高いものを返す。"""
    return max(levels, key=lambda level: URGENCY_ORDER[level])


# --- 緊急度を引き上げるルール -------------------------------------------


class EscalationRule(BaseModel):
    """疾患候補ごとの緊急度引き上げルール。

    - type="single_sign": いずれか1つの所見が min_severity 以上なら引き上げる
    - type="sign_count":   min_severity 以上の所見が min_count 個以上あれば引き上げる
    """

    type: Literal["single_sign", "sign_count"]
    min_severity: Severity
    urgency: UrgencyLevel
    min_count: Optional[int] = None

    @model_validator(mode="after")
    def _check_min_count(self) -> "EscalationRule":
        if self.type == "sign_count" and self.min_count is None:
            raise ValueError("type='sign_count' には min_count の指定が必要です")
        if self.type == "single_sign" and self.min_count is not None:
            raise ValueError("type='single_sign' に min_count は不要です")
        return self

    def matches(self, observed_signs: dict[str, Severity]) -> bool:
        threshold = _severity_score(self.min_severity)
        matched = [s for s in observed_signs.values() if _severity_score(s) >= threshold]

        if self.type == "single_sign":
            return len(matched) >= 1
        return len(matched) >= (self.min_count or 0)


# --- 疾患候補 -----------------------------------------------------------


class RiskCondition(BaseModel):
    """1つの疾患候補と、それを判定するための観察ポイント・ルール。"""

    name: str
    base_urgency: UrgencyLevel
    key_signs: list[str]  # 観察すべき所見名の一覧(表示用)
    escalation_rules: list[EscalationRule] = []

    def evaluate(self, observed_signs: dict[str, Severity]) -> UrgencyLevel:
        """観察された所見から、この疾患候補の緊急度を判定する。

        observed_signs には他の疾患候補向けの所見も混ざりうるため、
        自分の key_signs に含まれるものだけを判定に使う。
        """
        own_signs = {
            name: severity
            for name, severity in observed_signs.items()
            if name in self.key_signs
        }
        levels: list[UrgencyLevel] = [self.base_urgency]
        for rule in self.escalation_rules:
            if rule.matches(own_signs):
                levels.append(rule.urgency)
        return highest_urgency(levels)


# --- 症状全体 -----------------------------------------------------------


class Symptom(BaseModel):
    """1つの自覚症状(S)と、そこから考えられる疾患候補群。"""

    name: str
    risk_conditions: list[RiskCondition]

    @field_validator("risk_conditions")
    @classmethod
    def _must_have_condition(cls, v: list[RiskCondition]) -> list[RiskCondition]:
        if not v:
            raise ValueError("risk_conditionsは1件以上必要です")
        return v

    def evaluate(self, observed_signs: dict[str, Severity]) -> dict[str, UrgencyLevel]:
        """疾患候補ごとの緊急度と、全体としての最終緊急度をまとめて返す。"""
        per_condition: dict[str, UrgencyLevel] = {
            condition.name: condition.evaluate(observed_signs)
            for condition in self.risk_conditions
        }
        per_condition["__overall__"] = highest_urgency(list(per_condition.values()))
        return per_condition