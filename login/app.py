from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#########################BANCODEDADOS#######################
#Adicionando configuração para usar um banco de dados sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
########################LOGIN###############################
#Criando uma chave secreta (é necessária porque o Flask-Login exige que ele assine cookies de sessão para proteção contra adulteração de dados)
app.config["SECRET_KEY"] = "malbaecleia"
#Inicializando a classe LoginManager do Flask-Login, para poder efetuar login e logout de usuários.
login_manager = LoginManager(app)
#########################BANCODEDADOS#######################
#Inicializando app com o banco de dados
db = SQLAlchemy(app)
#Estrutura do banco de dados
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)

    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role
########################LOGIN###############################
#É necessário especificar uma função para recuperar um objeto de usuário com um ID de usuário
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        #Filtrando se há algum usuário no banco de dados com o mesmo nome de usuário daquele que está sendo enviado, se não houver o objeto fica vazio
        user = Users.query.filter_by(email=request.form["email"]).first()
        #Se houver usuário com o nome digitado, vai retornar True e entrar no if, se não houver a resposta é False e entra no else
        if user:
            flash("Usuário Existente")
            return render_template("registro.html")
        else:
            #Pegando os dados dos inputs do form e passando para o banco de dados
            user = Users(email=request.form["email"],
                         password=request.form["senha"],
                         role=request.form["função"])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    else:
        return render_template("sign.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Filtrando se há algum usuário no banco de dados com o mesmo nome de usuário daquele que está sendo enviado, se não houver o objeto fica vazio
        user = Users.query.filter_by(email=request.form["email"]).first()
        #Se houver usuário com o nome digitado, vai retornar True e entrar no if, se não houver a resposta é False e entra no else
        if user:
            #Verificando se esse usuário possui a mesma senha que o usuário digitou no formulário
            if user.password == request.form["senha"]:
                # Efetuando login do usuário
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Senha Incorreta")
                return render_template("login.html")
        else:
            flash("Usuário Inexistente")
            return render_template("login.html")
    else:
        return render_template("login.html")
@app.route("/logout")
def logout():
    #Efetuando logout do usuário
    logout_user()
    return redirect(url_for("home"))
@app.route("/professores")
def teachers():
    teachers = []
    #Pega todos os usuários com função de professor
    users = db.session.query(Users).filter_by(role="Professor")
    #Pega todos os usuários com função de professor e adiciona à lista teachers
    for teacher in users:
        email = teacher.email
        teachers.append(email)
    return render_template("teachers.html", teachers=teachers)
@app.route("/funcionários")
def staff():
    staff1 = []
    #Pega todos os usuários com função de funcionário
    users = db.session.query(Users).filter_by(role="Funcionário")
    #Pega todos os usuários com função de funcionário e adiciona à lista staff1
    for staff2 in users:
        email = staff2.email
        staff1.append(email)
    return render_template("staff.html", staff2=staff1)
@app.route("/estudantes")
def students():
    students = []
    #Pega todos os usuários com função de professor
    users = db.session.query(Users).filter_by(role="Estudante")
    #Pega todos os usuários com função de professor e adiciona à lista teachers
    for student in users:
        email = student.email
        students.append(email)
    return render_template("students.html", students=students)
@app.route("/detalhes")
def details():
    return render_template("details.html")

if __name__ == "__main__":
    #Para o db.create_all() funcionar
    app.app_context().push()
    #Criando o banco de dados
    db.create_all()
    app.run(debug=True)