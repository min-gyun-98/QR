from flask import Flask, render_template, Response
from pyzbar import pyzbar
import cv2
import os

app = Flask(__name__)

def gen_frames():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ret, frame = camera.read()
    barcode_info = 'login info'
    while ret:
        # Capture frame-by-frame
        ret, frame = camera.read()
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if barcode_info != 'login info':
            break
    camera.release()
    memInfo = barcode_info
    print(memInfo)

@app.route('/')
def index():
    # return render_template('index.html',now=str(now))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)