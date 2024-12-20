class CommentData:
    def __init__(self, username: str, comment: str, date: str):
        self.username = username
        self.comment = comment
        self.date =  date

    def to_dict(self):
        return {
            "username": self.username,
            "comment": self.comment,
            "date": self.date
        }