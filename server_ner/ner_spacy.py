import spacy

import server_ner.constants as cnt
from server_ner._cache import get_spacy_model


class NerSpacy:
    
    def __init__(self, lang:str=cnt.LANGUAGE_ES):
        self.ner_model = get_spacy_model(lang)

    
    def analyze_entities(self, text:str):
        doc = self.ner_model(text)

        return doc.ents
    

    def analyze_entities_dic(self, text:str):
        entities = []

        ents = self.analyze_entities(text)

        if  ents is not None:

            for e in ents:
                ed = {'name': e.text,
                    'type': e.label_,
                    'score': 0.0, # otherwise use https://github.com/explosion/spaCy/issues/881
                    'gloss': spacy.explain(e.label_),
                    #'start_word': e.start,
                    #'end_word': e.end,
                    #'nel': [{'kb_id': e.kb_id_, 'kb_nel_score': e._.score, 'kb_description': e._.description}],
                    #'start_char': e.start_char,
                    #'end_char': e.end_char
                }

                entities.append(ed)

        return entities