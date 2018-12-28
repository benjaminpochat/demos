from tensorflow.python.keras import models
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


class Predicter:
    def __init__(self, model: models, vocabulary: dict):
        self._model = model
        self._vocabulary = vocabulary

    def predict(self, text_content: str):
        tf_idf_vectorizer = TfidfVectorizer(ngram_range=(1,2),
                                            dtype='int32',
                                            strip_accents='unicode',
                                            decode_error='replace',
                                            analyzer='word',
                                            min_df=2,
                                            vocabulary=self._vocabulary)
        vectorized_texts = tf_idf_vectorizer.fit_transform(text_content)
        labels = self._model.predict(vectorized_texts, verbose=1)
        print(labels)


if __name__ == '__main__':
    model = models.load_model('mlp_model.h5')
    vocabulary = pickle.load(open('vocabulary.pkl', 'rb'))
    predicter = Predicter(model=model, vocabulary=vocabulary)
    text1 = open('text1.txt', 'r').read()
    text2 = open('text2.txt', 'r').read()
    text3 = open('text3.txt', 'r').read()
    text4 = open('text4.txt', 'r').read()
    text5 = open('text5.txt', 'r').read()
    predicter.predict(text_content=[text1, text2, text3, text4, text5])
