import unittest
from unittest import skip, expectedFailure

import config
from PandemicGame import PandemicGame
from city import City
from ai import AIController
from player import Player

# TODO: provide test cases for City, Deck, etc.


class GameSetupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings_location = 'testSettings.cfg'
        cls.settings = config.get_settings(cls.settings_location)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.pg = PandemicGame()
        self.pg.settings = self.settings

    def tearDown(self):
        pass

    def test_add_player(self):
        players = [Player('Evie'), Player('Amelia')]

        for player in players:
            self.pg.add_player(player)

            with self.subTest(player=player):
                self.assertIs(self.pg, player.game)
                self.assertIn(player, self.pg.players)
                self.assertEqual(player.name, self.pg.players[-1].name)
                # TODO: AIController assertions

    def test_get_infection_rate(self):
        self.pg.get_infection_rate()
        self.assertEqual(2, self.pg.infection_rate)

    def test_get_new_cities(self):
        self.pg.get_new_cities()

        self.assertIn('London', self.pg.city_map)
        city = self.pg.city_map['London']
        self.assertEqual('London', city.name)
        self.assertEqual('Blue', city.colour)
        self.assertEqual(6, len(city.connected_cities))
        self.assertEqual('Washington', city.connected_cities[3].name)
        self.assertEqual('Bejing', city.connected_cities[4].name)

    # TODO: separate for ".make_cities" method

    def test_get_new_decks(self):
        self.pg.get_new_decks()

        # TODO: these assertions should belong to Deck test cases
        top_player_card = self.pg.player_deck.take_top_card()
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('London', top_player_card.name)
        self.assertEqual('London', top_infect_card.name)
        self.assertEqual('Blue', top_player_card.colour)
        self.assertEqual('Blue', top_infect_card.colour)

    def test_get_new_diseases(self):
        self.pg.get_new_diseases()

        self.assertEqual('Red', self.pg.diseases['Red'].colour)
        self.assertEqual(30, self.pg.disease_cubes['Blue'])

    def test_set_starting_epidemics(self):
        self.pg.set_starting_epidemics()
        self.assertEqual(4, self.pg.starting_epidemics)

    def test_setup_game(self):
        del self.pg.settings

        players = [Player('Evie'), Player('Amelia')]
        for player in players:
            self.pg.add_player(player)

        self.pg.setup_game(self.settings_location)

        self.assertEqual(self.pg.settings, self.settings)

        self.assertEqual(0, self.pg.epidemic_count)
        self.assertEqual(0, self.pg.outbreak_count)
        self.assertFalse(self.pg.game_won)
        self.assertFalse(self.pg.game_over)

        self.assertIn('Yellow', City.cube_colours)
        City.cube_colours = []

        self.assertEqual(2, self.pg.infection_rate)

        self.assertIn('New York', self.pg.city_map)
        self.newyork = self.pg.city_map['New York']
        self.assertEqual('New York', self.newyork.name)
        self.assertEqual('Yellow', self.newyork.colour)
        self.assertEqual(3, len(self.newyork.connected_cities))

        top_player_card = self.pg.player_deck.take_top_card()
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('London', top_player_card.name)
        self.assertEqual('London', top_infect_card.name)

        self.assertEqual('Red', self.pg.diseases['Red'].colour)
        self.assertEqual(30, self.pg.disease_cubes['Black'])

        self.assertEqual(4, self.pg.starting_epidemics)

        self.assertEqual('London', players[0].location.name)
        self.assertEqual('London', players[1].location.name)

        self.assertEqual(0, AIController.number_AI)


