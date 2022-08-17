import cv2
from keras.models import load_model
import numpy as np
import time
import random
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def get_prediction():
    labels = ['rock', 'paper', 'scissors', 'nothing']
    start = time.time()
    while True:
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        cv2.imshow('frame', frame)
        runtime = time.time() - start
        if round(runtime, 1) == 1.5:
            print('\n\nYOUR   CHOICE\n\n     IS\n\nLOCKED    IN:\n\n')
        elif round(runtime, 1) == 2.5:
            print('\n333333\n    33\n333333\n    33\n333333\n')    
        elif round(runtime, 1) == 3.5:
            print('\n222222\n    22\n222222\n22\n222222\n')
        elif round(runtime, 1) == 4.5:
            print('\n1111\n  11\n  11\n  11\n111111\n')
        elif round(runtime, 1) > 5.5:
            prediction = model.predict(data)
            print('\nLOCKED!\n')
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
           print(runtime)
           break
    cv2.destroyAllWindows()
    return labels[np.argmax(prediction)]
    
def get_computer_choice():
    options = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(options)
    return computer_choice

def get_user_choice():
    while True:
        user_choice = get_prediction()
        if user_choice.lower() not in ['rock', 'paper', 'scissors']:
            print('\nSorry, a valid input was not detected. \n')
            input('Press Enter to try again...')
        else:
            print(f'Your choice was: {user_choice}\n')
            break
    return user_choice

def get_winner(computer_choice, user_choice):
    if computer_choice == 'rock':
        if user_choice == 'rock':
            winner = 'draw'
        elif user_choice == 'paper':
            winner = 'user'
        elif user_choice == 'scissors':
            winner = 'comp'
    elif computer_choice == 'paper':
        if user_choice == 'rock':
            winner = 'comp'
        elif user_choice == 'paper':
            winner = 'draw'
        elif user_choice == 'scissors':
            winner = 'user'
    elif computer_choice == 'scissors':
        if user_choice == 'rock':
            winner = 'user'
        elif user_choice == 'paper':
            winner = 'comp'
        elif user_choice == 'scissors':
            winner = 'draw'
    return winner

def play():
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    winner = get_winner(computer_choice, user_choice)
    time.sleep(1)
    print(f'The computer chose: {computer_choice}\n')
    time.sleep(1)
    if winner == 'draw':
        print('It was a draw.\n')
    elif winner == 'comp':
        print('The computer wins a point.\n')
    elif winner == 'user':
        print('The player wins a point.\n')
    return winner

if __name__ == '__main__':
    computer_score = 0
    user_score = 0
    print('\n'*50 + '\nWelcome to my Rock, Paper, Scissors game.\n')
    time.sleep(1)
    print('The winner is the first to reach 3 points.\n')
    time.sleep(1)
    while True:
        start = input('Press Enter to make your choice...\n')
        if start == 'x':
            break
        winner = play()
        time.sleep(1)
        if winner == 'comp':
            computer_score += 1
        elif winner == 'user':
            user_score += 1
        print(f'Computer score: {computer_score}\nPlayer score: {user_score}\n')
        time.sleep(1)
        if computer_score == 3:
            print('Bad luck, the computer won.\n')
            break
        if user_score == 3:
            print('Congratulations! The player is the winner.\n')
            break

cap.release()
cv2.destroyAllWindows()