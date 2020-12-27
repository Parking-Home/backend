from app import db


class Intents(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    intent = db.Column(db.String, nullable=False)
    dt = db.Column(db.DateTime, nullable=True)
    place = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<intent{self.user_id}>"
