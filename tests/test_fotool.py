# import subprocess
# import os

# def compare(res: str, expected: list):
#     expected = [set(i.split("\n")) for i in expected]
#     res = set(res.split("\n"))
#     return res in expected

# def test_list():
#     expected = [
#         "/requirements.txt\n/fotool.py\n/LICENSE\n/pyproject.toml\n/action_log\n/.gitignore\n/README.md\n",
#         "/requirements.txt\n/fotool.py\n/LICENSE\n/pyproject.toml\n/.gitignore\n/README.md\n"
#         ]
#     res = subprocess.check_output(["py", "fotool.py"]).decode()

#     assert compare(res.replace(os.getcwd(), ""), expected)

# def test_dir():
#     expected = [
#         "/1.txt\n/2.txt\n/3.txt\n",
#         ]
#     path = "tests/samples"
#     res = subprocess.check_output(["py", "fotool.py", "-d", "tests/samples"]).decode()
#     assert compare(res.replace(os.path.join(os.getcwd(), "tests/samples"), ""), expected)
