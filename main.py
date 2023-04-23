from flask import Flask
from auth.views import auth
from home.views import home

app = Flask(__name__)

app.secret_key = 'MAGI'

# Registrar los blueprints
app.register_blueprint(auth)
app.register_blueprint(home)

if __name__ == '__main__':
    app.run()