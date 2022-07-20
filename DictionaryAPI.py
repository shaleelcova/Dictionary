import requests


class DictionaryAPI:
    def __init__(self):
        self._url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
        self._response = None

    def retrieve_response(self, word):
        self._response = requests.get(self._url + word).json()
        return self._response

    def get_meaning(self, word):
        res = self.retrieve_response(word)
        result = {}
        for response in res:
            for part in response["meanings"]:
                result[part["partOfSpeech"]] = []
                for defi in part["definitions"]:
                    result[part["partOfSpeech"]].append(defi["definition"])
        return result


d = DictionaryAPI()
print(d.get_meaning("No"))