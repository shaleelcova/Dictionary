import requests


class DictionaryAPI:
    def __init__(self):
        self._url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
        self._response = None

    def retrieve_response(self, word):
        self._response = requests.get(self._url + word).json()
        return self._response


