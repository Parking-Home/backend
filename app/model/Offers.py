from app import db


class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<offers {self.id}>"
