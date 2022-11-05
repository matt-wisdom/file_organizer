"""
    Add delete action.

    To use, simple pass delete as value to action argument

    e.g:
        `fotool.py -l -d tests/__pycache__/ -a delete -e delete`

    Note that you cant reverse the deletion.
    To make it reversible you could move the files
    to trash (or some temp folder) and you'd have
    to extend the reverse method.
"""
import os


class DeleteExtension:
    def action(self, from_, to="", action="print"):
        if action == "delete":
            os.remove(from_)
            return
        self.default_action(from_, to, action)
