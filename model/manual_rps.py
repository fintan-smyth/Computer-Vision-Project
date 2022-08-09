
import random

def get_computer_choice():
    options = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(options)
    return computer_choice

def get_user_choice():
    valid = False
    while valid == False:
        user_choice = input('What is your choice? \n\n [ROCK] [PAPER] [SCISSORS]\n \n')
        if user_choice.lower() not in ['rock', 'paper', 'scissors']:
            print('Sorry, that is not a valid choice. \n')
        else:
            valid = True
    return user_choice

def get_winner(computer_choice, user_choice):
    if computer_choice == 'rock':
        if user_choice.lower() == 'rock':
            winner = 'draw'
        elif user_choice.lower() == 'paper':
            winner = 'user'
        elif user_choice.lower() == 'scissors':
            winner = 'comp'
    elif computer_choice == 'paper':
        if user_choice.lower() == 'rock':
            winner = 'comp'
        elif user_choice.lower() == 'paper':
            winner = 'draw'
        elif user_choice.lower() == 'scissors':
            winner = 'user'
    elif computer_choice == 'scissors':
        if user_choice.lower() == 'rock':
            winner = 'user'
        elif user_choice.lower() == 'paper':
            winner = 'comp'
        elif user_choice.lower() == 'scissors':
            winner = 'draw'
    return winner

def play():
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    winner = get_winner(computer_choice, user_choice)
    print(f'\nThe computer chose: {computer_choice}\n')
    if winner == 'draw':
        print('It was a draw.')
    elif winner == 'comp':
        print('Bad luck, the computer won.')
    elif winner == 'user':
        print('Congratulations! The player is the winner.')

if __name__ == '__main__':
    play()