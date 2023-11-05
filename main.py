from audiobookshelfapi import *
import json
import audiobookshelfenums

APITOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI3YzFjMDVmNy05MjI4LTRkN2YtODgzMC02OTg3OWRhMTljM2QiLCJ1c2VybmFtZSI6Im5pa28iLCJpYXQiOjE2OTkxNDE3Mjd9.fxjAvBS0xJmQ34A_Xtvb-PJJ2aj7DWzNez4qQF68W_g'

if __name__ == '__main__':
    a = Audiobookshelf_API("http://127.0.0.1:13378", APITOKEN)

    name = 'Audiobooks1'
    icon = Icon.BOOK_1
    mediaType = 'book'
    provider = Provider.AUDIBLE
    library = a.create_library(name, ['/audiobooks'], icon, mediaType, provider)
    print (json.dumps(library.to_dict(),indent=2))

