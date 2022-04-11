import glob
import string
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk import stem
import glob

porter_stemmer = stem.PorterStemmer()
stop_words = set(stopwords.words('english'))
abbreviation_file = open("abrevieri", "r")
abbreviation = {}
for line in abbreviation_file:
    line = line.replace("\n", "").split(" ")
    abbreviation[line[0]] = line[1]


def clean_text(text):
    for key, value in abbreviation.items():
        text = text.replace(key, value)
    for sign in string.punctuation:
        text = text.replace(sign, "")
    text = text.replace("\t", "")
    for x in "0123456789":
        text = text.replace(x, "")
    text = text.lower()
    return text


def extract_all_words_from_a_file(file_name):
    words = []
    my_tree = ET.parse(file_name)
    my_root = my_tree.getroot()
    for text in my_root.findall("text"):
        for paragraph in text.findall("p"):
            paragraph.text = clean_text(paragraph.text)
            for word in paragraph.text.split(" "):
                if word not in stop_words:
                    words.append(porter_stemmer.stem(word))
    words = [x for x in words if x != '']
    words = list(dict.fromkeys(words))
    return words


def extract_all_words_from_folder(folder_name):
    all_files = glob.glob(folder_name)
    words = []
    for file in all_files:
        words = words + extract_all_words_from_a_file(file)
    words = list(dict.fromkeys(words))
    words.sort()
    output_file_words = open("all_words.txt", "w")
    for word in words:
        output_file_words.write(word + " ")
    output_file_words.close()


def determine_topics_for_file(file_name):
    topics = []
    my_tree = ET.parse(file_name)
    my_root = my_tree.getroot()
    for metadata in my_root.findall("metadata"):
        for codes in metadata.findall("codes"):
            if codes.attrib.popitem()[1] == "bip:topics:1.0":
                for code in codes.iter("code"):
                    for topic in code.attrib.values():
                        topics.append(topic)
    return topics


def determine_frequency_vector_for_file(file_name, frequency_dict):
    my_tree = ET.parse(file_name)
    my_root = my_tree.getroot()
    words = dict(frequency_dict)
    for text in my_root.findall("text"):
        for paragraph in text.findall("p"):
            paragraph.text = clean_text(paragraph.text)
            for word in paragraph.text.split(" "):
                if word not in stop_words and porter_stemmer.stem(word) in words.keys():
                    words[porter_stemmer.stem(word)] += 1
    return words


def determine_frequency_vectors_of_each_file_in_directory(folder_name, frequency_dict):
    all_files = glob.glob(folder_name)
    output_file_words = open("frequency_vectors", "a+")
    output_file_words.truncate(0)
    for key in frequency_dict.keys():
        if key != "":
            output_file_words.writelines("@attribute " + key + "\n")
    output_file_words.writelines("@data\n")
    for file in all_files:
        words = determine_frequency_vector_for_file(file, frequency_dict)
        if len(words) != 0:
            output_file_words.write(file.title().split("\\")[1].replace(".Xml", "") + " # ")
            for key, value in words.items():
                if value != 0:
                    output_file_words.write(str(list(words.keys()).index(key)) + ":" + str(value)+" ")
            output_file_words.writelines("# ")
            for topic in determine_topics_for_file(file):
                output_file_words.write(topic + " ")
            output_file_words.write("\n")
    output_file_words.close()


def print_all_words_for_file(file_name):
    words = []
    file = open(file_name, "r")
    my_tree = ET.parse(file)
    my_root = my_tree.getroot()

    for text in my_root.findall("text"):
        for paragraph in text.findall("p"):
            paragraph.text = clean_text(paragraph.text)
            for word in paragraph.text.split(" "):
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
    # print words for file
    # print_all_words_for_file("Reuters_34/2504NEWS.XML")
