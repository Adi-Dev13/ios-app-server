#Webserver for IOS app
from flask import Flask, render_template, request, redirect, url_for
from time import sleep
import os 
import json
import ai
import threading
app = Flask(__name__)


app.secret_key = "adityawebserver1234510@1694208008secretkey"
allowed = ['.mp4', '.mov', '.webm', '.mkv']

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form['key'] == app.secret_key:
            user = request.form['user']
            inp = request.files["inp"]
            
            allow = False
            for al in allowed:
                if al in inp.filename:
                    allow = True
                    break
            if allow == False:
                return render_template('index.html')
            
            c_path = os.getcwd()
            c_path = c_path.split("\\")
            c_path = '/'.join(c_path)
            
            
            if user not in os.listdir(c_path+'/static/users'):
                os.mkdir(c_path+'/static/users/'+user)
                
            vidname = inp.filename.split('.')
            vidname = 'video.'+vidname[-1]
            
            vid_path = 'static/users/'+user+'/'
            path = c_path + '/' + vid_path + vidname
            inp.save(path)
            
            ai.runAI(ai.getvid(vid_path + vidname), c_path + '/static/users/'+user+'/output.mp4')
            
            vid_path = vid_path+'output.mp4'
            vid = ''
            for l in vid_path:
                if l == '/':
                    l = ':'
                vid+=l
                
                
            d = '{"vid" :' +'"'+ vid + '"' + '}'
            
            return redirect(url_for("res", data=d))
        else:
            return render_template('index.html')
            
    else:
        return render_template('index.html')
    
@app.route("/<data>")
def res(data):
    try:
        d = json.loads(data)
        d = d['vid']
        v = ''
        for l in d:
            if l == ':':
                l = '/'
            v+=l
        
        
        vid = 'http://localhost:5000/' + v
        
        return redirect(vid)
        
        
    except Exception as e:
        print(e)
        return redirect(url_for("home"))
    
    


    
if __name__ == "__main__":
    app.run(threaded=True)

