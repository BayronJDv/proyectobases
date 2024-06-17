from datetime import datetime
from app import db, bcrypt
from app import login_manager
from flask_login import UserMixin
from sqlalchemy import *
import enum

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

user_id_seq = Sequence('users_id_seq', start=1, increment=1)
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, user_id_seq, server_default=user_id_seq.next_value(), primary_key=True)

    user_name = db.Column(db.String(50))
    user_email = db.Column(db.String(60), unique=True,index=True)
    user_password = db.Column(db.String(80))
    user_adress = db.Column(db.String(200))
    create_date = db.Column(db.DateTime, default=datetime.now)
    cid = db.Column(db.Integer, db.ForeignKey('clients.cid'), nullable=False)
    
    servicios = db.relationship('Service', backref='User', lazy=True)
    role = db.Column(db.String(20), default='user')

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
    
    @classmethod
    def create_admin(cls, user, email, password,address, clientid):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode("utf-8"),
                   user_adress=address,
                   cid=clientid,
                   role='admin'
        )
        db.session.add(user)
        db.session.commit()
        return user

userm_id_seq = Sequence('usersm_id_seq', start=1000000, increment=1)
class Userm(UserMixin, db.Model):
    __tablename__ = "usersm"

    id = db.Column(db.Integer, userm_id_seq, server_default=userm_id_seq.next_value(), primary_key=True)
    userm_name = db.Column(db.String(50))
    userm_email = db.Column(db.String(60), unique=True,index=True)
    userm_password = db.Column(db.String(80))
    userm_adress = db.Column(db.String(200))
    create_date = db.Column(db.DateTime, default=datetime.now)
    did = db.Column(db.Integer, db.ForeignKey('deliverys.did'), nullable=False)
    servicios = db.relationship('Service', backref='Userm', lazy=True)
    role = db.Column(db.String(20), default='userm')

    def checkm_password(self, password):
        return bcrypt.check_password_hash(self.userm_password, password)
    
    @classmethod
    def create_userm(cls, user, email, password,address, deliveryid):
        userm = cls(userm_name=user,
                   userm_email=email,
                   userm_password=bcrypt.generate_password_hash(password).decode("utf-8"),
                   userm_adress=address,
                   did=deliveryid
        )
        db.session.add(userm)
        db.session.commit()
        return userm
    
# modeling service
class Service(db.Model):
    __tablename__ = 'servicios'

    Codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FechaHoraSolicitud = db.Column(db.DateTime, default=datetime.now)
    Origen = db.Column(db.String)
    Destino = db.Column(db.String)
    Descripcion = db.Column(db.String)
    TipoTransporte = db.Column(db.String,nullable=False)
    NumPaquetes = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    usermid = db.Column(db.Integer, db.ForeignKey('usersm.id'))
    usuarios = db.relationship('State', backref='Service', lazy=True)
    

class State(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)
    fechaac = db.Column(db.DateTime,default=datetime.now)
    serviceid = db.Column(Integer,db.ForeignKey('servicios.Codigo'))

# manages the logins of all users
@login_manager.user_loader
def load_user(user_id):
    # Intenta cargar como mensajes primero
    men = Userm.query.get(int(user_id))
    if men is not None:
        return men
    
    # Si no es un men, intenta cargar como RegularUser
    user = User.query.get(int(user_id))
    return user
