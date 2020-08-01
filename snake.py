import os
import random
import ctypes
import time
kernel32 = ctypes.WinDLL('kernel32')
hStdOut = kernel32.GetStdHandle(-11)
mode = ctypes.c_ulong()
kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
mode.value |= 4
kernel32.SetConsoleMode(hStdOut, mode)


def clear(): return os.system('cls')


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


def remove_last_element(array):
    array.pop(len(array) - 1)


def add_first_element(array, element):
    array.insert(0, element)


def move_snake(body, position, fed):
    add_first_element(body, position)
    if (not fed):
        remove_last_element(body)


def map_input_to_next_position(current_position, input):
    b = (0, 0)
    if (input == "w"):
        b = (0, -1)
    if (input == "s"):
        b = (0, 1)
    if (input == "a"):
        b = (-1, 0)
    if (input == "d"):
        b = (1, 0)
    return (current_position[0] + b[0], current_position[1] + b[1])


def validate_Step(size, body, step):
    valid = True
    if (step[0] < 0 or step[1] < 0 or step[0] > size - 1 or step[1] > size-1 or step in body):
        valid = False
    return valid


def colored_text(text, color):
    END = '\033[0m'
    return f"{color}{text}{END}"


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


size = 9
is_game_running = True
is_fed = True
initial_length = 3
starting_position = (4, 4)
snack_position = (None, None)
snake_body = [starting_position]
next_step = starting_position
validStep = False
snack_needed = False

print("pySnake!")
print("Controls:")
print("w - up")
print("s - down")
print("a - left")
print("d - right")
print("enter - confirm move")
print("Press enter to start!")
input()

while (is_game_running):
    clear()
    print(
        f"Score:  {colored_text(len(snake_body) - 3, bcolors.BLUE) if len(snake_body) - 3 >= 0 else 0}")
    print_game(size, snake_body, snack_position)
    is_fed = False
    while (not validStep):
        current_step = next_step
        next_step = map_input_to_next_position(next_step, input())
        #next_step = map_input_to_next_position(next_step, random.choice(["w", "s", "a", "d"]))
        # time.sleep(1)
        validStep = validate_Step(size, snake_body, next_step)
        if (not validStep):
            next_step = current_step
    if (next_step == snack_position):
        is_fed = True
        snack_needed = True
    if (initial_length > 1):
        initial_length -= 1
        if (initial_length == 1):
            snack_needed = True
        is_fed = True
    move_snake(snake_body, next_step, is_fed)
    if (snack_needed):
        while (snack_position in snake_body or (snack_needed)):
            snack_position = (random.randint(0, size - 1),
                              random.randint(0, size - 1))
            snack_needed = False
    validStep = False
