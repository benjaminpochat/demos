from enum import Enum

"""
Defines 3 types of subsets to structure the dataset the training process is based on.
See https://en.wikipedia.org/wiki/Training,_validation,_and_test_sets
"""
class DataSubsetType(Enum):
    TRAINING = 'TRAINING'
    VALIDATION = 'VALIDATION'
    TEST = 'TEST'
    UNKNOWN = 'UNKONWN'
