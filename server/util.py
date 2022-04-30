import joblib
import numpy as np
import json
import base64
import cv2
from wavelet import w2d

__class_name_to_number = {}     # {"chris_evans: 0, tom_holland: 1,..."}
__class_number_to_name = {}     # {"0: chris_evans, 1: tom_holland,..."}

__model = None                  # creates a private variable for trained model

# ----------------------------------------
# RETURN: an array of prediction
def classify_image(image_base64_data, file_path=None):
    imgs = get_cropped_image(file_path, image_base64_data)
    
    result = []

    for img in imgs:
        scaled_img_raw = cv2.resize(img, (32,32))                       # scale the image
        
        img_wave = w2d(img, 'db1', 5)                                   # convert to a wavelet transformed image
        scaled_img_wave = cv2.resize(img_wave, (32,32))                 # scale the wavelet transformed image
        
        combined_img = np.vstack((scaled_img_raw.reshape(32*32*3,1), scaled_img_wave.reshape(32*32,1)))

        len_image_array = 32 * 32 * 3 + 32 * 32

        # we convert the combined img to a float b/c some of the APIs needed later require float data type
        final = combined_img.reshape(1,len_image_array).astype(float)   

        result.append(__model.predict(final)[0]) 

    return result

# ----------------------------------------
# PURPOSE: converts the input base-64 string into an openCV image
# RETURN: an openCV image
def get_cv2_image_from_base64_string(b64str):
    # credit: stackoverflow.com
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

# ----------------------------------------
# PURPOSE: given an image path, return all cropped images of detected faces in that image
# RETURN: an array of cropped faces; return empty array is no face detected
# (note: this function is taken and modified from model building stage)
def get_cropped_image(image_path):  
    # prevents ipynb_checkpoints files from creating errors for imread
    if (image_path.endswith("jpg") or image_path.endswith("png") or image_path.endswith("jpeg")):  
        face_cascade = cv2.CascadeClassifier("opencv/haarcascades/haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("opencv/haarcascades/haarcascade_eye.xml")    

        if image_path:
            img = cv2.imread(image_path)
        else:
            img = get_cv2_image_from_base64_string(image_base64_data)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        cropped_faces = [] 

        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) >= 2:      
                cropped_faces.append(roi_color)

    return cropped_faces       
# ----------------------------------------
# RETURN:
def class_number_to_name(class_num):
    return __class_name_to_number[class_num]

# ----------------------------------------
# PURPOSE: load class dictionary and trained model into global variables
def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("./artifacts/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    global __model
    if __model is None:
        with open('./artifacts/saved_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")

# ----------------------------------------
# RETURN: a string that is the base-64 encoding of scarlett.jpeg
def get_b64_test_image_for_scarlett():
    with open("b64.txt") as f:
        return f.read()


if __name__ == '__main__':
    load_saved_artifacts()
    print(classify_image(get_b64_test_image_for_scarlett(), None))