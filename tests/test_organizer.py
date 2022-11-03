from logging import exception
import shutil
import pytest
import io
import marshal
import os
from fotool import organizer

sep = os.path.sep
samples_base = f"tests{sep}samples"
samples_files = [
    os.path.join(samples_base, "vid.mp4"),
    os.path.join(samples_base, "img.png"),
    os.path.join(samples_base, "1.txt"),
]
samples_types = [("mp4", "MP4 Files"), ("png", "PNG Files"), ("txt", "Text File")]
samples_files_type = dict(zip(samples_files, samples_types))
samples_files_groups = dict(
    zip(samples_files, [f".{sep}Video", f".{sep}Images", f".{sep}Documents"])
)
gen_new = [
    "A",
    "B",
    "N",
    "A",
    "S",
    "J",
    "S",
    "S",
    "AA",
    "AB",
    "AN",
    "AA",
    "AS",
    "AJ",
    "AS",
    "AS",
    "BB",
    "BN",
    "BA",
    "BS",
    "BJ",
]


def test_default_write_action_log():
    log = {"Random": "Data"}
    org = organizer.DefaultOrganizer(reversible=True)
    org.action_log_obj = io.BytesIO()
    org.action_logs = log
    assert org.default_write_action_log() == True
    org.action_log_obj.seek(0)
    assert log == marshal.loads(org.action_log_obj.read())

    org = organizer.DefaultOrganizer(reversible=False)
    org.action_log_obj = io.BytesIO()
    org.action_logs = log
    assert org.default_write_action_log() == False
    org.action_log_obj.seek(0)
    try:
        marshal.loads(org.action_log_obj.read())
    except EOFError:
        assert True
        return
    assert False


def test_default_add_to_log():
    org = organizer.DefaultOrganizer(reversible=True)
    data = ["write", "old", "new"]
    org.action_logs = {}
    org.default_add_to_log(*data)
    key = list(org.action_logs.keys())[0]
    assert org.action_logs[key] == [data[0], os.path.abspath(data[1]), data[2]]

    org = organizer.DefaultOrganizer(reversible=True)
    from_ = os.path.abspath(os.path.join(samples_base, "img.png"))
    org.default_add_to_log("print", from_, samples_base)
    key = list(org.action_logs.keys())[0]
    assert org.action_logs[key] == ["print", from_, from_]


@pytest.mark.parametrize("file", samples_files)
def test_default_get_file_type(file):
    org = organizer.DefaultOrganizer(reversible=True)
    type = org.default_get_file_type(file)
    assert samples_files_type[file] == type


def test_default_get_file_type_many():
    org = organizer.DefaultOrganizer(reversible=True)
    type = org.default_get_file_type(samples_files)
    assert type == [("mp4", "video/mp4"), ("png", "image/png"), ("txt", "Text File")]


def test_default_gen_new_names():
    org = organizer.DefaultOrganizer(reversible=True)
    org.action_logs = {}
    out = []
    i = 0
    for j in org.default_gen_new_names("ABNASJSS"):
        out.append(j)
        if i == 20:
            break
        i += 1
    assert out == gen_new


def test_default_gen_new_name_combination():
    org = organizer.DefaultOrganizer(reversible=True)
    for i in range(5):
        assert org.default_gen_new_name_combination("example.pdf") == f"{i}.pdf"


@pytest.mark.parametrize(
    ["filename", "regexp", "expected"],
    [
        [
            "sitemoviez.com-foobar-S01-E01.mp4",
            "(?<=viez.com-)(.*)",
            "foobar-S01-E01.mp4",
        ],
        ["randomfile_websiteA.pdf", "(.*)(?=_websiteA)", "randomfile.pdf"],
        [
            "prefixA_randomfile_websiteA.pdf",
            "(?<=prefixA_)(.*)(?=_websiteA)",
            "randomfile.pdf",
        ],
    ],
)
def test_default_gen_new_name_regex(filename, regexp, expected):
    org = organizer.DefaultOrganizer(reversible=True)
    assert org.default_gen_new_name_regex(filename, regexp) == expected

    org = organizer.DefaultOrganizer(reversible=True, case_sensitive=True)
    assert org.default_gen_new_name_regex(filename, regexp) == expected


@pytest.mark.parametrize("file", samples_files)
def test_default_generate_destination_group(file):
    org = organizer.DefaultOrganizer(reversible=True)
    assert samples_files_groups[file] == org.default_generate_destination_group(file)


