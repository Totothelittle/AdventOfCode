#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 6
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
import math
import re

INPUTFILE = "Advent of Code 2024/Day6/Input.in"

SAMPLE_CASES = [
    (
        """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
        """,
        41
    ),
]

SAMPLE_CASES2 = [
    (
        """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
        """,
        6
    ),
]



Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(
        Path(infile).read_text(), strip=strip, blank_lines=blank_lines
    )

def load_text(text: str, strip=True, blank_lines=False) -> Lines:
    if strip:
        lines = [line.strip() for line in text.strip("\n").split("\n")]
    else:
        lines = text.strip("\n").split("\n")
    if blank_lines:
        return lines
    return [line for line in lines if line.strip()]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        if not line.strip():
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

GROUND, OBSTACLE, OUTSIDE = ".", "#", " "

Direction = str
NORTH, EAST, SOUTH, WEST = "^", ">", "v", "<"
DIRECTION: set[Direction] = {NORTH, SOUTH, EAST, WEST}
RIGHT: dict[Direction, Direction] = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}


@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def neighbors(self) -> "List[Pos]":
        return [
            Pos(self.row, self.col + 1),
            Pos(self.row + 1, self.col),
            Pos(self.row, self.col - 1),
            Pos(self.row - 1, self.col),
        ]

    def neighbor(self, dxn: Direction) -> "Pos":
        if  dxn == NORTH:
            return self.north()
        if  dxn == SOUTH:
            return self.south()
        if  dxn == EAST:
            return self.east()
        if  dxn == WEST:
            return self.west()
        return self

    def north(self) -> "Pos":
        return Pos(self.row - 1, self.col)

    def south(self) -> "Pos":
        return Pos(self.row + 1, self.col)

    def east(self) -> "Pos":
        return Pos(self.row, self.col + 1)

    def west(self) -> "Pos":
        return Pos(self.row, self.col - 1)



@dataclass
class Guard:
    pos: Pos
    dxn: str

    def forward(self):
        return self.pos.neighbor(self.dxn)

    def to_right(self):
        return self.pos.neighbor(RIGHT[self.dxn])

    def advance(self):
        self.pos = self.pos.neighbor(self.dxn)

    def turn_right(self):
        self.dxn = RIGHT[self.dxn]

    def patrol(self,
            grid: "Grid",
            visited: set[Tuple[Pos, str]] = None,
            find_loops: bool = False
        ) -> bool:
        """Trace out the path this guard follows on his patrol, and
        determine if it's safe for the historians to work there.
        Returns True if the route is a loop within the grid,
        and False if the patrol leads the guard outside the grid.
        """
        if find_loops:
            grid.loops = 0

        if visited:
            path = set(visited)
        else:
            path: set[Tuple[pos, str]] = set()
            path.add((self.pos, self.dxn))

        while grid.at(self.pos) != OUTSIDE:
            original_dxn = self.dxn
            ahead = self.forward()

            # Turn right if we meet an obstacle
            while grid.at(ahead) == OBSTACLE:
                self.turn_right()
                assert self.dxn != original_dxn
                ahead = self.forward()
            grid.set(self.pos, original_dxn)
            self.advance()
            # print(f"advance {self.dxn} to {self.pos}")

            if (self.pos, self.dxn) in path:
                # We've been here before
                return True
            path.add((self.pos, self.dxn))

            if not find_loops:
                continue

            # Check whether we could create a loop by placing an obstacle here
            ahead = self.forward()
            if grid.at(ahead) == OBSTACLE:
                ahead = self.to_right()
                if grid.at(ahead) == OBSTACLE:
                    continue

            if grid.at(ahead) in DIRECTION:
                # placing an obstacle here interferes with the guard's route to
                # this point
                continue
            if grid.at(ahead) == OUTSIDE:
                # cannot place an obstacle outside the grid
                continue

            # Use a clean grid to see if an obstacle here produces a loop

            # print(f"\n---- test obstacle at {ahead} ...")
            new_guard = Guard(self.pos, self.dxn)
            new_grid = grid.clone(start=new_guard)
            new_grid.set(ahead, OBSTACLE)
            # print(new_grid)
            is_loop = new_guard.patrol(new_grid, visited=path)
            if is_loop:
                # print(f">> Obstacle at {ahead} would create a loop!")
                grid.loops += 1
            # else:
            #     print(">> No loop here\n")

        return False


@dataclass
class Grid:
    grid: dict[Pos, str]
    start: Optional[Guard] = None
    bounds: Optional[Any] = None
    loops: Optional[int] = None

    def __post_init__(self):
        for pos, ch in self.grid.items():
            if ch != GROUND:
                if ch in DIRECTION and self.start is None:
                    self.start = Guard(pos, ch)
            else:
                assert ch in (GROUND, OBSTACLE)

        rownums = [pos.row for pos in self.grid.keys()]
        rmin, rmax = min(rownums), max(rownums)
        colnums = [pos.col for pos in self.grid.keys()]
        cmin, cmax = min(colnums), max(colnums)
        self.bounds = (rmin, rmax, cmin, cmax)

    def at(self, pos: Pos) -> str:
        return self.grid[pos]

    def set(self, pos: Pos, char: str) -> None:
        self.grid[pos] = char

    def clone(self, start: Optional[Guard] = None) -> "Grid":
        clean_grid = defaultdict(lambda: OUTSIDE)
        for pos, ch in self.grid.items():
            if ch == OUTSIDE:
                continue
            if ch == OBSTACLE:
                clean_grid[pos] = ch
            else:
                clean_grid[pos] = GROUND
        if start:
            clean_grid[start.pos] = start.dxn
        return Grid(clean_grid)

    def __str__(self):
        lines = []
        rmin, rmax, cmin, cmax = self.bounds
        for r in range(rmin-1, rmax+2):
            line = []
            for c in range(cmin-1, cmax+2):
                line.append(self.grid[Pos(r, c)])
            lines.append("".join(line))
        return "\n".join(lines)

    def visited(self) -> int:
        result = 0
        for val in self.grid.values():
            if val in DIRECTION:
                result += 1
        return result


def parse_input(lines) -> Tuple[Grid, Guard]:
    new_grid = defaultdict(lambda: OUTSIDE)
    for row, line in enumerate(lines):
        assert line
        for col, ch in enumerate(line):
            new_grid[Pos(row, col)] = ch
    grid = Grid(new_grid)
    guard = grid.start
    return grid, guard


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    grid, guard = parse_input(lines)
    # print(grid)
    # print("-" * 64)
    # print(f"Start at {guard}")
    guard.patrol(grid, find_loops=True)
    # print(grid)
    # print("-" * 64)
    return grid.loops

def solve(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    grid, guard = parse_input(lines)
    # print(grid)
    # print("-" * 64)

    # print(f"Start at {guard}")
    guard.patrol(grid)
    # print(grid)
    # print("-" * 64)
    return grid.visited()


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    #assert result == 4559
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    #assert result == 1604
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
