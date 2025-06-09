from turtle import Turtle
from game_specs import SCREEN_DIMENSIONS, WALLS

class Paddle(Turtle):
    """
    Represents the player's paddle in the Breakout game.
    Inherits from the Turtle class for graphical representation and movement.
    """

    def __init__(self, position):
        """
        Initializes the paddle with dynamic size based on screen dimensions
        and places it at the given position.

        :param position: (tuple) The initial position of the paddle
        """
        super().__init__()
        screen_w = SCREEN_DIMENSIONS["width"]
        screen_h = SCREEN_DIMENSIONS["height"]

        self.shape("square")
        self.color("blue")
        self.penup()

        # Size is proportional to screen dimensions
        self.paddle_width = screen_w * 0.12          # 12% of screen width
        self.paddle_height = screen_h * 0.015        # 1.5% of screen height
        stretch_len = self.paddle_width / 20         # Base turtle size is 20x20
        stretch_wid = self.paddle_height / 20

        self.shapesize(stretch_wid = stretch_wid, stretch_len = stretch_len)
        self.goto(position)

        # Movement flags for continuous motion control
        self.moving_right = False
        self.moving_left = False

        # Save the original width for potential resizing
        self.original_width = self.paddle_width

    def start_move_right(self):
        """
        Start moving the paddle to the right.

        :return: None
        """
        self.moving_right = True

    def start_move_left(self):
        """
        Start moving the paddle to the left.

        :return: None
        """
        self.moving_left = True

    def stop_move_right(self):
        """
        Stop moving the paddle to the right.

        :return: None
        """
        self.moving_right = False

    def stop_move_left(self):
        """
        Stop moving the paddle to the left.

        :return: None
        """
        self.moving_left = False

    def go_right(self):
        """
        Moves the paddle to the right by a fixed step,
        making sure it does not go beyond the right wall.

        :return: None
        """
        new_x = self.xcor() + 20
        if new_x <= WALLS["right"] - (self.paddle_width / 2):
            self.goto(new_x, self.ycor())

    def go_left(self):
        """
        Moves the paddle to the left by a fixed step,
        making sure it does not go beyond the left wall.

        :return: None
        """
        new_x = self.xcor() - 20
        if new_x >= WALLS["left"] + (self.paddle_width / 2):
            self.goto(new_x, self.ycor())

    def resize(self, new_width):
        """
        Resizes the paddle to a new width (e.g., after collecting power-down).
        Also updates the shape scaling accordingly.

        :param new_width: ( float) The new size of the paddle
        :return: None
        """
        self.paddle_width = new_width
        stretch_len = self.paddle_width / 20
        stretch_wid = self.paddle_height / 20
        self.shapesize(stretch_wid = stretch_wid, stretch_len = stretch_len)
