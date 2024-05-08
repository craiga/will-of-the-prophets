"""Validators."""

import warnings
from datetime import datetime

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from will_of_the_prophets import models


def not_butthole_start_validator(value):  # noqa: ANN001, ANN201
    """Validator to ensure square is not the start of a butthole."""  # noqa: D401
    warnings.warn(  # noqa: B028
        "Validator does not consider butthole time frames.", DeprecationWarning
    )
    if models.Butthole.objects.filter(start_square=value).exists():
        raise ValidationError(_("Cannot be a special square."))

    return value


def not_special_square_validator(value):  # noqa: ANN001, ANN201
    """Validator to ensure square is not a special square."""  # noqa: D401
    warnings.warn(  # noqa: B028
        "Validator does not consider special square time frames.", DeprecationWarning
    )
    if models.SpecialSquare.objects.filter(square=value).exists():
        raise ValidationError(_("Cannot be a special square."))

    return value


class RollEmbargoValidator(validators.MinValueValidator):
    """Validate that an roll's embargo date is later than all others."""

    def __init__(self, message=None) -> None:  # noqa: ANN001, D107
        if message:
            self.message = message

    @property
    def limit_value(self):  # noqa: ANN201
        """
        Get the latest embargo datetime.

        This is the minimum allowable value.
        """
        rolls = models.Roll.objects.order_by("-embargo")
        try:
            return rolls.values_list("embargo", flat=True)[0]
        except IndexError:
            return timezone.make_aware(datetime.min)
