import asyncio
from upload_frames import read_explosion_frames
from curses_tools import get_frame_size, draw_frame
import curses


async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)


async def explode(canvas, center_row, center_column):
    explosion_frames = read_explosion_frames()
    rows, columns = get_frame_size(explosion_frames[0])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()
    for frame in explosion_frames:
        draw_frame(canvas, corner_row, corner_column, frame)

        await asyncio.sleep(0)
        draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await asyncio.sleep(0)


async def show_gameover(canvas, frame):
    canvas_rows, canvas_columns = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(frame)
    row = (canvas_rows - frame_rows) // 2
    column = (canvas_columns - frame_columns) // 2
    while True:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


