def test_import():
    import pybotic
    assert pybotic.world.world.test() == "Hello"
    pass
