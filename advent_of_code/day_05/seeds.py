from __future__ import annotations
from enum import Enum, auto
import sys
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Interval:
    start: int
    end: int

    def contains(self, value: int) -> bool:
        return self.start <= value <= self.end

    def split(self, other: Interval) -> List[Interval]:
        borders = sorted({self.start, self.end, other.start, other.end})
        return [Interval(borders[i], borders[i + 1]) for i in range(0, len(borders) - 1, 1)]

    def __eq__(self, other: Interval) -> bool:
        return self.start == other.start and self.end == other.end

    def __len__(self) -> int:
        return self.end - self.start + 1


@dataclass
class Map:
    destination_range: Interval
    source_range: Interval

    def __str__(self) -> str:
        return (
            f"{self.source_range.start:2d} - {self.source_range.end:2d} -> "
            f"{self.destination_range.start:2d} - {self.destination_range.end:2d}"
        )

    def __eq__(self, other: Map) -> bool:
        return self.source_range == other.source_range and self.destination_range == other.destination_range

    def remap(self, value: int) -> Optional[int]:
        if self.source_range.contains(value):
            delta = value - self.source_range.start
            return self.destination_range.start + delta

        return None

    def reverse_remap(self, value: int) -> Optional[int]:
        if self.destination_range.contains(value):
            delta = value - self.destination_range.start
            return self.source_range.start + delta

        return None

    def is_valid(self) -> bool:
        return len(self.source_range) > 0 and len(self.destination_range) > 0


class MergeState(Enum):
    READ = auto()
    CREATE_MAP = auto()
    MERGE_TO_LEFT = auto()
    MERGE_TO_RIGHT = auto()
    SPLIT = auto()
    DONE = auto()


