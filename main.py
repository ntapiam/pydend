from dend import Tridend

u = Tridend.unit()

y = Tridend.vee(u, u)
w = Tridend.vee(u, u, u)
ly = Tridend.vee(u, y)
yl = Tridend.vee(y, u)
lyl = Tridend.vee(u, y, u)


if __name__ == "__main__":
    print("Products:")
    print(f"\tShuffle: {y} ш {y} = {y@y}")
    print(f"\tQShuffle: {y} * {y} = {y*y}")

    print("Coproducts:")
    print(f"\tShuffle: Δ{lyl} = {lyl.coprod_sh()}")
    print(f"\tQShuffle: Δ{lyl} = {lyl.coprod_qsh()}")
