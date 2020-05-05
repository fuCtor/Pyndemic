# coding: utf-8
import sys
import itertools as its
import random
import logging
import i18n

from .game import *
from .city import NoCityCubesException
from .player import LastDiseaseCuredException
from . import log
from .commands import COMMANDS
from .api import HybridInputManager


class MainController:
    def __init__(self, input_file=None, random_state=None):
        if input_file is not None:
            self.input = HybridInputManager('file', input_file)
        else:
            self.input = HybridInputManager()

        if random_state is not None:
            random.seed(random_state)
            logging.info(
                i18n.t('main.seed', seed=str(random_state)))

    def run(self):
        logging.info(
            i18n.t('main.start_game', count=4))

        self.player_names = names = ['Alpha', 'Bravo', 'Charlie', 'Delta']
        self.players = players = {name: Player(name) for name in names}

        game = self.game = Game()

        for name in self.player_names:
            game.add_player(players[name])

        game.setup_game()
        game.start_game()

        try:
            self.game_cycle()
        except LastDiseaseCuredException as e:
            logging.warning(e)
            logging.warning(i18n.t('main.game_won'))
        except GameCrisisException as e:
            logging.warning(e)
            logging.warning(i18n.t('main.game_lost'))
        except KeyboardInterrupt:
            logging.warning(
                i18n.t('main.exit_decide'))

        logging.info(i18n.t('main.thats_all'))

    def game_cycle(self):
        name_cycle = its.cycle(self.player_names)
        game = self.game

        while True:
            player = self.player = self.players[next(name_cycle)]
            logging.info(
                i18n.t('main.active_player', name=player.name))

            game.start_turn(player)

            while player.action_count:
                logging.info(
                    i18n.t('main.actions_left', count=player.action_count))

                command = self.input()
                if not command:
                    continue

                logging.debug(
                    i18n.t('main.player_action', command=command))
                command = command.split()

                chosen_executor = None
                for executor in COMMANDS:
                    potential_executor = executor(game, player, self)
                    if potential_executor.check_valid_command(command):
                        chosen_executor = potential_executor
                        break
                if not chosen_executor:
                    logging.error(
                        i18n.t('main.command_parse_fail'))
                    continue

                try:
                    success = chosen_executor.execute(command)
                except NoCityCubesException as e:
                    logging.error(e)
                    success = False
                if not success:
                    logging.error(
                        i18n.t('main.command_execute_fail'))
                continue

                logging.info(
                    i18n.t('main.command_executed'))

            logging.info(
                i18n.t('main.no_actions_left'))

            # TODO: this must be a game method
            for i in range(2):
                game.draw_card(player)

            logging.info(
                i18n.t('main.cards_drawn'))

            game.infect_city_phase()

            logging.info(
                i18n.t('main.infected_phase_gone'))