@dataclass
class Mapping:
    name: str
    maps: List[Map]

    def __str__(self) -> str:
        text = f"{self.name}:\n"
        for map in self.maps:
            text += f"\t{map}\n"

        return text

    def __eq__(self, other: Mapping) -> bool:
        if len(self.maps) != len(other.maps):
            return False
        for other_map in other.maps:
            if any(other_map == map for map in self.maps) is False:
                return False

        return True

    def sort_maps(self) -> None:
        self.maps = sorted(self.maps, key=lambda x: x.source_range.start)

    def _merge_point(self, left, right, position_flag):
        point = None
        if left[2] == "d" and right[2] == "s":
            point = (left[1], right[1], "m", position_flag)
        elif left[2] == "s" and right[2] == "d":
            point = (right[1], left[1], "m", position_flag)
        else:
            raise Exception("invalid merge point")

        return point

    def merge(self, other: Mapping) -> "Mapping":
        borders = []
        for map in self.maps:
            borders.append((map.destination_range.start, map.source_range.start, "d", "b"))
            borders.append((map.destination_range.end, map.source_range.end, "d", "e"))
        for other_map in other.maps:
            borders.append((other_map.source_range.start, other_map.destination_range.start, "s", "b"))
            borders.append((other_map.source_range.end, other_map.destination_range.end, "s", "e"))

        borders = sorted(borders, key=lambda x: x[0])
        merged_maps = []

        left = None
        right = None

        state: MergeState = MergeState.READ
        while state != MergeState.DONE:
            if state == MergeState.READ:
                if len(borders) == 0 and left is None and right is None:
                    state = MergeState.DONE
                    continue

                if left is None:
                    left = borders.pop(0)
                if right is None:
                    right = borders.pop(0)

                if left[2] == right[2]:
                    state = MergeState.CREATE_MAP
                elif left[0] == right[0]:
                    state = MergeState.MERGE_TO_LEFT
                elif len(borders) > 0 and left[2] == "m" and right[0] == borders[0][0]:
                    state = MergeState.MERGE_TO_RIGHT
                elif left[0] != right[0]:
                    state = MergeState.SPLIT

            elif state == MergeState.CREATE_MAP:
                if left[2] == right[2] == "s" or left[2] == right[2] == "m":
                    map = Map(
                        source_range=Interval(left[0], right[0]),
                        destination_range=Interval(left[1], right[1]),
                    )
                elif left[2] == right[2] == "d":
                    map = Map(
                        source_range=Interval(left[1], right[1]),
                        destination_range=Interval(left[0], right[0]),
                    )
                else:
                    raise Exception("point type mismatch")

                print(f"Creating map {map}")
                assert map.is_valid()
                merged_maps.append(map)
                map = None

                left = right = None
                state = MergeState.READ

            elif state == MergeState.MERGE_TO_LEFT:
                borders.insert(0, self._merge_point(left, right, "b"))
                left = right = None
                state = MergeState.READ

            elif state == MergeState.MERGE_TO_RIGHT:
                # if left was merged I have to merge also right and right + 1 (right + 1 is first in borders)
                assert left[2] == "m"
                assert right[0] == borders[0][0]
                borders.insert(0, self._merge_point(right, borders.pop(0), "e"))
                borders.insert(0, left)
                left = right = None
                state = MergeState.READ

            elif state == MergeState.SPLIT:
                # split interval before right
                if left[3] == "b" and right[3] == "b":
                    delta = right[0] - left[0]
                    borders.insert(0, (left[0] + delta, left[1] + delta, left[2], "b"))  # merge point
                    borders.insert(0, right)
                    borders.insert(0, (left[0] + delta - 1, left[1] + delta - 1, left[2], "e"))  # end of left
                    borders.insert(0, left)

                # split interval after left
                elif left[3] == "e" and right[3] == "e":
                    delta = right[0] - left[0]
                    borders.insert(0, right)
                    borders.insert(0, (right[0] - delta + 1, right[1] - delta + 1, right[2], "b"))  # start of right
                    borders.insert(0, left)
                    borders.insert(0, (right[0] - delta, right[1] - delta, right[2], "e"))  # merge point

                # split interval after right (when left is merged)
                elif left[3] == "b" and right[3] == "e" and right[2] == "s":
                    assert left[2] == "m"
                    delta = right[1] - left[1]
                    # opposite type as right (I lost type of merged left)
                    borders.insert(0, (right[0] + 1, left[0] + delta + 1, "d", "b"))  # start of right
                    borders.insert(0, (right[0], left[0] + delta, "d", "e"))  # merge point
                    borders.insert(0, right)
                    borders.insert(0, left)

                elif left[3] == "b" and right[3] == "e" and right[2] == "d":
                    assert left[2] == "m"
                    delta = right[1] - left[0]
                    # opposite type as right (I lost type of merged left)
                    borders.insert(0, (right[0] + 1, left[1] + delta + 1, "s", "b"))  # start of right
                    borders.insert(0, (right[0], left[1] + delta, "s", "e"))  # merge point
                    borders.insert(0, right)
                    borders.insert(0, left)

                right = left = None
                state = MergeState.READ
            else:
                raise Exception("Unknown state")

        return Mapping(name=self.name.split("-")[0] + "-to-" + other.name.split("-")[2], maps=merged_maps)


def parse_file(filename: str) -> Tuple[List[int], Dict[str, Mapping]]:
    mappings: Dict[str, Mapping] = {}
    with open(filename) as f:
        text = f.read()

    seeds_pattern = re.compile(r"seeds:\s(?P<seeds>[0-9\s]+)")
    match = seeds_pattern.search(text)
    seeds = [int(num) for num in match.group("seeds").split()]

    map_pattern = re.compile(r"(?P<map_name>.*) map:\n(?P<maps>(?:\d+ \d+ \d+\n?)+)", re.MULTILINE)
    mappings_pattern = re.compile(r"(?P<destination>\d+)\s(?P<source>\d+)\s(?P<length>\d+)")

    for match in map_pattern.finditer(text):
        map_name = match.group("map_name")
        if map_name not in mappings:
            mappings[map_name] = Mapping(name=map_name, maps=[])

        for mapping in mappings_pattern.finditer(match.group("maps")):
            destination = int(mapping.group("destination"))
            source = int(mapping.group("source"))
            length = int(mapping.group("length"))
            mappings[map_name].maps.append(
                Map(
                    destination_range=Interval(destination, destination + length - 1),
                    source_range=Interval(source, source + length - 1),
                )
            )
        mappings[map_name].sort_maps()

    return seeds, mappings


