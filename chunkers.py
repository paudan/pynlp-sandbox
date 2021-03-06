import os, sys
from nltk_opennlp.chunkers import OpenNLPChunker, OpenNERChunker, OpenNERChunkerMulti
from treetagger import TreeTaggerChunker

class Chunkers:

    def __init__(self):
        self.__opennlp_chunkers = dict()
        self.__treetagger_chunkers = dict()
        self.__ner_multi_chunker = None

        self.__ner_date_chunkers = dict()
        self.__ner_location_chunkers = dict()
        self.__ner_money_chunkers = dict()
        self.__ner_organization_chunkers = dict()
        self.__ner_percentage_chunkers = dict()
        self.__ner_person_chunkers = dict()
        self.__ner_time_chunkers = dict()

    def __has_key(self, dict_, key_):
        if sys.version_info >= (3,):
            return key_ in dict_ and dict_[key_] is not None
        else:
            return dict_.has_key(key_) and dict_[key_] is not None

    def get_opennlp_chunker(self, language='en', use_punc_tag=True):
        if not self.__has_key(self.__opennlp_chunkers, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            path_to_model = os.path.join(dirname, 'opennlp_models', '{}-pos-chunker.bin'.format(language))
            if not (os.path.exists(path_to_model) and os.path.isfile(path_to_model)):
                return None
            self.__opennlp_chunkers[language] = OpenNLPChunker(path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                               path_to_model=path_to_model,
                                                               use_punc_tag=use_punc_tag)
        return self.__opennlp_chunkers[language]

    def get_treetagger_chunker(self, language='en'):
        if not self.__has_key(self.__treetagger_chunkers, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            self.__treetagger_chunkers[language] = TreeTaggerChunker(language=language,
                                                                     path_to_home=os.path.join(dirname, 'treetagger', 'cmd'))
        return self.__treetagger_chunkers[language]

    def __get_ner_chunker(self, chunkers_list, name_str, language, use_punc_tag=True):
        if not self.__has_key(chunkers_list, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            path_to_model = os.path.join(dirname, 'opennlp_models', '{}-ner-{}.bin'.format(language, name_str))
            if not (os.path.exists(path_to_model) and os.path.isfile(path_to_model)):
                return None
            chunkers_list[language] = OpenNERChunker(path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                     path_to_chunker=os.path.join(dirname, 'opennlp_models', '{}-chunker.bin'.format(language)),
                                                     path_to_ner_model=path_to_model,
                                                     use_punc_tag=use_punc_tag)
        return chunkers_list[language]

    def get_ner_date_chunker(self, language='en', use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_date_chunkers, 'date', language, use_punc_tag)

    def get_ner_location_chunker(self, language='en', use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_location_chunkers, 'location', language, use_punc_tag)

    def get_ner_money_chunker(self, language='en', use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_money_chunkers, 'money', language, use_punc_tag)

    def get_ner_organization_chunker(self, language='en', use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_organization_chunkers, 'organization', language, use_punc_tag)

    def get_ner_percentage_chunker(self, language='en', use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_percentage_chunkers, 'percentage', language, use_punc_tag)

    def get_ner_person_chunker(self, language='en', use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_person_chunkers, 'person', language, use_punc_tag)

    def get_ner_time_chunker(self, language, use_punc_tag=True):
        return self.__get_ner_chunker(self.__ner_time_chunkers, 'time', language, use_punc_tag)

    def get_english_multichunker(self, use_punc_tag=True):
        if self.__ner_multi_chunker is None:
            language = 'en'
            dirname, filename = os.path.split(os.path.abspath(__file__))
            ner_models = [
                os.path.join(dirname, 'opennlp_models', '{}-ner-person.bin'.format(language)),
                os.path.join(dirname, 'opennlp_models', '{}-ner-date.bin'.format(language)),
                os.path.join(dirname, 'opennlp_models', '{}-ner-location.bin'.format(language)),
                os.path.join(dirname, 'opennlp_models', '{}-ner-time.bin'.format(language)),
                os.path.join(dirname, 'opennlp_models', '{}-ner-money.bin'.format(language)),
                os.path.join(dirname, 'opennlp_models', '{}-ner-percentage.bin'.format(language)),
                os.path.join(dirname, 'opennlp_models', '{}-ner-organization.bin'.format(language))
            ]
            self.__ner_multi_chunker = OpenNERChunkerMulti(path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                           path_to_chunker=os.path.join(dirname, 'opennlp_models',
                                                                  '{}-chunker.bin'.format(language)),
                                                           ner_models=ner_models,
                                                           use_punc_tag=use_punc_tag)
        return self.__ner_multi_chunker