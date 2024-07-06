from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"
        
        if file and file.filename.endswith(('.xls', '.xlsx')):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            df = pd.read_excel(filename)
            sort_option = request.form['sort_option']
            if sort_option == 'name':
                df_sorted = df.sort_values(by='Name')
            elif sort_option == 'start_date':
                df_sorted = df.sort_values(by='Start Date')
            elif sort_option == 'end_date':
                df_sorted = df.sort_values(by='End Date')
            else:
                return "Invalid sorting option"
            output_filename = 'sorted_hackathons.xlsx'
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            df_sorted.to_excel(output_path, index=False, engine='openpyxl')
            return render_template('download.html', filename=output_filename)
    
    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
