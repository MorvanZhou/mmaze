import unittest
import random

import mmaze


class MazeToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.h = random.randint(2, 20)
        self.w = random.randint(2, 20)
        self.m = None

    def tearDown(self) -> None:
        self.assertEqual(self.h * 2 + 1, len(self.m.data))
        [self.assertEqual(self.w * 2 + 1, len(self.m.data[i])) for i in range(self.h)]

    def test_generate(self):
        self.m = mmaze.generate(width=self.w, height=self.h, method="BinaryTree")
        print(self.m)

        with self.assertRaises(ValueError):
            mmaze.generate(width=5, height=5, method="sss")

    def test_save(self):
        self.m = mmaze.generate(width=self.w, height=self.h, method="prims")
        self.m.save("save.png")

    def test_plot(self):
        self.m = mmaze.generate(width=self.w, height=self.h, method="prims")
        self.m.plot()

    def test_binary_tree(self):
        g = mmaze.generator.BinaryTree()
        self.m = g.generate(self.w, self.h)

    def test_backtracking(self):
        g = mmaze.generator.Backtracking()
        self.m = g.generate(self.w, self.h)

    def test_ellers(self):
        g = mmaze.generator.Ellers()
        self.m = g.generate(self.w, self.h)

    def test_growing_tree(self):
        g = mmaze.generator.GrowingTree()
        self.m = g.generate(self.w, self.h)

    def test_hunt_and_kill(self):
        g = mmaze.generator.HuntAndKill()
        self.m = g.generate(self.w, self.h)

    def test_kruskal(self):
        g = mmaze.generator.Kruskal()
        self.m = g.generate(self.w, self.h)

    def test_prims(self):
        g = mmaze.generator.Prims()
        self.m = g.generate(self.w, self.h)

    def test_division(self):
        g = mmaze.generator.Division()
        self.m = g.generate(self.w, self.h)

    def test_wilsons(self):
        g = mmaze.generator.Wilsons()
        self.m = g.generate(self.w, self.h)


class SolverTest(unittest.TestCase):
    def test_backtracking_solver(self):
        g = mmaze.generator.Prims()
        m = g.generate(10, 10)
        s = mmaze.solver.Backtracking()
        start = (0, 0)
        end = (9, 9)
        solutions = s.solve(m, start, end)

        self.assertGreater(len(solutions), 0)
        self.assertGreater(len(solutions[0]), 0)
        m.plot(start, end, solutions[0])

    def test_solve_from_maze(self):
        g = mmaze.generator.Prims()
        m = g.generate(10, 10)
        start = (0, 0)
        end = (9, 9)
        solutions = m.solve(start, end)

        self.assertGreater(len(solutions), 0)
        self.assertGreater(len(solutions[0]), 0)
        m.save("demo.png", start=start, end=end, solution=solutions[0])

    def test_solve_print(self):
        g = mmaze.generator.Prims()
        m = g.generate(3, 3)
        print(m)
        start = (0, 0)
        end = (2, 2)
        solutions = m.solve(start, end)
        print(m.to_number())

        self.assertGreater(len(solutions), 0)
        self.assertGreater(len(solutions[0]), 0)
        print(m.tostring(start=start, end=end, solution=solutions[0]))

    def test_print_number(self):
        g = mmaze.generator.Prims()
        m = g.generate(3, 3)
        start = (0, 0)
        end = (2, 2)
        solutions = m.solve(start, end)
        print(m.to_number(start, end, solutions[0]))
