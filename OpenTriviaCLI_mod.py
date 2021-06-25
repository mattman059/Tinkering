#!/usr/bin/env python3
import requests
import json
import html
import random
import time
import sys
import argparse
#### URLS ####
get_token_url = 'https://opentdb.com/api_token.php?command=request'
base_url = 'https://opentdb.com/api.php?'
lookup_categorys_url = 'https://opentdb.com/api_category.php'
lookup_category_url = 'https://opentdb.com/api_count.php?category='
#### VARS ####
token = ""
amount = 5

global run
run = True
logo = '''
   ____                     _______   _       _          _____ _      _____ 
  / __ \                   |__   __| (_)     (_)        / ____| |    |_   _|
 | |  | |_ __   ___ _ __      | |_ __ ___   ___  __ _  | |    | |      | |  
 | |  | | '_ \ / _ \ '_ \     | | '__| \ \ / / |/ _` | | |    | |      | |  
 | |__| | |_) |  __/ | | |    | | |  | |\ V /| | (_| | | |____| |____ _| |_ 
  \____/| .__/ \___|_| |_|    |_|_|  |_| \_/ |_|\__,_|  \_____|______|_____|
        | |                                                                 
        |_|                                                                 '''
version = "1.0"

def intro():
    print_logo()
    print('Hello and welcome to Open Trivia CLI')
    print('Write "help" to get help')

def print_logo(): # Print Ascii Logo
    print("\033c", end="") # Clear the Terminal
    print(logo)
    print()

def make_request(url):
    r = requests.get(url) 
    if r.status_code > 301:
        print(f"Error: Status code: {r.status_code}")
    else:
        return r

def get_token(url):
    r = make_request(url)
    return r.json()['token']

def get_questions(**kwargs):
    run = True
    global token
    if token == "": # Check if token exits
        token = get_token(get_token_url) # Get new token

    # check if category is available
    categorys_url = f"{lookup_category_url}{kwargs['category']}"
    categorys = make_request(categorys_url)
    try:
        categorys.json()
    except:
        if kwargs['category'] != "":
            run = False
    if run:
        url = base_url + f"amount={amount}&token={token}" # Create URL with amount and token
        for key, value in kwargs.items(): # Add custom properties
            url = url + f"&{key}={value}"
        r = make_request(url) #Make request
        return r.json()
    else:
        print('Category ID is not available, please check "?" for IDs')

def ask_questions(questions):
    question_counter = 0
    question_amount = len(questions['results'])
    right_answers = 0
    wrong_answers = 0
    percent_correct = 0
    for question in questions['results']:
        #print_logo()
        run = True
        counter = 1
        drawn_answers = 0
        print(f'Question number: {question_counter + 1}/{question_amount}')
        print(html.unescape(question['question']))
        answer_counter = len(question['incorrect_answers']) + 1
        right_answer = random.randint(1, answer_counter)
        question_counter = question_counter + 1
        while counter <= answer_counter:
            if counter == right_answer:
                answer = question['correct_answer']
            else:
                answer = question['incorrect_answers'][drawn_answers]
                drawn_answers = drawn_answers + 1
            print(f'{counter}. {html.unescape(answer)}')
            counter = counter +1
        while run:
            user_input_is_int = True
            user_input = input(">> ")
            try:
                user_input = int(user_input)
            except:
                user_input_is_int = False
                print(f'Please specifiy a number between 1 and {answer_counter}')
            if user_input_is_int:
                if user_input == right_answer:
                    print(f'Correct!')
                    right_answers = right_answers + 1
                else:
                    print(f'Wrong, answer {right_answer} was right ({html.unescape(question["correct_answer"])})')
                    wrong_answers = wrong_answers + 1
                run = False
                percent_correct = round((100 / (right_answers + wrong_answers) * right_answers),2)
                
                print(f'You had {right_answers}/{right_answers + wrong_answers} answer(s) right ({round((100 / (right_answers + wrong_answers) * right_answers), 2)})%')
                time.sleep(2.5)

    #print_logo()
    try:
        print(f'You had {right_answers}/{right_answers + wrong_answers} answer(s) right ({round((100 / (right_answers + wrong_answers) * right_answers), 2)})%')
    except ZeroDivisionError:
        pass
    if percent_correct >= 80:
        
        print("YOU WIN!")
        sys.exit(0)
    else:
        questions = get_questions(amount=amount, type='boolean', category=9, difficulty='easy')
        ask_questions(questions)
        
        
    input("Press any key to continue...")
    intro()

def print_categorys(): # Print all available categorys
    categorys = make_request(lookup_categorys_url)
    for category in categorys.json()['trivia_categories']:
        print(f"{category['name']} | {category['id']}, ")

def new_questions(question_type,difficulty,category):
    run = True
    if run:
        questions = get_questions(amount=amount, type=question_type, category=category, difficulty=difficulty)
        if questions != None:
            ask_questions(questions)
        else:
            print('Send N to retry')
    else:
        print('Send N to retry')

def user_input_handler(user_input):
    user_input = user_input.lower()
    if user_input == '?':
        print_categorys()
    elif user_input in ['v', 'version']:
        print(f"Version: {version}")
    elif user_input in ['q', 'exit', 'quit']:
        print("Bye!")
    elif user_input in ['new', 'n']:
        new_questions()
    else:
        print("Help:")
        print('     Write "n" to start a new game')
        print('     Write "?" to get a list of categorys')
        print('     Write "q" to exit the programm')
        print('     Write "v" to get the version')

# Main loop
intro()
while run:
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str)
    parser.add_argument('--category',type=int)
    parser.add_argument('--difficulty',type=str)
    args = parser.parse_args()
    
    new_questions(vars(args)['type'],\
                  vars(args)['difficulty'],\
                  vars(args)['category'])
