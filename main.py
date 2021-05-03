import time
import curses
import asyncio
from random import randint, choice
from curses_tools import draw_frame, read_controls, get_frame_size
import itertools
from utils import sleep, explode, show_gameover
from upload_frames import read_trash, read_rocket_frames, read_game_over
from physics import update_speed
from obstacles import Obstacle

TIC_TIMEOUT = 0.1
COROUTINES = []
OBSTACLES = []
OBSTACLES_IN_LAST_COLLISIONS = []


async def fill_orbit_with_garbage(canvas, width, frames):
    while True:
        column = randint(0, width - 1)
        coroutine_garbage = fly_garbage(canvas, column, choice(frames))
        COROUTINES.append(coroutine_garbage)
        await sleep(5)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()
    garbage_frame_rows, garbage_frame_columns = get_frame_size(garbage_frame)

    row = 0
    obstacle = Obstacle(row, column, garbage_frame_rows, garbage_frame_columns)
    OBSTACLES.append(obstacle)

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        if obstacle in OBSTACLES_IN_LAST_COLLISIONS:
            OBSTACLES.remove(obstacle)
            OBSTACLES_IN_LAST_COLLISIONS.remove(obstacle)
            await explode(canvas, row, column)
            return
        obstacle.row += speed


async def animate_spaceship(canvas, row, column, frames, game_over_frame):
    canvas_rows, canvas_columns = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(frames[0])
    row_speed = column_speed = 0

    for frame in itertools.cycle(frames):
        for obstacle in OBSTACLES:
            if obstacle.has_collision(row, column):
                COROUTINES.append(show_gameover(canvas, game_over_frame))
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)

        new_row, new_column, flag_fire = read_controls(canvas)
        row_speed, column_speed = update_speed(row_speed, column_speed, new_row, new_column)

        if 0 < row + row_speed < canvas_rows - frame_rows:
            row += row_speed
        if 0 < column + column_speed < canvas_columns - frame_columns:
            column += column_speed

        if flag_fire:
            COROUTINES.append(fire(canvas, row, column + 2))


async def fire(canvas, row, column, rows_speed=-0.3, columns_speed=0):
    while 0 < row:
        for obstacle in OBSTACLES:
            if obstacle.has_collision(row, column):
                OBSTACLES_IN_LAST_COLLISIONS.append(obstacle)
                return
        canvas.addstr(round(row), round(column), '|')
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(randint(1, 20))
        canvas.addstr(row, column, symbol)
        await sleep(randint(1, 20))
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(randint(1, 20))
        canvas.addstr(row, column, symbol)
        await sleep(randint(1, 20))


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    height, width = canvas.getmaxyx()

    for i in range(150):
        row = randint(1, height - 2)
        column = randint(1, width - 2)
        symbol = choice('+*.:')
        coroutine = blink(canvas, row, column, symbol)
        COROUTINES.append(coroutine)

    rocket_frames = read_rocket_frames()
    game_over_frame = read_game_over()
    coroutine_spaceship = animate_spaceship(canvas, height / 2, width / 2, rocket_frames,
                                            game_over_frame)
    COROUTINES.append(coroutine_spaceship)

    garbage_frames = read_trash()
    coroutine_garbage = fill_orbit_with_garbage(canvas, width, garbage_frames)
    COROUTINES.append(coroutine_garbage)

    while True:
        for coroutine in COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                COROUTINES.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
