from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from get_cursos import generate_cursos_csv
from get_relatorios import generate_reports_csv
from get_workspaces import generate_workspaces_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-cursos', methods=['GET', 'POST'])
def download_cursos_csv():
    if request.method == 'POST':
        data = request.form
        course_names_string = data.get('course_names', '').strip()
        course_names_input = [name.strip() for name in course_names_string.\
                                split(',')] if course_names_string else []
        
        if not course_names_input or not isinstance(course_names_input, list):
            return jsonify({"error": "nomes de cursos invalidos"}), 400
        
        
        csv_path = generate_cursos_csv(course_names_input)
        return send_from_directory(directory=os.path.dirname(csv_path),
                               path=os.path.basename(csv_path),
                               as_attachment=True)
        
    return render_template('index.html')
    
@app.route('/download-relatorios')
def download_relatorios_csv():
    csv_path = generate_reports_csv()
    return send_from_directory(directory=os.path.dirname(csv_path),
                               path=os.path.basename(csv_path),
                               as_attachment=True)
    
    
@app.route('/download-workspaces')
def download_workspaces_csv():
    csv_path = generate_workspaces_csv()
    return send_from_directory(directory=os.path.dirname(csv_path),
                               path=os.path.basename(csv_path),
                               as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    