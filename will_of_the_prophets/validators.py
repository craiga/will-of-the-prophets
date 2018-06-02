"""Validators."""

from django.core.exceptions import ValidationError
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

def future_validator(value):
    if value < timezone.now():
        raise ValidationError(_("Date should be in the future."))

    return value
