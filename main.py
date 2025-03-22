import sys
from itertools import product
from typing import List, Tuple

from dend import Tridend

u = Tridend.unit()

y = Tridend.vee(u, u)
w = Tridend.vee(u, u, u)
ly = Tridend.vee(u, y)
yl = Tridend.vee(y, u)
lyl = Tridend.vee(u, y, u)
wl = Tridend.vee(w, u)


def gen_compositions(k: int) -> List[Tuple[int, ...]]:
    if k == 0:
        return [()]

    compositions = []
    for i in range(1, k + 1):
        for rest in gen_compositions(k - i):
            compositions.append((i,) + rest)

    return compositions


def gen_trees(n: int) -> List[List["Tridend"]]:
    trees = [[Tridend.unit()]]
    for k in range(1, n + 1):
        trees.append([])
        for comp in gen_compositions(k + 1):
            if len(comp) == 1:
                continue
            for tup in product(*[trees[c - 1] for c in comp]):
                trees[k].append(Tridend.vee(*tup))

    return trees


@Tridend.linear_map
def sh2(b):
    x, y = b
    x1, y1 = x
    x2, y2 = y

    return (Tridend.to_vec(x1) @ Tridend.to_vec(x2)).outer(
        Tridend.to_vec(y1) @ Tridend.to_vec(y2)
    )


@Tridend.linear_map
def qsh2(b):
    x, y = b
    x1, y1 = x
    x2, y2 = y

    return (Tridend.to_vec(x1) * Tridend.to_vec(x2)).outer(
        Tridend.to_vec(y1) * Tridend.to_vec(y2)
    )


if __name__ == "__main__":
    from tqdm import tqdm

    N = 5
    print("Generating all Schröder trees up to degree", N)
    all_trees = gen_trees(N)
    for d, trees in enumerate(all_trees):
        print(f"degree {d}:")  # , ', '.join([str(tree) for tree in trees]))
        print(f"\ttotal = {len(trees)}")

    flat_trees = [t for level in all_trees[1:] for t in level]
    # print("Checking bialgebra property for quasi-shuffle...")
    # for s, t in tqdm(product(flat_trees, flat_trees), total=len(flat_trees) ** 2):
    #     prod = s * t
    #     delta_prod = prod.coprod_qsh()
    #
    #     delta_s = s.coprod_qsh()
    #     delta_t = t.coprod_qsh()
    #     prod_delta = qsh2(delta_s.outer(delta_t))
    #
    #     try:
    #         assert delta_prod == prod_delta
    #     except AssertionError:
    #         print(f"*-Bialgebra check failed for\ns = {s}\nt = {t}")
    #         print("Δs =", delta_s)
    #         print("Δt =", delta_t)
    #         print("s * t =", prod)
    #         for term in prod.keys():
    #             print("\tu =", term)
    #             print("\tΔu =", Tridend.to_vec(term).coprod_sh())
    #         print("Δ(s * t) =", delta_prod)
    #         print("Δs * Δt =", prod_delta)
    #         sys.exit(1)
    #
    # print("Done!")
    # print("Checking bialgebra property for shuffle...")

    for s, t in tqdm(product(flat_trees, flat_trees), total=len(flat_trees) ** 2):
        prod = s @ t
        delta_prod = prod.coprod_sh()

        delta_s = s.coprod_sh()
        delta_t = t.coprod_sh()
        prod_delta = sh2(delta_s.outer(delta_t))

        try:
            assert delta_prod == prod_delta
        except AssertionError:
            print(f"ш-Bialgebra check failed for\ns = {s}\nt = {t}")
            print("Δs =", delta_s)
            print("Δt =", delta_t)
            print("s ш t =", prod)
            for term in prod.keys():
                print("\tu =", term)
                print("\tΔu =", Tridend.to_vec(term).coprod_sh())
            print("Δ(s ш t) =", delta_prod)
            print("Δs ш Δt =", prod_delta)
            sys.exit(1)

    print("Done!")
