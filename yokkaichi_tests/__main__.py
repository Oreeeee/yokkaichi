import sys

try:
    import pytest
except ImportError:
    print("Install yokkaichi[testing] to run tests!")
    sys.exit(1)


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv"]))
