from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) #__name__ referencia a propria pagina
app.config.from_pyfile('config.py') # puxa as configurações de um arquivo python
db = SQLAlchemy(app) # instância do banco de dados do SQLAlchamy

from views import *

if __name__ == '__main__':
    app.run(debug=True) #debug=True para toda vez que tiver mudança no código, Flask atualiza
