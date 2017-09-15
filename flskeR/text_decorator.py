
def rookie():
    def decorator(f):
        print(0000)
        print("enter ..")
        print(f)
        print("out")
        return f
    return decorator


@rookie()
def f():
    print("FFFFFFF")
    return
print(__file__)
print(__name__)