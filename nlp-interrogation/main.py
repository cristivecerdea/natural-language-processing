from functions import *
import keyboard
import time
import collections


def interrogate_input_from_file():
    interrogation = "interrogation.txt"
    interrogation = prepare_interrogation(interrogation, freq_vector)
    print(interrogation)
    inter_normalized_vector = normalize_vector(interrogation, vectors)
    print(inter_normalized_vector)
    similarity_vector = {}
    for key in normalized_vectors.keys():
        cosine_similarity = calculate_cosine_similarity(inter_normalized_vector, normalized_vectors[key])
        similarity_vector[key] = cosine_similarity
    similarity_vector = dict(sorted(similarity_vector.items(), key=lambda item: item[1], reverse=True))
    i = 0
    for key, value in similarity_vector.items():
        print(key + str(value))
        i += 1
        if i > 10:
            break


if __name__ == '__main__':
    attributes = extract_attributes("frequency_vectors")
    freq_vector = create_freq_vector(attributes)
    vectors = extract_data("frequency_vectors")
    normalized_vectors = normalize_vectors(vectors)
    # print vectors
    for item in normalized_vectors.items():
        print(item)
    # print idf for attribute
    # for key, value in IDF_dict.items():
    #     print(key + str(value))
    print("press space for an interrogation and esc for exit")
    while True:
        if keyboard.is_pressed("space"):
            print("\binterrogation")
            interrogate_input_from_file()
            time.sleep(0.2)
            print("press space for an interrogation and esc for exit")
        if keyboard.is_pressed("esc"):
            print("esc pressed, ending loop")
            break

