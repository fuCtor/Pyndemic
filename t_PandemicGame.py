import unittest
from PandemicGame import PandemicGame
from player import Player


class MyTestCase(unittest.TestCase):
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
        for x in range(0,11):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertTrue(self.pg.has_x_cube_city(3))

    def test_complete_round(self):
        self.pg.inital_infect_phase()
        self.pg.draw_inital_hands()
        self.assertEqual(3, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.pg.complete_round()
        self.assertEqual(0, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual('Cambridge', self.player1.location.name)
        self.assertEqual(0, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.assertEqual('Bristol', self.player1.location.name)

    def test_add_player(self):
        self.assertEqual(self.pg, self.player1.game)

    def test_add_disease_cubes(self):
        self.assertEqual(30, self.pg.disease_cubes['Red'])
        self.assertEqual(30, self.pg.disease_cubes['Blue'])

    def test_setup_game(self):
        self.london = self.pg.city_map['London']
        self.newyork = self.pg.city_map['New York']
        self.top_player_card = self.pg.player_deck.take_top_card()
        self.top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual(30, self.pg.disease_cubes['Red'])
        self.assertEqual(30, self.pg.disease_cubes['Blue'])
        self.assertEqual('Evie', self.pg.players[0].name)
        self.assertEqual('Amelia', self.pg.players[1].name)
        self.assertFalse(self.pg.game_won)
        self.assertFalse(self.pg.game_over)
        self.assertEqual('London', self.london.name)
        self.assertEqual(6, len(self.london.connected_cities))
        self.assertEqual('Blue', self.london.colour)
        self.assertEqual('New York', self.newyork.name)
        self.assertEqual(3, len(self.newyork.connected_cities))
        self.assertEqual('Yellow', self.newyork.colour)
        self.assertEqual(2, self.pg.infection_rate)
        self.assertEqual(0, self.pg.epidemic_count)
        self.assertEqual(0, self.pg.outbreak_count)
        self.assertEqual('London', self.top_player_card.name)
        self.assertEqual('London', self.top_infect_card.name)
        self.assertEqual('Blue', self.top_player_card.colour)
        self.assertEqual('Blue', self.top_infect_card.colour)
        self.assertEqual('London', self.pg.players[0].location.name)
        self.assertEqual('London', self.pg.players[1].location.name)

    def test_get_new_decks(self):
        self.pg.get_new_decks(self.settings_location)
        top_player_card = self.pg.player_deck.take_top_card()
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('London', top_player_card.name)
        self.assertEqual('London', top_infect_card.name)

    def test_add_card(self):
        top_player_card = self.pg.player_deck.take_top_card()
        self.player1.add_card(top_player_card)
        self.assertEqual(1, len(self.player1.hand))
        self.assertTrue(self.player1.hand_contains('London'))

    def test_get_new_cities(self):
        self.pg.get_new_cities(self.settings_location)
        city1 = self.pg.city_map['London']
        self.assertEqual(6, len(city1.connected_cities))
        self.assertEqual('Blue', city1.colour)
        self.assertEqual('Washington', city1.connected_cities[4].name)

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

    def test_get_infection_rate(self):
        self.assertEqual(2, self.pg.infection_rate)

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
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Southampton'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Plymouth'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Liverpool'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Manchester'].get_cubes('Blue'))
        self.assertEqual(9, self.pg.infect_deck.getDiscardCount())
        self.assertEqual(12, self.pg.disease_cubes.get('Blue'))

    def test_draw_initial_hands(self):
        self.pg.start_game()
        # TODO: assertions

    def test_draw_card(self):
        self.pg.draw_card(self.player1)
        self.assertEqual('London', self.player1.hand[0].name)

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

    def test_cure_disease(self):
        self.assertFalse(self.pg.diseases.get('Blue').cured)
        for i in range(15):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.build_lab())
        self.assertTrue(self.player1.cure_disease('Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester'))
        self.assertTrue(self.pg.diseases['Blue'].cured)
        self.assertEqual(2, self.player1.action_count)

    def test_CheckShareKnowledge(self):
        self.player1.set_location('London')
        self.player2.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.checkShareKnowledge('London', self.player2))
        self.player2.set_location('New York')
        self.assertFalse(self.player1.checkShareKnowledge('London', self.player2))

    def test_ShareKnowledge(self):
        self.player1.set_location('London')
        self.player2.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(True, self.player1.shareKnowledge('London', self.player2))
        self.assertEqual('London', self.player2.hand[0].name)
        self.assertEqual(3, self.player1.action_count)

    def test_CheckTreatDisease(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('London', 'Blue')
        self.assertTrue(self.player1.checkTreatDisease('Blue'))
        self.assertFalse(self.player1.checkTreatDisease('Red'))

    def test_TreatDiseaseNoCure(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(2, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.treatDisease('Blue'))
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual(False, self.player1.treatDisease('Red'))
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)

    def test_GetNewDiseaes(self):
        self.assertFalse(self.pg.diseases.get('Blue').cured)
        self.assertFalse(self.pg.diseases.get('Red').cured)
        self.pg.diseases.get('Blue').setCured(True)
        self.assertTrue(self.pg.diseases.get('Blue').cured)

    def test_TreatDiseaseCure(self):
        self.pg.diseases.get('Blue').setCured(True)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.infect_city('London', 'Blue')
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(2, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.treatDisease('Blue'))
        self.assertEqual(0, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual(False, self.player1.treatDisease('Red'))
        self.assertEqual(0, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.player1.action_count)

    def test_CheckCharterFlight(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.checkCharterFlight('London', 'Texas'))

    def test_CharterFlight(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.charterFlight('London', 'New York'))
        self.assertEqual(1, self.pg.player_deck.getDiscardCount())
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual('New York', self.player1.location.name)
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual(self.player1.charterFlight('New York', 'Brighton'), False)
        self.assertEqual(1, self.pg.player_deck.getDiscardCount())
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('New York', self.player1.location.name)

    def test_CheckShuttleFlight(self):
        for x in range(30):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(True, self.player1.build_lab())
        self.player1.set_location('New York')
        self.assertEqual(True, self.player1.build_lab())
        self.assertTrue(self.player1.checkShuttleFlight('New York', 'London'))

    def test_ShuttleFlight(self):
        for x in range(30):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(True, self.player1.build_lab())
        self.player1.set_location('New York')
        self.assertEqual(True, self.player1.build_lab())
        self.assertEqual(True, self.player1.shuttleFlight('New York', 'London'))
        self.assertEqual(1, self.player1.action_count)
        self.assertEqual('London', self.player1.location.name)

    def test_Checkbuild_lab(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertFalse(self.pg.city_map['London'].hasLab)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.checkbuild_lab())

    def test_build_lab(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertFalse(self.pg.city_map['London'].hasLab)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.build_lab())
        self.assertEqual(3, self.player1.action_count)
        self.assertTrue(self.pg.city_map['London'].getLab())
        self.assertEqual(1, self.pg.player_deck.getDiscardCount())
        self.assertEqual('London', self.pg.player_deck.discard[0].name)

    def test_CheckDirectFlight(self):
        self.player1.set_location('Jinan')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.hand_contains('London'))
        self.assertTrue(self.player1.checkDirectFlight('Jinan', 'London'), True)

    def test_DirectFlight(self):
        self.player1.set_location('Moscow')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual('Moscow', self.player1.location.name)
        self.assertTrue(self.player1.directFlight('Moscow', 'London'))
        self.assertEqual(1, self.pg.player_deck.getDiscardCount())
        self.assertEqual('London', self.player1.location.name)
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual(self.player1.directFlight('Texas', 'New York'), False)
        self.assertEqual(1, self.pg.player_deck.getDiscardCount())
        self.assertEqual('London', self.pg.player_deck.discard[0].name)
        self.assertEqual('London', self.player1.location.name)
        self.assertEqual(3, self.player1.action_count)

    def test_CheckStandardMove(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.checkStandardMove('London', 'Brighton'))

    def test_StandardMove(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.standardMove('London', 'Brighton'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Brighton', self.player1.location.name)
        self.assertFalse(self.player1.standardMove('New York', 'London'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Brighton', self.player1.location.name)
        self.assertFalse(self.player1.standardMove('Brighton', 'New York'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Brighton', self.player1.location.name)
        self.assertTrue(self.player1.standardMove('Brighton', 'Southampton'))
        self.assertEqual(2, self.player1.action_count)
        self.assertEqual('Southampton', self.player1.location.name)

    def test_CheckLongMove(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.checkLongMove('London', 'Plymouth'))
        self.assertTrue(self.player1.checkLongMove('London', 'Baoding'))
        self.assertFalse(self.player1.checkLongMove('Plymouth', 'Baoding'))
        self.assertFalse(self.player1.checkLongMove('Baoding', 'London'))

    def test_LongMove(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.longMove('London', 'Plymouth'))
        self.assertEqual(1, self.player1.action_count)
        self.assertEqual('Plymouth', self.player1.location.name)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.longMove('London', 'Oxford'))
        self.assertEqual(3, self.player1.action_count)
        self.assertEqual('Oxford', self.player1.location.name)
        self.player1.set_location('Moscow')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertTrue(self.player1.longMove('Moscow', 'Detroit'))
        self.assertEqual(2, self.player1.action_count)
        self.assertEqual('Detroit', self.player1.location.name)

    def test_MakeCities(self):
        self.assertEqual('London', self.pg.city_map['London'].name)
        self.assertEqual(40, self.pg.city_map.__len__())
        self.assertEqual('Yellow', self.pg.city_map['Washington'].colour)

    def test_hand_contains(self):
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.hand_contains('London'))
        self.assertFalse(self.player1.hand_contains('New York'))

    def test_DiscardCard(self):
        self.pg.draw_card(self.player1)
        self.assertEqual(1, self.player1.getHandSize())
        self.assertEqual(True, self.player1.discardCard('London'))
        self.assertEqual(0, self.player1.getHandSize())
        self.assertEqual(1, self.pg.player_deck.discard.__len__())
        self.assertEqual('London', self.pg.player_deck.discard[0].name)

    def test_AIcontroller(self):
        self.assertEqual('AIcontroller1', self.player1.getController().name)

    def test_AI_CurePossible(self):
        for x in range(9):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.build_lab())
        self.assertTrue(self.player1.getController().curePossible())

    def test_AI_build_labSensible(self):
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertFalse(self.pg.city_map['London'].hasLab)
        self.assertEqual(4, self.player1.action_count)
        self.assertEqual(True, self.player1.build_lab())
        self.player1.set_location('Jacksonville')
        for x in range(21):
            self.pg.draw_card(self.player1)
        self.assertEqual(6, self.player1.getDistanceFromLab())
        self.assertTrue(self.player1.hand_contains('Jacksonville'))
        self.assertTrue(self.player1.getController().build_labSensible())

    def test_ResetDistances(self):
        self.pg.resetDistances()
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertEqual(True, self.player1.build_lab())
        self.assertEqual(999, self.pg.city_map['London'].getDistance())
        self.assertEqual(999, self.pg.city_map['Moscow'].getDistance())
        self.pg.setLabDistances()
        self.assertNotEqual(999, self.pg.city_map['London'].getDistance())
        self.assertNotEqual(999, self.pg.city_map['Moscow'].getDistance())
        self.pg.resetDistances()
        self.assertEqual(999, self.pg.city_map['London'].getDistance())
        self.assertEqual(999, self.pg.city_map['Moscow'].getDistance())

    def test_RemoveAllCubes(self):
        self.pg.infect_city('Leeds', 'Yellow')
        self.pg.infect_city('Leeds', 'Yellow')
        self.assertEqual(2, self.pg.city_map['Leeds'].get_cubes('Yellow'))
        self.pg.city_map['Leeds'].removeAllCubes('Yellow')
        self.assertEqual(0, self.pg.city_map['Leeds'].get_cubes('Yellow'))
        self.pg.infect_city('Bristol', 'Red')
        self.assertEqual(1, self.pg.city_map['Bristol'].get_cubes('Red'))
        self.pg.city_map['Bristol'].removeAllCubes('Red')
        self.assertEqual(0, self.pg.city_map['Bristol'].get_cubes('Red'))

    def test_SetCityDistanceName(self):
        self.pg.setCityDistanceName('Leeds')
        self.assertEqual(2, self.pg.city_map['London'].getDistance())
        self.assertEqual(3, self.pg.city_map['Moscow'].getDistance())

    def test_SetDistanceCitiesName(self):
        cities = ['Leeds', 'Atlanta', 'Moscow']
        self.pg.setCitiesDistancesNames(cities)
        self.assertEqual(1, self.pg.city_map['London'].getDistance())
        self.assertEqual(0, self.pg.city_map['Moscow'].getDistance())

    def test_setDistanceLabs(self):
        for x in range(21):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertEqual(True, self.player1.build_lab())
        self.player1.set_location('New York')
        self.pg.draw_card(self.player1)
        self.assertEqual(True, self.player1.build_lab())
        self.player1.set_location('Jinan')
        self.pg.setLabDistances()
        self.assertEqual(0, self.pg.city_map['London'].getDistance())
        self.assertEqual(1, self.pg.city_map['Moscow'].getDistance())
        self.assertEqual(3, self.player1.getDistanceFromLab())

    def test_getInputs(self):
        print("Checking test inputs at start of game")
        testInputs = self.player1.getInputs()
        print("Checking first 40 inputs (0-39) for city cubes are all 0")
        for x in range(40):
            self.assertEqual(testInputs[x],0)
        print("Checking inputs (40-46 for player1 potential cards are all 0")
        for x in range(40, 46):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (47-53 for player2 potential cards are all 0")
        for x in range(47, 53):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (54-60 for player3 potential cards are all 0")
        for x in range(54, 60):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (61-68 for player4 potential cards are all 0")
        for x in range(61, 68):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for player cards in discard are all 0")
        for x in range(69, 109):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for infect cards in discard are all 0")
        for x in range(110, 150):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for epidemic cards in game is 0")
        self.assertEqual(0, testInputs[151])
        print("Checking inputs for epidemic drawn in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for outbreaks in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for infection rate is 2")
        self.assertEqual(2, testInputs[152])
        print("Checking location for each player is set to London")
        self.assertEqual(0.975, testInputs[153])
        print("Checking the number of research stations in London is set to 1")
        self.assertEqual(1, testInputs[158])
        print("Checking number of research stations in each location is to 0")
        for x in range(159, 199):
            self.assertEqual(testInputs[x], 0.975)
        print("checking each disease is set to uncured")
        for x in range(200, 203):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for x in range(204, 207):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("standard not possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("direct")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("charter")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("shuttle")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, testInputs[300])
        self.assertEqual(0, testInputs[301])

        self.pg.draw_inital_hands()
        self.pg.inital_infect_phase()
        self.pg.start_turn(self.player1)

        print("Checking test inputs after game Start during player 1 turn")
        testInputs = self.player1.getInputs()
        print("Checking first 40 inputs (0-39) for city cubes are all correct")
        self.assertEqual(0.25, testInputs[0])
        self.assertEqual(0.25, testInputs[3])
        self.assertEqual(0.25, testInputs[6])
        self.assertEqual(0.50, testInputs[1])
        self.assertEqual(0.50, testInputs[4])
        self.assertEqual(0.50, testInputs[7])
        self.assertEqual(0.75, testInputs[2])
        self.assertEqual(0.75, testInputs[5])
        self.assertEqual(0.75, testInputs[8])
        for x in range(9, 40):
            self.assertEqual(testInputs[x],0)
        print("Checking inputs (40-46 for player1 potential cards are all 0")
        self.assertEqual(0.975, testInputs[41])
        self.assertEqual(0.95, testInputs[42])
        self.assertEqual(0.925, testInputs[43])
        self.assertEqual(0.9, testInputs[44])
        for x in range(45, 53):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (47-53 for player2 potential cards are all 0")
        for x in range(47, 53):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (54-60 for player3 potential cards are all 0")
        for x in range(54, 60):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs (61-68 for player4 potential cards are all 0")
        for x in range(61, 68):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for player cards in discard are all 0")
        for x in range(69, 109):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for infect cards in discard are all 0")
        for x in range(110, 150):
            self.assertEqual(testInputs[x], 0)
        print("Checking inputs for epidemic cards in game is 0")
        self.assertEqual(0, testInputs[151])
        print("Checking inputs for epidemic drawn in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for outbreaks in game is 0")
        self.assertEqual(0, testInputs[152])
        print("Checking inputs for infection rate is 2")
        self.assertEqual(0, testInputs[152])
        print("Checking location for each player is set to London")
        for x in range(153, 158):
            self.assertEqual(testInputs[x], 0.975)
        print("Checking number of research stations in each location is to 0.75")
        for x in range(159, 199):
            self.assertEqual(0, testInputs[x])
        print("checking each disease is set to uncured")
        for x in range(200, 203):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for x in range(204, 207):
            self.assertEqual(testInputs[x], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("standard not possible")
        for x in range(208, 248):
            self.assertEqual(testInputs[x], 0)
        print("direct")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("charter")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("shuttle")
        for x in range(249, 289):
            self.assertEqual(testInputs[x], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, testInputs[300])
        self.assertEqual(0, testInputs[301])


if __name__ == '__main__':
    unittest.main()
