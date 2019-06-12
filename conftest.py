import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )
    parser.addoption(
        "--slow-only", action="store_true", default=False, help="only run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-slow"):
        # skip slow tests
        skip_slow = pytest.mark.skip(reason="need --skip-slow option to not run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    if config.getoption("--slow-only"):
        # skip non-slow tests
        skip_fast = pytest.mark.skip(reason="--slow-only option enabled; skipping fast test")
        for item in items:
            if "slow" not in item.keywords:
                item.add_marker(skip_fast)