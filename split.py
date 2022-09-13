"""
Contact me:
   e-mail:   enrique@enriquecatala.com 
   Linkedin: https://www.linkedin.com/in/enriquecatala/
   Web:      https://enriquecatala.com
   Twitter:  https://twitter.com/enriquecatala
   Support:  https://github.com/sponsors/enriquecatala
   Youtube:  https://www.youtube.com/enriquecatala
Description
----
    This script splits the training data into train and test sets.This will split randomly into train and test the IOB file       
    Helper script to shuffle and split between train and test a file containing [IOB format](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)).
This is usually used when working with NLP tasks like Named Entity Recognition.
NOTE: Please, be aware that i´m using the split from memory, so if you have a big file, it will be slow or crash if file does´nt fit in memory
Input
----
    input_file
        File with the IOB tagged phrases
    percentage_train
        Percentage of the data to be used for training
    output_folder
        Folder where the output files will be saved
Output
----
    Two files inside the output folder:
        train.iob
        test.iob
    Phrases will be randomly splitted into train and test sets
"""


import sys
import argparse
import random

if __name__=='__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_file', type=str, help='Input file', default='data/train_bioes.txt')
    argparser.add_argument('percentage_train', type=float, help='Percentage of train', default=0.9)
    argparser.add_argument('output_folder', type=str, help='Output folder', default='./')

    # check if debug mode
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace():
        #Simulate the args to be expected
        argv = ["data/train_bioes.txt","0.9","split_data"]
        # Parse arguments
        args = argparser.parse_args(argv)
    else:
        args = argparser.parse_args()

    input_file = args.input_file
    percentage_train = args.percentage_train
    output_folder = args.output_folder

    phrases = []    
    # read the input_file and count empty lines
    with open(input_file, 'r') as f:
        lines = f.readlines()        
        # number of phrases = number of \n lines
        num_phrases = 0
        phrase = []
        for line in lines:
            phrase.append(line)
            if line == '\n':
                num_phrases += 1
                phrases.append(phrase)
                phrase = []
        
    # number of phrases detected
    print('Number of phrases detected: {}'.format(num_phrases))
    
    # Number of train_phrases
    train_phrases = int(num_phrases * percentage_train)
    print("Train phrases: {}".format(train_phrases))
    # Number of test_lines
    test_phrases = num_phrases - train_phrases
    print("Dev phrases: {}".format(test_phrases))
    
    # Shuffling phrases
    print("Shuffling phrases randomly...")
    random.shuffle(phrases)

    print(f"Writting data to folder: {output_folder}")
    # read the input_file and write each line to a new file
    train_phrases_written = 0
    
    with open(f'{output_folder}/train.txt', 'w') as f_train:
        with open(f'{output_folder}/dev.txt', 'w') as f_test:
            for phrase in phrases:
                if train_phrases_written < train_phrases:
                    f_train.write(''.join(phrase))
                    train_phrases_written += 1
                else:
                    f_test.write(''.join(phrase))

    print("Done!")