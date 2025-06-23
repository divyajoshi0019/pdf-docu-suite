import os
from flask import Flask, request, send_file, render_template, jsonify, after_this_request
from pypdf import PdfWriter
from docx import Document
from pdf2docx import Converter
from docx2pdf import convert as convert_docx_to_pdf
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'
CONVERTED_FOLDER = 'converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# --- Main Navigation ---

@app.route('/')
def index():
    return render_template('index.html')

# --- PDF Merger ---

@app.route('/merge', methods=['GET'])
def merge_page():
    return render_template('merge.html')

@app.route('/api/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('pdfs')
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No files uploaded'}), 400
        
    if len(files) > 5:
        return jsonify({'error': 'You can upload a maximum of 5 files'}), 400

    merger = PdfWriter()
    temp_files = []
    output_path = None

    try:
        for file in files:
            if file.filename == '':
                continue
            if file and file.filename.lower().endswith('.pdf'):
                temp_path = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()) + '.pdf')
                file.save(temp_path)
                temp_files.append(temp_path)
                merger.append(temp_path)
            else:
                return jsonify({'error': 'Invalid file type. Please upload only PDF files.'}), 400

        if len(merger.pages) == 0:
            return jsonify({'error': 'No valid PDF files were uploaded.'}), 400

        unique_id = str(uuid.uuid4())
        output_path = os.path.join(MERGED_FOLDER, f'merged_{unique_id}.pdf')
        
        with open(output_path, 'wb') as f:
            merger.write(f)
        
        merger.close()

        @after_this_request
        def cleanup(response):
            try:
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
            except OSError as e:
                app.logger.error(f"Error removing merged file: {e.strerror}")
            return response

        return send_file(output_path, as_attachment=True, download_name='merged.pdf')

    finally:
        for temp_path in temp_files:
            if os.path.exists(temp_path):
                os.remove(temp_path)

# --- Word to PDF Converter ---

@app.route('/word-to-pdf', methods=['GET'])
def word_to_pdf_page():
    return render_template('word_to_pdf.html')

@app.route('/api/word-to-pdf', methods=['POST'])
def word_to_pdf():
    file = request.files.get('file')

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    if not file.filename.lower().endswith(('.doc', '.docx')):
        return jsonify({'error': 'Invalid file type. Please upload a Word document.'}), 400

    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(CONVERTED_FOLDER, f'{os.path.splitext(file.filename)[0]}.pdf')
    file.save(temp_path)

    try:
        convert_docx_to_pdf(temp_path, output_path)

        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except OSError as e:
                app.logger.error(f"Error cleaning up word2pdf files: {e.strerror}")
            return response

        return send_file(output_path, as_attachment=True)
    
    except Exception as e:
        # On Windows, docx2pdf requires MS Word to be installed.
        app.logger.error(f"Word to PDF conversion failed: {e}")
        return jsonify({'error': 'Conversion failed. Please ensure you have Microsoft Word installed.'}), 500

# --- PDF to Word Converter ---

@app.route('/pdf-to-word', methods=['GET'])
def pdf_to_word_page():
    return render_template('pdf_to_word.html')

@app.route('/api/pdf-to-word', methods=['POST'])
def pdf_to_word():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    temp_pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_docx_path = os.path.join(CONVERTED_FOLDER, f'{os.path.splitext(file.filename)[0]}.docx')
    file.save(temp_pdf_path)

    try:
        cv = Converter(temp_pdf_path)
        cv.convert(output_docx_path, start=0, end=None)
        cv.close()

        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
                if os.path.exists(output_docx_path):
                    os.remove(output_docx_path)
            except OSError as e:
                app.logger.error(f"Error cleaning up pdf2word files: {e.strerror}")
            return response

        return send_file(output_docx_path, as_attachment=True)
    
    except Exception as e:
        app.logger.error(f"PDF to Word conversion failed: {e}")
        return jsonify({'error': 'An error occurred during conversion.'}), 500

if __name__ == '__main__':
    app.run(debug=True) 