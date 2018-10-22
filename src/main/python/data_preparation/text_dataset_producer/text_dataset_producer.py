import collections


class TextDatasetProducer:

    def build_dataset_from_word_list(self, words :list, number_of_words :int) -> tuple:
        """Process raw inputs into a dataset."""
        count = [['UNKNOWN', -1]]
        count.extend(collections.Counter(words).most_common(number_of_words - 1))
        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)
        data = list()
        unk_count = 0
        for word in words:
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNKNOWN']
                unk_count += 1
            data.append(index)
        count[0][1] = unk_count
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return data, count, dictionary, reversed_dictionary

    def build_dataset_from_text(self, text :str, number_of_words :int) -> tuple:
        return self.build_dataset_from_word_list(text.split(), number_of_words)

