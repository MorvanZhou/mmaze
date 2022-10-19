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
solutions = m.sovle(start=(0, 0), end=(9, 9))
m.plot(solution=solutions[0])
```

<img src="https://raw.githubusercontent.com/MorvanZhou/mmaze/master/demo.png" alt="drawing" width="300"/>

## Install

```
pip install mmaze
```

## More demo use cases

Demo can be found in test file: [tests](https://github.com/MorvanZhou/mmaze/blob/master/tests/mmaze_test.py)
