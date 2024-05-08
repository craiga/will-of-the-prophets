"""Views."""

import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import condition
from django.views.generic.edit import CreateView

from will_of_the_prophets import board, forms, models

logger = logging.getLogger(__name__)


def get_last_modified(request):  # noqa: ANN001, ANN201, ARG001
    """Get board's last modified datetime."""
    try:
        last_modified = (
            models.Roll.objects.filter(embargo__lte=timezone.now())
            .latest("embargo")
            .embargo
        )
        logger.debug("Got last modified date %s", last_modified)
        return last_modified  # noqa: TRY300
    except models.Roll.DoesNotExist:
        logger.info("Cannot calculate last modified date as no rolls were found.")
        return None


@xframe_options_exempt
@condition(last_modified_func=get_last_modified)
@cache_control(max_age=3600)
def public_board(request):  # noqa: ANN001, ANN201
    """
    Board for the public.

    Does not take embargoed rolls into account.
    """
    now = timezone.now()
    response = render(
        request,
        "will_of_the_prophets/public_board.html",
        {
            "board": board.Board(now),
            "current_square_types": models.SpecialSquareType.objects.current(now),
            "archived_square_types": models.SpecialSquareType.objects.archived(now),
        },
    )

    canonical_url = settings.PUBLIC_BOARD_CANONICAL_URL
    if canonical_url:
        response["Link"] = f'<{canonical_url}>; rel="canonical"'

    return response


@xframe_options_exempt
@condition(last_modified_func=get_last_modified)
@cache_control(max_age=3600)
def roll_frequency(request):  # noqa: ANN001, ANN201
    """Show roll frequency."""
    roll_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for roll in models.Roll.objects.filter(embargo__lte=timezone.now()):
        roll_count[roll.number] += 1

    max_count = max(roll_count.values())

    return render(
        request,
        "will_of_the_prophets/roll_frequency.html",
        {"roll_frequency": roll_count, "max_count": max_count},
    )


class RollView(LoginRequiredMixin, CreateView):
    """View for rolling the die."""

    form_class = forms.RollForm
    template_name = "will_of_the_prophets/roll.html"

    def get_context_data(self, **kwargs):  # noqa: ANN003, ANN201, D102
        last_roll = models.Roll.objects.order_by("-embargo").first()
        last_roll_embargo = None
        if last_roll:
            last_roll_embargo = last_roll.embargo

        return super().get_context_data(
            **kwargs,
            last_roll=last_roll,
            board=board.Board(now=last_roll_embargo),
            special_square_types=models.SpecialSquareType.objects.current(
                last_roll_embargo
            ),
        )

    def get_success_url(self):  # noqa: ANN201, D102
        return reverse("roll") + "#chula"
