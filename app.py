from flask import Flask, render_template, request, redirect, url_for
import cv2
import face_recognition
import os
import subprocess

app = Flask(__name__)

# Load images and corresponding names
image_folder_path = "C:/Work/Applied AI Alt/images/"
files_path = "C:/Work/Applied AI Alt/files/"
image_files = ["Faizaan_Talha.jpg", "Hashim_Bilal.jpg", "Rana_AbdulRehman.jpg", "Afraz_Tahir.jpg"]
names = ["Faizaan_Talha", "Hashim_Bilal", "Rana_AbdulRehman", "Afraz_Tahir"]

# Get face encodings of known faces
known_face_encodings = []
for image_file in image_files:
    img = face_recognition.load_image_file(image_folder_path + image_file)
    face_encoding = face_recognition.face_encodings(img)[0]
    known_face_encodings.append(face_encoding)

# Flag to check if file has been opened
file_opened = False

# Open webcam
cap = cv2.VideoCapture(0)

# Function to open secure drive window
def open_secure_drive(name):
    # Perform actions related to opening a file for the recognized person
    file_to_open = f"{name}.txt"
    file_path = os.path.join(files_path, file_to_open)

    # Open the file using the default associated program (e.g., notepad on Windows)
    subprocess.Popen(["start", "notepad", file_path], shell=True)

# Function to handle face recognition
def recognize_face():
    global file_opened

    print("Recognizing face...")

    ret, frame = cap.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)

        if True in matches:
            first_match_index = matches.index(True)
            name = names[first_match_index]
            file_opened = True
            open_secure_drive(name)
            print("Face recognized:", name)
            break  # Break the loop after recognizing a face

# Route for the home page
@app.route('/')
def home():
    global file_opened

    # If the file has been opened, reset the flag
    if file_opened:
        file_opened = False

    return render_template('index.html')

# Route to trigger face recognition
@app.route('/recognize_face', methods=['POST'])
def recognize_face_route():
    recognize_face()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)