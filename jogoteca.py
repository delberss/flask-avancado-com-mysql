from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__) #__name__ referencia a propria pagina
app.config.from_pyfile('config.py') # puxa as configurações de um arquivo python
db = SQLAlchemy(app) # instância do banco de dados do SQLAlchamy
csrf = CSRFProtect(app)


from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True) #debug=True para toda vez que tiver mudança no código, Flask atualiza
