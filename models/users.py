from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def jsonify(self):
        return {'username': self.username, 'password': self.password}
    
    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
    
    def find_by_username(username):
        return UserModel.query.filter_by(username=username).first()

    def find_by_id(id):
        return UserModel.query.filter_by(id=id).first()
