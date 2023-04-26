import os
import tempfile
from flask import Flask, render_template, request, Blueprint, send_file, session, redirect

from conversor.conversor import extraer_tablas_pdf, procesar_tablas, guardar_en_excel

auth = Blueprint('auth', __name__)

@auth.route('/auth')
def auth_view():
    return render_template('conversor.html')

@auth.route('/upload', methods=['POST'])
def upload():
    pdf = request.files['pdf']
    if pdf and allowed_file(pdf.filename):
        # El archivo es un PDF, haga algo con él aquí
        pdf_filename = pdf.filename
        pdf.save(pdf_filename)
        with tempfile.NamedTemporaryFile(prefix='excel_maajico_',suffix='.xlsx', delete=False, ) as temp:
            temp_filename = temp.name
            tablas = extraer_tablas_pdf(pdf_filename)
            datos_procesados = procesar_tablas(tablas)
            guardar_en_excel(datos_procesados, temp_filename)
            os.remove(pdf_filename)
            session[f"excel"] = (temp_filename)
            
            return 'ok'
    else:
        # El archivo no es un PDF
        error = 'Por favor, sube un archivo PDF válido'
        return error

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@auth.route('/bridge', methods=['GET'])
def bridge():
    return render_template('descarga.html')

@auth.route('/download', methods=['GET'])
def download():
    temp_filename = session['excel']
    return send_file(temp_filename, as_attachment=True)

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.run(debug=True)