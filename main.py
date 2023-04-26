from flask import Flask
from auth.views import api
from rutas_front_maaji.views import home

app = Flask(__name__)

app.secret_key = 'MAGI'

# Registrar los blueprints
app.register_blueprint(api)
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)