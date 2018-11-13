import os

def load_texts_and_labels(text_file_root_folder :str, training_text_files_folder :str, validation_text_files_folder :str):
    """
    TODO : suppress copy/paste in the code
    TODO : extract in a loading class
    TODO : add randomization
    :param text_file_root_folder:
    :param training_text_files_folder:
    :param validation_text_files_folder:
    :return:
    """
    training_texts = []
    training_labels = []
    validation_texts = []
    validation_labels = []

    for input_subdir_name in os.listdir(text_file_root_folder + '/' + training_text_files_folder):
        label = input_subdir_name
        for text_file_name in os.listdir(text_file_root_folder + '/' + training_text_files_folder + '/' + input_subdir_name):
            text_file = open(text_file_root_folder + '/' + training_text_files_folder + '/' + input_subdir_name + '/' + text_file_name, 'r')
            training_texts.append(text_file.read())
            training_labels.append(label)
    for input_subdir_name in os.listdir(text_file_root_folder + '/' + validation_text_files_folder):
        label = input_subdir_name
        for text_file_name in os.listdir(text_file_root_folder + '/' + validation_text_files_folder + '/' + input_subdir_name):
            text_file = open(text_file_root_folder + '/' + validation_text_files_folder + '/' + input_subdir_name + '/' + text_file_name, 'r')
            validation_texts.append(text_file.read())
            validation_labels.append(label)
    return training_texts, training_labels, validation_texts, validation_labels
