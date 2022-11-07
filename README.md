# MMaze

A python maze generator and solver.

## Usage

Generating a maze with specific width and height. Print on screen directly.

```python
import mmaze

m = mmaze.generate(width=3, height=3)
print(m)

"""
■■■■■■■
■ ■   ■
■ ■ ■■■
■     ■
■■■ ■■■
■     ■
■■■■■■■
"""
```

Plot the maze to image.

```python
m = mmaze.generate(width=3, height=3)
m.plot()
```

<img src="https://raw.githubusercontent.com/MorvanZhou/mmaze/master/demo33.png" alt="drawing" width="180"/>

Get solution and plot on screen:

```python
m = mmaze.generate(width=3, height=3)
solutions = m.solve(start=(0, 0), end=(2, 2))
print(m.tostring(solution=solutions[0]))

"""
■■■■■■■
■S■   ■
■*■ ■■■
■***  ■
■■■*■■■
■  **E■
■■■■■■■
"""
```

Generate a solution and plot to an image.

```python
m = mmaze.generate(width=10, height=10)
solutions = m.solve(start=(0, 0), end=(9, 9))
m.plot(solution=solutions[0])
```

<img src="https://raw.githubusercontent.com/MorvanZhou/mmaze/master/demo.png" alt="drawing" width="300"/>

To make a symmetric maze by passing a symmetry method. Note that width or height must be odd number when you want to
solve the generated maze.

In this repo, only backtracking / growingtree / huntandkill / prims algorithms can generate symmetric maze.

```python
start = (0, 0)
end = (10, 10)
m = mmaze.generate(width=11, height=11, symmetry="horizontal")
solutions = m.solve(start=start, end=end)
m.plot(solution=solutions[0], start=start, end=end)
```

<img src="https://raw.githubusercontent.com/MorvanZhou/mmaze/master/demo_symmetry.png" alt="drawing" width="300"/>

## Install

```
pip install mmaze
```

## More demo use cases

Demo can be found in test file: [tests](https://github.com/MorvanZhou/mmaze/blob/master/tests/mmaze_test.py)
