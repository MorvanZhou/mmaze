import json
import argparse

from mmaze import generate

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output path")
parser.add_argument("--symmetry", default="n", help="symmetry way, support h, v, b, n")
parser.add_argument(
    "-m", "--method", default="backtracking",
    help="method: backtracking, binarytree, division, ellers, growingtree, huntandkill, kruskal, prims, wilsons")
parser.add_argument("-s", "--size", default="5x5", help="maze size, height x width, default to 5x5")

args = parser.parse_args()

if __package__ == "mmaze" and __name__ == "__main__":
    hw = args.size
    symmetry = args.symmetry
    method = args.method
    h, w = hw.split("x", 1)
    h = int(h)
    w = int(w)
    m = generate(w, h, symmetry=symmetry, method=method)
    if args.output is not None:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(m.to_number(), f)
    else:
        print(m)
