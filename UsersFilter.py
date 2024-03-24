from telegram.ext.filters import MessageFilter

class UsersFilter(MessageFilter):
    data_filter = False

    def __init__(self, user_ids):
        self.user_ids = user_ids

    def filter(self, message):
        print(f"Checking if user {message.from_user.id} is in {self.user_ids}")
        return message.from_user.id in self.user_ids