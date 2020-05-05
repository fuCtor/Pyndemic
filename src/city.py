# coding: utf-8
import logging
import i18n

from .exceptions import GameException


class NoCityCubesException(GameException):
    def __init__(self, city, colour):
        self.city = city
        self.colour = colour

    def __str__(self):
        return i18n.t('city.no_cubes_left', colour=self.colour, city=self.city.name)


class City:
    def __init__(self, name, colour):
        self.name = name
        self.has_lab = False
        self.colour = colour
        self.cubes = {}
        self.distance = 999
        self.connected_cities = []
        logging.debug(
            i18n.t('city.created', city=str(self)))

    def __str__(self):
        return i18n.t('city.__str__', name=self.name, colour=self.colour)

    def info(self):
        has_lab = i18n.t('city.built') if self.has_lab else i18n.t('city.not_built')
        result = (i18n.t('city.info_prompt', 
            name=self.name, colour=self.colour, cities=len(self.connected_cities), has_lab=has_lab))

        return result

    def init_colours(self, cube_colours):
        for colour in cube_colours:
            self.cubes[colour] = 0

    def remove_cube(self, colour):
        if not self.cubes[colour]:
            raise NoCityCubesException(self, colour)
        self.cubes[colour] -= 1
        logging.debug(
            i18n.t('city.remove_cube', colour=colour, city=str(self)))

    def add_cube(self, colour):
        self.cubes[colour] += 1
        logging.debug(
            i18n.t('city.add_cube', colour=colour, city=str(self)))

    def build_lab(self):
        if self.has_lab:
            return False
        self.has_lab = True
        logging.debug(
            i18n.t('city.build_lab', city=str(self)))

        return True

    def add_connection(self, new_city):
        self.connected_cities.append(new_city)

    # TODO redesign this method
    def remove_all_cubes(self, colour):
        if not self.cubes[colour]:
            raise NoCityCubesException(self, colour)
        dropped_cubes = self.cubes[colour]
        self.cubes[colour] = 0
        logging.debug(
            i18n.t('city.remove_all_cubes', colour=colour, city=str(self)))

        return dropped_cubes

    def get_max_cubes(self):
        return max(self.cubes.values())