@pytest.mark.parametrize(
    "file", samples_files + [os.path.join(samples_base, "action_log")]
)
def test_default_generate_destination_group_nomatch(file):
    org = organizer.DefaultOrganizer(reversible=True)
    nomatchdir = "nomatch"
    assert samples_files_groups.get(
        file, nomatchdir
    ) == org.default_generate_destination_group(file, nomatchdir=nomatchdir)


@pytest.mark.parametrize(
    "file", samples_files + [os.path.join(samples_base, "action_log")]
)
def test_default_generate_destination_group_nomatch_dd(file):
    org = organizer.DefaultOrganizer(reversible=True)
    nomatchdir = os.path.join("[:dd:]", "nomatch")
    assert f"{sep}home" + samples_files_groups.get(file, f"{sep}nomatch").replace(
        ".", ""
    ) == org.default_generate_destination_group(
        file, f"{sep}home", nomatchdir=nomatchdir
    )


def test_default_copy():
    org = organizer.DefaultOrganizer(reversible=True)
    to = os.path.join(samples_base, "4.txt")
    from_ = os.path.join(samples_base, "1.txt")
    assert org.default_copy(from_, to) == to
    assert os.path.exists(to) and os.path.exists(from_)

    assert org.default_copy(to, from_, move=True) == -1
    assert org.default_copy(to, from_, move=True, overwrite=True) == from_
    assert os.path.exists(to) is False

    assert org.default_copy(from_, samples_base, move=True, overwrite=True) == from_
    try:
        assert org.default_copy("~/does-not-exist", ".", overwrite=True) == -1
        assert (
            org.default_copy("~/does-not-exist", ".", move=True, overwrite=True) == -1
        )
    except FileNotFoundError:
        pass


def test_default_rename():
    org = organizer.DefaultOrganizer(reversible=True)
    to = os.path.join(samples_base, "rename2.txt")
    from_ = os.path.join(samples_base, "rename.txt")
    assert org.default_rename(from_, to) == to
    assert org.default_rename(to, from_, copy=True) == from_
    assert os.path.exists(to) and os.path.exists(from_)

    assert org.default_rename(to, from_) == -1
    assert org.default_rename(to, from_, overwrite=True) == from_

    try:
        org.default_rename("~/Doentt", ".", overwrite=True, copy=True)
        assert False
    except AssertionError:
        assert False
    except Exception as e:
        pass


fuzzy_expected = {"filerandom": True, "filer": False, "": True}


@pytest.mark.parametrize(
    ["search", "string"],
    [["filerandom", "file_random.jpg"], ["filer", "pureos.iso"], ["", "file"]],
)
def test_default_fuzzysearch(search, string):
    org = organizer.DefaultOrganizer(reversible=True)
    assert org.default_fuzzy_search(search, string) is fuzzy_expected[search]


simple_expected = {"filerandom": False, "pure": True, "": True}


@pytest.mark.parametrize(
    ["search", "string"],
    [["filerandom", "file_random.jpg"], ["pure", "pureos.iso"], ["", "dd"]],
)
def test_default_simplesearch(search, string):
    org = organizer.DefaultOrganizer(reversible=True)
    assert org.default_simple_search(search, string) is simple_expected[search]


simple_expected_case = {"file": True, "Pure": False, "": True}


@pytest.mark.parametrize(
    ["search", "string"],
    [["file", "file_random.jpg"], ["Pure", "pureos.iso"], ["", "dd"]],
)
def test_default_simplesearch_case(search, string):
    org = organizer.DefaultOrganizer(reversible=True, case_sensitive=True)
    assert org.default_simple_search(search, string) is simple_expected_case[search]


def test_default_walk_dir():
    org = organizer.DefaultOrganizer(reversible=True)
    path = os.path.join(samples_base, "walk")
    assert set(org.default_walk_dir(path)) == {
        f"tests{sep}samples{sep}walk{sep}1.txt",
        f"tests{sep}samples{sep}walk{sep}vid.mp4",
        f"tests{sep}samples{sep}walk{sep}rename.txt",
        f"tests{sep}samples{sep}walk{sep}3.txt",
        f"tests{sep}samples{sep}walk{sep}action_log",
        f"tests{sep}samples{sep}walk{sep}2.txt",
        f"tests{sep}samples{sep}walk{sep}img.png",
    }

    assert set(org.default_walk_dir(path, extensions=["png"])) == {
        f"tests{sep}samples{sep}walk{sep}img.png",
    }


