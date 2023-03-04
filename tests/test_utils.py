import os


TEST_ROOT = os.path.dirname(__file__)


def create_test_dump():
    test_dump = os.path.join(TEST_ROOT, 'test_dump')
    if not os.path.isdir(test_dump):
        os.mkdir(test_dump)
    return test_dump


