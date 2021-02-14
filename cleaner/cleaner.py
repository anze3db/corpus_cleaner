# locila .,:;?＂!。，；：？！‚¿¡…'"‘’`“”„()<=>[]{}«»‹›《》-–—一*
# ohranjanje velikih zacetnic
import csv
import os
import re

def main():
    rules = get_rules()
    process_files(rules)

def get_rules():
    rules = []
    with open('rules.csv') as csvfile:
        rulereader = csv.reader(csvfile, delimiter=',')
        for row in rulereader:
            rules.append(row)

    return rules

def process_files(rules):
    EXISTING_CORPUS = 'existing-corpus'

    for root, dirs, files in os.walk(EXISTING_CORPUS):
        for filename in files:
            old_file = open(EXISTING_CORPUS + '/' + filename)
            new_file = create_new_file(filename) 

            for line in old_file.readlines():
                line = apply_rules(line, rules)
                new_file.write(line)

            old_file.close()
            new_file.close()

def create_new_file(filename):
    NEW_CORPUS = 'new-corpus'
    try:
        os.remove(NEW_CORPUS + '/' + filename)
    except OSError:
        print('File did not exist before!')
        pass

    file = open(NEW_CORPUS + '/' + filename, 'a+')  # open file in append mode - write mode also works
    return file


def apply_rules(line, rules):
    for rule in rules:
        if rule[1] == 'x':
            # remove all occurences 
            line = line.lower().replace(rule[0].lower(), '')
        else:
            # replace all occurences with rule[1]
            line = line.lower().replace(rule[0].lower(), rule[1].lower())
    return line

main()