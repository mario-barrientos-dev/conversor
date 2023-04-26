import os
import tempfile
from flask import Flask, request, Blueprint, send_file, session, after_this_request
from conversor.conversor_excel import extraer_tablas_pdf, procesar_tablas, guardar_en_excel
from pdf2docx import Converter


api = Blueprint('api', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@api.route('/upload', methods=['POST'])
def upload():
    pdf = request.files['pdf']
    conversion_type = request.form['conversion_type']
    print(conversion_type)
    if conversion_type == 'Excel':
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
    elif conversion_type == 'Word':
        if pdf and allowed_file(pdf.filename):
            pdf_filename = pdf.filename
            pdf.save(pdf_filename)

            # Crear un archivo temporal utilizando mkstemp
            temp_fd, temp_filename = tempfile.mkstemp(prefix='word_maajico_', suffix='.docx')
            os.close(temp_fd)
            

            cv = Converter(pdf_filename)
            cv.convert(temp_filename, start=0, end=None)
            cv.close()

            os.remove(pdf_filename)
            session[f"word"] = (temp_filename)

            return 'ok'
        else:
            error = 'Por favor, sube un archivo PDF válido'
            return error
    else:
        return 'Tipo de conversión no válido'

@api.route('/download', methods=['GET'])
def download():
    
    if 'excel' in session:
        temp_filename = session['excel']

        @after_this_request
        def clean(response):
            try:
                session.pop('excel', None)
                print('Borró excel')
            except Exception as e:
                print(f"Error al eliminar el archivo: {e}")
            return response

        return send_file(temp_filename, as_attachment=True)
    if 'word' in session:
        temp_filename = session['word']

        @after_this_request
        def clean(response):
            try:
                session.pop('word', None)
                print('Borró word')
            except Exception as e:
                print(f"Error al eliminar el archivo: {e}")
            return response

        return send_file(temp_filename, as_attachment=True)

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(api)
    app.run(debug=True)