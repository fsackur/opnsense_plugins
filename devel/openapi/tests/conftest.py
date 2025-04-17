
def pytest_addoption(parser):
    parser.addoption("--yaml", action="store_true", default=False)
    parser.addoption("--slice")
    parser.addoption("--url")


# https://pytest-with-eric.com
