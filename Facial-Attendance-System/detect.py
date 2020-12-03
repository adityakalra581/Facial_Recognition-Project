## Facial Recognition Attendance System: Recognizing the face and checking whether the name is present in the CSV or Not. 
# If yes then it does not overwrite and if no it will write the name with date.


import face_recognition
import os
import cv2
from datetime import datetime


KNOWN_FACES_DIR = "known_faces"
# UNKNOWN_FACES_DIR = "unknown_faces"
TOLERANCE = 0.5  
## 0-1, 
## higher value will give more matches but less accuracy.
## Lower value will give less matches with high accuracy.

FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  ## Use hog if running on cpu and "cnn" if on GPU 

# cap = cv2.VideoCapture("E:\\GITHUB\\Facial_Recognition-Project\\face-identification-project\\sample_videos\\ssr-1.mp4")
cap = cv2.VideoCapture(0)


print("loading the images")

known_faces = []
known_names = []
names = []


for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)



def Attendance(x):
    with open('Attendance.csv','r+') as f:
        data = f.readlines()
        name_list = []
        for line in data:
            entry = line.split(',')
            name_list.append(entry[0])
        if x not in name_list:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            date_string = now.strftime("%d-%m-%Y")
            f.writelines(f'\n{x},{date_string},{dtstring}')


print("processing")
while True:
#     print(filename)
    ret,image=cap.read()
#     image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
    locations = face_recognition.face_locations(image, model = MODEL)
    encodings = face_recognition.face_encodings(image, locations)
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    for face_encodings, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encodings, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match found: {match}")
            names.append(match)
            

          # First Rectangle for Face Detection
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [255,0,0]
            cv2.rectangle(image, top_left,bottom_right, color, FRAME_THICKNESS)    

          # Second Rectangle for Name
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)
            color = [255,0,0]
            cv2.rectangle(image, top_left,bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)
            Attendance(match)
        else:
            print("Match Not Found")
    

#     cv2.imshow(filename,image)
#     cv2.imwrite(os.path.join(path,"output%d.jpg" % i),image) #Is not working for some reason
    cv2.imshow('Image',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    ## Press q and the loop will get off.        
        break

cap.release()
cv2.destroyAllWindows()
