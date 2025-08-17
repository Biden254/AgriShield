from celery import shared_task
from django.utils import timezone
from django.conf import settings
from apps.alerts.models import Alert, AlertDelivery
from apps.integrations.sms.providers import send_sms
from django.contrib.auth import get_user_model
from apps.core.utils.risk_calculator import RiskCalculator
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def check_and_trigger_alerts(self):
    """Main task to check risks and trigger alerts"""
    try:
        from apps.core.models import Village

        # Get villages with recent indicator updates
        villages = Village.objects.filter(
            floodindicator__timestamp__gte=timezone.now() - timezone.timedelta(hours=6)
        ).distinct()

        for village in villages:
            current_risk = RiskCalculator.calculate_village_risk(village)
            active_alerts = village.alerts.filter(is_active=True)

            # Only create new alert if risk level changed
            if not active_alerts.exists() or active_alerts.first().alert_level != current_risk:
                create_village_alert.delay(village.id, current_risk)

    except Exception as e:
        logger.error(f"Failed to check alerts: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task
def create_village_alert(village_id, risk_level):
    """Create alert record for a village"""
    from apps.core.models import Village
    from apps.data.models import FloodIndicator

    village = Village.objects.get(id=village_id)

    # Get recent indicators for alert context
    recent_indicators = FloodIndicator.objects.filter(
        village=village,
        timestamp__gte=timezone.now() - timezone.timedelta(hours=24)
    ).select_related('village')

    # Prepare alert data
    rainfall_data = None
    river_level = None
    indigenous_indicators = {}

    for indicator in recent_indicators:
        if indicator.indicator_type == 'RAINFALL':
            rainfall_data = {
                'value': indicator.value,
                'unit': 'mm',
                'source': 'KMD'
            }
        elif indicator.indicator_type == 'RIVER_LEVEL':
            river_level = indicator.value
        elif indicator.indicator_type == 'INDIGENOUS':
            indigenous_indicators[str(indicator.id)] = indicator.value

    # Determine alert validity period
    valid_until = timezone.now() + timezone.timedelta(
        hours=48 if risk_level == 'HIGH' else 72
    )

    # Create the alert
    alert = Alert.objects.create(
        village=village,
        alert_level=risk_level,
        message="",  # Will be generated before sending
        valid_until=valid_until,
        rainfall_data=rainfall_data,
        river_level=river_level,
        indigenous_indicators=indigenous_indicators or None
    )

    # Generate proper message
    alert.message = alert.generate_message()
    alert.save()

    # Trigger delivery
    deliver_village_alert.delay(alert.id)


@shared_task(bind=True, max_retries=3)
def deliver_village_alert(self, alert_id):
    """Deliver alert to all farmers in a village"""
    try:
        alert = Alert.objects.get(id=alert_id)
        farmers = User.objects.filter(farmer_profile__village=alert.village).select_related('farmer_profile__village')

        for farmer in farmers:
            # Avoid duplicate deliveries
            if not AlertDelivery.objects.filter(alert=alert, farmer=farmer).exists():
                delivery = AlertDelivery.objects.create(
                    alert=alert,
                    farmer=farmer,
                    delivery_method='SMS',
                    status='PENDING'
                )

                # Send SMS asynchronously
                send_alert.delay(delivery.id)

    except Exception as e:
        logger.error(f"Failed to deliver alert {alert_id}: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_alert(self, delivery_id):
    """Actually send the alert via preferred method"""
    try:
        delivery = AlertDelivery.objects.get(id=delivery_id)

        if delivery.delivery_method == 'SMS':
            success = send_sms(
                phone_number=delivery.farmer.phone_number,
                message=delivery.alert.message
            )

            if success:
                delivery.status = 'DELIVERED'
                delivery.delivery_confirmed = True
            else:
                delivery.status = 'FAILED'

            delivery.sent_at = timezone.now()
            delivery.save()

    except Exception as e:
        logger.error(f"Failed to send alert {delivery_id}: {str(e)}")
        self.retry(exc=e, countdown=60)
