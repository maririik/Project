from namegen import __version__

def test_version():
    # Check that the package has a version attribute
    assert __version__ == "0.1.0"