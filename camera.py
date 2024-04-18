import cv2
from flask import Flask, render_template, Response, request

application = Flask(__name__)

class VideoCamera(object):
    def __init__(self, camera_source=0):
        self.video = cv2.VideoCapture(camera_source)
        
        self.classNames = []
        self.classFile = 'coco.names'
        with open(self.classFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        self.configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weightsPath = 'frozen_inference_graph.pb'

        self.net = cv2.dnn_DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def __del__(self):
        self.video.release()

    def set_camera_source(self, camera_source):
        self.video.release()
        self.video = cv2.VideoCapture(int(camera_source))

    def get_frame(self):
        ret, frame = self.video.read()

        classIds, confs, bbox = self.net.detect(frame, confThreshold=0.5)
        print(classIds, bbox)

        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, self.classNames[classId - 1], (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

video_camera = VideoCamera()

@application.route('/')
def detect():
    return render_template('detect.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type:image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@application.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@application.route('/switch_camera')
def switch_camera():
    camera_source = request.args.get('camera')
    video_camera.set_camera_source(camera_source)
    return "Switched to camera {}".format(camera_source)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='5000', debug=True)
