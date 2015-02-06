'''
Created on Jan 23, 2015

@author: cz
'''
from flask import Flask
from flask import request
from flask import abort, redirect, url_for, render_template
from plotGenerator import autoplotGenerator
import flask.views

import os
from util import __SAVE_CSV_DIR


app = Flask(__name__)


app.debug = True



@app.route('/')
def index_start():
    return render_template("plot_temp.html")
    # filename = "test2.xls"
    # autoplotGenerator(filename)
    # return render_template('auto_visual_scatter_test1.html')
    # return render_template('auto_visual.html')
#     # return "index page"

@app.route('/index')
def index():
    celtarr = os.listdir(__SAVE_CSV_DIR)
#     print celtarr
    return render_template('index.html', eltarr = celtarr)
    

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filename = str(len(os.listdir(__SAVE_CSV_DIR)))+'.xls'
        f = request.files['fileToUpload']
        filepath = __SAVE_CSV_DIR + '/' +  filename
        f.save(filepath)
        print url_for('result')
        return redirect(url_for('result')+"?filename="+filename)
#     return 'succeed uploading... '
    return 'ERROR upload'


@app.route("/result", methods=['GET', 'POST'])
def show_result_page():
    if request.method == 'GET':
        cquery = request.args.get('filename')
        output = autoplotGenerator(cquery)
        return render_template(output)    

if __name__ == "__main__":
    app.run()
