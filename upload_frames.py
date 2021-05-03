def read_rocket_frames():
    with open('frames/rocket_frame_1.txt', 'r') as my_file:
        frame_1 = my_file.read()
    with open('frames/rocket_frame_2.txt', 'r') as my_file:
        frame_2 = my_file.read()
    frames = [
        frame_1,
        frame_1,
        frame_2,
        frame_2,
    ]
    return frames


def read_trash():
    with open('frames/trash_small.txt', 'r') as my_file:
        trash_1 = my_file.read()
    with open('frames/trash_large.txt', 'r') as my_file:
        trash_2 = my_file.read()
    with open('frames/trash_xl.txt', 'r') as my_file:
        trash_3 = my_file.read()
    garbage_frames = [
        trash_1,
        trash_2,
        trash_3,
    ]
    return garbage_frames


def read_game_over():
    with open('frames/game_over.txt', 'r') as my_file:
        game_over_frame = my_file.read()
    return game_over_frame


def read_explosion_frames():
    with open('frames/explosion_frame_1.txt', 'r') as my_file:
        frame_1 = my_file.read()
    with open('frames/explosion_frame_2.txt', 'r') as my_file:
        frame_2 = my_file.read()
    with open('frames/explosion_frame_3.txt', 'r') as my_file:
        frame_3 = my_file.read()
    with open('frames/explosion_frame_4.txt', 'r') as my_file:
        frame_4 = my_file.read()
    explosion_frames = [
        frame_1,
        frame_2,
        frame_3,
        frame_4,
    ]
    return explosion_frames
