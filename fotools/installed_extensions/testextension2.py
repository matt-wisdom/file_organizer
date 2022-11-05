from fotools.organizer import DefaultOrganizer


class RandomExtension(DefaultOrganizer):
    def copy(self, from_, to, move=False, overwrite=False):
        return super().default_copy(from_, to, move, overwrite)

    def action(self, from_, to="", action="print"):
        print("WWW")
        return super().default_action(from_, to, action)
