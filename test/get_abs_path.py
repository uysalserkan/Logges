import inspect
import os


def abs_path():
    abs_path = os.path.abspath((inspect.stack()[0])[1])
    directory_of_1py = os.path.dirname(abs_path)
    return directory_of_1py


def abs_path_2(filename=__file__):
    return os.path.abspath(filename)


# if __name__ == '__main__':
#     print(abs_path())
