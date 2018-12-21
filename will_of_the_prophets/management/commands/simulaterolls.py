"""Simulate rolls."""

from django.core.management.base import BaseCommand

from will_of_the_prophets import board


class Command(BaseCommand):
    """Simulate rolls."""

    help = __doc__

    def handle(self, *args, **options):
        """Simulate some rolls."""
        game_board = board.Board()

        roll_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for _ in range(0, 100):
            roll = board.roll_weighted_die(game_board)
            roll_counts[roll] = roll_counts[roll] + 1

        current_position = game_board.get_current_position()
        self.stdout.write("Result\tCount\tSquare")
        for roll, roll_count in roll_counts.items():
            square = board.Square(current_position + roll)
            self.stdout.write(f"{roll}\t{roll_count}\t{square}")
