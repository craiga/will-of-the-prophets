"""Views."""

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from will_of_the_prophets import board, forms, models


def public_board(request):
    """
    Board for the public.

    Does not take embargoed rolls into account.
    """
    special_square_types = models.SpecialSquareType.objects.all()
    return render(request, 'will_of_the_prophets/public_board.html',
                  {'board': board.Board(),
                   'special_square_types': special_square_types})


class RollView(LoginRequiredMixin, FormView):
    """View for rolling the die."""

    form_class = forms.RollForm
    template_name = 'will_of_the_prophets/roll.html'
    success_url = '/rolls/'

    def get_context_data(self, **kwargs):
        last_roll = models.Roll.objects.order_by('-embargo').first()
        return super().get_context_data(
            **kwargs,
            last_roll=last_roll,
            board=board.Board(now=last_roll.embargo),
        )
