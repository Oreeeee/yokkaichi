import sys

try:
    import pytest
except ImportError:
    print("Install yokkaichi[testing] to run tests!")
    sys.exit(1)


def main():
    sys.exit(pytest.main(["-vv"]))


if __name__ == "__main__":
    main()
