import cv2
from keras.models import load_model
import numpy as np
import time
import random
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

class rps:

    def __init__(self, score_limit=3):
        self.score_limit = score_limit
        self.computer_score = 0
        self.user_score = 0
        self.options = ['rock', 'paper', 'scissors']
        print('\n'*100 + '\nWelcome to my Rock, Paper, Scissors game.\n')
        time.sleep(1)
        if self.score_limit == 1:
            print(f'The winner is the first to reach {self.score_limit} point.\n')
        else:
            print(f'The winner is the first to reach {self.score_limit} points.\n')
        time.sleep(1)


    def get_prediction(self):
        cap = cv2.VideoCapture(0)
        labels = ['rock', 'paper', 'scissors', 'nothing']
        print('Image capture starting...')
        start = time.time()
        while True:
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image
            runtime = time.time() - start
            if 1.5 < runtime < 2.4 :
                cv2.putText(frame, "CHOICE LOCKED IN...", (90,390), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 3)
            elif 3 < runtime < 3.5:
                cv2.putText(frame, "3", (280,270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5)
            elif 4 < runtime < 4.5:
                cv2.putText(frame, "2", (280,270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5)
            elif 5 < runtime < 5.5:
                cv2.putText(frame, "1", (280,270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5)
            elif runtime > 6:
                cv2.putText(frame, "LOCKED!", (180,270), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,180,0), 5)
            cv2.imshow('frame', frame)
            if runtime > 6.1:
                prediction = model.predict(data)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                prediction = 'none'
                break
        cv2.destroyAllWindows()
        cap.release()
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