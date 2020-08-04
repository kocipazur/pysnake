import os
import random
import ctypes
import time


# <editor-fold desc="Definitions">
# region Definitions

def initialize_windows_shell():
    kernel32 = ctypes.WinDLL('kernel32')
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)


def clear(): return os.system('cls')


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def colored_text(text, color):
    END = '\033[0m'
    return f"{color}{text}{END}"


def print_game(game_size, snake, snack):
    for y in range(game_size):
        for x in range(game_size):
            if ((x, y) in snake):
                if ((x, y) == snake[0]):
                    print(colored_text("S", bcolors.GREEN), end="")
                else:
                    print(colored_text("s", bcolors.RED), end="")
            elif ((x, y) == snack):
                print(colored_text("m", bcolors.YELLOW), end="")
            else:
                print(" ", end="")
        print()


def show_title():
    print("pySnake!")


def show_controlls():
    print("Controls:")
    print("w - up")
    print("s - down")
    print("a - left")
    print("d - right")
    print("enter - confirm move")


def remove_last_element(array):
    array.pop(len(array) - 1)


def add_first_element(array, element):
    array.insert(0, element)


def move_snake(body, position, fed):
    add_first_element(body, position)
    if (not fed):
        remove_last_element(body)


def map_input_to_next_position(input, current_position):
    inputed = input()
    b = (0, 0)
    if (inputed == "w"):
        b = (0, -1)
    if (inputed == "s"):
        b = (0, 1)
    if (inputed == "a"):
        b = (-1, 0)
    if (inputed == "d"):
        b = (1, 0)
    return (current_position[0] + b[0], current_position[1] + b[1])


def validate_Step(size, body, step):
    valid = True
    if (step[0] < 0 or step[1] < 0 or step[0] > size - 1 or step[1] > size-1 or step in body):
        valid = False
    return valid


def show_score(snake_body, initial_length):
    print(
        f"Score: {colored_text(len(snake_body) - initial_length, bcolors.BLUE) if len(snake_body) - initial_length >= 0 else colored_text(0, bcolors.BLUE)}")


def get_keyboard_input():
    user_input = input()
    return user_input


def move_step_through_wall(step, size):
    x_position = step[0]
    y_position = step[1]
    if (x_position < 0):
        x_position = size - 1
    elif (y_position < 0):
        y_position = size - 1
    elif (x_position == size):
        x_position = 0
    elif (y_position == size):
        y_position = 0
    return (x_position, y_position)


def get_next_step(next_step, size, snake_body, input_function):
    next_step = map_input_to_next_position(input_function, next_step)
    next_step = move_step_through_wall(next_step, size)
    return next_step


def generate_snack_position(snake_body, size):
    snack_needed = True
    snack_position = (None, None)
    while (snack_position in snake_body or (snack_needed)):
        snack_position = (random.randint(0, size - 1),
                          random.randint(0, size - 1))
        snack_needed = False
    return snack_position


def run_initial_game_loop(snake_body, initial_length, starting_position, size, inputMethod):
    is_fed = True
    next_step = starting_position
    for i in range(0, initial_length - 1):
        clear()
        show_score(snake_body, initial_length)
        print_game(size, snake_body, None)
        next_step = get_next_step(
            next_step, size, snake_body, inputMethod)
        if (next_step in snake_body and i < 2):
            snake_body = snake_body[:snake_body.index(next_step) + 1]
        move_snake(snake_body, next_step, is_fed)
    return snake_body


def run_main_game_loop(snake_body, initial_length, size, inputMethod):
    is_fed = False
    snack_needed = True
    next_step = snake_body[0]
    is_game_running = True
    while (is_game_running):
        clear()
        show_score(snake_body, initial_length)
        if (snack_needed):
            snack_position = generate_snack_position(snake_body, size)
            snack_needed = False
        print_game(size, snake_body, snack_position)
        next_step = get_next_step(
            next_step, size, snake_body, inputMethod)
        if (next_step == snack_position):
            is_fed = True
            snack_needed = True
        if (next_step in snake_body):
            snake_body = snake_body[:snake_body.index(next_step) + 1]
        move_snake(snake_body, next_step, is_fed)
        is_fed = False


def run_game():
    size = 9
    initial_length = 3
    starting_position = (4, 4)
    snake_body = [starting_position]
    show_title()
    show_controlls()
    input()
    snake_body = run_initial_game_loop(
        snake_body, initial_length, starting_position, size, get_keyboard_input)
    run_main_game_loop(snake_body, initial_length, size, get_keyboard_input)

# endregion
# </editor-fold>
# ================================================= end of definitions


initialize_windows_shell()
run_game()
