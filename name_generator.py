import csv
import random

_MARKOV_DEPTH = 2
_MIN_LEN = 4
_MAX_LEN = 12
_NAMES_TO_GENERATE = 20
_NICKNAME_CHANCE = 0.1
# Chance nickname is form "Strong-Arms" rather than "The Strong"
_NICKNAME_BODY_TYPE_CHANCE = 0.6
# [sson/bur/dottir, place, god, none]
_SURNAME_CHANCES_RAW = [4, 4, 2, 1]
_SURNAME_CHANCES = "S" * _SURNAME_CHANCES_RAW[0] + \
                   "P" * _SURNAME_CHANCES_RAW[1] + \
                   "G" * _SURNAME_CHANCES_RAW[2] + \
                   "N" * _SURNAME_CHANCES_RAW[3]
_LETTERS = {}
_GODS = []
_LOCS = []
_DESC = []
_BODY = []


def load_data():
    load_letters()
    load_gods()
    load_locations()
    load_descriptors()
    load_body()


def load_letters():
    with open('data/names.csv', newline='') as csvfile:
        name_reader = csv.reader(csvfile)
        for row in name_reader:
            name = row[0] + "*"
            for i in range(len(name)):
                start_index = max(i - _MARKOV_DEPTH, 0)
                str_slice = name[start_index:i]
                next_letter = name[i]
                if str_slice not in _LETTERS.keys():
                    _LETTERS[str_slice] = {}
                if next_letter not in _LETTERS[str_slice].keys():
                    _LETTERS[str_slice][next_letter] = 1
                else:
                    _LETTERS[str_slice][next_letter] += 1


def load_gods():
    with open('data/gods.csv', newline='') as csvfile:
        god_reader = csv.reader(csvfile)
        for row in god_reader:
            _GODS.append(row[0])


def load_locations():
    with open('data/place_names.csv', newline='') as csvfile:
        loc_reader = csv.reader(csvfile)
        for row in loc_reader:
            _LOCS.append(row[0])
    with open('data/bernen_districts.csv', newline='') as csvfile:
        loc_reader = csv.reader(csvfile)
        for row in loc_reader:
            _LOCS.append(row[0])


def load_descriptors():
    with open('data/descriptors.csv', newline='') as csvfile:
        desc_reader = csv.reader(csvfile)
        for row in desc_reader:
            _DESC.append(row[0])


def load_body():
    with open('data/body.csv', newline='') as csvfile:
        body_reader = csv.reader(csvfile)
        for row in body_reader:
            _BODY.append(row[0])


def generate_given_name():
    name = ''
    while True:
        start_index = max(len(name) - _MARKOV_DEPTH, 0)
        str_slice = name[start_index:len(name)]
        letter_choices = ''
        for letter in _LETTERS[str_slice].keys():
            letter_choices += letter * _LETTERS[str_slice][letter]

        if len(letter_choices) == 0:
            name = ''
        else:
            chosen_letter = random.choice(letter_choices)
            if chosen_letter == '*':
                if len(name) < _MIN_LEN:
                    name = ''
                else:
                    return name
            else:
                name += chosen_letter
                if len(name) > _MAX_LEN:
                    name = ''


load_data()
for i in range(_NAMES_TO_GENERATE):
    forename = generate_given_name()
    forename = forename[0].upper() + forename[1:]
    surname_type = random.choice(_SURNAME_CHANCES)
    surname = ''
    if surname_type == 'S':
        surname = generate_given_name()
        surname_suffix = random.choice(["bur", "sson", "dottir"])
        if surname[-1] == surname_suffix[0]:
            if surname[-2] == surname_suffix[0]:
                surname_suffix = surname_suffix[2:]
            else:
                surname_suffix = surname_suffix[1:]
        surname += surname_suffix
        surname = surname[0].upper() + surname[1:]
    elif surname_type == 'P':
        surname = "of " + random.choice(_LOCS)
    elif surname_type == 'G':
        surname = random.choice(_GODS) + 'gard'

    #nickname
    if random.random() < _NICKNAME_CHANCE:
        #body type
        if random.random() < _NICKNAME_BODY_TYPE_CHANCE:
            nickname = random.choice(_DESC) + "-" + random.choice(_BODY)
            surname = "\"" + nickname + "\" " + surname
        else:
            nickname = "The " + random.choice(_DESC)
            if surname:
                surname += " \"" + nickname + "\""
            else:
                surname = "\"" + nickname + "\""

    print(forename + " " + surname)
