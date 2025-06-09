from turtle import Turtle
from game_specs import SCREEN_DIMENSIONS,BLOCK_ROWS, COLORS
from random import random

class Blocks:
    """
    Manages a collection of block objects for the Breakout game.

    attr blocks: (list) List to store all created block turtle objects.
    attr extra_rows: (int) Additional rows to add to the default block rows (can be used to increase difficulty).
    """

    def __init__(self):
        self.blocks = []     # List to store the created blocks
        self.extra_rows = 0  # Extra rows beyond the default count

    def create_block(self, color, positions, stretches):
        """
        Creates a single block (Turtle object) with specified color, position, and size.
        Each block has a small chance to be a power-up or power-down block.

        :param color: (str) The color of the block.
        :param positions: (dict) Dictionary with 'x' and 'y' keys for block coordinates.
        :param stretches: (dict) Dictionary with 'stretch_wid' and 'stretch_len' for scaling the block size.
        :return: (block): Turtle (The created block Turtle object.)
        """

        block = Turtle()
        block.shape("square")
        block.shapesize(
            stretch_wid = stretches["stretch_wid"],
            stretch_len = stretches["stretch_len"]
        )
        block.color(color)
        block.penup()
        block.goto(x = positions["x"], y = positions["y"])
        block.speed(0)

        # Generate a random float between 0.0 and 1.0
        chance = random()
        if chance < 0.1:
            # 10% chance the block is a power-down block
            block.is_powerdown = True
            block.is_powerup = False
        elif chance < 0.2:
            # Next 10% chance (from 0.1 to 0.2) the block is a power-up block
            block.is_powerdown = False
            block.is_powerup = True
        else:
            # Remaining 80% chance the block is a normal block (no power-up or power-down)
            block.is_powerdown = False
            block.is_powerup = False

        # Add the created block to the blocks list
        self.blocks.append(block)

        # Return the block object for further use
        return block

    def create_block_row(self):
        """
        Creates multiple rows of blocks spanning across the screen width.
        The number of rows is limited to a maximum of 12, including extra rows.
        Blocks are spaced evenly with small gaps and their sizes scale relative to screen dimensions.
        The colors cycle through a predefined COLORS list for each row.

        :return: None
        """

        screen_dim = SCREEN_DIMENSIONS
        colors = COLORS
        rows = min(BLOCK_ROWS + self.extra_rows, 12)

        screen_width = screen_dim["width"]
        screen_height = screen_dim["height"]

        spacing_x = screen_width * 0.005     # 0.5% horizontal spacing between blocks
        spacing_y = screen_height * 0.005    # 0.5% vertical spacing between blocks

        blocks_per_row = int(screen_width / 70)   # Approximate block count per row (~70px per block + margin)
        block_width = (screen_width - (blocks_per_row - 1) * spacing_x) / blocks_per_row
        block_height = screen_height * 0.03    # Block height ~3% of screen height

        # Turtle squares have base size 20x20 pixels, so scale accordingly
        stretch_len = block_width / 20
        stretch_wid = block_height / 20

        # Starting positions to center blocks horizontally and place them near the top
        start_x = - (screen_width / 2) + (block_width / 2)
        start_y = screen_height / 2 - (screen_height * 0.15)    # Start 15% below top of screen


        for row in range(rows):
            # Select the color for the current row by cycling through the colors list
            color = colors[row % len(colors)]

            # Select the color for the current row by cycling through the colors list
            y = start_y - row * (block_height + spacing_y)

            for col in range(blocks_per_row):
                # Calculate the x-coordinate for the current block in the row,
                # spacing blocks horizontally
                x = start_x + col * (block_width + spacing_x)

                # Create a block at the calculated position with the specified color and size
                self.create_block(
                    color,
                    positions = {"x": x, "y": y},
                    stretches = {"stretch_wid": stretch_wid, "stretch_len": stretch_len}
                )
