from flask import Flask, render_template, Response, request
from camera import VideoCamera

application = Flask(__name__)

@application.route('/')
def home():
    return render_template('home.html')

# Define route for the about page
@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/detect')
def detect():
    return render_template('detect.html')

# Define route for the report page
@application.route('/report')
def report():
    return render_template('report.html')

# Function to generate video frames
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route for video feed
@application.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# Specify the path to save the bug_reports.txt file
BUG_REPORTS_FILE = 'data/bug_reports.txt'

# Route for handling form submission
@application.route('/submit_form', methods=['POST'])
def submit_form():
    bug_description = request.form.get('bug_description')
    user_email = request.form.get('user_email')

    # Store the data in the text file
    with open(BUG_REPORTS_FILE, 'a') as file:
        file.write(f"Bug Description: {bug_description}\n")
        file.write(f"User Email: {user_email}\n")
        file.write('\n')

    # Send a thank you message
    thank_you_message = "Thank you for reporting the bug! We appreciate your feedback."
    return render_template('thank_you.html', message=thank_you_message)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)
