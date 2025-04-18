
def pytest_addoption(parser):
    parser.addoption("--yaml", action="store_true", default=False)
    parser.addoption("--slice")
    parser.addoption("--url")
    parser.addoption("--log-path")

# https://pytest-with-eric.com
