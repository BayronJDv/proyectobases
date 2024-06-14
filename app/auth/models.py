from datetime import datetime
from app import db, bcrypt
from app import login_manager
from flask_login import UserMixin


class Client(db.Model):
    __tablename__ = 'clients'

    cid= db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_adress = db.Column(db.String(200))
    client_email = db.Column(db.String(100))
    client_telephone = db.Column(db.String(20))

    usuarios = db.relationship('User', backref='client', lazy=True)

    @classmethod
    def create_client(cls, name, address, email,telephone):
        client = cls(client_name=name,
                   client_email=email,
                   client_adress=address,
                   client_telephone=telephone
        )
        db.session.add(client)
        db.session.commit()
        return client

class Delivery(db.Model):
    __tablename__ = 'deliverys'

    did= db.Column(db.Integer, primary_key=True, autoincrement=True)
    delivery_name = db.Column(db.String(100), nullable=False)
    delivery_adress = db.Column(db.String(200))
    delivery_email = db.Column(db.String(100))
    delivery_telephone = db.Column(db.String(20))

    usuariosm = db.relationship('Userm', backref='delivery', lazy=True)

    @classmethod
    def create_delivery(cls, name, address, email,telephone):
        delivery = cls(delivery_name=name,
                   delivery_email=email,
                   delivery_adress=address,
                   delivery_telephone=telephone
        )
        db.session.add(delivery)
        db.session.commit()
        return delivery

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True,index=True)
    user_password = db.Column(db.String(80))
    user_adress = db.Column(db.String(200))
    create_date = db.Column(db.DateTime, default=datetime.now)
    cid = db.Column(db.Integer, db.ForeignKey('clients.cid'), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod
    def create_user(cls, user, email, password,address, clientid):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode("utf-8"),
                   user_adress=address,
                   cid=clientid
        )
        db.session.add(user)
        db.session.commit()
        return user

class Userm(UserMixin, db.Model):
    __tablename__ = "usersm"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True,index=True)
    user_password = db.Column(db.String(80))
    user_adress = db.Column(db.String(200))
    create_date = db.Column(db.DateTime, default=datetime.now)
    did = db.Column(db.Integer, db.ForeignKey('deliverys.did'), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod
    def create_userm(cls, user, email, password,address, deliveryid):
        userm = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode("utf-8"),
                   user_adress=address,
                   did=deliveryid
        )
        db.session.add(userm)
        db.session.commit()
        return userm


@login_manager.user_loader
def load_user(user_id):
    # Intenta cargar como Admin primero
    admin = Userm.query.get(int(user_id))
    if admin is not None:
        return admin
    
    # Si no es un Admin, intenta cargar como RegularUser
    user = User.query.get(int(user_id))
    return user
