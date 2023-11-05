from audiobookshelfapi import *
import json
import audiobookshelfenums

APITOKEN = ''

if __name__ == '__main__':
    a = Audiobookshelf_API("http://127.0.0.1:13378", APITOKEN)

    name = 'Audiobooks1'
    icon = Icon.BOOK_1
    mediaType = 'book'
    provider = Provider.AUDIBLE
    library = a.create_library(name, ['/audiobooks'], icon, mediaType, provider)
    print (json.dumps(library.to_dict(),indent=2))

