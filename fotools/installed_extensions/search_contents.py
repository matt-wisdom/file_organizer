"""
    Search allowed files content for search string and print the lines that match
"""

allowed = ["txt", "html", "py", "rb", "pl", "js", "css", "htm", "c", "rtf", "md"]


class Extension:
    def simple_search(self, search, filepath):
        """
            Act on doc files
        """
        try:
            res = self.default_get_file_type(filepath)
        except Exception:
            return False
        if not res:
            return False
        self.extra_attr["search_string"] = search
        if res[0] in allowed:
            return True
        return False

    def action(self, from_, to="", action="print"):
        if action == "print":
            for i, line_str in enumerate(open(from_).readlines()):
                char = line_str.find(self.extra_attr["search_string"])
                if char != -1:
                    print(f"{from_}:{i+1}:{char+1}\n")
            return
        self.default_action(from_, to, action)
