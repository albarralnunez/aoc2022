from pathlib import Path
from typing import IO, Union, Callable
import re
import dataclasses
from functools import cached_property
from time import time


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Dir:
    name: str
    parent: Union["Dir", None] = dataclasses.field(repr=False, default=None)
    dirs: list["Dir"] = dataclasses.field(default_factory=list)
    files: list[File] = dataclasses.field(default_factory=list)

    @cached_property
    def size(self):
        size = 0
        for file in self.files:
            size += file.size
        for dir in self.dirs:
            size += dir.size
        return size

    def mkdir(self, dir: "Dir"):
        self.dirs.append(dir)

    def touch(self, file: File):
        self.files.append(file)

    def tree(self, depth=0):
        repr = ""
        repr += f"{' ' * depth}- {self.name} (dir, size={self.size})\n"
        for file in self.files:
            repr += f"{' ' * (depth+4)}- {file.name} (file, size={file.size})\n"
        for dir in self.dirs:
            repr += dir.tree(depth + 4)
        return repr

    def find_all_dirs_by(self, comparition: Callable, size: int) -> list["Dir"]:
        dirs = []
        if comparition(self.size, size):
            dirs.append(self)
        for dir in self.dirs:
            dirs += dir.find_all_dirs_by(comparition, size)
        return dirs


def read_dirs(f: IO) -> Dir:
    file_match = re.compile(r"^(\d+)\s([\w\.]+)")
    line = f.readline()
    dir = Dir(name=line.strip()[-1])
    root_dir = dir
    for line in f:
        clean_line = line.strip()
        file_line = file_match.match(clean_line)
        if file_line:
            file = File(name=file_line.group(2), size=int(file_line.group(1)))
            dir.touch(file)
        if clean_line.startswith("$ cd"):
            if clean_line[-1] == ".":
                if dir.parent is None:
                    raise ValueError("Can't go up from root dir")
                dir = dir.parent
            else:
                new_dir = Dir(name=clean_line[-1], parent=dir)
                dir.mkdir(new_dir)
                dir = new_dir
    return root_dir


def problem_1(f: IO):
    root_dir = read_dirs(f)
    dirs = root_dir.find_all_dirs_by(lambda x, y: x <= y, 100000)
    result = sum(dir.size for dir in dirs)
    return result


def problem_2(f: IO):
    root_dir = read_dirs(f)
    total_disk_size = 70000000
    free_space = total_disk_size - root_dir.size
    missing_space_for_update = 30000000 - free_space
    dirs = root_dir.find_all_dirs_by(lambda x, y: x >= y, missing_space_for_update)
    return min(dirs, key=lambda dir: dir.size).size


@timer_func
def time_problem_1(input_path: Path):
    for _ in range(100000):
        with input_path.open() as f:
            problem_1(f)


def main():
    # input_path = Path("files/day7/test_input.txt")
    input_path = Path("files/day7/input.txt")
    time_problem_1(input_path)
    with input_path.open() as f:
        solution = problem_1(f)
        print("Problem 1:")
        print(solution)

    with input_path.open() as f:
        solution = problem_2(f)
        print("Problem 2:")
        print(solution)


if __name__ == "__main__":
    main()
