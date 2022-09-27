import os
import typing as tp

from mmaze.cell import CellType

if tp.TYPE_CHECKING:
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


def _plot(
        maze: "Maze",
        start: tp.Optional[tp.Sequence[int]] = None,
        end: tp.Optional[tp.Sequence[int]] = None,
        solution: tp.Optional[tp.Sequence[tp.Sequence]] = None,
):
    plt.figure(figsize=((maze.width - 1) / 2, (maze.height - 1) / 2))

    img = []
    for row in maze.data:
        img_row = []
        for cell in row:
            if cell == CellType.ROAD:
                v = (1., 1., 1.)
            elif cell == CellType.WALL:
                v = (60 / 255, 60 / 255, 60 / 255)
            else:
                v = (0.6, 0.6, 0.6)
            img_row.append(v)
        img.append(img_row)
    if solution is not None:
        cmap = plt.get_cmap("cool")
        len_s = len(solution)
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap)

        for i, p in enumerate(solution):
            img[p[0]][p[1]] = scalar_map.to_rgba(i / len_s)[:3]
    if start is not None:
        p = [p * 2 + 1 for p in start]
        plt.text(
            p[0], p[1], "S",
            size=min(maze.width, maze.height),
            c="#09479A", fontweight="heavy",
            ha="center", va="center")
    if end is not None:
        p = [p * 2 + 1 for p in end]
        plt.text(
            p[0], p[1], "E",
            size=min(maze.width, maze.height),
            c="#09479A", fontweight="heavy",
            ha="center", va="center")

    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    plt.tight_layout()


def plot(
        maze: "Maze",
        start: tp.Optional[tp.Sequence[int]] = None,
        end: tp.Optional[tp.Sequence[int]] = None,
        solution: tp.Optional[tp.Sequence[tp.Sequence]] = None,
):
    _try_import_plt()
    plt.clf()
    _plot(maze, start, end, solution)
    plt.show()


def save(
        path: str,
        maze: "Maze",
        start: tp.Optional[tp.Sequence[int]] = None,
        end: tp.Optional[tp.Sequence[int]] = None,
        solution: tp.Optional[tp.Sequence[tp.Sequence]] = None,
):
    _try_import_plt()
    plt.clf()
    _plot(maze, start, end, solution)
    _dir = os.path.dirname(path)
    if _dir != "":
        os.makedirs(_dir, exist_ok=True)
    plt.savefig(path, bbox_inches='tight')
