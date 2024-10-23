import spacy
from cachetools import cached

import server_ner.constants as cnt

@cached(cache={})
def get_spacy_model(lang:str=cnt.LANGUAGE_ES):
    
    if lang == cnt.LANGUAGE_ES:
        model =  spacy.load(cnt.SPACY_MODEL_ES_LARGE, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "senter"])
        return model
    
    if lang == cnt.LANGUAGE_EN:
        model =  spacy.load(cnt.SPACY_MODEL_EN_LARGE, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "senter"])
        return model
    