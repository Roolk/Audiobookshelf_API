from audiobookshelfapi import *
import json
import audiobookshelfenums

APITOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI3YzFjMDVmNy05MjI4LTRkN2YtODgzMC02OTg3OWRhMTljM2QiLCJ1c2VybmFtZSI6Im5pa28iLCJpYXQiOjE2OTkxNDE3Mjd9.fxjAvBS0xJmQ34A_Xtvb-PJJ2aj7DWzNez4qQF68W_g'
APITOKEN2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c3JfMGhseGhpcnlsb2d2a2NzM3pxIiwidXNlcm5hbWUiOiJuaWtvIiwiaWF0IjoxNjY2OTA3NjExfQ.Mn0viYaZI2SrwzX-Nhy5dzDNVoLMyuPqKKjiE3C0hF0'

URL = "http://127.0.0.1:13378"
URL2 = "http://goldmine.local:13378"


if __name__ == '__main__':
    a = AudiobookshelfAPI(URL, APITOKEN)
    libs = a.get_all_libraries()
    for lib in libs:
        print(lib.name, lib.id)
        '''
        series = a.get_library_series(lib.id)
        for serie in series:
            print(json.dumps(serie.to_dict(), indent=2))
        '''
