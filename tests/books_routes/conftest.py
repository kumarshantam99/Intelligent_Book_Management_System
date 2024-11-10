import pytest

def pytest_configure(config):
    # Get the existing ini values or create new list if none exist
    values = getattr(config.option, "asyncio_default_fixture_loop_scope", [])
    if not isinstance(values, list):
        values = []
    
    # Add our value to the list
    values.append("function")
    
    # Set the values back
    setattr(config.option, "asyncio_default_fixture_loop_scope", values)

# Mark all tests in this directory as asyncio
pytest_plugins = ["pytest_asyncio"]

# Fixtures that will be shared across test files
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    