from flask import Flask, Response
import cv2

app = Flask(__name__)

# Apri la webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Leggi il frame dalla webcam
        success, frame = cap.read()
        if not success:
            break
        # Codifica il frame in formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        # Crea un flusso di dati per la trasmissione
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''<html>
              <body>
                <h1>Webcam Stream</h1>
                <img src="/video_feed" width="640" height="480">
              </body>
              </html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
