# -*- coding: utf-8 -*-
import os
from nltk_opennlp.taggers import OpenNLPTagger
from treetagger import TreeTagger
from OpenDutchWordnet import Wn_grid_parser


def test_dutch_wordnet():
    instance = Wn_grid_parser(Wn_grid_parser.odwn)
    le_el = instance.les_find_le("havenplaats-n-1")
    assert le_el.get_id() == 'havenplaats-n-1'
    assert le_el.get_lemma() == 'havenplaats'
    assert le_el.get_pos() == 'noun'
    assert le_el.get_sense_id() == 'o_n-109910434'
    assert le_el.get_provenance() == 'cdb2.2_Auto'
    assert le_el.get_synset_id() == 'eng-30-08633957-n'

    synset_el = instance.synsets_find_synset('eng-30-00324560-v')
    assert synset_el is not None
    assert synset_el.get_id() == 'eng-30-00324560-v'
    assert synset_el.get_ili() == 'i23355'

    relation = synset_el.get_relations("has_hyperonym")
    assert relation is not None
    relation_el = relation[0]
    assert relation_el is not None
    assert relation_el.get_provenance() == 'pwn'
    assert relation_el.get_reltype() == 'has_hyperonym'
    assert relation_el.get_target(), 'eng-30-00322847-v'


def test_treetagger():
    def test_language(language, phrase):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        tt = TreeTagger(language=language,
                        path_to_home=os.path.join(dirname, 'treetagger', 'cmd'))
        return tt.tag(phrase)

    en_tags = test_language('english', 'What is the airspeed of an unladen swallow?')
    assert en_tags[1][0] == 'is'
    assert en_tags[1][1] == 'VBZ'
    de_tags = test_language('german', 'Das Haus hat einen großen hübschen Garten.')
    assert de_tags[0][0] == 'Das'
    assert de_tags[0][1] == 'ART'


def test_opennlp_tagger():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    language = 'en'
    tt = OpenNLPTagger(language=language,
                       path_to_bin=os.path.join(dirname, 'apache-opennlp', 'bin'),
                       path_to_model=os.path.join(dirname, 'opennlp_models', 'en-pos-maxent.bin'))
    phrase = 'Pierre Vinken , 61 years old , will join the board as a nonexecutive director Nov. 29 .'
    en_tags = tt.tag(phrase)
    assert en_tags[0][0] == 'Pierre'
    assert en_tags[0][1] == 'NNP'