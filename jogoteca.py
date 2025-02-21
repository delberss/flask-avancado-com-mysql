from flask import Flask, render_template, request, redirect, session, flash, url_for
from Jogo import Jogo
from Usuario import Usuario
from flask_sqlalchemy import SQLAlchemy

jogo1 = Jogo('Fifa', 'Esporte', 'PS5/XBOX')
jogo2 = Jogo('Call of Duty', 'FPS ', 'PC')
jogo3 = Jogo('Counter-Strike', 'FPS ', 'PC')

lista_jogos = [jogo1, jogo2, jogo3]

usuario1 = Usuario('Delber', 'delberss', '123')
usuario2 = Usuario('Pantera', 'panterass', '123')
usuario3 = Usuario('Messi', 'leomessi', 'barça')

usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3,
}

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


@app.route('/')
def index():
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
    jogo = Jogo(nome,categoria,console)
    lista_jogos.append(jogo)
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
    senha_form = request.form['senha']
    proxima_pagina = request.form['proxima']

    if not proxima_pagina or proxima_pagina == "None":
        proxima_pagina = url_for('index')

    if usuario_form in usuarios:
        usuario = usuarios[usuario_form]
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
