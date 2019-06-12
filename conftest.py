import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    print(config.getoption("--skip-slow"))
    if not config.getoption("--skip-slow"):
        # --runslow given in cli: skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --skip-slow option to not run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
