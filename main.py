from spy_details import spy, Spy, ChatMessage, friends
from message import Steganography
from datetime import datetime
import getpass
import string
import colour

STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.', 'Keeping the British end up, Sir']



print "Hello! Let\'s get started"

question = "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)?  "
existing = raw_input((question))


def add_status(current_status_message):
    updated_status_message = None

    if current_status_message != None:
        print 'Your current status message is %s \n' % (current_status_message)
    else:
        print 'You don\'t have any status message currently \n'

    default = raw_input("Do you want to select from the older status (y/n)? ")

    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")

        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = raw_input("\nChoose from the above messages ")

        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print 'The option you chose is not valid! Press either y or n.'

    if current_status_message:
        print 'Your updated status message is: %s' % (current_status_message)
    else:
        print 'You current don\'t have a status update'

    return updated_status_message


def add_friend():
    new_friend = Spy('', '', 0, 0.0)
    new_friend.name = raw_input("Please add your friend's name: \n")

    if set('[special symbols":;\']+$ " "').intersection(new_friend):
        print "Invalid entry."
    else:
        print new_friend

    new_friend.salutation = raw_input("Formal Salutation: Mr. or Ms. or Mrs. \n")
    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?\n")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?\n")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating>= spy.rating:
        friends.append(new_friend)
        print 'New Friend Added!\n'
    else:
        print "Sorry! Invalid entry. We can\'t add spy with the details you provided!!\n"

    return len(friends)

def select_a_friend():
    item_number = 0

    for friend in friends:
        print '%d. %s aged %d with rating %.2f is online' % (item_number + 1, friend['name'],
                                                             friend['age'],
                                                             friend['rating'])
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")

    friend_choice_position = friend_choice - 1
    #base index=1

    return friend_choice_position


def send_message():
    friend_choice = select_a_friend()

    original_image = raw_input("What is the name of the image?")
    output_path = "output.jpg"
    text = raw_input("What do you want to say? ")
    if len(text) == 0:
        print 'Speak up!\n'
    elif text ==  'In serious trouble'or 'Save Me' or 'M stuck\n':
        print 'Hold on!'
    elif text == 'incorrect' or 'Hack' or '#' or '&':
        #special symbols r invalid
        print 'Spychat isnt for kids!\n'

    else:
        print 'You are good to go!\n'

    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text, True)

    friends[friend_choice].chats.append(new_chat)

    print "Your secret message image is ready!"

def read_message():
    sender = select_a_friend()

    output_path = raw_input("What is the name of the file?")

    hidden_text = Steganography.decode(output_path)

    print hidden_text

    new_chat = ChatMessage(hidden_text, False)

    friends[sender].chats.append(new_chat)
    # new chats r added
    words = hidden_text.split(' ')
    print 'words in the secret message is : ' + str(len(words))
    print 'hidden text has been saved! ;)\n'


def read_chat_history():
    read_for = select_a_friend()

    print '\n'
    #show friends

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print(chat.time.startime("%d %B %Y"), 'yellow')
            print('Your words:', 'green')
            print chat.message
        else:
            print(chat.time.startime("%d %B %Y"), 'yellow')
            print(friends[read_for].name + ' word: ', 'green')
            print chat.message


def start_chat(spy):
    current_status_message = None

    spy.name = spy.salutation + " " + spy.name
    if spy.age > 12 and spy.age < 50:
        print "Authentication complete. Welcome " + spy.name + " age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard"

        show_menu = True

        while show_menu:
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Select a Friend \n 4. Send a secret message \n 5. Read a secret message \n 6. Read Chats from a user \n 7. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = raw_input(menu_choice)

                # Set status
                if menu_choice == 1:
                    current_status_message = add_status(current_status_message)
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                else:
                    show_menu = False
    else:
        print 'Sorry you are not of the correct age to be a spy'


if existing.upper() == "Y":

    pswd = getpass.getpass('Password:\n')

    if pswd == 'valid':
        start_chat(Spy)

    else:
        print 'Wrong Password!Try Again'
else:

    spy = Spy('', '',0,0.0)
    spy.name = raw_input("Hello Spy! Please tell us your name : \n")

    if len(spy.name) > 0:
        invalidchar = set(string.specialcharacters.replace('_', ' '))
        if any(char in invalidchar for char in spy.name):
            print 'no name no spy '
        else:

            spy.salutation = raw_input("Should I call you Mr. or Mrs. or Ms.?: \n")

            spy.age = raw_input("What is your age?\n")
            spy.age = int(spy.age)

            spy.rating = raw_input("What is your spy rating?\n")
            spy.rating =float(spy.rating)

        start_chat(spy)