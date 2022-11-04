"""
    Add delete action.

    To use, simple pass delete as value to action argument

    e.g:
        `fotool.py -l -d tests/__pycache__/ -a delete -e delete`
"""
import os

class DeleteExtension:
    def action(self, from_, to="", action="print"):
        if action == "delete":
            os.remove(from_)
            return
        self.default_action(from_, to, action)