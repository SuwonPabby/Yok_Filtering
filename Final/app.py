from flask import Flask, render_template, request, send_file
from flask.templating import render_template_string
from werkzeug.utils import secure_filename
import os 
import module as md
import pickle
from module import dataset_train

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('home.html')



        

@app.route('/file-upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        with open(os.path.abspath('./grad_web/train_dataset.p'), 'rb') as file:    
            train_dataset = pickle.load(file)
        origin_file = request.files['file']
        origin_file.save(os.path.abspath('./grad_web/uploads/inputvideo.mp4'))
        model_dir = os.path.abspath('./grad_web/keras_model_1.h5')
        video_dir = os.path.abspath('./grad_web/uploads/inputvideo.mp4')
        output_dir = os.path.abspath('./grad_web/outputs/outputvideo.mp4')
        working_path = os.path.abspath('./grad_web/workingspace')
        md.final_output(model_dir, video_dir, output_dir, working_path, train_dataset)
        # os.remove(video_dir)
        # for file in os.scandir(working_path):
        #     os.remove(file.path)
        return render_template('download page.html')

@app.route('/file-download', methods = ['GET', 'POST'])       
def download_file():
    if request.method == 'POST':
        return send_file(os.path.abspath('./grad_web/outputs/outputvideo.mp4')
                         , attachment_filename = 'filtered.mp4'
                         ,as_attachment = True) 



if __name__ == '__main__':
    app.run('0.0.0.0', port = 8080, debug=True)
   
