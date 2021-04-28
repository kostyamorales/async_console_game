import time
import curses
import asyncio
from random import randint, choice
from curses_tools import draw_frame, read_controls, get_frame_size

TIC_TIMEOUT = 0.1


async def animate_spaceship(canvas, row, column, frame_1, frame_2):
    max_row, max_column = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(frame_1)
    while True:
        draw_frame(canvas, row, column, frame_1)
        canvas.refresh()
        time.sleep(0.2)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame_1, negative=True)

        new_row, new_column, _ = read_controls(canvas, row, column)

        if 0 < new_row < max_row - frame_rows:
            row = new_row

        if 0 < new_column < max_column - frame_columns:
            column = new_column

        draw_frame(canvas, row, column, frame_2)
        canvas.refresh()
        time.sleep(0.2)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame_2, negative=True)


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
    with open("files/rocket_frame_1.txt", "r") as my_file:
        frame_1 = my_file.read()
    with open("files/rocket_frame_2.txt", "r") as my_file:
        frame_2 = my_file.read()
    return frame_1, frame_2


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    height, width = canvas.getmaxyx()
    coroutines = []

    for i in range(50):
        row = randint(1, height - 2)
        column = randint(1, width - 2)
        symbol = choice('+*.:')
        coroutine = blink(canvas, row, column, symbol)
        coroutines.append(coroutine)

    coroutine_fire = fire(canvas, height / 2, width / 2)
    coroutines.append(coroutine_fire)

    frame_1, frame_2 = read_rocket_frames()
    coroutine_spaceship = animate_spaceship(canvas, height / 2, width / 2, frame_1, frame_2)
    coroutines.append(coroutine_spaceship)

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
