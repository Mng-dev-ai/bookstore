from flask_restful import Resource
import requests
import re

class getCountOccurrences(Resource):
    def get(self, word:str) -> dict:
      url = "https://www.gutenberg.org/cache/epub/19033/pg19033.txt"
      response = requests.get(url)
      text = response.text
      return {word:sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), text))}