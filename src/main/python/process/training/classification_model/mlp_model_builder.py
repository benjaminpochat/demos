import tensorflow as tf

from tensorflow.python.keras import models
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from src.main.python.process.training.text_dataset_producer.text_ngrams_vectorizer import NgramVectorizer



class MlpModelBuilder:
    """
    A class for building multi layer perceptron model
    See https://developers.google.com/machine-learning/guides/text-classification/step-4#build_n-gram_model_option_a
    """
    def __init__(self,
                 layers_number :int = 2,
                 unit_number :int = 64,
                 dropout_rate :float = 0.2):
        self._layers_number = layers_number
        self._unit_number = unit_number
        self._dropout_rate = dropout_rate

    def build_model(self,
                          data,
                          learning_rate=1e-3,
                          epochs=1000,
                          batch_size=128):
        """Trains n-gram model on the given dataset.

        # Arguments
            data: tuples of training and validation texts and labels.
            learning_rate: float, learning rate for training model.
            epochs: int, number of epochs.
            batch_size: int, number of samples per batch.
            layers: int, number of `Dense` layers in the model.
            units: int, output dimension of Dense layers in the model.
            dropout_rate: float: percentage of input to drop at Dropout layers.

        # Raises
            ValueError: If validation data has label values which were not seen
                in the training data.
        """
        # Get the data.
        (training_texts, training_labels), (validation_texts, validation_labels) = data

        self._verify_data(validation_labels)

        vectorizer = NgramVectorizer()
        training_vector, validation_vector = vectorizer.ngram_vectorize(training_texts, training_labels, validation_texts)

        self._create_mlp_model(input_shape=training_vector.shape[1:])

        self._compile_model(learning_rate)

        self._train_model(
            batch_size,
            epochs,
            training_vector,
            training_labels,
            validation_vector,
            validation_labels)

        #self._model.save('IMDb_mlp_model.h5')

    def _verify_data(self, validation_labels):
        # Verify that validation labels are in the same range as training labels.
        unexpected_labels = [v for v in validation_labels if v not in range(2)]
        if len(unexpected_labels):
            raise ValueError('Unexpected label values found in the validation set:'
                             ' {unexpected_labels}. Please make sure that the '
                             'labels in the validation set are in the same range '
                             'as training labels.'.format(unexpected_labels=unexpected_labels))

    def _create_mlp_model(self, input_shape):
        """Creates an instance of a multi-layer perceptron model.

        # Arguments
            layers: int, number of `Dense` layers in the model.
            units: int, output dimension of the layers.
            dropout_rate: float, percentage of input to drop at Dropout layers.
            input_shape: tuple, shape of input to the model.
            num_classes: int, number of output classes.

        # Returns
            An MLP model instance.
        """

        self._model = models.Sequential()
        self._model.add(Dropout(rate=self._dropout_rate, input_shape=input_shape))

        for _ in range(self._layers_number-1):
            self._model.add(Dense(units=self._unit_number, activation='relu'))
            self._model.add(Dropout(rate=self._dropout_rate))

        self._model.add(Dense(units=1, activation='sigmoid'))

    def _compile_model(self, learning_rate):
        optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
        self._model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

    def _train_model(self,
                     batch_size,
                     epochs,
                     training_vector,
                     training_labels,
                     validation_vector,
                     validation_labels):
        # Create callback for early stopping on validation loss. If the loss does
        # not decrease in two consecutive tries, stop training.
        callbacks = [tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=2)]
        # Train and validate model.
        history = self._model.fit(
            training_vector,
            training_labels,
            epochs=epochs,
            callbacks=callbacks,
            validation_data=(validation_vector, validation_labels),
            verbose=2,  # Logs once per epoch.
            batch_size=batch_size)

        # Print results.
        history = history.history
        print('Validation accuracy: {acc}, loss: {loss}'.format(
                acc=history['val_acc'][-1], loss=history['val_loss'][-1]))