def seed_to_location(seed: int, maps: Dict[str, List[Map]]):
    for map_name, map_lists in maps.items():
        for one_map in map_lists:
            value = one_map.remap(seed)

            if value is not None:
                print(f"{seed} remapped to {value} by {map_name}")
                seed = value
                break

    return seed


def location_to_seed(location: int, maps: Dict[str, List[Map]]):
    for map_name, map_lists in reversed(maps.items()):
        for one_map in map_lists:
            value = one_map.reverse_remap(location)

            if value is not None:
                print(f"{location} remapped to {value} by {map_name}")
                location = value
                break
            else:
                return None

    return location


def main():
    if len(sys.argv) != 2:
        print("Usage: python seeds.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    seeds, mappings = parse_file(filename)

    # print(f"Seeds: {seeds}")
    # print(f"Maps: {maps}")

    # part two, seeds contains pairs of seeds
    seeds_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    print(f"Seeds ranges: {seeds_ranges}")

    # locations = []
    # for seed in seeds:
    #     print(f"Remapping seed {seed}")
    #     locations.append(seed_to_location(seed, maps))

    #     print(f"The lowest location number is {min(locations)}")

    merged = None
    for mapping in mappings.values():
        if merged is None:
            print(f"First mapping {mapping.name}")
            merged = mapping
        else:
            print(f"Merging mapping {merged.name} with {mapping.name}")
            print(mapping)
            merged = merged.merge(mapping)

        print(merged)


if __name__ == "__main__":
    main()

    # # split bottom interval before right
    # if left[2] == "s" and left[3] == "b" and right[2] == "d" and right[3] == "b":
    #     delta = right[0] - left[0]
    #     borders.insert(0, (left[0] + delta, left[1] + delta, left[2], "b"))  # merge point
    #     borders.insert(0, right)
    #     borders.insert(0, (left[0] + delta - 1, left[1] + delta - 1, left[2], "e"))  # end of left
    #     borders.insert(0, left)
    #     right = left = None

    # # split bottom interval after left
    # elif left[2] == "d" and left[3] == "e" and right[2] == "s" and right[3] == "e":
    #     delta = right[0] - left[0]
    #     borders.insert(0, right)
    #     borders.insert(0, (right[0] - delta + 1, right[1] - delta + 1, right[2], "b"))  # start of right
    #     borders.insert(0, left)
    #     borders.insert(0, (right[0] - delta, right[1] - delta, right[2], "e"))  # merge point

    # # split upper interval before right
    # elif left[2] == "d" and left[3] == "b" and right[2] == "s" and right[3] == "b":
    #     delta = right[0] - left[0]
    #     borders.insert(0, (left[0] + delta, left[1] + delta, left[2], "b"))  # merge point
    #     borders.insert(0, right)
    #     borders.insert(0, (left[0] + delta - 1, left[1] + delta - 1, left[2], "e"))  # end of left
    #     borders.insert(0, left)
    #     right = left = None

    # # split upper interval after left
    # elif left[2] == "s" and left[3] == "e" and right[2] == "d" and right[3] == "e":
    #     delta = right[0] - left[0]
    #     borders.insert(0, right)
    #     borders.insert(0, (right[0] - delta + 1, right[1] - delta + 1, right[2], "b"))  # start of right
    #     borders.insert(0, left)
    #     borders.insert(0, (right[0] - delta, right[1] - delta, right[2], "e"))  # merge point
    #     right = left = None
