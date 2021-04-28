import time
import curses
import asyncio
from random import randint, choice


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


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    height, width = canvas.getmaxyx()
    coroutines = []

    for i in range(50):
        row = randint(1, height - 2)
        column = randint(1, width - 2)
        symbol = choice('+*.:')
        coroutine = blink(canvas, row, column, symbol)
        coroutines.append(coroutine)

    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        canvas.refresh()
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
