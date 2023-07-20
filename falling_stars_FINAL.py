import random
import pgzrun
# constants
FONT_COLOR = (255, 255, 255)
WIDTH = 850
HEIGHT = 650
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FINAL_LEVEL = 6
START_SPEED = 10
COLORS = ["yellow", "blue", "green"]
#global variables
current_level = 1
game_over = False
game_complete = False
stars = []
animations = []


def draw():
    global stars, current_level, game_over, game_complete
    screen.clear()
    screen.blit("night", (0, 0))
    if game_over:
        display_message(" GAME OVER!", "Try again.")
    elif game_complete:
        display_message(" WELL PLAYED! ", " YOU WON: -)")
    else:
        for star in stars:
            star.draw()


def update():
    global stars
    if len(stars) == 0:
        # If the stars list is empty, MAKE_STARS function is called.
        stars = make_stars(current_level)


# This is used to call all of the other functions required to run the game
def make_stars(number_of_extra_stars):
    colors_to_create = get_colors_to_create(number_of_extra_stars)
    new_stars = create_stars(colors_to_create)
    layout_stars(new_stars)
    animate_stars(new_stars)
    return new_stars


# def get_colors_to_create(number_of_extra_stars):
#     This returns a list of colors that will be used to draw the stars.
# The choice() method returns a randomly selected element from the specified sequence.
def get_colors_to_create(number_of_extra_stars):
    colors_to_create = ["red"]
    for i in range(0, number_of_extra_stars):
        random_color = random.choice(COLORS)
        colors_to_create.append(random_color)
    return colors_to_create


# def create_stars(colors_to_create):
#     This function uses the list of colors as a parameter and creates Actors for each star.(making STARS)
#     return []
def create_stars(colors_to_create):
    new_stars = []
    for color in colors_to_create:
        # An Actor can be drawn on the screen, moved around, and even interact with other Actors in the game.
        # Each Actor is given a “script” (the Python code) to tell it how to behave in the game.
        star = Actor(color + "-star")
        new_stars.append(star)
    return new_stars


# def layout_stars(stars_to_layout):
#     pass
# This function puts the stars in the right position on the screen.
def layout_stars(stars_to_layout):
    number_of_gaps = len(stars_to_layout) + 1
    gap_size = WIDTH / number_of_gaps
    # The shuffle() method takes a sequence, like a list, and reorganize the order of the items.
    # Note: This method changes the original list, it does not return a new list.
    random.shuffle(stars_to_layout)
    # enumerate function in Python converts a data collection object into an enumerate object
    for index, star in enumerate(stars_to_layout):
        new_x_pos = (index + 1) * gap_size
        star.x = new_x_pos
        # This for loop sets the position of the current star along the x-axis
        # by multiplying the position of the star in the list by the size of the gap


# def animate_stars(stars_to_animate):
#     pass
# This function makes the stars move down the screen.
def animate_stars(stars_to_animate):
    for star in stars_to_animate:
        # The higher the level, the shorter the duration, so the faster the animation
        duration = START_SPEED - current_level
        # DIFFERENT SPEED
        # random_speed_adjustment = random.randint(3, 5)
        # duration = START_SPEED - current_level - random_speed_adjustment
        star.anchor = ("center", "bottom")
        animation = animate(star, duration=duration,
                            on_finished=handle_game_over, y=HEIGHT)
        animations.append(animation)


def handle_game_over():
    global game_over
    game_over = True


def on_mouse_down(pos):
    global stars, current_level
    for star in stars:
        if star.collidepoint(pos):
            if "red" in star.image:
                red_star_click()
            else:
                handle_game_over()


def red_star_click():
    global current_level, stars, animations, game_complete
    stop_animations(animations)
    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level = current_level + 1
        stars = []
        animations = []


def stop_animations(animations_to_stop):
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()


def display_message(heading_text, sub_heading_text):
    screen.draw.text(heading_text, fontsize=40,
                     center=CENTER, color=FONT_COLOR)
    screen.draw.text(sub_heading_text, fontsize=30, center=(
        CENTER_X, CENTER_Y + 30), color=FONT_COLOR)


def shuffle():
    global stars
    if stars:
        # list comprehension
        # get each star’s position along the x-axis in the form of a list
        x_values = [star.x for star in stars]
        random.shuffle(x_values)
        for index, star in enumerate(stars):
            new_x = x_values[index]
            animation = animate(star, duration=0.5, x=new_x)
            animations.append(animation)


clock.schedule_interval(shuffle, 1)

pgzrun.go()
