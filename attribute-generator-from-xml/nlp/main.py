import string
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk import stem
import glob

porter_stemmer = stem.SnowballStemmer('english')
stop_words = set(stopwords.words('english'))
abbreviation_file = open("abrevieri", "r")
abbreviation = {}
for line in abbreviation_file:
    line = line.replace("\n", "").split("|")
    abbreviation[line[0]] = line[1]


def clean_text(text):
    for key, value in abbreviation.items():
        text = text.replace(key, value)
    for sign in string.punctuation:
        text = text.replace(sign, " ")
    text = text.replace("\t", "")
    for x in "0123456789":
        text = text.replace(x, "")
    text = text.lower()
    text = text.replace("\n", "")
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
    title = clean_text(extract_title_for_file(file_name))
    for word in title.split(" "):
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


def extract_title_for_file(file_name):
    my_tree = ET.parse(file_name)
    my_root = my_tree.getroot()
    text = "\n" + my_root.findall("title")[0].text
    return text


def extract_code_for_a_class(file_name, class_attrib):
    elements = []
    my_tree = ET.parse(file_name)
    my_root = my_tree.getroot()
    for metadata in my_root.findall("metadata"):
        for codes in metadata.findall("codes"):
            if codes.attrib.popitem()[1] == class_attrib:
                for code in codes.iter("code"):
                    for topic in code.attrib.values():
                        elements.append(topic)
    return elements


def determine_topics_for_file(file_name):
    return extract_code_for_a_class(file_name, "bip:topics:1.0")


def determine_countries_for_file(file_name):
    return extract_code_for_a_class(file_name, "bip:countries:1.0")


def determine_industries_for_file(file_name):
    return extract_code_for_a_class(file_name, "bip:industries:1.0")


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
    title = clean_text(extract_title_for_file(file_name))
    for word in title.split(" "):
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


def prepare_interrogation(file_name, frequency_dict):
    file = open(file_name, "r")
    text = file.read()
    text = clean_text(text)
    interrogation_words = {}
    for word in text.split(" "):
        if word not in stop_words:
            word = porter_stemmer.stem(word)
            if word in frequency_dict.keys():
                word_index = (list(frequency_dict.keys()).index(word))
                if word_index not in interrogation_words.keys():
                    interrogation_words[word_index] = 1
                else:
                    interrogation_words[word_index] += 1
    return dict(sorted(interrogation_words.items()))


def prepare_frequency_vector_from_word_file(file_name):
    words_file = open(file_name, "r")
    words_list = words_file.read().split(" ")
    freq_vector = {}
    for item in words_list:
        freq_vector[item] = 0
    return freq_vector


if __name__ == "__main__":
    directory_name = "Reuters_7083/*"
    # extracts all the words form the text tag from all files in folder
    extract_all_words_from_folder(directory_name)

    # creates the frequency vectors for all the files in the given directory
    freq_vector = {}
    freq_vector = prepare_frequency_vector_from_word_file("all_words.txt")
    determine_frequency_vectors_of_each_file_in_directory(directory_name, freq_vector)
    # print words for file
    # print_all_words_for_file("Reuters_34/2504NEWS.XML")
    # extract countries from a file
    # print(determine_countries_for_file("Reuters_34\\2504NEWS.XML"))
    # extract title from file
    # extract_title_for_file("Reuters_34\\2504NEWS.XML")
