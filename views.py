from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem, deleta_arquivo
import time

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

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #usando o ?proxima=editar como parametro para proxima pagina
        return redirect(url_for('login', proxima=url_for('editar'))) 
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)

    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index')) # passa a função que instancia a pagina


@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()

    nome = request.form['nome']
    jogo.nome = nome

    categoria = request.form['categoria']
    jogo.categoria = categoria

    console = request.form['console']
    jogo.console = console

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login')) 
    
    jogo = Jogos.query.filter_by(id=id).first()  # Buscar o objeto real
    if jogo:
        db.session.delete(jogo)  # Deletar o objeto do banco
        db.session.commit()
        flash(f'{jogo.nome} deletado com sucesso', 'success')  # Flash com nome do jogo e categoria de sucesso
    else:
        flash('Jogo não encontrado!', 'danger')  # Caso o ID não exista

    return redirect(url_for('index'))

     

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
    

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