class GameTestCase(unittest.TestCase):
    def setUp(self):
        self.settings_location = 'testSettings.cfg'
        self.player1 = Player('Evie')
        self.player2 = Player('Amelia')
        self.pg = PandemicGame()
        self.pg.add_player(self.player1)
        self.pg.add_player(self.player2)
        self.pg.setup_game(self.settings_location)

    def test_add_epidemics(self):
        self.pg.add_epidemics()
        self.assertFalse(self.pg.has_x_cube_city(3))
        for i in range(0,11):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertTrue(self.pg.has_x_cube_city(3))

    @expectedFailure
    def test_complete_round(self):
        self.pg.inital_infect_phase()
        self.pg.draw_inital_hands()
        self.assertEqual(3, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.pg.complete_round()
        self.assertEqual(0, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual('Cambridge', self.player1.location.name)
        self.assertEqual(0, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.assertEqual('Bristol', self.player1.location.name)

    def test_add_card(self):
        top_player_card = self.pg.player_deck.take_top_card()
        self.player1.add_card(top_player_card)
        self.assertEqual(1, len(self.player1.hand))
        self.assertTrue(self.player1.hand_contains('London'))

    def test_infect_city(self):
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))

    def test_infect_city_phase(self):
        self.pg.infect_city_phase()
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(2, len(self.pg.infect_deck.discard))
        self.assertEqual('London', self.pg.infect_deck.discard[0].name)
        self.assertEqual(28, self.pg.disease_cubes['Blue'])

    def test_epidemic_phase(self):
        self.pg.epidemic_phase()
        self.assertEqual(3, self.pg.city_map['Belgorod'].get_cubes('Black'))
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('Belgorod', top_infect_card.name)
        self.assertEqual('Black', top_infect_card.colour)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertEqual(0, len(self.pg.infect_deck.discard))

    def test_outbreak_trigger(self):
        for i in range(4):
            self.pg.infect_city('London', 'Blue')
        self.assertEqual(3, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Washington'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Bejing'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Moscow'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.outbreak_count)

    def test_outbreak(self):
        self.pg.outbreak('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Washington'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Bejing'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Moscow'].get_cubes('Blue'))

    def test_shuffle(self):
        import random
        random.seed(42)

        self.assertEqual('London', self.pg.player_deck.take_top_card().name)
        self.pg.player_deck.shuffle()
        self.assertNotEqual('Oxford', self.pg.player_deck.take_top_card().name)

        self.assertEqual('London', self.pg.infect_deck.take_top_card().name)
        self.pg.infect_deck.shuffle()
        self.assertNotEqual('Oxford', self.pg.infect_deck.take_top_card().name)

    def test_start_game(self):
        self.pg.start_game()
        self.top_player_card = self.pg.player_deck.take_top_card()
        self.top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual(9, len(self.pg.infect_deck.discard))
        self.assertEqual(0, len(self.pg.player_deck.discard))
        self.assertTrue(self.pg.has_x_cube_city(3))
        self.assertEqual(3, self.pg.get_count_x_cube_city(3))
        self.assertTrue(self.pg.has_x_cube_city(2))
        self.assertEqual(3, self.pg.get_count_x_cube_city(2))
        self.assertTrue(self.pg.has_x_cube_city(1))
        self.assertEqual(3, self.pg.get_count_x_cube_city(1))
        self.assertEqual(4, len(self.player1.hand))
        self.assertEqual(4, len(self.player2.hand))
        self.assertNotEqual('London', self.top_player_card.name)
        self.assertNotEqual('London', self.top_infect_card.name)
        for i in range (10):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)

    def test_get_max_cubes(self):
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('New York', 'Blue')
        self.pg.infect_city('New York', 'Blue')
        self.pg.infect_city('Moscow', 'Red')
        self.pg.infect_city('Moscow', 'Red')
        self.pg.infect_city('Moscow', 'Red')
        self.pg.infect_city('Moscow', 'Blue')
        self.assertEqual(1, self.pg.city_map['London'].get_max_cubes())
        self.assertEqual(2, self.pg.city_map['New York'].get_max_cubes())
        self.assertEqual(3, self.pg.city_map['Moscow'].get_max_cubes())

    def test_inital_infect_phase(self):
        self.pg.inital_infect_phase()
        self.assertEqual(3, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Southampton'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Plymouth'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Liverpool'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Manchester'].get_cubes('Blue'))
        self.assertEqual(9, len(self.pg.infect_deck.discard))
        self.assertEqual(12, self.pg.disease_cubes['Blue'])

    def test_draw_initial_hands(self):
        self.pg.start_game()
        # TODO: assertions

    def test_draw_card(self):
        self.pg.draw_card(self.player1)
        self.assertEqual('London', self.player1.hand[0].name)

    @skip('\'PandemicGame.all_one_colour\' method is not provided yet.')
    def test_check_cure_disease(self):
        for i in range(9):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.build_lab())
        self.assertTrue(
            self.player1.check_cure_disease('Oxford', 'Cambridge', 'Brighton', 'Southampton', 'Bristol'))
        self.assertFalse(
            self.player1.check_cure_disease('Brighton', 'Liverpool', 'Brighton', 'Southampton', 'Manchester'))
        self.assertFalse(
            self.player1.check_cure_disease('Brighton', 'Liverpool', 'New York', 'Southampton', 'Manchester'))

    @skip('\'PandemicGame.all_one_colour\' method is not provided yet.')
    def test_cure_disease(self):
        self.assertFalse(self.pg.diseases['Blue'].cured)
        for i in range(15):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.build_lab())
        self.assertTrue(self.player1.cure_disease('Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester'))
        self.assertTrue(self.pg.diseases['Blue'].cured)
        self.assertEqual(2, self.player1.action_count)

    def test_check_share_knowledge(self):
        self.player1.set_location('London')
        self.player2.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.check_share_knowledge('London', self.player2))
        self.player2.set_location('New York')
        self.assertFalse(self.player1.check_share_knowledge('London', self.player2))

    def test_share_knowledge(self):
        self.player1.set_location('London')
        self.player2.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(True, self.player1.share_knowledge('London', self.player2))
        self.assertEqual('London', self.player2.hand[0].name)
        self.assertEqual(3, self.player1.action_count)

    def test_check_treat_disease(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('London', 'Blue')
        self.assertTrue(self.player1.check_treat_disease('Blue'))
        self.assertFalse(self.player1.check_treat_disease('Red'))

    def test_treat_disease_no_cure(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(2, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.treat_disease('Blue'))
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual(False, self.player1.treat_disease('Red'))
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)

    def test_get_new_diseaes(self):
        self.assertFalse(self.pg.diseases['Blue'].cured)
        self.assertFalse(self.pg.diseases['Red'].cured)
        self.pg.diseases['Blue'].cured = True
        self.assertTrue(self.pg.diseases['Blue'].cured)

    def test_treat_disease_cure(self):
        self.pg.diseases['Blue'].cured = True
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(2, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.treat_disease('Blue'))
        self.assertEqual(0, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)
        self.assertFalse(self.player1.treat_disease('Red'))
        self.assertEqual(0, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)

    def test_check_charter_flight(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.check_charter_flight('London', 'Texas'))

    def test_charter_flight(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.charter_flight('London', 'New York'))
        self.assertEqual(1, len(self.pg.player_deck.discard))
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual('New York', self.player1.location.name)
        self.assertEqual(3, self.player1.action_count)
        self.assertFalse(self.player1.charter_flight('New York', 'Brighton'))
        self.assertEqual(1, len(self.pg.player_deck.discard))
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('New York', self.player1.location.name)

    def test_check_shuttle_flight(self):
        for i in range(30):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('New York')
        self.assertTrue(self.player1.build_lab())
        self.assertTrue(self.player1.check_shuttle_flight('New York', 'London'))

    def test_shuttle_flight(self):
        for i in range(30):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('New York')
        self.assertTrue(self.player1.build_lab())
        self.assertTrue(self.player1.shuttle_flight('New York', 'London'))
        self.assertEqual(1, self.player1.action_count)
        self.assertEqual('London', self.player1.location.name)

    def test_check_build_lab(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertFalse(self.pg.city_map['London'].has_lab)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.check_build_lab())

    def test_build_lab(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertFalse(self.pg.city_map['London'].has_lab)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.build_lab())
        self.assertEqual(3, self.player1.action_count)
        self.assertTrue(self.pg.city_map['London'].has_lab)
        self.assertEqual(1, len(self.pg.player_deck.discard))
        self.assertEqual('London', self.pg.player_deck.discard[0].name)

    def test_check_direct_flight(self):
        self.player1.set_location('Jinan')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.hand_contains('London'))
        self.assertTrue(self.player1.check_direct_flight('Jinan', 'London'))

    def test_direct_flight(self):
        self.player1.set_location('Moscow')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual('Moscow', self.player1.location.name)
        self.assertTrue(self.player1.direct_flight('Moscow', 'London'))
        self.assertEqual(1, len(self.pg.player_deck.discard))
        self.assertEqual('London', self.player1.location.name)
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual(3, self.player1.action_count)
        self.assertFalse(self.player1.direct_flight('Texas', 'New York'))
        self.assertEqual(1, len(self.pg.player_deck.discard))
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual('London', self.player1.location.name)
        self.assertEqual(3, self.player1.action_count)

    def test_check_standard_move(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.check_standard_move('London', 'Brighton'))

    def test_standard_move(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.standard_move('London', 'Brighton'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Brighton', self.player1.location.name)
        self.assertFalse(self.player1.standard_move('New York', 'London'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Brighton', self.player1.location.name)
        self.assertFalse(self.player1.standard_move('Brighton', 'New York'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Brighton', self.player1.location.name)
        self.assertTrue(self.player1.standard_move('Brighton', 'Southampton'))
        self.assertEqual(2, self.player1.action_count)
        self.assertEqual('Southampton', self.player1.location.name)

    def test_check_long_move(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.check_long_move('London', 'Plymouth'))
        self.assertTrue(self.player1.check_long_move('London', 'Baoding'))
        self.assertFalse(self.player1.check_long_move('Plymouth', 'Baoding'))
        self.assertFalse(self.player1.check_long_move('Baoding', 'London'))

    def test_long_move(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.long_move('London', 'Plymouth'))
        self.assertEqual(1, self.player1.action_count)
        self.assertEqual('Plymouth', self.player1.location.name)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.long_move('London', 'Oxford'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Oxford', self.player1.location.name)
        self.player1.set_location('Moscow')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.long_move('Moscow', 'Detroit'))
        self.assertEqual(2, self.player1.action_count)
        self.assertEqual('Detroit', self.player1.location.name)

    def test_make_cities(self):
        self.assertEqual('London', self.pg.city_map['London'].name)
        self.assertEqual(40, len(self.pg.city_map))
        self.assertEqual('Yellow', self.pg.city_map['Washington'].colour)

    def test_hand_contains(self):
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.hand_contains('London'))
        self.assertFalse(self.player1.hand_contains('New York'))

    def test_discard_card(self):
        self.pg.draw_card(self.player1)
        self.assertEqual(1, len(self.player1.hand))
        self.assertEqual(True, self.player1.discard_card('London'))
        self.assertEqual(0, len(self.player1.hand))
        self.assertEqual(1, len(self.pg.player_deck.discard))
        self.assertEqual('London', self.pg.player_deck.discard[0].name)

    def test_AIController(self):
        self.assertEqual('AIController1', self.player1.controller.name)

    @skip('\'PandemicGame.all_one_colour\' method is not provided yet.')
    def test_AI_cure_possible(self):
        for i in range(9):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.build_lab())
        self.assertTrue(self.player1.controller.cure_possible())

    def test_AI_build_lab_sensible(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.hand_contains('London'))
        self.assertFalse(self.pg.city_map['London'].has_lab)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('Jacksonville')
        for i in range(21):
            self.pg.draw_card(self.player1)
        self.assertEqual(6, self.player1.get_distance_from_lab())
        self.assertTrue(self.player1.hand_contains('Jacksonville'))
        self.assertTrue(self.player1.controller.build_lab_sensible())

    def test_reset_distances(self):
        self.pg.reset_distances()
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.assertEqual(999, self.pg.city_map['London'].distance)
        self.assertEqual(999, self.pg.city_map['Moscow'].distance)
        self.pg.set_lab_distances()
        self.assertNotEqual(999, self.pg.city_map['London'].distance)
        self.assertNotEqual(999, self.pg.city_map['Moscow'].distance)
        self.pg.reset_distances()
        self.assertEqual(999, self.pg.city_map['London'].distance)
        self.assertEqual(999, self.pg.city_map['Moscow'].distance)

    def test_remove_all_cubes(self):
        self.pg.infect_city('Leeds', 'Yellow')
        self.pg.infect_city('Leeds', 'Yellow')
        self.assertEqual(2, self.pg.city_map['Leeds'].get_cubes('Yellow'))
        self.pg.city_map['Leeds'].remove_all_cubes('Yellow')
        self.assertEqual(0, self.pg.city_map['Leeds'].get_cubes('Yellow'))
        self.pg.infect_city('Bristol', 'Red')
        self.assertEqual(1, self.pg.city_map['Bristol'].get_cubes('Red'))
        self.pg.city_map['Bristol'].remove_all_cubes('Red')
        self.assertEqual(0, self.pg.city_map['Bristol'].get_cubes('Red'))

    def test_set_city_distance_name(self):
        self.pg.set_city_distance_name('Leeds')
        self.assertEqual(2, self.pg.city_map['London'].distance)
        self.assertEqual(3, self.pg.city_map['Moscow'].distance)

    def test_set_cities_distances_names(self):
        cities = ['Leeds', 'Atlanta', 'Moscow']
        self.pg.set_cities_distances_names(cities)
        self.assertEqual(1, self.pg.city_map['London'].distance)
        self.assertEqual(0, self.pg.city_map['Moscow'].distance)

    def test_set_lab_distances(self):
        for i in range(21):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('New York')
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('Jinan')
        self.pg.set_lab_distances()
        self.assertEqual(0, self.pg.city_map['London'].distance)
        self.assertEqual(1, self.pg.city_map['Moscow'].distance)
        self.assertEqual(3, self.player1.get_distance_from_lab())

    @expectedFailure
    def test_get_inputs(self):
        test_inputs = self.player1.get_inputs()
        self.assertIsNotNone(test_inputs)
        print("check_ing test inputs at start of game")
        print("check_ing first 40 inputs (0-39) for city cubes are all 0")
        for i in range(40):
            self.assertEqual(test_inputs[i],0)
        print("check_ing inputs (40-46 for player1 potential cards are all 0")
        for i in range(40, 46):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (47-53 for player2 potential cards are all 0")
        for i in range(47, 53):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (54-60 for player3 potential cards are all 0")
        for i in range(54, 60):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (61-68 for player4 potential cards are all 0")
        for i in range(61, 68):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for player cards in discard are all 0")
        for i in range(69, 109):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for infect cards in discard are all 0")
        for i in range(110, 150):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for epidemic cards in game is 0")
        self.assertEqual(0, test_inputs[151])
        print("check_ing inputs for epidemic drawn in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for outbreaks in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for infection rate is 2")
        self.assertEqual(2, test_inputs[152])
        print("check_ing location for each player is set to London")
        self.assertEqual(0.975, test_inputs[153])
        print("check_ing the number of research stations in London is set to 1")
        self.assertEqual(1, test_inputs[158])
        print("check_ing number of research stations in each location is to 0")
        for i in range(159, 199):
            self.assertAlmostEqual(test_inputs[i], 0.975)
        print("checking each disease is set to uncured")
        for i in range(200, 203):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for i in range(204, 207):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("standard not possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("direct")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("charter")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("shuttle")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, test_inputs[300])
        self.assertEqual(0, test_inputs[301])

        self.pg.draw_inital_hands()
        self.pg.inital_infect_phase()
        self.pg.start_turn(self.player1)

        print("check_ing test inputs after game Start during player 1 turn")
        test_inputs = self.player1.get_inputs()
        print("check_ing first 40 inputs (0-39) for city cubes are all correct")
        self.assertEqual(0.25, test_inputs[0])
        self.assertEqual(0.25, test_inputs[3])
        self.assertEqual(0.25, test_inputs[6])
        self.assertEqual(0.50, test_inputs[1])
        self.assertEqual(0.50, test_inputs[4])
        self.assertEqual(0.50, test_inputs[7])
        self.assertEqual(0.75, test_inputs[2])
        self.assertEqual(0.75, test_inputs[5])
        self.assertEqual(0.75, test_inputs[8])
        for i in range(9, 40):
            self.assertEqual(test_inputs[i],0)
        print("check_ing inputs (40-46 for player1 potential cards are all 0")
        self.assertAlmostEqual(0.975, test_inputs[41])
        self.assertAlmostEqual(0.95, test_inputs[42])
        self.assertAlmostEqual(0.925, test_inputs[43])
        self.assertAlmostEqual(0.9, test_inputs[44])
        for i in range(45, 53):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (47-53 for player2 potential cards are all 0")
        for i in range(47, 53):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (54-60 for player3 potential cards are all 0")
        for i in range(54, 60):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (61-68 for player4 potential cards are all 0")
        for i in range(61, 68):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for player cards in discard are all 0")
        for i in range(69, 109):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for infect cards in discard are all 0")
        for i in range(110, 150):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for epidemic cards in game is 0")
        self.assertEqual(0, test_inputs[151])
        print("check_ing inputs for epidemic drawn in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for outbreaks in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for infection rate is 2")
        self.assertEqual(0, test_inputs[152])
        print("check_ing location for each player is set to London")
        for i in range(153, 158):
            self.assertEqual(test_inputs[i], 0.975)
        print("check_ing number of research stations in each location is to 0.75")
        for i in range(159, 199):
            self.assertEqual(0, test_inputs[i])
        print("checking each disease is set to uncured")
        for i in range(200, 203):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for i in range(204, 207):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("standard not possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("direct")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("charter")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("shuttle")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, test_inputs[300])
        self.assertEqual(0, test_inputs[301])


if __name__ == '__main__':
    unittest.main()
