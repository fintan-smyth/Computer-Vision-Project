import cv2
from keras.models import load_model
import numpy as np
import time
import random

class rps:
    '''
    A game of Rock, Paper, Scissors that randomly generates a choice for the computer and receives the player's input through video capture.
    It starts with a score limit that will cause the game to finish once it is reached.


    Parameters:
    -----------
    score_limit: int
        The number of wins required to finish the game.
    

    Attributes:
    -----------
    model: keras model
        The model that I have trained to differentiate between rock, paper, scissors signs.
    data: numpy array
        The array that will contain the visual data from the webcam to be interpreted by the model.
    score_limit: int
        The number of wins required to finish the game. Equal to the score_limit parameter
    computer_score: int
        The number of wins that the computer has achieved. Starts at 0.
    user_score: int
        The number of wins the player has achieved. Starts at 0
    options: list
        A list of the options you can choose to play in rock, paper, scissors.
    

    Methods:
    ----------
    get_prediction()
        Determines the player's choice through video capture.
    get_computer_choice()
        Randomly generates the computer's choice.
    get_user_choice()
        Calls get_prediction until a valid choice is received and returns that choice.
    get_winner(computer_choice, user_choice)
        Compares the output of get_computer_choice and get_user_choice and returns who was the winner.
    play()
        Repeatedly runs rounds of rock, paper, scissors until the score limit is reached.
    '''

    def __init__(self, score_limit=3):
        self.model = load_model('keras_model.h5')
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
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

        '''
        Determines the player's choice through video capture.
        
        Once the capture starts, a countdown is shown to the player. 
        When the countdown finishes the image shown at that moment is interpreted according to the model and a prediction is output.
        '''

        cap = cv2.VideoCapture(0)
        labels = ['rock', 'paper', 'scissors', 'nothing']
        print('Image capture starting...')
        start = time.time()
        while True:
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1
            self.data[0] = normalized_image
            runtime = time.time() - start
            if 1.5 < runtime < 3 :
                cv2.putText(frame, "CHOICE LOCKED IN...", (90,390), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 3)
            elif 3.5 < runtime < 4:
                cv2.putText(frame, "3", (280,270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5)
            elif 4.5 < runtime < 5:
                cv2.putText(frame, "2", (280,270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5)
            elif 5.5 < runtime < 6:
                cv2.putText(frame, "1", (280,270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 5)
            elif runtime > 6.5:
                cv2.putText(frame, "LOCKED!", (180,270), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,180,0), 5)
            cv2.imshow('frame', frame)
            if runtime > 6.7:
                prediction = self.model.predict(self.data)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                prediction = [0,0,0,1]
                break
        cv2.destroyAllWindows()
        cap.release()
        return labels[np.argmax(prediction)]
    

    def get_computer_choice(self):

        '''
        Randomly generates a choice for the computer.
        '''

        computer_choice = random.choice(self.options)
        return computer_choice

    
    def get_user_choice(self):

        '''
        Calls get_prediction and determines if the predicted choice is valid.
        
        If it is not, the player is prompted to input make choice again.
        Once a valid input is detected the choice is returned.
        '''

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

        '''
        Compares the output of get_computer_choice and get_user_choice and returns who was the winner.

        The choices are compared using an array of possible outcomes, win_matrix. 
        The first index corresponds to the index of computer_choice in the options list. 
        The second index corresponds to the index of user_choice in the options list. 

        Parameters:
        -----------
        computer_choice: str
            The choice the computer is playing.
        user_choice: str
            The choice the user is playing.
        '''

        win_matrix = np.array([     ['draw', 'user', 'comp'],
                                    ['comp', 'draw', 'user'],
                                    ['user', 'comp', 'draw']    ])

        winner = win_matrix[self.options.index(computer_choice),self.options.index(user_choice)]
        return winner

    
    def play(self):

        '''
        Repeatedly runs rounds of rock, paper, scissors until the score limit is reached.
        
        When a round is played, if there is a winner a point is added to the winner's score.
        Once the score limit is reached, a statement is output indicating the winner and the game finishes.
        '''

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