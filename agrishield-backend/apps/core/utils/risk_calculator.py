import logging
from django.utils import timezone
from django.db.models import Avg, Q
from apps.data.models import FloodIndicator

logger = logging.getLogger(__name__)

class RiskCalculator:
    """
    Calculates flood risk scores using scientific indicators
    with zone-based risk multipliers.
    """

    # Indicator weights (must sum to 1.0, enforced in _normalize_weights)
    WEIGHTS = {
        'RAINFALL': 0.45,
        'RIVER_LEVEL': 0.45,
        'SATELLITE': 0.10,
    }

    # Risk thresholds (0–10 scale)
    THRESHOLDS = {
        'LOW': 3.0,
        'MODERATE': 6.0,
        'HIGH': 8.5,
    }

    # Time window for relevant indicators (hours)
    TIME_WINDOW = 48

    @classmethod
    def calculate_village_risk(cls, village):
        """
        Calculate current flood risk for a village with zone-based multipliers.
        Returns risk level (LOW/MODERATE/HIGH).
        """
        try:
            base_score = cls._calculate_base_score(village)
            zone_factor = cls._get_zone_factor(village)
            adjusted_score = base_score * zone_factor
            return cls._score_to_risk_level(adjusted_score)
        except Exception as e:
            logger.exception(f"Risk calculation failed for {village.name}: {str(e)}")
            return 'LOW'

    @classmethod
    def _calculate_base_score(cls, village):
        """Calculate raw risk score (0–10) before zone adjustments."""
        indicators = FloodIndicator.objects.filter(
            Q(village=village) | Q(affects_villages=village),
            timestamp__gte=timezone.now() - timezone.timedelta(hours=cls.TIME_WINDOW)
        ).distinct()

        if not indicators.exists():
            return 0.0

        weights = cls._normalize_weights(cls.WEIGHTS)
        scores = {}

        for ind_type, weight in weights.items():
            type_indicators = indicators.filter(indicator_type=ind_type)

            if not type_indicators.exists():
                scores[ind_type] = 0.0
                continue

            if ind_type in ['RAINFALL', 'RIVER_LEVEL']:
                avg_value = type_indicators.aggregate(avg=Avg('value'))['avg'] or 0.0
                scores[ind_type] = cls._normalize_value(ind_type, avg_value)

            elif ind_type == 'SATELLITE':
                # Binary – presence indicates risk
                scores[ind_type] = 1.0

        # Weighted sum scaled to 0–10
        return sum(score * weight * 10 for ind_type, score in scores.items())

    @classmethod
    def _get_zone_factor(cls, village):
        """Get risk multiplier from flood zones."""
        zones = village.flood_zones.all()
        if not zones.exists():
            return 1.0
        return max(z.risk_factor for z in zones)

    @classmethod
    def _score_to_risk_level(cls, score):
        """Convert numeric score to risk level."""
        if score >= cls.THRESHOLDS['HIGH']:
            return 'HIGH'
        elif score >= cls.THRESHOLDS['MODERATE']:
            return 'MODERATE'
        return 'LOW'

    @staticmethod
    def _normalize_value(indicator_type, value):
        """
        Normalize different indicator values to 0–1 scale.
        Based on known thresholds for Budalang'i region.
        """
        if indicator_type == 'RAINFALL':
            return min(value / 150.0, 1.0)  # 150mm = extreme
        elif indicator_type == 'RIVER_LEVEL':
            return min((value - 4.0) / 3.0, 1.0)  # 4m normal → 7m extreme
        return 0.0

    @staticmethod
    def _normalize_weights(weights):
        """Ensure weights sum to 1.0 (auto-normalize)."""
        total = sum(weights.values())
        if total == 0:
            raise ValueError("Indicator weights cannot all be zero.")
        return {k: v / total for k, v in weights.items()}
