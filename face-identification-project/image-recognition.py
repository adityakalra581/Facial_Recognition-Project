import face_recognition
import os
import cv2


KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
TOLERANCE = 0.5  
## 0-1, 
## higher value will give more matches but less accuracy.
## Lower value will give less matches with high accuracy.

FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  
## Use hog(Histogram of Oriented Gradients)
## if running on cpu and "cnn" if on GPU 

print("loading the images")

known_faces = []
known_names = []

path='D:\\GITHUB\\face-mask-detector\\face-identification-project\\output'
i =0

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print("processing")
for filename in os.listdir(UNKNOWN_FACES_DIR):
    print(filename)
    image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
    locations = face_recognition.face_locations(image, model = MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    for face_encodings, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encodings, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match found: {match}")

          # First Rectangle for Face Detection
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0,255,0]
            cv2.rectangle(image, top_left,bottom_right, color, FRAME_THICKNESS)    

          # Second Rectangle for Name
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)
            color = [0,255,0]
            cv2.rectangle(image, top_left,bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)
        else:
            print("Match Not Found")
    
# #     cv2.imshow(filename,image)
#     new = cv2.resize(image,(600,600))
#     cv2.imwrite(os.path.join(path,"output%d.jpg" % i),new)
#     cv2.waitKey(5000)
#     i += 1



    # Show image
    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(filename)