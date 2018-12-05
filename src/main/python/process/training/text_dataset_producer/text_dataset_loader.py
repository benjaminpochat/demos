import os
import random

class TextAndLabelLoader:

    def __init__(self):
        self._training_texts = []
        self._training_labels = []
        self._validation_texts = []
        self._validation_labels = []
        self._label_dict = {}
        self._label_index = 0

    def load_texts_and_labels(
            self,
            text_file_root_folder: str,
            training_text_files_folder: str,
            validation_text_files_folder: str):
        """
        :param text_file_root_folder:
        :param training_text_files_folder:
        :param validation_text_files_folder:
        :return:
        """

        self._load_text_files_foldered_by_label(
            text_file_root_folder,
            training_text_files_folder,
            self._training_texts,
            self._training_labels)
        self._load_text_files_foldered_by_label(
            text_file_root_folder,
            validation_text_files_folder,
            self._validation_texts,
            self._validation_labels)
        self._training_texts, self._training_labels = self.shuffle_texts_and_labels(self._training_texts, self._training_labels)
        return self._training_texts, self._training_labels, self._validation_texts, self._validation_labels

    def _load_text_files_foldered_by_label(
            self,
            text_file_root_folder: str,
            text_files_folder: str,
            texts: list,
            labels: list):
        for input_subdir_name in os.listdir(text_file_root_folder + '/' + text_files_folder):
            self._load_text_files_from_label_folder(
                input_subdir_name,
                text_file_root_folder,
                text_files_folder,
                texts,
                labels)
        return self._label_index

    def _load_text_files_from_label_folder(
            self,
            input_subdir_name: str,
            text_file_root_folder: str,
            text_files_folder: str,
            texts,
            labels):
        label = input_subdir_name
        if label not in self._label_dict:
            self._label_dict[label] = self._label_index
            self._label_index = self._label_index + 1
        label_folder_path = text_file_root_folder + '/' + text_files_folder + '/' + input_subdir_name
        for text_file_name in os.listdir(label_folder_path):
            text_file = open(label_folder_path + '/' + text_file_name, 'r')
            texts.append(text_file.read())
            labels.append(self._label_dict[label])

    def shuffle_texts_and_labels(self, texts, labels):
        random_indices = [i for i in range(0, len(texts))]
        random.shuffle(random_indices)
        shuffled_texts = []
        shuffled_labels = []
        for j in range(0, len(texts)):
            shuffled_texts.append(texts[random_indices[j]])
            shuffled_labels.append(labels[random_indices[j]])
        return shuffled_texts, shuffled_labels
