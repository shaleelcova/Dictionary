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

    def get_synonyms(self, word):
        res = self.retrieve_response(word)
        result = []
        for response in res:
            for part in response["meanings"]:
                result += part["synonyms"]
        return result

    def get_example(self, word):
        res = self.retrieve_response(word)
        result = []
        for response in res:
            for part in response["meanings"]:
                for example in part["definitions"]:
                    try:
                        result.append(example["example"])
                    except KeyError:
                        continue
        return result
