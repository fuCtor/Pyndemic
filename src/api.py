# coding: utf-8
from abc import ABCMeta, abstractmethod
import logging
import i18n


class InputManager(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self):
        pass


class ConsoleInputManager(InputManager):
    def __init__(self):
        pass

    def __call__(self):
        command = input(i18n.t('api.prompt'))
        return command


class FileInputManager(InputManager):
    def __init__(self, input_file):
        with open(input_file, 'r') as fin:
            self._cached = fin.readlines()
        self._cached.reverse()

    def __call__(self):
        try:
            command = self._cached.pop().rstrip()
        except IndexError:
            raise IndexError(
                i18n.t('api.no_more_commands'))

        return command


class HybridInputManager(InputManager):
    def __init__(self, input_mode='console', input_file=None):
        self.input_mode = input_mode

        if self.input_mode == 'file':
            self.input = FileInputManager(input_file)
            logging.info(i18n.t('api.using_file_mode'))
        else:
            self.input = ConsoleInputManager()
            logging.info(i18n.t('api.using_console_mode'))

    def __call__(self):
        try:
            command = self.input()
        except IndexError:
            self.input_mode = 'console'
            logging.warning(
                'No more commands in file input! '
                'Now switching to console mode.')
            self.input = ConsoleInputManager()
            command = self.input()

        return command

