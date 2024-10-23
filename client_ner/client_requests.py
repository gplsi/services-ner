import requests
import json
from http import HTTPStatus

def main():

    lang = 'en'
    pretty = ""

    #host = 'http://192.168.1.132'  # home
    # host = 'http://10.16.225.188'  # ua
    host = 'http://doky.difusionlabs.com'
    #host = 'http://localhost'
    port = 7003
    #host = 'http://127.0.0.1'
    #port = 5000
    service = '/sensors/ner'
    url = f'{host}:{port}{service}'

    headers = {"Content-type": "application/json", "key": "254d4a6b00b78b94f846b85528298d43"}
    params = {"documents":[{'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}, {'id': 1130, 'text': 'RT @F1: Max Verstappen has never won in Singapore but if he does this weekend he could clinch the world title 🌎🏆@ChrisMedlandF1 looks at…', 'lang': 'en'}]}

    try:
        params_json = json.dumps(params)

        response = requests.request("POST", url, headers=headers, data=params_json)
        
        if response.status_code == HTTPStatus.OK:
            print(response.json())
        else:
            print(response.json())
    except Exception as e:
        print(e)


if __name__ == '__main__':  
    main()