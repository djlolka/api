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

    def increase(self):
        if self.spn > 0.001:
            if 0.001 <= self.spn < 0.01:
                self.spn -= 0.001
            elif 0.01 <= self.spn < 0.1:
                self.spn -= 0.01
            elif 0.1 <= self.spn < 1:
                self.spn -= 0.1
            elif 1 <= self.spn < 10:
                self.spn -= 1
            elif 10 <= self.spn <= 90:
                self.spn -= 10

    def decrease(self):
        if self.spn < 90:
            if 0.001 <= self.spn < 0.01:
                self.spn += 0.001
            elif 0.01 <= self.spn < 0.1:
                self.spn += 0.01
            elif 0.1 <= self.spn < 1:
                self.spn += 0.1
            elif 1 <= self.spn < 10:
                self.spn += 1
            elif 10 <= self.spn < 90:
                self.spn += 10

    def update(self, key):
        if key == pygame.K_PAGEUP:
            self.decrease()
        elif key == pygame.K_PAGEDOWN:
            self.increase()


def get_image(dict_params):
    api_server = 'https://static-maps.yandex.ru/1.x/'
    response = requests.get(api_server, params=dict_params)
    if not response:
        print('error', response.status_code, response.reason)
        sys.exit()
    with open(MAP_FILE, "wb") as file:
        file.write(response.content)


def UI(my_map):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(MAP_FILE), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                my_map.update(event.key)
                get_image(my_map.make_dict())
                pygame.event.clear()
        screen.blit(pygame.image.load(MAP_FILE), (0, 0))
        pygame.display.flip()

    pygame.quit()


my_map = MapParams(longitude, latitude, spn, 'map')
get_image(my_map.make_dict())
UI(my_map)
