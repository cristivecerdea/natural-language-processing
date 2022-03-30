import glob
import string
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
import glob


def extract_all_words_from_folder(folder_name):
    all_files = glob.glob(folder_name)
    abbreviation_file = open("abrevieri", "r")

    abbreviation = {}
    for line in abbreviation_file:
        line = line.replace("\n", "").split(" ")
        abbreviation[line[0]] = line[1]
    words = []
    stop_words = set(stopwords.words('english'))
    for file in all_files:
        my_tree = ET.parse(file)
        my_root = my_tree.getroot()

        for text in my_root.findall("text"):
            for paragraph in text.findall("p"):
                for key, value in abbreviation.items():
                    paragraph.text = paragraph.text.replace(key, value)
                for char in string.punctuation:
                    paragraph.text = paragraph.text.replace(char, " ")
                paragraph.text = paragraph.text.replace("\t", "")
                for x in "0123456789":
                    paragraph.text = paragraph.text.replace(x, "")
                for word in paragraph.text.split(" "):
                    word = word.lower()
                    if word not in stop_words:
                        words.append(word)
        words = [x for x in words if x != '']
        words = list(dict.fromkeys(words))
        words.sort()

    output_file_words = open("all_words.txt", "w")
    for word in words:
        output_file_words.write(word + " ")
    output_file_words.close()


def determine_frequency_vectors_of_each_file_in_directory(folder_name, frequency_dict):
    all_files = glob.glob(folder_name)
    abbreviation_file = open("abrevieri", "r")

    abbreviation = {}
    for line in abbreviation_file:
        line = line.replace("\n", "").split(" ")
        abbreviation[line[0]] = line[1]

    stop_words = set(stopwords.words('english'))
    for file in all_files:
        my_tree = ET.parse(file)
        my_root = my_tree.getroot()
        words = dict(frequency_dict)
        for text in my_root.findall("text"):
            for paragraph in text.findall("p"):
                for key, value in abbreviation.items():
                    paragraph.text = paragraph.text.replace(key, value)
                for char in string.punctuation:
                    paragraph.text = paragraph.text.replace(char, " ")
                paragraph.text = paragraph.text.replace("\t", "")
                for x in "0123456789":
                    paragraph.text = paragraph.text.replace(x, "")
                for word in paragraph.text.split(" "):
                    word = word.lower()
                    if word not in stop_words and word in words.keys():
                        words[word] += 1
        file_name = file.split("\\")[1].replace(".XML", ".txt")
        output_file_words = open("frequency_vectors\\"+file_name, "w")
        for key, value in words.items():
            output_file_words.writelines(key + " " + str(value) + "\n")
        output_file_words.close()


def print_all_words_for_file(file_name):
    abbreviation_file = open("abrevieri", "r")

    abbreviation = {}
    for line in abbreviation_file:
        line = line.replace("\n", "").split(" ")
        abbreviation[line[0]] = line[1]
    words = []
    stop_words = set(stopwords.words('english'))
    file = open(file_name, "r")
    my_tree = ET.parse(file)
    my_root = my_tree.getroot()

    for text in my_root.findall("text"):
        for paragraph in text.findall("p"):
            for key, value in abbreviation.items():
                paragraph.text = paragraph.text.replace(key, value)
            for char in string.punctuation:
                paragraph.text = paragraph.text.replace(char, " ")
            paragraph.text = paragraph.text.replace("\t", "")
            for x in "0123456789":
                paragraph.text = paragraph.text.replace(x, "")
            for word in paragraph.text.split(" "):
                word = word.lower()
                if word not in stop_words:
                    words.append(word)
    words = [x for x in words if x != '']
    words.sort()
    print(words)


if __name__ == "__main__":
    directory_name = "Reuters_34/*"
    # extracts all the words form the text tag from all files in folder
    extract_all_words_from_folder(directory_name)

    # creates the frequency vectors for all the files in the given directory
    words_file = open("all_words.txt", "r")
    words_list = words_file.read().split(" ")
    freq_vector = {}
    for item in words_list:
        freq_vector[item] = 0
    determine_frequency_vectors_of_each_file_in_directory(directory_name, freq_vector)

    #print words for file
    print_all_words_for_file("Reuters_34/2538NEWS.XML")
