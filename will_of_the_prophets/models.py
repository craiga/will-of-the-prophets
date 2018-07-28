"""Models."""

import random

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.models import model_to_dict

from model_utils.models import TimeStampedModel

# pylint: disable=cyclic-import
from will_of_the_prophets.validators import (not_butthole_start_validator,
                                             not_special_square_validator,
                                             RollEmbargoValidator)


SQUARE_VALIDATORS = [validators.MinValueValidator(1),
                     validators.MaxValueValidator(100)]


class SpecialSquareType(models.Model):
    """A special square type."""

    name = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='special_square')

    def __str__(self):
        return self.name


class SpecialSquare(models.Model):
    """A special square."""

    square = models.PositiveIntegerField(
        unique=True,
        validators=SQUARE_VALIDATORS + [not_butthole_start_validator])
    type = models.ForeignKey(SpecialSquareType,
                             on_delete=models.PROTECT,
                             related_name='squares')

    def __str__(self):
        return '{type} at {square}'.format(square=self.square,
                                           type=str(self.type))


class Butthole(models.Model):
    """A butthole."""

    start_square = models.PositiveIntegerField(
        unique=True,
        validators=SQUARE_VALIDATORS + [not_special_square_validator])
    end_square = models.PositiveIntegerField(validators=SQUARE_VALIDATORS)

    def clean(self):
        if self.start_square == self.end_square:
            raise ValidationError("A butthole cannot start and end in the "
                                  "same square.")

        return super().clean()

    def __str__(self):
        return '{start_square} to {end_square}'.format(**model_to_dict(self))


def default_roll_number():
    return random.randint(1, 6)


class Roll(TimeStampedModel):
    """A roll of the 'dice'."""

    number = models.PositiveIntegerField(default=default_roll_number)
    embargo = models.DateTimeField(validators=[RollEmbargoValidator()])

    def __str__(self):
        return '{number} on {embargo}'.format(**model_to_dict(self))
