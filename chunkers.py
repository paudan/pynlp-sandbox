import os, sys
from nltk_opennlp.chunkers import OpenNLPChunker, OpenNERChunker, OpenNERChunkerMulti
from treetagger import TreeTaggerChunker

class Chunkers:

    def __init__(self):
        self.opennlp_chunkers = dict()
        self.treetagger_chunkers = dict()
        self.ner_multi_chunker = None

        self.ner_date_chunkers = dict()
        self.ner_location_chunkers = dict()
        self.ner_money_chunkers = dict()
        self.ner_organization_chunkers = dict()
        self.ner_percentage_chunkers = dict()
        self.ner_person_chunkers = dict()
        self.ner_time_chunkers = dict()

    def __has_key(self, dict_, key_):
        if sys.version_info >= (3,):
            return key_ in dict_ and dict_[key_] is not None
        else:
            return dict_.has_key(key_) and dict_[key_] is not None

    def get_opennlp_chunker(self, language='en'):
        if not self.__has_key(self.opennlp_chunkers, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            path_to_model = os.path.join(dirname, 'opennlp_models', '{}-pos-chunker.bin'.format(language))
            if not (os.path.exists(path_to_model) and os.path.isfile(path_to_model)):
                return None
            self.opennlp_chunkers[language] = OpenNLPChunker(language=language,
                                                            path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                            path_to_model=path_to_model)
        return self.opennlp_chunkers[language]

    def get_treetagger_chunker(self, language='en'):
        if not self.__has_key(self.treetagger_chunkers, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            self.treetagger_chunkers[language] = TreeTaggerChunker(language=language,
                                                    path_to_home=os.path.join(dirname, 'treetagger', 'cmd'))
        return self.treetagger_chunkers[language]

    def __get_ner_chunker(self, chunkers_list, name_str, language):
        if not self.__has_key(chunkers_list, language):
            dirname, filename = os.path.split(os.path.abspath(__file__))
            path_to_model = os.path.join(dirname, 'opennlp_models', '{}-ner-{}.bin'.format(language, name_str))
            if not (os.path.exists(path_to_model) and os.path.isfile(path_to_model)):
                return None
            chunkers_list[language] = OpenNERChunker(language=language,
                                                     path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                                     path_to_chunker=os.path.join(dirname, 'opennlp_models', '{}-chunker.bin'.format(language)),
                                                     path_to_ner_model=path_to_model)
        return chunkers_list[language]

    def get_ner_date_chunker(self, language='en'):
        return self.__get_ner_chunker(self.ner_date_chunkers, 'date', language)

    def get_ner_location_tagger(self, language='en'):
        return self.__get_ner_chunker(self.ner_location_chunkers, 'location', language)

    def get_ner_money_tagger(self, language='en'):
        return self.__get_ner_chunker(self.ner_money_chunkers, 'money', language)

    def get_ner_organization_tagger(self, language='en'):
        return self.__get_ner_chunker(self.ner_organization_chunkers, 'organization', language)

    def get_ner_percentage_tagger(self, language='en'):
        return self.__get_ner_chunker(self.ner_percentage_chunkers, 'percentage', language)

    def get_ner_person_tagger(self, language='en'):
        return self.__get_ner_chunker(self.ner_person_chunkers, 'person', language)

    def get_ner_time_tagger(self, language):
        return self.__get_ner_chunker(self.ner_time_chunkers, 'time', language)

    def get_ner_time_tagger(self, language='en'):
        if self.ner_multi_chunker is None:
            dirname, filename = os.path.split(os.path.abspath(__file__))
            self.ner_multi_chunker = OpenNERChunkerMulti(language=language,
                                     path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                                     path_to_chunker=os.path.join(dirname, 'opennlp_models',
                                                                  '{}-chunker.bin'.format(language)),
                                     ner_models=[
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-person.bin'.format(language)),
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-date.bin'.format(language)),
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-location.bin'.format(language)),
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-time.bin'.format(language)),
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-money.bin'.format(language)),
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-percentage.bin'.format(language)),
                                         os.path.join(dirname, 'opennlp_models', '{}-ner-organization.bin'.format(language))])
        return self.ner_multi_chunker