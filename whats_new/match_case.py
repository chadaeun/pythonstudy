def match_point(point):
    x = 1
    y = 2

    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y={y}")
        case (x, 0):
            print(f"X={x}")
        case (x, y):
            print(f"X={x}, Y={y}")
        case _:
            raise ValueError("Not a point")

match_point((0, 1))


a = 2
b = 5

match a:
    case b:
        print(a, b)

print(a, b)