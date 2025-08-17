import uuid
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Minimal, reliable audit fields for all models.
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class UUIDModel(TimeStampedModel):
    """
    UUID primary key base model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class SoftDeleteModel(UUIDModel):
    """
    Soft-delete support for critical records (alerts, snapshots, etc.).
    """
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteQuerySet.as_manager()

    def delete(self, using=None, keep_parents=False):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    class Meta:
        abstract = True


class ConfigKV(UUIDModel):
    """
    Simple key/value config store for feature flags and thresholds.
    Keep core app self-contained; higher layers can override via settings/env.
    """
    key = models.CharField(max_length=128, unique=True, db_index=True)
    value = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = 'core'
        db_table = "core_config_kv"
        verbose_name = "Core Config KV"
        verbose_name_plural = "Core Config KV"
        indexes = [models.Index(fields=["key"])]

    def __str__(self):
        return f"{self.key}"


class Village(UUIDModel):
    """
    Represents a village/community where users and alerts are linked.
    """
    name = models.CharField(max_length=128, unique=True)
    county = models.CharField(max_length=128, blank=True, null=True)
    region = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        app_label = 'core'
        db_table = "core_village"
        verbose_name = "Village"
        verbose_name_plural = "Villages"
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name
