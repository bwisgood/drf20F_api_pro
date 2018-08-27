class A:
    a = 1
    def __init__(self):
        b = 2

    def __repr__(self):
        return "123"
    def __str__(self):
        return "456"


if __name__ == '__main__':
    a = A()
    print(repr(a))
    print(a.__repr__())
    print(a)