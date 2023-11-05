from enum import Enum

__all__ = ['Icon', 'Provider']

class Icon(Enum):
  DATABASE = 'database'
  AUDIOBOOKSHELF = 'audiobookshelf'
  BOOKS_1 = 'books-1'
  BOOKS_2 = 'books-2'
  BOOK_1 = 'book-1'
  MICROPHONE_1 = 'microphone-1'
  MICROPHONE_3 = 'microphone-3'
  RADIO = 'radio'
  PODCAST = 'podcast'
  RSS = 'rss'
  HEADPHONES = 'headphones'
  MUSIC = 'music'
  FILE_PICTURE = 'file-picture'
  ROCKET = 'rocket'
  POWER = 'power'
  STAR = 'star'
  HEART = 'heart'
  
class Provider(Enum):
  GOOGLE = 'google'
  OPENLIBRARY = 'openlibrary'
  ITUNES = 'itunes'
  AUDIBLE = 'audible'
  AUDIBLE_CA = 'audible.ca'
  AUDIBLE_UK = 'audible.uk'
  AUDIBLE_AU = 'audible.au'
  AUDIBLE_FR = 'audible.fr'
  AUDIBLE_DE = 'audible.de'
  AUDIBLE_JP = 'audible.jp'
  AUDIBLE_IT = 'audible.it'
  AUDIBLE_IN = 'audible.in'
  AUDIBLE_ES = 'audible.es'
  FANTLAB = 'fantlab'