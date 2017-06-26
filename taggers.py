import os, sys
from nltk_opennlp.taggers import OpenNLPTagger
from treetagger import TreeTagger

class Taggers:

    def __init__(self):
        self.__maxent_postagger = dict()
        self.__perceptron_postagger = dict()
        self.__treetaggers = dict()

    def __has_key(self, dict_, key_):
        if sys.version_info >= (3,):
            return key_ in dict_ and dict_[key_] is not None
        else:
            return dict_.has_key(key_) and dict_[key_] is not None

    def get_maxent_postagger(self, language='en'):
        if not self.__has_key(self.__maxent_postagger, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            path_to_model = os.path.join(dirname, 'opennlp_models', '{}-pos-maxent.bin'.format(language))
            if not (os.path.exists(path_to_model) and os.path.isfile(path_to_model)):
                return None
            self.__maxent_postagger[language] = OpenNLPTagger(language=language,
                                                              path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                              path_to_model=path_to_model)
        return self.__maxent_postagger[language]

    def get_perceptron_postagger(self, language='en'):
        if not self.__has_key(self.__perceptron_postagger, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            path_to_model = os.path.join(dirname, 'opennlp_models', '{}-pos-perceptron.bin'.format(language))
            if not (os.path.exists(path_to_model) and os.path.isfile(path_to_model)):
                return None
            self.__perceptron_postagger[language] = OpenNLPTagger(language=language,
                                                                  path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                                  path_to_model=path_to_model)
        return self.__perceptron_postagger[language]

    def get_treetagger_postagger(self, language='en'):
        if not self.__has_key(self.__treetaggers, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            self.__treetaggers[language] = TreeTagger(language=language,
                                                      path_to_home=os.path.join(dirname, 'treetagger', 'cmd'))
        return self.__treetaggers[language]