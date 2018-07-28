"""Validators."""

from datetime import datetime

from django.core.exceptions import ValidationError
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from will_of_the_prophets import models


def not_butthole_start_validator(value):
    if models.Butthole.objects.filter(start_square=value).exists():
        raise ValidationError(_("Cannot be a special square."))

    return value


def not_special_square_validator(value):
    if models.SpecialSquare.objects.filter(square=value).exists():
        raise ValidationError(_("Cannot be a special square."))

    return value


class RollEmbargoValidator(validators.MinValueValidator):
    """Validate that an roll's embargo date is later than all others."""

    def __init__(self, message=None):
        # pylint: disable=super-init-not-called
        if message:
            self.message = message

    @property
    def limit_value(self):
        """
        Get the latest embargo datetime.

        This is the minimum allowable value.
        """
        rolls = models.Roll.objects.order_by('-embargo')
        try:
            return rolls.values_list('embargo', flat=True)[0]
        except IndexError:
            return timezone.make_aware(datetime.min)
