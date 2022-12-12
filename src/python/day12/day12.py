from termcolor import colored
from pathlib import Path
from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Iterable
from time import sleep, time
from os import system, name
from collections import defaultdict
from queue import PriorityQueue


Position = tuple[int, int]

def clear():
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux
    else:
        _ = system("clear")


@dataclass()
class Terrain:
    matrix: list[str]
    starting_position: Position
    finish_position: Position
    trail_starting_points: list[Position]

    def __str__(self):
        description = f"Start: {self.starting_position} Finish: {self.finish_position}\n"
        return description + "\n".join(self.matrix)

    def _adjacent_positions(self, position: Position, value: str) -> list[Position]:
        adjacent_positions = []
        x, y = position
        if x > 0:
            cell_value = self.matrix[x - 1][y]
            if ord(cell_value) <= ord(value) + 1:
                adjacent_positions.append((x - 1, y))
        if x < len(self.matrix) - 1:
            cell_value = self.matrix[x + 1][y]
            if ord(cell_value) <= ord(value) + 1:
                adjacent_positions.append((x + 1, y))
        if y > 0:
            cell_value = self.matrix[x][y - 1]
            if ord(cell_value) <= ord(value) + 1:
                adjacent_positions.append((x, y - 1))
        if y < len(self.matrix[0]) - 1:
            cell_value = self.matrix[x][y + 1]
            if ord(cell_value) <= ord(value) + 1:
                adjacent_positions.append((x, y + 1))
        return adjacent_positions

    @cached_property
    def adjacent_list(self) -> dict[Position, list[Position]]:
        adjacent_list = {}
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                adjacent_list[(i, j)] = self._adjacent_positions(
                    position=(i, j),
                    value=value,
                )
        return adjacent_list

    @classmethod
    def from_file(cls, path: Path) -> "Terrain":
        matrix = []
        trail_starting_points = []
        with open(path, "r") as f:
            i = 0
            for line in f:
                if "S" in line:
                    starting_position = (i, line.index("S"))
                    line = line.replace("S", "a")
                if "E" in line:
                    finish_position = (i, line.index("E"))
                    line = line.replace("E", "z")
                if "a" in line:
                    trail_starting_points.append((i, line.index("a")))
                matrix.append(line.strip())
                i += 1
        return cls(
            matrix=matrix,
            starting_position=starting_position,
            finish_position=finish_position,
            trail_starting_points=trail_starting_points,
        )

    def get_neighbors(self, v):
        return self.adjacent_list[v]

    def dijkstra(self, start_node, target_node):
        start_node = start_node
        target_node = target_node

        visited = set()
        D = defaultdict(lambda: float('inf'))
        D[start_node] = 0

        pq = PriorityQueue()
        pq.put((0, start_node))

        parent = dict()
        parent[start_node] = None
        path_found = False
        iteratrion = 0
        while not pq.empty():
            (dist, current_node) = pq.get()
            if current_node == target_node:
                path_found = True
                break
            visited.add(current_node)

            for neighbour in self.get_neighbors(current_node):
                if neighbour not in visited:
                    old_cost = D[neighbour]
                    new_cost = D[current_node] + 1
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbour))
                        D[neighbour] = new_cost
                        parent[neighbour] = current_node
            iteratrion += 1

        path = []
        if path_found:
            path.append(target_node)
            while True:
                parent_node = parent[target_node]
                if parent_node is None:
                    break
                path.append(parent_node)
                target_node = parent_node
            path.reverse()
        return (path, iteratrion)

    def a_star_algorithm(self, start: Position, finish: Position)-> Optional[list[Position]]:
        # In this open_lst is a lisy of nodes which have been visited, but who's
        # neighbours haven't all been always inspected, It starts off with the start
        # node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst: set[Position] = set([start])
        closed_lst: set[Position] = set([])

        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo: dict[Position, int]  = {}
        poo[start] = 0

        # par contains an adjac mapping of all nodes
        par: dict[Position, Position] = {}
        par[start] = start

        while len(open_lst) > 0:
            n: Optional[Position] = None

            for v in open_lst:
                if n is None:
                    n = v

            if n is None:
                return None

            # if the current node is the stop
            # then we start again from start
            if n == finish:
                reconst_path = []

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return reconst_path

            # for all the neighbors of the current node do
            for m in self.get_neighbors(n):
                # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + 1

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + 1:
                        poo[m] = poo[n] + 1 
                        par[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)

        return None

    def print_paths(self, path: list[Position]) -> Iterable[str]:
        matrix_str = self.matrix.copy()
        matrix = [list(row) for row in matrix_str]
        for position in path:
            matrix[position[0]][position[1]] = colored(matrix[position[0]][position[1]], "white", "on_white")
            yield "\n".join(["".join(row) for row in matrix])

def debug(terrain: Terrain, path: list[Position]):
    clear() 
    for path_str in terrain.print_paths(path):
        print(colored("#" * 20, "white", "on_white"))
        print(terrain)
        print(colored("#" * 20, "white", "on_white"))
        print(path_str)
        print(colored("#" * 20, "white", "on_white"))
        sleep(0.1)
        clear() 

def problem1(terrain: Terrain, debug: bool = False):
    # path = terrain.a_star_algorithm(terrain.starting_position, terrain.finish_position)
    path, _ = terrain.dijkstra(terrain.starting_position, terrain.finish_position)
    if debug:
        debug(terrain, path)
    return len(path) - 1

def problem2(terrain: Terrain):
    paths = []
    for starting_position in terrain.trail_starting_points:
        path = terrain.a_star_algorithm(starting_position, terrain.finish_position)
        paths.append(path)
    return min(map(len, paths)) - 1

def preformance_comparition(terrain: Terrain):
    start_time = time()
    for _ in range(100000):
        terrain.a_star_algorithm(terrain.starting_position, terrain.finish_position)
    print(f"A* algorithm took {time() - start_time} seconds")
    start_time = time()
    for _ in range(100000):
        terrain.dijkstra(terrain.starting_position, terrain.finish_position)
    print(f"Dijkstra algorithm took {time() - start_time} seconds")

def main():
    input_path = Path("files/day12/test_input.txt")
    # input_path = Path("files/day12/input.txt")
    terrain = Terrain.from_file(input_path)
    print(colored("Problem 1: ", "blue"))
    print(problem1(terrain))
    print(colored("Problem 2: ", "blue"))
    print(problem2(terrain))
    preformance_comparition(terrain)

if __name__ == "__main__":
    main()
