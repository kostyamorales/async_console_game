import time
import curses
import asyncio
from random import randint, choice
from curses_tools import draw_frame, read_controls, get_frame_size
import itertools

TIC_TIMEOUT = 0.1


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    # column = max(column, 0)
    # column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def animate_spaceship(canvas, row, column, frames):
    canvas_rows, canvas_columns = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(frames[0])

    for frame in itertools.cycle(frames):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)

        new_row, new_column, _ = read_controls(canvas, row, column)
        if 0 < new_row < canvas_rows - frame_rows:
            row = new_row
        if 0 < new_column < canvas_columns - frame_columns:
            column = new_column


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(randint(1, 20)):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def read_rocket_frames():
    with open('files/rocket_frame_1.txt', 'r') as my_file:
        frame_1 = my_file.read()
    with open('files/rocket_frame_2.txt', 'r') as my_file:
        frame_2 = my_file.read()
    return frame_1, frame_2


def read_trash():
    with open('files/trash_small.txt', 'r') as my_file:
        trash_1 = my_file.read()
    with open('files/trash_large.txt', 'r') as my_file:
        trash_2 = my_file.read()
    with open('files/trash_xl.txt', 'r') as my_file:
        trash_3 = my_file.read()
    return trash_1, trash_2, trash_3


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    height, width = canvas.getmaxyx()
    coroutines = []

    for i in range(150):
        row = randint(1, height - 2)
        column = randint(1, width - 2)
        symbol = choice('+*.:')
        coroutine = blink(canvas, row, column, symbol)
        coroutines.append(coroutine)

    coroutine_fire = fire(canvas, height / 2, width / 2)
    coroutines.append(coroutine_fire)

    frame_1, frame_2 = read_rocket_frames()
    frames = [
        frame_1,
        frame_1,
        frame_2,
        frame_2
    ]
    coroutine_spaceship = animate_spaceship(canvas, height / 2, width / 2, frames)
    coroutines.append(coroutine_spaceship)

    trash_1, trash_2, trash_3 = read_trash()
    garbage_frames = [
        trash_1,
        trash_2,
        trash_3
    ]
    column = randint(0, width - 1)
    coroutine_garbage = fly_garbage(canvas, column, choice(garbage_frames))
    coroutines.append(coroutine_garbage)

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
