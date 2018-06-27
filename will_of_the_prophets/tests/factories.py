"""Model factories."""

import factory
import pytz

from will_of_the_prophets import models


class SpecialSquareTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.SpecialSquareType


class SpecialSquareFactory(factory.django.DjangoModelFactory):
    """Special square factory."""

    type = factory.SubFactory(SpecialSquareTypeFactory)

    class Meta:
        model = models.SpecialSquare


class ButtholeFactory(factory.django.DjangoModelFactory):
    """Butthole factory."""

    start_square = factory.Sequence(lambda n: n + 2)
    end_square = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = models.Butthole


class RollFactory(factory.django.DjangoModelFactory):
    """Roll factory."""

    number = factory.Faker('pyint')
    embargo = factory.Faker('date_time', tzinfo=pytz.utc)

    class Meta:
        model = models.Roll
