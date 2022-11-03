from fotool import main, organizer, organizer

def test_parse_extension():
    ext = main.parse_extension("testextension")
    assert issubclass(ext, organizer.DefaultOrganizer)
    assert hasattr(ext, "action")
    assert hasattr(ext, "copy")
    
    ext = main.parse_extension("testextension:Extension")
    assert issubclass(ext, organizer.DefaultOrganizer)
    assert hasattr(ext, "action")
    assert hasattr(ext, "copy")

def test_parse_extension_invalid():
    ext = main.parse_extension("testextension-Ext")
    assert ext is None
    
    ext = main.parse_extension("testextension_wrong:PExtension")
    assert ext is None

    ext = main.parse_extension("testextension_wrong")
    assert ext is None

def test_do_nothing():
    assert main.donothing() is None

# TODO: Add more tests