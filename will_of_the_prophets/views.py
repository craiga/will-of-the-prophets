"""Views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import condition
from django.views.generic.edit import CreateView

from will_of_the_prophets import board, forms, models


def get_last_modified(request):
    """Get board's last modified datetime."""
    try:
        return (
            models.Roll.objects.filter(embargo__lte=timezone.now())
            .latest("embargo")
            .embargo
        )
    except models.Roll.DoesNotExist:
        return None


@xframe_options_exempt
@condition(last_modified_func=get_last_modified)
def public_board(request):
    """
    Board for the public.

    Does not take embargoed rolls into account.
    """
    special_square_types = models.SpecialSquareType.objects.all()
    return render(
        request,
        "will_of_the_prophets/public_board.html",
        {"board": board.Board(), "special_square_types": special_square_types},
    )


class RollView(LoginRequiredMixin, CreateView):
    """View for rolling the die."""

    form_class = forms.RollForm
    template_name = "will_of_the_prophets/roll.html"

    def get_context_data(self, **kwargs):
        last_roll = models.Roll.objects.order_by("-embargo").first()
        return super().get_context_data(
            **kwargs,
            last_roll=last_roll,
            board=board.Board(now=last_roll.embargo),
            special_square_types=models.SpecialSquareType.objects.all()
        )

    def get_success_url(self):
        return reverse("roll") + "#chula"
