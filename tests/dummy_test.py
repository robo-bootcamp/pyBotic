def test_import():
    import pybot
    assert pybot.world.world.test() == "Hello"
    pass
