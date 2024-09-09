from flask import Flask, render_template, Response, jsonify
import gunicorn
from camera import *


# app = Flask(__name__)
app = Flask(__name__, static_folder='static')

@app.route('/Emovision')
def emovision():
    return render_template('Emovision.html')

headings = ("Name","URL")
df1 = music_rec()
df1 = df1.head(15)
@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    return render_template('Index.html', headings=headings, data=df1)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
if __name__ == '__main__':
    app.run(debug=True)



