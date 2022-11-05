"""
    Upload matching files to pcloud.

    Requires pycloud to be installed.

    `pip install pcloud`
"""
import os

from pcloud import PyCloud


class PcloudUploadExtension:
    def action(self, from_, to="", action="print"):
        pc = PyCloud(os.getenv("PCLOUD_USER"), os.getenv("PCLOUD_PASS"))
        if action == "upload":
            pc.uploadfile(files=[from_])
        self.default_action(from_, to, action)
