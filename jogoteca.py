from flask import Flask, render_template, request, redirect, session, flash, url_for
from Jogo import Jogo
from Usuario import Usuario
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) #__name__ referencia a propria pagina
app.secret_key = 'dssoares'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    )

db = SQLAlchemy(app) # instância do banco de dados do SQLAlchamy

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.nome
    
class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.nome

@app.route('/')
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', lista_jogos=lista_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #usando o ?proxima=novo como parametro para proxima pagina
        return redirect(url_for('login', proxima=url_for('novo'))) 
    return render_template('novo.html', titulo='Novo jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))

    novoJogo = Jogos(nome=nome, categoria=categoria, console=console)

    db.session.add(novoJogo)
    db.session.commit()

    return redirect(url_for('index')) # passa a função que instancia a pagina

@app.route('/login')
def login():
    proxima = request.args.get('proxima') #pega o argumento se existir
    #passa esse argumento para tela renderizada
    return render_template('login.html', proxima=proxima) 

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario_form = request.form['usuario']
    usuario = Usuarios.query.filter_by(nickname=usuario_form).first()
    proxima_pagina = request.form['proxima']

    if not proxima_pagina or proxima_pagina == "None":
        proxima_pagina = url_for('index')

    if usuario:
        senha_form = request.form['senha']
        if senha_form == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname.capitalize() + ' logado com sucesso!')
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado. Senha incorreta')
            return redirect(url_for('login'))
    else:
        flash('Usuário não cadastrado.')
        return redirect(url_for('login'))

app.run(debug=True) #debug=True para toda vez que tiver mudança no código, Flask atualiza
