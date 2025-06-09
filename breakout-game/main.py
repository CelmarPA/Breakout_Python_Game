# Libraries
from turtle import Screen, hideturtle
from game_specs import SCREEN_DIMENSIONS, WALLS
from paddle import Paddle
from ball import Ball
from scoreboard import ScoreBoard
from blocks import Blocks
from sounds import SoundManager
from math import pi, sin, cos
from random import uniform


class ScreenGame:
    """
    Main class that manages the Breakout game using the Turtle graphics library.

    Responsibilities:
    - Configure the game window and graphical elements.
    - Control the game state such as levels, pauses, and player turns.
    - Handle player interaction with the paddle and the ball.
    - Manage blocks, scoreboard, and sounds.
    - Detect events like ball falling and game over.
    - Update the interface and run the main game loop.

    Main attributes:
    - screen: Turtle Screen object for graphical interface.
    - canvas: Tkinter canvas associated with the screen for advanced manipulation.
    - root: Main Tkinter window of the application.
    - sounds: Game sound manager.
    - paddle: Instance of the player-controlled paddle.
    - ball: Instance of the game ball.
    - scoreboard: Instance managing scores and lives.
    - blocks: Instance managing the blocks to be destroyed.
    - level: Current game level.
    - bottom_margin: Bottom margin used for paddle positioning.
    - list_blocks: Current list of active blocks.
    - paused: Flag indicating if the game is paused.
    - turn_ready: Flag controlling turn start after pause.

    Key methods:
    - __init__: Initializes the screen, configures environment, and waits for the start.
    - screen_config: Sets up the window, graphical elements, and event bindings.
    - start_level: Prepares the level by creating blocks, setting ball speed and paddle size.
    - update_paddle: Continuously updates paddle position based on key presses.
    - move_paddle: Binds keyboard events to move the paddle.
    - game_loop: Main loop that updates game state and runs game logic.
    - ball_fell: Detects when the ball falls, updates lives, switches players or ends game.
    - toggle_pause: Pauses or resumes the game.
    - on_resize and handle_resize: Handle window resizing events.
    - center_canvas: Centers the canvas inside the Tkinter window.
    - wait_turn_start: Shows the turn start message and waits for player input.
    - start_game: Starts the level and game loop after player confirmation.
    - end_game: Ends the game, displays the winner, and clears the screen.

    This class relies on other modules/classes such as Paddle, Ball, ScoreBoard, Blocks, and SoundManager for modular design.
    """

    def __init__(self):
        self.screen = Screen()  # Create the main Turtle graphics screen
        hideturtle()            # Hide the default turtle cursor globally
        self.canvas = self.screen.getcanvas()       # Get the Tkinter canvas from Turtle screen
        self.root = self.canvas.winfo_toplevel()    # Get the top-level Tkinter window

        self.sounds = SoundManager()                # Initialize the sound manager for game audio

        # Initialize core game components to None (to be set up later)
        self.paddle = None
        self.ball = None
        self.scoreboard = None
        self.blocks = None
        self.level = 1      # Set the starting level to 1

        # Define bottom margin as 5% of screen height, for paddle placement
        self.bottom_margin = SCREEN_DIMENSIONS["height"] * 0.05

        self.list_blocks = None      # Will hold the current blocks on screen
        self.paused = False          # Game is not paused initially
        self.turn_ready = False      # Flag indicating if the turn is ready to start

        # Configure the screen settings (size, background, event bindings)
        self.screen_config()

        # Start the paddle movement update loop
        self.update_paddle()

        # Display the initial screen waiting for the player's turn to start
        self.wait_turn_start()

    def screen_config(self):
        """
        Configures the main game screen and UI elements for the Breakout game.

        Sets up the screen dimensions, background color, and title.
        Initializes the canvas and centers it within the root window.
        Binds the resize event to adjust the canvas dynamically.
        Creates game objects: paddle, ball, scoreboard, and blocks.
        Sets up sound effects for the ball.
        Enables keyboard listening and starts paddle movement.
        Binds the Return key to toggle the game pause state.

        :return: None
        """

        # Set up the screen size using predefined width and height constants
        self.screen.setup(width=SCREEN_DIMENSIONS["width"], height=SCREEN_DIMENSIONS["height"])

        # Set the background color of the game screen to black
        self.screen.bgcolor("black")

        # Set the window title to "Breakout"
        self.screen.title("Breakout")

        # Turn off automatic screen updates for manual control (for smoother animations)
        self.screen.tracer(0)

        # Set the root window background color to black
        self.root.configure(bg = "black")

        # Remove any previous geometry manager from the canvas
        self.canvas.pack_forget()

        # Place the canvas in the top-left corner with specified width and height
        self.canvas.place(x = 0, y = 0, width = SCREEN_DIMENSIONS["width"], height = SCREEN_DIMENSIONS["height"])

        # Center the canvas within the root window (custom method)
        self.center_canvas()

        # Bind the root window resize event to a handler for dynamic canvas resizing
        self.root.bind("<Configure>", self.on_resize)

        # Calculate the starting Y position for the paddle based on the bottom wall and margin
        start_y = WALLS["bottom"] + self.bottom_margin
        self.paddle = Paddle((0, start_y))  # Initialize the paddle object at the calculated position
        self.ball = Ball()  # Initialize the ball object
        self.scoreboard = ScoreBoard(self.sounds)   # Initialize the scoreboard object and pass the sounds manager
        self.blocks = Blocks()  # Initialize the blocks (bricks) for the game

        # Assign sound effects to the ball object
        self.ball.set_sounds(self.sounds)

        # Enable the screen to listen for keyboard events
        self.screen.listen()

        # Start the paddle movement handler
        self.move_paddle()

        # Bind the Return (Enter) key to toggle the pause state of the game
        self.screen.onkey(self.toggle_pause, "Return")

    def start_level(self):
        """
        Initializes the current level by resetting and creating game elements.

        - Clears existing blocks from the previous level.
        - Creates new rows of blocks based on the current level.
        - Resets the ball's position and adjusts its movement speed and direction.
        - Gradually decreases the paddle width down to a minimum size limit.

        :return: None
        """

        # Hide all existing blocks (remove from display)
        for block in self.blocks.blocks:
            block.hideturtle()

        # Clear the list of blocks to remove old blocks from the game state
        self.blocks.blocks.clear()

        # Set the number of extra rows of blocks based on the current level (level - 1)
        self.blocks.extra_rows = self.level - 1

        # Create new block rows accordingly
        self.blocks.create_block_row()

        # Update the list_blocks reference to the newly created blocks
        self.list_blocks = self.blocks.blocks

        # Reset the ball to its starting position
        self.ball.reset_position()

        # Define base speed and incremental increase per level
        base_speed = 10
        increment = 2

        # Calculate the ball speed for this level, increasing with level number
        speed = base_speed + (self.level - 1) * increment

        # Choose a random launch angle between -45° and +45° (in radians)
        angle = uniform(-pi / 4, pi / 4)

        # Set the ball's horizontal and vertical movement components based on the speed and angle
        self.ball.x_move = speed * sin(angle)
        self.ball.y_move = speed * cos(angle)

        # Calculate the minimum allowed paddle width (5% of screen width)
        min_width = SCREEN_DIMENSIONS["width"] * 0.05

        # Calculate new paddle width by reducing it 10%, but don't go below minimum width
        new_width = max(self.paddle.paddle_width * 0.9, min_width)

        # Resize the paddle to the new width
        self.paddle.resize(new_width)

    def update_paddle(self):
        """
        Updates the paddle's position based on its current movement direction.
        Checks if the paddle is flagged as moving right or left,
        and moves it accordingly. Then schedules the next update call.

        This method is repeatedly called every 20 milliseconds
        to smoothly animate the paddle movement.

        :return: None
        """

        # If the paddle is set to move right, move it right
        if self.paddle.moving_right:
            self.paddle.go_right()

        # If the paddle is set to move left, move it left
        if self.paddle.moving_left:
            self.paddle.go_left()

        # Schedule the next paddle update call after 20 milliseconds
        self.screen.ontimer(self.update_paddle, 20)

    def move_paddle(self):
        """
         Sets up key event bindings to control the paddle movement.

        - Binds arrow keys and 'a'/'d' keys to start and stop moving the paddle left or right.
        - Uses key press events to start movement and key release events to stop movement.

        :return:
        """
        self.screen.onkeypress(self.paddle.start_move_right, "Right")
        self.screen.onkeyrelease(self.paddle.stop_move_right, "Right")
        self.screen.onkeypress(self.paddle.start_move_left, "Left")
        self.screen.onkeyrelease(self.paddle.stop_move_left, "Left")

        self.screen.onkeypress(self.paddle.start_move_right, "d")
        self.screen.onkeyrelease(self.paddle.stop_move_right, "d")
        self.screen.onkeypress(self.paddle.start_move_left, "a")
        self.screen.onkeyrelease(self.paddle.stop_move_left, "a")

    def game_loop(self):
        """
        Main game loop that updates the game state and screen.

        - Runs only if the game is not paused.
        - Updates the screen graphics.
        - Moves the ball and checks for collisions with paddle and blocks.
        - Checks if all blocks are cleared to progress to the next level.
        - Plays a sound effect when advancing levels (if sounds are enabled).
        - Pauses the game and waits to start the next turn when level is cleared.
        - Checks if the ball has fallen below the paddle (missed).
        - Schedules the next loop iteration after 20 milliseconds.

        :return: None
        """

        # Continue the game loop only if the game is not paused
        if not self.paused:
            # Update the screen display (manual control because tracer is off)
            self.screen.update()

            # Move the ball and handle collision with paddle and blocks
            self.ball.move_ball(self.paddle, self.list_blocks, self.scoreboard)

            # If there are no blocks left, level is cleared
            if not self.list_blocks:
                # Play the next level sound if sounds are enabled
                if hasattr(self, "sounds"):
                    self.sounds.play("next_level")

                self.level += 1     # Increase the level number
                self.paused = True  # Pause the game before starting the next level
                self.wait_turn_start()  # Call method to wait and start the next turn
                return  # Exit the current game loop iteration

            # Check if the ball has fallen below the paddle (missed)
            self.ball_fell()

            # Schedule the next iteration of the game loop after 20 milliseconds
            self.screen.ontimer(self.game_loop, 20)

    def ball_fell(self):
        """
        Handles the event when the ball falls below the paddle (missed).

        - Detects if the ball has fallen off the screen.
        - Decreases the current active player's lives and plays the 'life lost' sound.
        - Updates the UI to reflect the remaining lives (hearts).
        - If player one's lives reach zero, switches to player two:
            - Resets player two's score.
            - Hides and clears existing blocks.
            - Pauses the game and waits to start the next turn.
        - If player two's lives reach zero, ends the game.
        - If lives remain, repositions the paddle and resets the ball without pausing.

        :return: None
        """

        # Check if the ball has fallen below the paddle
        if self.ball.detect_ball_fall():

            # If active player is player one
            if self.scoreboard.active_player == 1:
                self.scoreboard.player_one_lives -= 1   # If active player is player one
                self.scoreboard.sounds.play("life_lost")    # Play the 'life lost' sound effect
                self.scoreboard.update_hearts()     # Update the hearts/lives display on the scoreboard

                # If player one has no lives left
                if self.scoreboard.player_one_lives == 0:
                    self.scoreboard.active_player = 2   # Switch active player to player two
                    self.scoreboard.player_two_score = 0    # Reset player two's score

                    # Hide all existing blocks
                    for block in self.list_blocks:
                        block.hideturtle()

                    # Clear the blocks list to remove all blocks
                    self.blocks.blocks.clear()

                    # Pause the game and wait to start the next turn
                    self.paused = True
                    self.wait_turn_start()
                    return

            else:
                # Active player is player two, so decrement their lives
                self.scoreboard.player_two_lives -= 1
                self.sounds.play("life_lost")       # Play the 'life lost' sound effect
                self.scoreboard.update_hearts()     # Update the hearts/lives display

                # If player two has no lives left, end the game
                if self.scoreboard.player_two_lives == 0:
                    self.end_game()
                    return

            # If the player still has lives left, reposition the paddle to the starting Y position
            start_y = WALLS["bottom"] + self.bottom_margin
            self.paddle.goto(0, start_y)

            # Reset the ball's position to the starting point
            self.ball.reset_position()

    def toggle_pause(self):
        """
        Toggles the game's pause state.

        - Switches the 'paused' flag between True and False.
        - If the game is paused:
            - Updates the scoreboard to show paused state.
            - Updates the screen once to reflect the pause.
        - If the game is unpaused:
            - Updates the scoreboard to show active state.
            - Restarts the main game loop.

        :return: None
        """

        # Flip the paused state (True becomes False, False becomes True)
        self.paused = not self.paused

        if self.paused:
            # Notify scoreboard that the game is paused (e.g., show pause message)
            self.scoreboard.is_paused()
            self.screen.update()    # Update screen to reflect pause state
        else:
            # Notify scoreboard that the game is resumed
            self.scoreboard.not_paused()
            # Restart the main game loop to continue gameplay
            self.game_loop()

    def on_resize(self, event):
        """
        Handles window resize events by scheduling the actual resize handler.

        - This method is called whenever the window is resized.
        - It defers execution of the resize handling by 10 milliseconds
          to avoid rapid repeated calls during continuous resizing.
        - The actual resize logic is executed in the 'handle_resize' method.

        :param event: (event) The resize event object passed by the window manager.
        :return: None
        """
        # Store the event (though currently unused in this snippet)
        _event = event

        # Schedule the handle_resize method to run after 10 milliseconds
        self.root.after(10, self.handle_resize)

    def handle_resize(self):
        """
        Handles adjustments needed after the window resize event.

        - Updates any pending tasks related to the root window.
        - Retrieves the current width and height of the root window.
        - Centers the canvas within the window.
        - Changes the root window background color to white if
          the window exceeds the predefined screen dimensions,
          otherwise sets it to black.

        :return: None
        """

        # Process any pending events and updates for the root window
        self.root.update_idletasks()

        # Get the current width and height of the root window
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Center the canvas within the resized window
        self.center_canvas()

        # Change background color based on window size relative to screen dimensions
        if root_width > SCREEN_DIMENSIONS["width"] or root_height > SCREEN_DIMENSIONS["height"]:
            self.root.configure(bg = "white")
        else:
            self.root.configure(bg = "black")

    def center_canvas(self):
        """
        Centers the canvas within the root window.

        - Calculates the horizontal and vertical position to place the canvas
          so that it is centered based on the current size of the root window.
        - Uses integer division (//) to avoid floating-point positions.
        - Applies the calculated position using the `place()` geometry manager.

        :return: None
        """

        # Get the current width and height of the root window
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Calculate the top-left (x, y) coordinates to center the canvas
        x = (root_width - SCREEN_DIMENSIONS["width"]) // 2
        y = (root_height - SCREEN_DIMENSIONS["height"]) // 2

        # Move the canvas to the calculated position
        self.canvas.place(x = x, y = y)

    def wait_turn_start(self):
        """
         Prepares the game to start a new turn for the current player.

        - Determines which player's turn it is.
        - Displays a message or screen indicating the start of that player's turn.
        - Sets the turn readiness flag too False to prevent the game from running prematurely.
        - Binds the space bar key to start the game when pressed.
        - Updates the screen to reflect the turn-start message.

        :return: None
        """

        # Get the current active player name
        player = "Player 1" if self.scoreboard.active_player == 1 else "Player 2"

        # Show a visual message or prompt to indicate who's turn it is
        self.scoreboard.show_turn_start(player)

        # Mark that the turn is not yet started
        self.turn_ready = False

        # Bind the space key to begin the game when pressed
        self.screen.onkey(self.start_game, "space")

        # Force an update to the screen so the turn start message is visible
        self.screen.update()

    def start_game(self):
        """
        Starts the game turn after the player presses the space bar.

        - Prevents the method from running multiple times if the space bar
          is pressed repeatedly.
        - Marks the turn as ready and unpauses the game.
        - Hides the turn start message.
        - Resets the paddle position to the starting point.
        - Initializes the level (recreates blocks and sets ball speed/direction).
        - Starts the main game loop.

        :return: None
        """

        # Prevent multiple calls if the player presses space repeatedly
        if self.turn_ready:
            return

        # Mark that the turn is ready and unpause the game
        self.turn_ready = True
        self.paused = False

        # Hide the "turn start" message
        self.scoreboard.hide_turn_start()

        # Reset the paddle to its starting position
        start_y = WALLS["bottom"] + self.bottom_margin
        self.paddle.goto(0, start_y)

        # Start a new level and begin the main game loop
        self.start_level()
        self.game_loop()


    def end_game(self):
        """
        Ends the game and displays the winner.

        - Hides the ball, paddle, and all remaining blocks.
        - Clears the list of blocks.
        - Compares player scores to determine the winner (or a draw).
        - Displays the winning message using the scoreboard.
        - Plays the 'game over' sound.
        - Pauses the game and updates the screen to reflect the final state.

        :return: None
        """

        # Hide the ball and paddle
        self.ball.hideturtle()
        self.paddle.hideturtle()

        # Hide and clear all remaining blocks
        for block in self.list_blocks:
            block.hideturtle()
        self.blocks.blocks.clear()

        # Retrieve scores
        p1 = self.scoreboard.player_one_score
        p2 = self.scoreboard.player_two_score

        # Determine the winner or if it's a draw
        if p1 > p2:
            winner = "Player 1"
            score = p1

        elif p2 > p1:
            winner = "Player 2"
            score = p2

        else:
            winner = "Draw"
            score = p1  # Doesn't matter in case of a draw

        # Show winner message and play game over sound
        self.scoreboard.show_winner(winner, score)
        self.sounds.play("game_over")

        # Pause the game and update the screen
        self.paused = True
        self.screen.update()

if __name__ == "__main__":
    # Create an instance of the custom game screen
    screen = ScreenGame()

    # Start the main event loop to keep the window open and responsive
    screen.screen.mainloop()
