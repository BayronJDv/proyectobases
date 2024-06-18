from datetime import datetime
import os
from flask import render_template, flash, redirect, url_for, jsonify, request, make_response, send_file
from app.auth.forms import *
from app.auth import authentication
from app.auth.models import User,Client,Userm,Delivery,Service,State,Sucursal
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
import base64
from sqlalchemy import extract

from app.auth.crearPdf import *

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('authentication.log_in_user'))
            if current_user.role != role:
                flash("No tienes permisos para acceder a esta página.")
                return redirect(url_for('authentication.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def cambiarEstado(codigo,numE,foto,usuario):
    estado = State.query.filter_by(serviceid=codigo).first()
    servicio = Service.query.filter_by(Codigo=codigo).first()
    foto_binario = base64.b64decode(foto)
    match numE:
        case 2:
            estado.estado='Recogido'
            estado.imagen=foto_binario
            servicio.usermid=usuario
        case 3:
            estado.estado='Entregado'
            estado.imagen=foto_binario
            servicio.usermid=usuario
        case _:
            print("La pagina fue modificada, tenga cuidado")
    try:
        db.session.add(estado)
        db.session.add(servicio)
        db.session.commit()
        print("Estado actualizado correctamente")
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar el estado: {str(e)}")


@authentication.route("/register", methods=["GET","POST"])
def register_user():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        tipo = form.type.data
        if tipo == "client":
            User.create_user(
                user=form.name.data,
                email=form.email.data,
                password=form.password.data,
                address=form.address.data,
                clientid=form.clientid.data
            )
            flash("Registration Done...")
            return redirect(url_for("authentication.log_in_user"))
        Userm.create_userm(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data,
            address=form.address.data,
            deliveryid=form.clientid.data
        )
        flash("Registration Done...")
        return redirect(url_for("authentication.log_in_user"))
    return render_template("registration.html", form=form)

@authentication.route("/registerClient", methods=["GET","POST"])
def register_client():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.index"))
    form = RegistrationclientForm()
    if form.validate_on_submit():
        Client.create_client(
            name = form.name.data,
            address = form.address.data,
            email= form.email.data,
            telephone= form.telephone.data
        )
        flash("Registration Done... Now you can create a user with yout client id ")
        return redirect(url_for("authentication.register_user")) 
    return render_template("rclient.html", form=form)

@authentication.route("/registerdelivery", methods=["GET","POST"])
def register_delivery():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    form = RegistrationDeliveryForm()
    if form.validate_on_submit():
        Delivery.create_delivery(
            name = form.name.data,
            address = form.address.data,
            email= form.email.data,
            telephone= form.telephone.data
        )
        flash("Registration Done... Now you can create a userm with your id ")
        return redirect(url_for("authentication.register_user")) 
    return render_template("rdelivery.html", form=form)

@authentication.route("/")
def index():
    return render_template("index.html")

@authentication.route("/login", methods=["GET","POST"])
def log_in_user():
    if current_user.is_authenticated:
        flash("You are already logged in the system")
        return redirect(url_for("authentication.index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        if user and user.check_password(form.password.data):
            if user.user_name == 'admin':
                login_user(user, form.stay_loggedin.data)                
                return redirect(url_for("authentication.admin"))

            login_user(user, form.stay_loggedin.data)
            return redirect(url_for("authentication.homepage"))
        
        men = Userm.query.filter_by(userm_email=form.email.data).first()
        if men and men.checkm_password(form.password.data):
            login_user(men, form.stay_loggedin.data)
            return redirect(url_for("authentication.homepagem"))

        flash("Invalid credentials...")
        return redirect(url_for("authentication.log_in_user"))
    
    return render_template("login.html", form=form)

@authentication.route("/UserRequest", methods=["GET","POST"])
@login_required
@role_required('user')
def UserRequest():
    with open(f'espera.jpeg', 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read())
    
    form = RequestForm()
    if form.validate_on_submit():
        new_service = Service(
            Origen=form.origen.data,
            Destino=form.destino.data,
            Descripcion=form.Descripcion.data,
            TipoTransporte=form.transporte.data,
            NumPaquetes=form.numpaquetes.data,
            userid=current_user.id
        )
        db.session.add(new_service)
        db.session.commit()
        new_state = State(
            serviceid=new_service.Codigo,
            estado = "solicitado",
            imagen = base64.b64decode(encoded_string)
        )
        db.session.add(new_state)
        db.session.commit()
        flash('Service request created successfully!', 'success')
        return redirect(url_for("authentication.homepage"))
    return render_template("UserRequest.html", form = form)

@authentication.route("/homepage")
@login_required
@role_required('user')
def homepage():
    return render_template("homepage.html")

@authentication.route('/get_imagen', methods=['POST'])
@login_required
@role_required('user')
def get_imagen():
    data = request.get_json()
    codigo = data['codigo']
    estado = State.query.filter_by(serviceid=codigo).first()
    encoded_string = base64.b64encode(estado.imagen).decode('utf-8')

    return jsonify({'imagen_base64': encoded_string})    

def cambiarEstado(codigo,numE,foto,usuario):
    estado = State.query.filter_by(serviceid=codigo).first()
    servicio = Service.query.filter_by(Codigo=codigo).first()
    foto_binario = base64.b64decode(foto)
    match numE:
        case 2:
            estado.estado='Recogido'
            estado.imagen=foto_binario
            estado.fechaac = datetime.now()
            servicio.usermid=usuario
        case 3:
            estado.estado='Entregado'
            estado.imagen=foto_binario
            estado.fechaac = datetime.now()
            servicio.usermid=usuario
        case _:
            print("La pagina fue modificada, tenga cuidado")
    try:
        db.session.add(estado)
        db.session.add(servicio)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar el estado: {str(e)}")


@authentication.route('/change_estado', methods=['POST'])
@login_required
@role_required('userm')
def change_estado_route():
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No se recibieron datos JSON'}), 400 

    codigo = data['codigo']
    nume = data['nume']
    foto = data['foto']
    usuario = data['usuario']
    
    cambiarEstado(codigo, nume, foto, usuario)
    
    return jsonify({'message': f'Pedido con código {codigo} cambio de estado!'})

@authentication.route("/homepagem")
@login_required
@role_required('userm')
def homepagem():
    return render_template("homepagem.html")

@authentication.route("/accept")
@login_required
@role_required('userm')
def accept():
    pedidos = Service.query.filter(Service.usermid.is_(None)).all()
    return render_template("accept.html",pedidos=pedidos)

@authentication.route("/myservices", methods=["GET"])
@login_required
@role_required('userm')
def myservices():
    user_id = current_user.id
    misPedidos = (db.session.query(Service).join(State, Service.Codigo == State.serviceid).filter(Service.usermid == user_id).filter(State.estado != 'Entregado').all())
    return render_template("myservices.html", misPedidos=misPedidos)

@authentication.route("/admin")
@login_required
@role_required('admin')
def admin():
    usuarios = User.query.all()
    mensajeros = Userm.query.all()
    return render_template("admin.html",usuarios=usuarios,mensajeros=mensajeros)

@authentication.route("/get_user_pdf", methods=['POST'])
@login_required
@role_required('admin')
def get_user_pdf():    
    data = request.get_json()
    usuario_id = data['usuarioId']
    mes = data['mes']
    anio = data['anio']
    usuario = User.query.filter_by(id=usuario_id).first()
    servicios = Service.query.filter(Service.userid == usuario_id,extract('month', Service.FechaHoraSolicitud) == mes, extract('year', Service.FechaHoraSolicitud) == anio).all()

    pdfUsuario(usuario.user_name,usuario.user_email,usuario.user_adress,usuario.create_date,servicios)    
    try:
        with open(f'enviar/lastReport.pdf', 'rb') as f:
            content = f.read()
            response = make_response(content)
            response.headers['Content-Disposition'] = f'attachment; filename=reporte_{usuario_id}_{mes}_{anio}.pdf'
            response.headers['Content-Type'] = 'application/pdf'
            return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@authentication.route("/get_ms_pdf", methods=['POST'])
@login_required
@role_required('admin')
def get_ms_pdf():
    data = request.get_json()
    mensajero_id = data['mensajeroId']
    mes = data['mes']
    anio = data['anio']
    mensajero = Userm.query.filter_by(id=mensajero_id).first()
    servicios = Service.query.filter(Service.usermid == mensajero_id,extract('month', Service.FechaHoraSolicitud) == mes, extract('year', Service.FechaHoraSolicitud) == anio).all()
    pdfMensajero(mensajero.userm_name,mensajero.userm_email,mensajero.userm_adress,mensajero.create_date,servicios)    

    try:
        with open(f'enviar/lastReport.pdf', 'rb') as f:
            content = f.read()
            response = make_response(content)
            response.headers['Content-Disposition'] = f'attachment; filename=reporte_{mensajero_id}_{mes}_{anio}.pdf'
            response.headers['Content-Type'] = 'application/pdf'
            return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user():      
    logout_user()
    return redirect(url_for("authentication.log_in_user"))

@authentication.route("/delete", methods=["GET","POST"])
@login_required
def delete():
    user = User.query.get(current_user.id)
    userm = Userm.query.get(current_user.id)
    if user:
        logout_user()
        db.session.delete(user)
        db.session.commit()      
        return redirect(url_for("authentication.log_in_user"))
    logout_user()
    db.session.delete(userm)
    db.session.commit()      
    return redirect(url_for("authentication.log_in_user"))
@authentication.route("/myrequest", methods=["POST","GET"])
def myrequest():
    miid = current_user.id
    servicio_estado = db.session.query(Service, State).join(State, Service.Codigo == State.serviceid).filter(Service.userid == miid).all()
    myrequest = [{'service': pedido, 'estado': estado} for pedido, estado in servicio_estado]
    if len(myrequest) > 0:
        return render_template("myrequest.html",myrequest=myrequest)
    else:
        flash("Aun no has realizado ningun pedido")
        return redirect(url_for("authentication.homepage"))

@authentication.route("/rsucursal", methods=["POST","GET"])
def rsucursal():
    form = RegistrationSucursalForm()
    if form.validate_on_submit():
        id = current_user.id
        losid = db.session.query(Client.cid).join(User, Client.cid==User.cid).filter(User.id == id).first()
        miid = losid[0]
        new_sucursal = Sucursal(
            sucursal_name=form.name.data,
            sucursal_adress=form.address.data,
            sucursal_telephone=form.telephone.data,
            clientid = miid
        )
        db.session.add(new_sucursal)
        db.session.commit()
        flash('Sucursal created successfully!','success')
        return redirect(url_for("authentication.homepage"))
    return render_template("rsucursal.html",form = form )

@authentication.route("/myinfo", methods=["POST","GET"])
def myinfo():
    userinfo = User.query.get(current_user.id)
    sucursales = Sucursal.query.filter_by(clientid = User.cid).all()
    return render_template("myinfo.html", user = userinfo, sucursales = sucursales)
@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
