from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Literal, Dict

from .risk_calculator import Tier, tier_to_int, int_to_tier


@dataclass(frozen=True)
class AlertDecision:
    """
    Decision returned by should_trigger_alert().
    """
    trigger: bool
    reason: str
    new_tier: Tier
    previous_tier: Optional[Tier]
    do_escalation_sms: bool
    do_downgrade_sms: bool


def should_trigger_alert(
    previous_tier: Optional[Tier],
    new_tier: Tier,
    last_change_at: Optional[datetime],
    now: datetime,
    *,
    hysteresis_steps: int = 1,
    min_interval_between_changes: timedelta = timedelta(minutes=30),
) -> AlertDecision:
    """
    Simple, conservative hysteresis policy:
      - Only alert on upward movement of >= hysteresis_steps.
      - Downgrades are gated by min_interval_between_changes (optional SMS).
    """
    if previous_tier is None:
        # First classification -> no SMS blast; let caller decide to "seed" state.
        return AlertDecision(
            trigger=False,
            reason="no_previous_tier",
            new_tier=new_tier,
            previous_tier=None,
            do_escalation_sms=False,
            do_downgrade_sms=False,
        )

    prev_i = tier_to_int(previous_tier)
    new_i = tier_to_int(new_tier)

    # Prevent flip-flop spam
    if last_change_at and (now - last_change_at) < min_interval_between_changes:
        return AlertDecision(
            trigger=False,
            reason="cooldown_active",
            new_tier=new_tier,
            previous_tier=previous_tier,
            do_escalation_sms=False,
            do_downgrade_sms=False,
        )

    if new_i >= prev_i + hysteresis_steps:
        return AlertDecision(
            trigger=True,
            reason="tier_escalated",
            new_tier=new_tier,
            previous_tier=previous_tier,
            do_escalation_sms=True,
            do_downgrade_sms=False,
        )

    if new_i < prev_i:
        # Downgrade - usually optional; you may want to send a reassuring SMS only
        # when moving from severe/high back to moderate/low.
        return AlertDecision(
            trigger=True,
            reason="tier_downgraded",
            new_tier=new_tier,
            previous_tier=previous_tier,
            do_escalation_sms=False,
            do_downgrade_sms=True,
        )

    return AlertDecision(
        trigger=False,
        reason="tier_unchanged_or_minor_variation",
        new_tier=new_tier,
        previous_tier=previous_tier,
        do_escalation_sms=False,
        do_downgrade_sms=False,
    )


# --- Messaging ---

# Compact SMS templates (keep < 160 chars where possible).
TIER_TITLES: Dict[Tier, str] = {
    "low": "Hatari Ndogo",
    "moderate": "Tahadhari",
    "high": "Onyo Kuu",
    "severe": "Dharura",
}

def _eta_from_rate(level_cm: float, danger_cm: float, rate_cm_hr: float) -> Optional[int]:
    """
    Rough ETA (hours) until danger level, assuming monotonic rise.
    """
    if rate_cm_hr <= 0:
        return None
    if level_cm >= danger_cm:
        return 0
    remaining = max(danger_cm - level_cm, 0.0)
    return int(round(remaining / rate_cm_hr))


def build_alert_message(
    *,
    village_name: str,
    river_name: str,
    tier: Tier,
    level_cm: float,
    rate_cm_hr: float,
    danger_level_cm: float,
    severe_level_cm: float,
    language: str = "sw",  # 'sw' or 'en'
) -> str:
    """
    Build concise, actionable SMS referencing scientific evidence (WRA levels & rate).
    """
    eta_h = _eta_from_rate(level_cm, danger_level_cm, rate_cm_hr)

    if language == "en":
        title = {
            "low": "Low Risk",
            "moderate": "Advisory",
            "high": "Warning",
            "severe": "Emergency",
        }[tier]
        parts = [
            f"AgriShield {title}: {village_name}.",
            f"{river_name} level {int(round(level_cm))}cm, rising {rate_cm_hr:.1f}cm/hr.",
        ]
        if eta_h is not None and eta_h > 0:
            parts.append(f"Est. {eta_h}h to danger.")
        if tier in ("high", "severe"):
            parts.append("Move livestock, harvest early, avoid crossings.")
        elif tier == "moderate":
            parts.append("Prepare: secure tools, check routes.")
        return " ".join(parts)[:160]

    # Kiswahili (default)
    title_sw = TIER_TITLES[tier]
    parts_sw = [
        f"AgriShield {title_sw}: {village_name}.",
        f"Kiwango cha {river_name} {int(round(level_cm))}cm, kina panda {rate_cm_hr:.1f}cm/saa.",
    ]
    if eta_h is not None and eta_h > 0:
        parts_sw.append(f"Muda makadirio {eta_h}saa kufikia hatari.")
    if tier in ("high", "severe"):
        parts_sw.append("Hamisha mifugo, vuna mapema, epuka kuvuka.")
    elif tier == "moderate":
        parts_sw.append("Jiandae: linda zana, kagua njia.")
    return " ".join(parts_sw)[:160]
