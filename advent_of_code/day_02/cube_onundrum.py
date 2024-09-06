import re
from dataclasses import dataclass
from typing import List


FILENAME = "input.txt"

TOTAL_RED_CUBES = 12
TOTAL_GREEN_CUBES = 13
TOTAL_BLUE_CUBES = 14


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    game_id: int
    cube_sets: List[CubeSet]


def parse_game(line) -> Game:
    # regex for parsing the line which looks like this:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    match = re.search(r"Game (\d+): (.+)", line)
    game = Game(game_id=int(match.group(1)), cube_sets=[])
    sets = match.group(2).split(";")
    for set in sets:
        cube_set = create_set(set)
        game.cube_sets.append(cube_set)

    return game


def create_set(set: str) -> CubeSet:
    cube_set = CubeSet()
    cubes = set.split(",")
    for cube in cubes:
        cube = cube.strip()
        count, color = cube.split(" ")

        if color == "red":
            cube_set.red = int(count)
        elif color == "green":
            cube_set.green = int(count)
        elif color == "blue":
            cube_set.blue = int(count)
        else:
            raise ValueError(f"Unknown color: {color}")

    return cube_set


def is_game_possible(game: Game) -> bool:
    for set_ in game.cube_sets:
        if set_.red > TOTAL_RED_CUBES or set_.green > TOTAL_GREEN_CUBES or set_.blue > TOTAL_BLUE_CUBES:
            return False

    return True


def minimum_playable_cubes(game: Game) -> int:
    max_red = max(set_.red for set_ in game.cube_sets)
    max_green = max(set_.green for set_ in game.cube_sets)
    max_blue = max(set_.blue for set_ in game.cube_sets)

    return max_red * max_green * max_blue


def main():
    sum_posible_games = 0
    sum_playable_cubes = 0

    # Read the input file
    with open(FILENAME) as f:
        lines = f.readlines()

    for line in lines:
        game = parse_game(line)
        playable_cubes = minimum_playable_cubes(game)
        sum_playable_cubes += playable_cubes
        playable = is_game_possible(game)
        if playable:
            sum_posible_games += game.game_id

        print(
            f"Game {game.game_id} is {'possible' if playable else 'not possible'}, "
            f"minimum playable cubes: {playable_cubes}"
        )

    print(f"Final sum possible games from file: {FILENAME} is {sum_posible_games}")
    print(f"Final sum playable cubes from file: {FILENAME} is {sum_playable_cubes}")


if __name__ == "__main__":
    main()
