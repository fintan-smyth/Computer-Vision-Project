import cv2
from keras.models import load_model
import numpy as np
import time
import random
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

class rps:

    def __init__(self, score_limit=3):
        self.score_limit = score_limit
        self.computer_score = 0
        self.user_score = 0
        self.options = ['rock', 'paper', 'scissors']
        print('\n'*50 + '\nWelcome to my Rock, Paper, Scissors game.\n')
        time.sleep(1)
        print(f'The winner is the first to reach {self.score_limit} points.\n')
        time.sleep(1)


    def get_prediction(self):
        labels = ['rock', 'paper', 'scissors', 'nothing']
        start = time.time()
        while True:
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image
            cv2.imshow('frame', frame)
            runtime = time.time() - start
            if 1.47 < round(runtime, 2) < 1.55:
                print('\n\nYOUR   CHOICE\n\n     IS\n\nLOCKED    IN:\n\n')
            elif 2.47 < round(runtime, 2) < 2.55:
                print('\n333333\n    33\n333333\n    33\n333333\n')    
            elif 3.47 < round(runtime, 2) < 3.55:
                print('\n222222\n    22\n222222\n22\n222222\n')
            elif 4.47 < round(runtime, 2) < 4.55:
                print('\n1111\n  11\n  11\n  11\n111111\n')
            elif round(runtime, 2) > 5.5:
                prediction = model.predict(data)
                print('\nLOCKED!\n')
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(runtime)
                prediction = 'error'
                break
        cv2.destroyAllWindows()
        if type(prediction) == str:
            return prediction
        else:
            return labels[np.argmax(prediction)]
    

    def get_computer_choice(self):
        computer_choice = random.choice(self.options)
        return computer_choice

    
    def get_user_choice(self):
        while True:
            user_choice = self.get_prediction()
            if user_choice.lower() not in self.options:
                print('\nSorry, a valid input was not detected. \n')
                input('Press Enter to try again...')
            else:
                print(f'Your choice was: {user_choice}\n')
                break
        return user_choice

    
    def get_winner(self, computer_choice, user_choice):
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

    
    def play(self):
        while True:
            start = input('Press Enter to make your choice...\n')
            if start == 'x':
                break    
            computer_choice = self.get_computer_choice()
            user_choice = self.get_user_choice()
            winner = self.get_winner(computer_choice, user_choice)
            time.sleep(1)
            print(f'The computer chose: {computer_choice}\n')
            time.sleep(1)
            if winner == 'draw':
                print('It was a draw.\n')
            elif winner == 'comp':
                print('The computer wins a point.\n')
                self.computer_score += 1
            elif winner == 'user':
                print('The player wins a point.\n')
                self.user_score += 1
            print(f'Computer score: {self.computer_score}\nPlayer score: {self.user_score}\n')
            time.sleep(1)
            if self.computer_score == self.score_limit:
                print('Bad luck, the computer won.\n')
                break
            if self.user_score == self.score_limit:
                print('Congratulations! The player is the winner.\n')
                break 
                

if __name__ == '__main__':
    game = rps(score_limit = 3)
    game.play()
    

cap.release()
cv2.destroyAllWindows()