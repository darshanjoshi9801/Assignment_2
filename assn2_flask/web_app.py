from flask import *
from zipfile import ZipFile


app = Flask(__name__)


@app.route('/')
def file_upload():
    return render_template('index.html')


@app.route('/success' , methods=['GET','POST'])
def success():
    if request.method == 'POST':
        file = request.files['zipfile']
        with ZipFile(file ,'r') as zip_file:
            zip_file.printdir()
            zip_file.extractall()
    return "zip file extracted successfully"


if __name__ == '__main__':
    app.run(debug=True)



