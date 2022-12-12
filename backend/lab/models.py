from django.db import models
from django.utils import timezone

from knepp.db.mixins import Timestamps, StandardModel
from lab.enums import ChemicalType, DevelopmentType


class Brand(StandardModel, Timestamps):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Chemical(StandardModel, Timestamps):
    name = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(
        choices=((ct.value, ct.name) for ct in ChemicalType)
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.brand} {self.name}"


class Development(StandardModel, Timestamps):
    name = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(
        choices=((dt.value, dt.name) for dt in DevelopmentType)
    )

    def __str__(self) -> str:
        return self.name


class Step(StandardModel, Timestamps):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    development = models.ForeignKey(Development, on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    temperature = models.IntegerField(default=20)
    accuracy = models.IntegerField(default=0)
    duration = models.DurationField(default=timezone.timedelta(minutes=10))

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = ("development", "order")
