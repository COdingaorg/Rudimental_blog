import os
import urllib.request, json
from app.models import Quote

#getting api key
quote_url = os.environ.get('API_URL')

#get quotes from api
def get_quotes():
  '''
  function that returns quotes- randomly
  '''
  with urllib.request.urlopen(quote_url) as url:
    quotes_response = url.read()
    quotes_response_readable = json.loads(quotes_response)
    quotes_item = process_results(quotes_response_readable)
  return quotes_item
    
def process_results(quotes_response_readable):
  id = quotes_response_readable.get('id')
  author = quotes_response_readable.get('author')
  quote = quotes_response_readable.get('quote')
  link = quotes_response_readable.get('permalink')

  new_quote = Quote(id, author, quote, link)

  return new_quote
