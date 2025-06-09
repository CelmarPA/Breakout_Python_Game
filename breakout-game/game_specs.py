# Screen dimensions for the game window (max width: 960px, max height: 1024px)
SCREEN_DIMENSIONS = {
    "width": 960,
    "height": 1024
}

# Wall boundaries based on screen dimensions, defining the play area edges
WALLS = {
    "left": SCREEN_DIMENSIONS['width'] / 2 * -1,
    "right": SCREEN_DIMENSIONS['width'] / 2,
    "top": SCREEN_DIMENSIONS['height'] / 2,
    "bottom": SCREEN_DIMENSIONS['height'] / 2 * -1
}

# Color palette for blocks, indexed by row number modulo the number of colors
COLORS = {
    0: "red",
    1: "orange",
    2: "green",
    3: "yellow"
}

# Number of block rows to create in the game
BLOCK_ROWS = 8

# Initial number of lives the player has
LIVES = 3
