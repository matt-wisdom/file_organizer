import pathlib

from fotool import extensions, main, organizer

test_exts = ['testextension2:RandomExtension',
             'testextension:Extension',
             'testextension:OtherExtension']

def test_parse_extension():
    ext = extensions.parse_extension("testextension")
    assert issubclass(ext, organizer.DefaultOrganizer)
    assert hasattr(ext, "action")
    assert hasattr(ext, "copy")

    ext = extensions.parse_extension("testextension:Extension")
    assert issubclass(ext, organizer.DefaultOrganizer)
    assert hasattr(ext, "action")
    assert hasattr(ext, "copy")

    ext = extensions.parse_extension("testextension:OtherExtension")
    assert issubclass(ext, organizer.DefaultOrganizer)
    assert hasattr(ext, "action")
    assert hasattr(ext, "copy")

def test_parse_extension_randomname():
    ext = extensions.parse_extension("testextension2")
    assert issubclass(ext, organizer.DefaultOrganizer)

def test_parse_extension_invalid():
    try:
        ext = extensions.parse_extension("doenotexists")
        assert False
    except ModuleNotFoundError:
        pass

    try:
        ext = extensions.parse_extension("testextension2:PExtension")
        assert False
    except Exception:
        pass

def test_install_extension():
    path = pathlib.Path("tests/samples/extensions/test.py")
    extensions.install_extension(path)
    assert pathlib.Path("extensions/test.py").exists()
    pathlib.Path("extensions/test.py").unlink()

def test_install_extension_wrong():
    path = pathlib.Path("tests/samples/extensions/wrong.txt")
    try:
        extensions.install_extension(path)
        assert False
    except ValueError:
        pass
    assert pathlib.Path("extensions/wrong.txt").exists() is False

def test_list_extensions():
    for ext in test_exts:
        assert ext in extensions.list_extensions()

def test_extension_help():
    assert extensions.get_extension_doc("testextension") == "\n    Test\n"