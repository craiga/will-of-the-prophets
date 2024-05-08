"""Models."""

import random
import warnings

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from model_utils.models import TimeFramedModel, TimeStampedModel
from s3direct.fields import S3DirectField

from will_of_the_prophets.validators import RollEmbargoValidator

SQUARE_VALIDATORS = [validators.MinValueValidator(1), validators.MaxValueValidator(100)]


class SpecialSquareTypeModelQuerySet(models.QuerySet):  # noqa: D101
    def current(self, now=None):  # noqa: ANN001, ANN201, D102
        now = now if now else timezone.now()
        return super().filter(squares__in=SpecialSquare.objects.active(now)).distinct()

    def archived(self, now):  # noqa: ANN001, ANN201, D102
        now = now if now else timezone.now()
        return (
            super()
            .exclude(
                models.Q(squares__end__gt=now) | models.Q(squares__end__isnull=True)
            )
            .distinct()
        )


SpecialSquareTypeModelManager = models.Manager.from_queryset(
    SpecialSquareTypeModelQuerySet
)


class SpecialSquareType(models.Model):
    """A special square type."""

    name = models.TextField()
    description = models.TextField()
    image = S3DirectField(dest="special_square")
    auto_move = models.IntegerField(
        default=0, help_text="Automatically move the runabout by this many places"
    )

    objects = SpecialSquareTypeModelManager()

    def __str__(self) -> str:  # noqa: D105
        return self.name


class TimeFramedModelQuerySet(models.QuerySet):  # noqa: D101
    def active(self, now=None):  # noqa: ANN001, ANN201, D102
        now = now if now else timezone.now()
        return (
            super()
            .filter(models.Q(start__lt=now) | models.Q(start__isnull=True))
            .filter(models.Q(end__gt=now) | models.Q(end__isnull=True))
        )


TimeFramedModelManager = models.Manager.from_queryset(TimeFramedModelQuerySet)


class SpecialSquare(TimeFramedModel):
    """A special square."""

    square = models.PositiveIntegerField(validators=SQUARE_VALIDATORS)
    type = models.ForeignKey(
        SpecialSquareType, on_delete=models.PROTECT, related_name="squares"
    )

    objects = TimeFramedModelManager()

    def __str__(self) -> str:  # noqa: D105
        return f"{self.type!s} at {self.square}"


class Butthole(TimeFramedModel):
    """A butthole."""

    start_square = models.PositiveIntegerField(validators=SQUARE_VALIDATORS)
    end_square = models.PositiveIntegerField(validators=SQUARE_VALIDATORS)

    objects = TimeFramedModelManager()

    def clean(self):  # noqa: ANN201, D102
        if self.start_square == self.end_square:
            msg = "A butthole cannot start and end in the " "same square."
            raise ValidationError(msg)

        return super().clean()

    def __str__(self) -> str:  # noqa: D105
        return "{start_square} to {end_square}".format(**model_to_dict(self))


def default_roll_number():  # noqa: ANN201, D103
    warnings.warn("Default roll number no longer used.", category=DeprecationWarning)  # noqa: B028
    return random.randint(1, 6)  # noqa: S311


class Roll(TimeStampedModel):
    """A roll of the 'dice'."""

    number = models.PositiveIntegerField(blank=False, null=False)
    embargo = models.DateTimeField(validators=[RollEmbargoValidator()])

    def __str__(self) -> str:  # noqa: D105
        return "{number} on {embargo}".format(**model_to_dict(self))
