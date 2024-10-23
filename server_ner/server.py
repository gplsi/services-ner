
import  logging
import json
import os

from http import HTTPStatus

from flask import Flask, Response, request
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import re

import server_ner.constants as cnt
from server_ner.ner_spacy import NerSpacy

logs_folder = os.getenv('LOGS_FOLDER', default='/tmp/logs')

print('- Configuring server logs...')
Path(logs_folder).mkdir(parents=True, exist_ok=True)
logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)
logger_handler = TimedRotatingFileHandler(f'{logs_folder}/server.log', when='d', interval=1)
logger.addHandler(logger_handler)
logger_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
logger_handler.setFormatter(logger_formatter)
logger_error = logging.getLogger('server_error')
logger_error.setLevel(logging.DEBUG)
logger_error_handler = TimedRotatingFileHandler(f'{logs_folder}/server_error.log', when='d', interval=1)
logger_error.addHandler(logger_error_handler)
logger_error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
logger_error_handler.setFormatter(logger_error_formatter)

print('Server started successfully')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root() :
  return 'It works!'


@app.route('/sensors/ner', methods=['POST'])
def get_ner() :
    """ 
    Asumes all request data comes as JSON
    {
        'documents': [
                        {
                            'id': unique_id,
                            'text': text to be analyzed,
                            'lang': language of the text [es|en],
                        }
                    ],
        'pretty': '' (may be empty, only key is important)
    }
    """

    try:
        key = request.headers.get('key')
        if str(key) == str(os.getenv('API_KEY')):
            query = request.json

            if query is not None:
                if verify_query(query):

                    docs = query[cnt.QUERY_KEYS_DOCUMENTS] if cnt.QUERY_KEYS_DOCUMENTS in query.keys() else None
                    indent = 2 if cnt.QUERY_KEYS_PRETTY in query.keys() else None

                    docsa = {'documents_analized': []}

                    for doc in docs:
                        doca = analyze_document(doc)
                        docsa['documents_analized'].append(doca)
                    

                    docsa_json = json.dumps(docsa, indent=indent)
                    return Response(status=HTTPStatus.OK, response=docsa_json)

                else:
                    template = '{"documents": [ {"id": unique_id, "text": text to be analyzed, "lang": [es|en] }], "pretty":}'
                    emsg = {'error_msg': f'Error generating entities. Try checking query JSON, must match this template: {template}'}
                    emsg = json.dumps(emsg)
                    logger.debug(emsg)
                    print(emsg)
                    return Response(status=HTTPStatus.BAD_REQUEST, response=emsg)              
            else:
                emsg = {'error_msg': 'Error generating entities - no JSON data received...'}
                emsg = json.dumps(emsg)
                logger.debug(emsg)
                print(emsg)
                return Response(status=HTTPStatus.BAD_REQUEST, response=emsg)   
        else :
            emsg = {'error_msg': 'Incorrect or not authentication token...'}
            emsg = json.dumps(emsg)
            logger.debug(emsg)
            print(emsg)
            return Response(status=HTTPStatus.UNAUTHORIZED, response=emsg)

    except Exception as e:
        template = '{"documents": [ {"id": unique_id, "text": text to be analyzed, "lang": [es|en] }], "pretty":}'
        emsg = {'error_msg': f'Error generating entities. Try checking query JSON, must match this template: {template}'}
        emsg = json.dumps(emsg)
        logger.debug(emsg)
        logger_error.exception(emsg)
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, response=emsg)



def analyze_document(doc):
    """
    Convenience method to analize the decument and get the response json. Assumes document has correct format

    """

    id = doc[cnt.DOCUMENT_KEYS_ID]
    text = doc[cnt.DOCUMENT_KEYS_TEXT]
    text = re.sub(r'[^\w\s]', '', text)

    lang = doc[cnt.DOCUMENT_KEYS_LANG]

    try:
        ner = NerSpacy(lang)
        doca = {'id':id, 'entities': ner.analyze_entities_dic(text)}
        return doca

    except Exception as e:
        emsg = {'error_msg': f'Error generating entities - {e}'}
        emsg_str = json.dumps(emsg)
        logger.debug(emsg_str)
        logger_error.exception(emsg_str)
        return emsg



def verify_query(query):
    
    docs = query[cnt.QUERY_KEYS_DOCUMENTS] if cnt.QUERY_KEYS_DOCUMENTS in query.keys() else None
    
    if docs is not None:
        for doc in docs:
            if (cnt.DOCUMENT_KEYS_ID not in doc.keys()) or (cnt.DOCUMENT_KEYS_TEXT not in doc.keys()):
                return False

    else:
        return False

    return True



# run only if invoked directly
if __name__ == "__main__":
    app.run()


