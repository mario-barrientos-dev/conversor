from flask import Blueprint, render_template, request

home = Blueprint('home', __name__)

@home.route('/')
def home_view():
    return render_template('home.html')

@home.route('/coominsoon')
def coominsoon():
    return render_template('coominsoon.html')

@home.route('/convert')
def auth_view():
    convert_to = request.args.get('convert_to', 'unknown')
    print(convert_to)
    return render_template('conversor.html', conversion_type=convert_to)

@home.route('/bridge')
def bridge():
    return render_template('descarga.html')