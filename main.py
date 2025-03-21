from dend import Tridend, STree

u = Tridend.unit()

y = Tridend.vee(u, u)
w = Tridend.vee(u, u, u)
ly = Tridend.vee(u, y)
yl = Tridend.vee(y, u)


if __name__ == "__main__":
    print(f"Shuffle: {y} ш {y} = {y@y}")
    print(f"QShuffle: {y} * {y} = {y*y}")
