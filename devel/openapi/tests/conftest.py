
# from fixtures import spec_from_file

# https://pytest-with-eric.com

def pytest_addoption(parser):
    parser.addoption("--yaml", action="store_true", default=False)


# def pytest_generate_tests(metafunc):
#     # This is called for every test. Only get/set command line arguments
#     # if the argument is specified in the list of test "fixturenames".
#     option_value = metafunc.config.option.yaml
#     if option_value and 'spec' in metafunc.fixturenames:
#         print(dir(metafunc.config.option))
#         _spec = spec_from_file.__wrapped__() #"openapi.yml")
#         metafunc.parametrize("spec", [_spec], ids=["yaml-from-file"])

def pytest_generate_tests(metafunc):
    print("\nmetafunc:")
    for k, v in metafunc.__dict__.items():
        if k.startswith("__"): continue
        print(f"    {k.ljust(20)}{v}")