def test_default_walk_dir_recursive():
    org = organizer.DefaultOrganizer(reversible=True)
    path = os.path.join(samples_base, "inner")
    assert (
        len(
            set((org.default_walk_dir_recursive(path))).difference(
                {
                    f"tests{sep}samples{sep}inner{sep}in_inner{sep}ty.txt",
                    f"tests{sep}samples{sep}inner{sep}in_inner{sep}img.png",
                    f"tests{sep}samples{sep}inner{sep}innerfile.txt",
                }
            )
        )
        == 0
    )

    assert (
        len(
            set((org.default_walk_dir_recursive(path, "txt"))).difference(
                {
                    f"tests{sep}samples{sep}inner{sep}in_inner{sep}ty.txt",
                    f"tests{sep}samples{sep}inner{sep}innerfile.txt",
                }
            )
        )
        == 0
    )


@pytest.mark.parametrize(
    "file", ["python.exe", "amazing.file", "whatever", "5.py", "."]
)
def test_default_generate_destination_alphabetic(file):
    expected = {
        "python.exe": "./p-t",
        "amazing.file": "./a-e",
        "whatever": "./u-y",
        "5.py": "./0-9",
        ".": "hello",
    }
    org = organizer.DefaultOrganizer(reversible=True)
    assert (
        org.default_generate_destination_alphabetic(file, nomatchpath="hello")
        == expected[file]
    )


def test_default_generate_destination_alphabetic_sepnum():
    org = organizer.DefaultOrganizer(reversible=True)
    assert org.default_generate_destination_alphabetic("5.py", sep_nums=True) == "./5-0"

def test_default_generate_destination_type():
    org = organizer.DefaultOrganizer(reversible=True)
    assert org.default_generate_destination_type(samples_files[0]) == "./MP4 Files"

def test_default_generate_groups():
    org = organizer.DefaultOrganizer(reversible=True)
    org.groups = ["5"]
    assert org.default_generate_groups(4, True) is None
    assert org.groups == ["5"]

def create_action_files(count):
    base = os.path.join(samples_base, "actions")
    shutil.rmtree(base)
    os.mkdir(base)
    paths = []
    for i in range(count):
        path = os.path.join(base, f"{i}.txt")
        with open(path, "w") as f:
            f.write("Whatever")
        paths.append(path)
    return paths

def test_default_action_copy():
    base = os.path.join(samples_base, "actions")
    org = organizer.DefaultOrganizer(reversible=True)
    paths = create_action_files(1)
    target = os.path.join(base, "hmm.txt")
    res = org.default_action(paths[0], target, "copy")
    assert res == target
    assert os.path.isfile(res) and os.path.isfile(paths[0])

def test_default_action_rename():
    base = os.path.join(samples_base, "actions")
    org = organizer.DefaultOrganizer(reversible=True)
    paths = create_action_files(1)
    target = os.path.join(base, "hmm.txt")
    res = org.default_action(paths[0], target, "rename")
    assert res == target
    assert os.path.isfile(res) and not os.path.isfile(paths[0])

def test_default_action_copy_rename():
    base = os.path.join(samples_base, "actions")
    org = organizer.DefaultOrganizer(reversible=True)
    paths = create_action_files(1)
    target = os.path.join(base, "hmm.txt")
    res = org.default_action(paths[0], target, "copy_rename")
    assert res == target
    assert os.path.isfile(res) and os.path.isfile(paths[0])

def test_default_action_move():
    base = os.path.join(samples_base, "actions")
    org = organizer.DefaultOrganizer(reversible=True)
    paths = create_action_files(1)
    target = os.path.join(base, "hmm.txt")
    res = org.default_action(paths[0], target, "move")
    assert res == target
    assert os.path.isfile(res) and not os.path.isfile(paths[0])

def test_default_action_print():
    base = os.path.join(samples_base, "actions")
    org = organizer.DefaultOrganizer(reversible=True)
    paths = create_action_files(1)
    _ = org.default_action(paths[0], "", "print")
    assert os.path.isfile(paths[0])

    target = os.path.join(base, "hmm.txt")
    _ = org.default_action(paths[0], target, "print")
    assert os.path.isfile(paths[0])

    org = organizer.DefaultOrganizer(reversible=True, newline=True)
    _ = org.default_action(paths[0], target, "print")
    assert os.path.isfile(paths[0])

def test_default_action_invalid():
    org = organizer.DefaultOrganizer(reversible=True)
    paths = create_action_files(1)
    try:
        _ = org.default_action(paths[0], "", "ok")
        assert False
    except:
        pass
    assert os.path.isfile(paths[0])

def test_default_reverse_no_actionfile():
    try:
        org = organizer.DefaultOrganizer(reversible=True, reverse=True, action_log="nofileexists")
        assert False
    except FileNotFoundError:
        pass

# def test_default_reverse():
#     org = organizer.DefaultOrganizer(reversible=True)
#     org.default_copy()