import cv2
from keras.models import load_model
import numpy as np
import time
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def get_prediction():
    labels = ['Rock', 'Paper', 'Scissors', 'Nothing']
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    start = time.time()
    while True:
        prediction = model.predict(data)
        cv2.imshow('frame', frame)
        runtime = time.time() - start
        # Press q to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(runtime)
    return labels[np.argmax(prediction)]
    

print(get_prediction())