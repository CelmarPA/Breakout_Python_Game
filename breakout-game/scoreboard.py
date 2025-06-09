import os
from turtle import Turtle, Screen
import turtle
from PIL import Image, ImageDraw, ImageFont
from game_specs import SCREEN_DIMENSIONS, LIVES

# Load custom font or fallback to default
FONT_PATH = "fonts/PressStart2P-Regular.ttf"
font_size = int(SCREEN_DIMENSIONS["width"] * 0.035)     # ~3.5% da largura

try:
    FONT = ImageFont.truetype(FONT_PATH, font_size)
except OSError:
    FONT = ImageFont.load_default()


class ScoreBoard:
    """
    Class responsible for managing the game scoreboard, player scores, names, lives,
    pause status, winner display, and other text-based graphics using Turtle and PIL.
    """

    def __init__(self, sounds):
        self.screen = Screen()
        self.sounds = sounds
        self.image_cache = {}    # Cache to avoid regenerating the same images
        self.font = FONT

        # Player info and state
        self.player_one = "Player 1"
        self.player_two = "Player 2"
        self.player_one_score = 0
        self.player_two_score = 0
        self.game_paused = "PAUSED"

        self.max_lives = 5
        self.player_one_lives = LIVES
        self.player_two_lives = LIVES
        self.active_player = 1  # Player 1 starts

        # Graphical configuration for heart icons
        self.hearts_p1 = []
        self.hearts_p2 = []
        self.heart_size = int(font_size * 0.95)
        self.spacing = int(self.heart_size * 0.2)
        self.total_width = 3 * self.heart_size + 2 * self.spacing

        self.screen_w = SCREEN_DIMENSIONS["width"]
        self.screen_h = SCREEN_DIMENSIONS["height"]

        # Turtles used in dynamic elements
        self.winner_turtle = None
        self.score_turtle = None
        self.turn_info = None
        self.start_hint = None

        # Pre-register images for player names, scores and pause screen
        self.create_and_register_image("player1_name", self.player_one)
        self.create_and_register_image("player2_name", self.player_two)
        self.create_and_register_image("score1", str(self.player_one_score).zfill(3))
        self.create_and_register_image("score2", str(self.player_two_score).zfill(3))
        self.create_and_register_image("paused", str(self.game_paused))

        # Screen's dimensions
        screen_w = SCREEN_DIMENSIONS["width"]
        screen_h = SCREEN_DIMENSIONS["height"]

        # Calculate positions for UI elements
        img_half_width = (screen_w * 0.3) / 2
        x_right = screen_w / 2 - img_half_width - 10
        x_left = -screen_w / 2 + img_half_width + 10

        y_name = screen_h / 2 - font_size - 15
        y_score = y_name - font_size - 10

        # Name and score turtles for each player
        self.name1 = self.create_turtle("player1_name", x_left, y_name)
        self.name2 = self.create_turtle("player2_name", x_right, y_name)
        self.score1 = self.create_turtle("score1", x_left, y_score)
        self.score2 = self.create_turtle("score2", x_right, y_score)

        # Pause screen turtle
        self.paused = self.create_turtle("paused", 0, 0, visible=False)

        # Initialize heart/life icons
        self.create_life_icons()

    def update_scoreboard(self):
        """
        Updates the visual scoreboard for both players.
        This method converts each player's current score to a three-digit string,
        generates a corresponding image (e.g., '005.gif' for a score of 5), registers it,
        and then sets the respective turtle's shape to that image.

        :return: None
        """

        # Format player one's score as a 3-digit string and register the corresponding image
        self.create_and_register_image("score1", str(self.player_one_score).zfill(3))
        # Set the turtle shape to the updated image for player one's score
        self.score1.shape("gifs/score1.gif")

        # Format player two's score as a 3-digit string and register the corresponding image
        self.create_and_register_image("score2", str(self.player_two_score).zfill(3))
        # Set the turtle shape to the updated image for player two's score
        self.score2.shape("gifs/score2.gif")

    def is_paused(self):
        """
        Displays the pause indicator on the screen.
        This method makes the 'paused' turtle (or graphic element) visible,
        indicating that the game is currently paused

        :return: None
        """
        self.paused.showturtle()

    def not_paused(self):
        """
        Hides the pause indicator from the screen.
        This method makes the 'paused' turtle (or graphic element) invisible,
        indicating that the game is currently running.

        :return: None
        """
        self.paused.hideturtle()

    def player_one_point(self):
        """
        Increments Player One's score by 1 and updates the scoreboard.
        This method is called whenever Player One scores a point.

        :return: None
        """
        self.player_one_score += 1
        self.update_scoreboard()

    def player_two_point(self):
        """
        Increments Player Two's score by 1 and updates the scoreboard.
        This method is called whenever Player Two scores a point.

        :return: None
        """
        self.player_two_score += 1
        self.update_scoreboard()

    def create_and_register_image(self, name, text):
        """
        Creates a text image, saves it as a GIF, registers it with the turtle screen,
        and caches it to avoid redundant regeneration.

        :param name: (str) The name/key used for the image (also used as the filename).
        :param text: (str) The text to render in the image.
        :return: None
        """

        # Initialize the image cache if it doesn't exist
        if not hasattr(self, "image_cache"):
            self.image_cache = {}

        # Skip if the image with the same text is already cached
        if name in self.image_cache and self.image_cache[name]["text"] == text:
            return

        font = self.font

        # Calculate text dimensions
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Padding around the text
        padding_x = 20
        padding_y = 10

        # Final image size with padding
        img_width = text_width + 2 * padding_x
        img_height = text_height + 2 * padding_y

        # Create a black image
        img = Image.new("RGB", (img_width, img_height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Center the text
        x = (img_width - text_width) // 2
        y = (img_height - text_height) // 2
        draw.text((x, y), text=text, font=font, fill=(255, 255, 255))

        # Ensure 'gifs' directory exists
        if not os.path.exists("gifs"):
            os.makedirs("gifs")

        gif_path = f"gifs/{name}.gif"
        img.save(gif_path)

        # Safely re-register the shape to update the screen
        if gif_path in self.screen.getshapes():
            try:
                self.screen.addshape(gif_path)  # Safe overwrite
            except turtle.TurtleGraphicsError:
                pass
        else:
            self.screen.addshape(gif_path)

        # Cache the image data for future reuse
        self.image_cache[name] = {
            "text": text,
            "width": img_width,
            "height": img_height,
            "padding_x": padding_x,
            "padding_y": padding_y
        }

    def create_life_icons(self):
        """
        Creates and positions heart icons representing player lives on the screen.
        Loads the heart shape once, then creates individual turtle objects for each life
        for both players, positioning them relative to player name positions.

        Adds created heart turtles to the hearts_p1 and hearts_p2 lists.
        Calls reposition_hearts and update_hearts to finalize layout and display.

        :return: None
        """

        # Register the heart shape on the turtle screen
        self.screen.addshape("gifs/heart.gif")

        # Calculate vertical position for the hearts, just above player one's name
        y_hearts = self.name1.ycor() + self.heart_size + 5

        # Calculate horizontal base positions for each player's hearts,
        # aligning them based on total width and player name positions
        align_to_p_offset = self.total_width / 2
        x_base_left = self.name1.xcor() - align_to_p_offset
        x_base_right = self.name2.xcor() - align_to_p_offset

        # Create heart icons for player one, spaced horizontally
        for i in range(self.max_lives):
            heart = Turtle()
            heart.penup()
            heart.shape("gifs/heart.gif")
            heart.goto(x_base_left - i * (self.heart_size + self.spacing), y_hearts)
            self.hearts_p1.append(heart)

        # Create heart icons for player two, spaced horizontally
        for i in range(self.max_lives):
            heart = Turtle()
            heart.penup()
            heart.shape("gifs/heart.gif")
            heart.goto(x_base_right - i * (self.heart_size + self.spacing), y_hearts)
            self.hearts_p2.append(heart)

        # Ensure hearts are positioned correctly after creation
        self.reposition_hearts()

        # Update heart display based on current lives
        self.update_hearts()

    def reposition_hearts(self):
        """
        Repositions the heart icons above each player's name to ensure proper alignment.
        Uses cached image width and padding to calculate the starting X position,
        then spaces hearts horizontally based on heart size and spacing.

        :return: None
        """

        # Calculate vertical position for hearts, above the player's name
        y_hearts = self.name1.ycor() + self.heart_size

        # Player 1: retrieve cached width and padding for player1_name image
        p1_data = self.image_cache.get("player1_name", {})
        width_p1 = p1_data.get("width", 0)
        padding_p1 = p1_data.get("padding_x", 0)
        # Calculate starting X position aligned to the "P" in "Player"
        x_start_p1 = self.name1.xcor() - (width_p1 / 2) + padding_p1

        # Player 2: retrieve cached width and padding for player2_name image
        p2_data = self.image_cache.get("player2_name", {})
        width_p2 = p2_data.get("width", 0)
        padding_p2 = p2_data.get("padding_x", 0)
        # Calculate starting X position aligned to the "P" in "Player"
        x_start_p2 = self.name2.xcor() - (width_p2 / 2) + padding_p2

        # Position each heart for player 1 with horizontal spacing
        for i, heart in enumerate(self.hearts_p1):
            x = x_start_p1 + i * (self.heart_size + self.spacing)
            heart.goto(x, y_hearts)

        # Position each heart for player 2 with horizontal spacing
        for i, heart in enumerate(self.hearts_p2):
            x = x_start_p2 + i * (self.heart_size + self.spacing)
            heart.goto(x, y_hearts)

    @staticmethod
    def create_turtle(shape_name, x, y, visible = True):
        """
        Creates a Turtle object with a specified shape and initial position.

        :param shape_name: (str) The name of the shape file (without the path or extension) to be used for the turtle.
        :param x: (int or float) The initial x-coordinate where the turtle will be placed.
        :param y: (int or float) The initial y-coordinate where the turtle will be placed.
        :param visible: (bool): Whether the turtle should be visible after creation (default is True).
        :return: (object) Turtle
        """

        t = Turtle()
        t.penup()   # Prevent drawing when moving to the starting position
        t.goto(x, y)    # Move turtle to the specified position
        t.shape(f"gifs/{shape_name}.gif")   # Set the turtle's shape to the given GIF file
        if not visible:
            t.hideturtle()  # Hide the turtle if visibility is False

        return t

    def show_winner(self, winner_name, winner_score):
        """
        Displays the winner's name and final score on the screen.
        This method hides all current scoreboard elements, creates the winner text and final score
        images, and positions them centrally on the screen using turtle graphics.

        :param winner_name: (str) The name of the winning player.
        :param winner_score: (int) The final score of the winning player.
        :return: None
        """

        # Hide all existing scoreboard elements to clear the screen
        self.name1.hideturtle()
        self.name2.hideturtle()
        self.score1.hideturtle()
        self.score2.hideturtle()
        self.paused.hideturtle()

        # Create and register images for the winner text and the final score
        text = f"{winner_name} {'Wins!!!' if winner_name != 'Draw' else '!!!'}"
        self.create_and_register_image("winner_text", text)
        self.create_and_register_image("final_score_text", f"Points: {str(winner_score).zfill(3)}")

        # Create turtles to display the winner text and final score centered on the screen
        self.winner_turtle = self.create_turtle("winner_text", 0, 30)
        self.score_turtle = self.create_turtle("final_score_text", 0, -30)

    def show_turn_start(self, player_name):
        """
        Displays the start of a player's turn on the screen.
        This method creates and registers images showing the current player's name
        and a prompt to press the SPACE key to start. Then it positions these messages
        centered on the screen using turtle graphics.

        :param player_name: (str) The name of the player whose turn is starting.
        :return: None
        """

        # Create and register an image with the current player's name
        self.create_and_register_image("turn_info", player_name)
        # Create and register an image with the instruction to press SPACE
        self.create_and_register_image("start_hint", "Press SPACE")

        # Create turtles to display the turn information and start hint, positioned on screen
        self.turn_info = self.create_turtle("turn_info", 0, 40)
        self.start_hint = self.create_turtle("start_hint", 0, -20)

    def hide_turn_start(self):
        """
        Hides the turn start display elements from the screen.
        This method checks if the turtles displaying the turn information and start hint
        exist, and if so, hides them to clear the turn start messages from the screen.

        :return: None
        """

        # Hide the turn information turtle if it exists
        if hasattr(self, "turn_info"):
            self.turn_info.hideturtle()

        # Hide the start hint turtle if it exists
        if hasattr(self, "start_hint"):
            self.start_hint.hideturtle()

    def active_powerdown(self, ball, paddle):
        """
        Activates a power-down effect on the paddle by shrinking its width temporarily.
        The paddle's width is reduced by half or to a minimum percentage of the screen width.
        After 5 seconds, the paddle's original width is restored automatically.

        :param ball: (object) The ball object involved in the game (currently unused in this method).
        :param paddle: (object) The paddle object to apply the power-down effect on.
        :return: None
        """

        # Currently unused but kept for possible future reference
        _ball = ball

        # Calculate the shrunken width (at least 4% of screen width)
        shrinked = max(paddle.paddle_width * 0.5, SCREEN_DIMENSIONS["width"] * 0.04)

        # Initialize restoring flag if it doesn't exist
        if not hasattr(paddle, "restoring_powerdown"):
            paddle.restoring_powerdown = False

        # If not already restoring, save original width and mark as restoring
        if not paddle.restoring_powerdown:
            paddle.original_width = paddle.paddle_width
            paddle.restoring_powerdown = True

        # Resize the paddle to the smaller width
        paddle.resize(shrinked)

        def restore():
            """
            Restores the paddle to its original width if this is the last active power-down.

            :return: None
            """
            if paddle.restoring_powerdown:
                paddle.resize(paddle.original_width)
                paddle.restoring_powerdown = False

        # Schedule restoration after 5000 ms (5 seconds)
        self.screen.ontimer(restore, 5000)

    def update_hearts(self):
        """
        Updates the visibility of life heart icons for both players based on their current lives.
        Shows the hearts up to the player's current number of lives and hides the rest.

        :return: None
        """

        # Update hearts for Player 1
        for i, heart in enumerate(self.hearts_p1):
            if i < self.player_one_lives:
                heart.showturtle()  # Show heart if life is available
            else:
                heart.hideturtle()  # Hide heart if life is lost

        # Update hearts for Player 2
        for i, heart in enumerate(self.hearts_p2):
            if i < self.player_two_lives:
                heart.showturtle()  # Show heart if life is available
            else:
                heart.hideturtle()  # Hide heart if life is lost

    def flash_heart(self, heart):
        """
        Makes a given heart icon flash by toggling its visibility several times.
        The heart will toggle between visible and hidden 6 times,
        with 100 milliseconds between each toggle, ending hidden.

        :param heart: (object) The heart turtle object to flash.
        :return: None
        """
        def toggle(times):
            if times > 0:
                # Toggle visibility: hide on even counts, show on odd counts
                heart.hideturtle() if times % 2 == 0 else heart.showturtle()
                # Schedule the next toggle after 100 milliseconds
                self.screen.ontimer(lambda: toggle(times - 1), 100)
            else:
                # Ensure the heart ends hidden
                heart.hideturtle()

        toggle(6)

    def recover_life(self, player):
        """
        Recovers one life for the specified player, up to the maximum allowed lives,
        and updates the heart icons on the screen.

        :param player: (int) Player number (1 or 2) indicating which player to recover a life for.
        :return: None
        """

        max_lives = self.max_lives

        if player == 1 and self.player_one_lives < max_lives:
            self.player_one_lives += 1
        elif player == 2 and self.player_two_lives < max_lives:
            self.player_two_lives += 1

        self.update_hearts()
