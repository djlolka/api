import pygame
import requests
import sys

MAP_FILE = "map.png"

longitude = 56.261086
latitude = 58.007368
spn = 0.002


class MapParams:
    def __init__(self, long, lat, spn, l_map):
        self.spn = spn
        self.long = long
        self.lat = lat
        self.l_map = l_map

    def make_dict(self):
        self.dict = {}
        self.dict['ll'] = str(self.long) + ',' + str(self.lat)
        self.dict['l'] = self.l_map
        self.dict['spn'] = ','.join([str(self.spn), str(self.spn)])
        return self.dict


def get_image(dict_params):
    api_server = 'https://static-maps.yandex.ru/1.x/'
    response = requests.get(api_server, params=dict_params)
    if not response:
        print('error', response.status_code, response.reason)
        sys.exit()
    with open(MAP_FILE, "wb") as file:
        file.write(response.content)


def UI():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(MAP_FILE), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()


my_map = MapParams(longitude, latitude, spn, 'map')
get_image(my_map.make_dict())
UI()
