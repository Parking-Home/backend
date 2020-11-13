from app import db


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)

    def __repr__(self):
        return f"<notifications {self.id}>"
