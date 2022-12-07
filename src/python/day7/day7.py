from pathlib import Path
from typing import IO, Union
import re
import dataclasses
import copy


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

    @property
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
            repr += dir.tree(depth+4)
        return repr
    
    def find_all_dirs_by(self, comparition: callable, size: int) -> list["Dir"]:
        dirs = []
        if comparition(self.size, size):
            dirs.append(self)
        for dir in self.dirs:
            dirs += dir.find_all_dirs_by(comparition, size)
        return dirs

def read_dirs(f: IO) -> Dir:
    file_match = re.compile(r"^(\d+)\s([\w\.]+)")
    f.readline()
    dir = Dir(name="/")
    root_dir = copy.copy(dir)
    for line in f:
        clean_line = line.strip()
        file_line = file_match.match(clean_line)
        if file_line:
            file = File(
                name=file_line.group(2),
                size=int(file_line.group(1))
            )
            dir.touch(file)
        if clean_line.startswith("$ cd"):
            if clean_line[-1] == ".":
                dir = dir.parent
            else:
                new_dir = Dir(
                    name=clean_line[-1],
                    parent=dir
                )
                dir.mkdir(new_dir)
                dir = new_dir
    return root_dir


def problem_1(f: IO):
    root_dir = read_dirs(f)
    dirs = root_dir.find_all_dirs_by(lambda x, y: x <= y, 100000)
    return sum(dir.size for dir in dirs)

def problem_2(f: IO):
    root_dir = read_dirs(f)
    total_disk_size = 70000000
    free_space = total_disk_size - root_dir.size
    missing_space_for_update = 30000000 - free_space 
    dirs = root_dir.find_all_dirs_by(lambda x, y: x >= y, missing_space_for_update)
    return min(dirs, key=lambda dir: dir.size).size

def main():
    # input_path = Path("files/day7/test_input.txt")
    input_path = Path("files/day7/input.txt")
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
