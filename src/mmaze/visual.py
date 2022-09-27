import os
import typing

from mmaze.cell import CellType

if typing.TYPE_CHECKING:
    from mmaze.maze import Maze

plt = None
cm = None
mpl = None


def _try_import_plt():
    try:
        import matplotlib
    except ModuleNotFoundError:
        import subprocess
        import sys
        print("Dependency not found, try installing matplotlib==3.5.0")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib==3.5.0"])

    finally:
        global plt, cm, mpl
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        from matplotlib import cm


def _plot(maze: "Maze", solution: list = None):
    plt.figure(figsize=(5, 5))

    img = []
    for row in maze.data:
        img_row = []
        for cell in row:
            if cell == CellType.ROAD:  # road
                v = (1., 1., 1.)  # white
            elif cell == CellType.WALL:  # wall
                v = (0., 0., 0.)  # black
            else:
                v = (0.6, 0.6, 0.6)
            img_row.append(v)
        img.append(img_row)
    if solution is not None and len(solution) > 2:
        sol = solution[1: -1]
        cmap = plt.get_cmap("cool")
        len_s = len(sol)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap)

        for i, p in enumerate(sol):
            img[p[0]][p[1]] = scalar_map.to_rgba(i / len_s)[:3]
        plt.text(solution[0][0], solution[0][1], "S", c="#09479A", fontweight="heavy", ha="center", va="center")
        plt.text(solution[-1][0], solution[-1][1], "E", c="#09479A", fontweight="heavy", ha="center", va="center")
    plt.imshow(img, interpolation='nearest')
    plt.xticks([]), plt.yticks([])


def plot(maze: "Maze", solution: list = None):
    _try_import_plt()
    _plot(maze, solution)
    plt.show()
    plt.clf()


def save(path: str, maze: "Maze", solution: list = None):
    _try_import_plt()
    _plot(maze, solution)
    _dir = os.path.dirname(path)
    if _dir != "":
        os.makedirs(_dir, exist_ok=True)
    plt.savefig(path, bbox_inches='tight')
    plt.clf()
