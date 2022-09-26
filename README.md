# MMaze

A simple python maze generator and solver.


## Simple usage

Generating a maze with specific width and height. Print on screen directly.

```python
import mmaze

m = mmaze.generate(width=3, height=3)
print(m)

"""
#######
# #   #
# ### #
#     #
# #####
#     #
#######
"""
```

Plot the maze to image.

```python
m = mmaze.generate(width=3, height=3)
m.plot()
```

Get solution and plot on screen:

```python
m = mmaze.generate(width=10, height=10)
solutions = m.sovle(start=(0, 0), end=(9, 9))
m.plot(solution=solutions[0])
```



## Demo
Demo can be found in test file: [tests](https://github.com/MorvanZhou/tests/mmaze_test.py)

## Install

```
pip install mmaze
```

## Download or fork
Download [link](https://github.com/MorvanZhou/mmaze/archive/master.zip)

Fork this repo:
```
$ git clone https://github.com/MorvanZhou/mmaze.git
```

## Results
![img](https://raw.githubusercontent.com/MorvanZhou/mmaze/master/demo.png)
