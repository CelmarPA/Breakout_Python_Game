from turtle import Turtle
from math import ceil
from game_specs import SCREEN_DIMENSIONS, WALLS
from math import pi, sin, cos
from random import uniform

class Ball(Turtle):
    """
    The Ball class manages the behavior and appearance of the ball in the game.
    It handles movement, collisions with walls, paddles, and blocks, as well as
    triggering related sound effects and interactions.
    """

    def __init__(self):
        super().__init__()
        screen_w = SCREEN_DIMENSIONS["width"] # The width of the game's screen

        self.sounds = None

        self.shape("circle")
        self.color("white")
        self.penup()

        # Ball size proportional to screen width
        ball_diameter = screen_w * 0.02     # 2% da width
        stretch_factor = ball_diameter / 20
        self.shapesize(stretch_wid = stretch_factor, stretch_len = stretch_factor)

        # Store radius for collision detection
        self.radius = (self.shapesize()[0] * 20) / 2
        self.goto(0, 0)

        # Initial movement speed
        self.x_move = 10
        self.y_move = 10
        self.max_horizontal_speed = 10

        self.walls = WALLS      # Screen boundary positions

    def move_ball(self, paddle, blocks, scoreboard):
        """
        Moves the ball incrementally to ensure smooth motion and accurate collision detection.
        This function divides the ball's movement into small steps (sub-pixels) to check for collisions
        at multiple points along its path. This prevents the ball from "tunneling" through objects like
        the paddle or blocks when moving at high speeds.

        :param paddle: (object) The paddle object the ball can collide with.
        :param blocks: (list) A list of block objects that the ball can break.
        :param scoreboard: (object) The scoreboard object used to update the player's score.
        :return: None
        """
        # Define the maximum distance the ball can move in one step (to prevent skipping over collisions)
        max_step = 1

        # Determine the larger movement in either x or y direction
        max_move = max(abs(self.x_move), abs(self.y_move))

        # Calculate how many small steps are needed to ensure smooth movement
        steps = ceil(max_move / max_step)

        # Calculate the amount to move per step in both directions
        dx = self.x_move / steps
        dy = self.y_move / steps

        # Move the ball in small increments, checking for collisions after each move
        for _ in range(steps):
            self.goto(self.xcor() + dx, self.ycor() + dy)   # Move the ball slightly
            self.detect_walls()     # Check for collision with walls (and bounce if needed)

            # If the ball hits the paddle, stop movement for this frame
            if self.detect_paddle(paddle):
                break

            # If the ball hits any block, update the score and stop movement for this frame
            if self.detect_blocks(blocks, scoreboard, paddle):
                break

    def bounce_y(self):
        """
        Invert vertical direction (used after top/paddle collision).

        :return: None
        """
        self.y_move *= -1

    def bounce_x(self):
        """
        Invert horizontal direction (used after side wall/block collision).

        :return: None
        """
        self.x_move *= -1

    def detect_walls(self):
        """
        Detects and handles collisions between the ball and the screen boundaries (walls).
        If the ball collides with the left, right, or top wall, it is repositioned slightly
        away from the wall (using a margin) and its movement direction is reversed (bounced).
        The bounce only occurs if the ball is moving toward the wall, to avoid double bouncing.

        :return: None
        """

        margin = 0.1   # Small offset to prevent the ball from sticking to the wall

        # Check for collision with the left wall
        if self.xcor() < self.walls["left"] + self.radius:
            # Push the ball slightly away from the wall
            self.setx(self.walls["left"] + self.radius + margin)
            if self.x_move < 0:  # Only bounce if the ball is moving left
                self.bounce_x()

        # Check for collision with the right wall
        elif self.xcor() > self.walls["right"] - self.radius:
            self.setx(self.walls["right"] - self.radius - margin)
            if self.x_move > 0:  # Only bounce if the ball is moving right
                self.bounce_x()

        # Check for collision with the top wall
        if self.ycor() > self.walls["top"] - self.radius:
            self.sety(self.walls["top"] - self.radius - margin)
            if self.y_move > 0:  # Only bounce if the ball is moving upward
                self.bounce_y()

    def detect_paddle(self, paddle):
        """
        Detects and handles collision between the ball and the paddle.
        If the ball intersects the paddle's area (considering the ball's radius), it will bounce off.
        The bounce angle depends on where the ball hits the paddle — hitting near the edges gives a
        more horizontal angle. The function also optionally plays a sound on collision.

        :param paddle: (object) The paddle object that the ball can collide with.
        :return: (bool) True if a collision was detected and handled, False otherwise.
        """
        # Get paddle center coordinates
        px, py = paddle.xcor(), paddle.ycor()

        # Calculate paddle width and height (assuming shapesize is in turtle units, multiplied by 20 px)
        pw = paddle.shapesize()[1] * 20     # width scales with second index
        ph = paddle.shapesize()[0] * 20     # height scales with first index

        # Define the paddle's bounding box
        left = px - pw / 2
        right = px + pw / 2
        top = py + ph / 2
        bottom = py - ph / 2

        # Get ball coordinates
        bx, by = self.xcor(), self.ycor()

        # Check for collision (ball intersects paddle area, accounting for radius)
        if bottom - self.radius <= by <= top + self.radius and left <= bx <= right:
            # Reposition the ball on top of the paddle to prevent sticking
            self.sety(top + self.radius)

            # Compute current speed magnitude
            speed = (self.x_move ** 2 + self.y_move ** 2) ** 0.5

            # Determine where on the paddle the ball hit (-1 on left edge, +1 on right edge)
            hit_offset = (bx - px) / (pw / 2)

            # Adjust horizontal velocity based on hit position
            self.x_move = hit_offset * self.max_horizontal_speed

            # Recalculate vertical speed to preserve total speed
            self.y_move = abs((speed ** 2 - self.x_move ** 2) ** 0.5)

            # Play bounce sound, if sound system is available
            if hasattr(self, "sounds"):
                self.sounds.play("bounce")

            return True

        return False    # No collision

    def detect_blocks(self, blocks, scoreboard, paddle):
        """
        Detects and handles collisions between the ball and any visible block.
        If the ball intersects a block (circular collision detection), it bounces in the
        appropriate direction (horizontal or vertical), plays sounds, triggers power-ups or
        power-downs (if applicable), updates the scoreboard, and removes the block.

        :param blocks: (list) A list of block objects currently in the game.
        :param scoreboard: (object) The scoreboard used to track and update player scores and lives.
        :param paddle: (object) The paddle object, required for applying power-down effects.
        :return: (bool) True if a block was hit and handled, False otherwise.
        """
        # Iterate over a copy to allow removal during loop
        for block in blocks[:]:
            if not block.isvisible():
                continue    # Skip already removed blocks

            # Get block's position and size
            block_x, block_y = block.xcor(), block.ycor()
            block_width = block.shapesize()[1] * 20
            block_height = block.shapesize()[0] * 20

            # Calculate block boundaries
            left = block_x - block_width / 2
            right = block_x + block_width / 2
            top = block_y + block_height / 2
            bottom = block_y - block_height / 2

            # Get ball position
            ball_x, ball_y = self.xcor(), self.ycor()

            # Find the closest point on the block to the ball (for circular collision)
            closest_x = max(left, min(ball_x, right))
            closest_y = max(bottom, min(ball_y, top))

            # Compute distance between ball and closest point
            dx = ball_x - closest_x
            dy = ball_y - closest_y

            # Check for collision (circle-rectangle overlap)
            if dx ** 2 + dy ** 2 <= self.radius ** 2:
                # Determine bounce direction based on which axis has more overlap
                if abs(dx) > abs(dy):
                    self.bounce_x()
                    # Reposition to avoid overlap
                    self.setx(left - self.radius if ball_x < block_x else right + self.radius)
                else:
                    self.bounce_y()
                    self.sety(bottom - self.radius if ball_y < block_y else top + self.radius)

                # Play block hit sound
                if self.sounds:
                    self.sounds.play("hit_block")

                # Powerdown effect (optional)
                if getattr(block, "is_powerdown", False):
                    self.sounds.play("powerdown")
                    scoreboard.active_powerdown(self, paddle)

                # Powerup effect (optional)
                elif getattr(block, "is_powerup", False):
                    self.sounds.play("powerup")
                    scoreboard.recover_life(player=scoreboard.active_player)

                # Hide and remove the block
                block.hideturtle()
                blocks.remove(block)

                # Update score based on active player
                if scoreboard.active_player == 1:
                    scoreboard.player_one_point()
                else:
                    scoreboard.player_two_point()

                return True  # Stop after the first block hit

        return False    # No block collision

    def detect_ball_fall(self):
        """
        Checks if the ball has fallen below the bottom wall (i.e., the player missed the ball).
        This method is typically used to detect when the player loses a life.

        :return: (bool)  True if the ball has fallen below the bottom wall, False otherwise.
        """
        if self.ycor() < WALLS["bottom"]:
            return True
        return False

    def reset_position(self):
        """
        Resets the ball's position to a starting point near the bottom of the screen
        and assigns a new random upward movement direction with a speed based on its
        current velocity or a default speed.

        The ball's starting vertical position is slightly above the bottom wall,
        and its movement angle is randomly chosen between -45° and +45° relative to vertical.

        This ensures the ball always moves upward after reset.

        :return:None
        """

        # Calculate the starting Y position slightly above the bottom wall
        start_y = WALLS["bottom"] + (SCREEN_DIMENSIONS["height"] * 0.05) + 25
        self.goto(0, start_y)   # Centered horizontally

        # Random angle between -45° and +45° (converted to radians)
        angle = uniform(-pi / 4, pi / 4)

        # Calculate current speed magnitude; default to 10 if speed is zero
        speed = (self.x_move ** 2 + self.y_move ** 2) ** 0.5 or 10

        # Set new x and y movement components based on the angle and speed
        self.x_move = speed * sin(angle)
        self.y_move = abs(speed * cos(angle))    # Always move upward (positive y)

    def set_sounds(self, sounds):
        """
        Assigns a sound manager or sound handler to the ball object for playing sound effects.

        :param sounds: (object) An object responsible for managing and playing sound effects.
        :return: None
        """
        self.sounds = sounds
