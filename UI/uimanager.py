import pygame
import pygame_gui
from Components.player import Player
from GameState.startgame import NewGame
from Database.database import Database
from GameState.optionssetting import OptionsSettings


class UIManager:
    def __init__(self, game_world):
        self.game_world = game_world
        self.ui_manager = pygame_gui.UIManager((game_world.width, game_world.height))
        self.screen = game_world.screen

        self.menu_buttons = []
        self.create_menu_buttons()

        # For dialogs
        self.name_entry_window = None
        self.name_entry_line = None
        self.player_select_window = None
        self.player_dropdown = None

        self.startgame = NewGame(self.game_world)
        self.startgame.database = Database()  # Attach your database

        # options
        self.sound_manager = self.game_world.sound_manager
        self.options_setting = None


    def create_menu_buttons(self):
        # Create your menu buttons and add them to self.menu_buttons
        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width()/2-200, self.screen.get_height()/2-250), (400, 100)),
            text="New Game",
            manager=self.ui_manager
        )
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width()/2-200, self.screen.get_height()/2-150), (400, 100)),
            text="CONTINUE",
            manager=self.ui_manager
        )
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width()/2-200, self.screen.get_height()/2-50), (400, 100)),
            text="OPTIONS",
            manager=self.ui_manager
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width()/2-200, self.screen.get_height()/2+150), (400, 100)),
            text="QUIT",
            manager=self.ui_manager
        )

        self.back_to_map_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width - 220, self.screen.height - 320), (200, 50)),
            text="RETURN TO MAP",
            manager=self.ui_manager,
            visible=False 
        )
        
        self.show_deck_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width - 220, self.screen.height - 160), (200, 50)),
            text="Show Deck",
            manager=self.ui_manager
        )
        self.show_discard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width - 220, self.screen.height - 240), (200, 50)),
            text="Show Discard",
            manager=self.ui_manager
        )
                # End turn button
        self.end_turn_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width - 220, self.screen.height - 80), (200, 60)),
            text="End Turn",
            manager=self.ui_manager
        )

        self.menu_buttons = [self.new_game_button, self.continue_button, self.options_button, self.quit_button]
        self.game_buttons = [self.show_deck_button, self.show_discard_button, self.end_turn_button]
        
    def show_menu_buttons(self):
        for button in self.menu_buttons:
            button.show()

    def hide_menu_buttons(self):
        for button in self.menu_buttons:
            button.hide()

    def show_game_buttons(self):
        for button in self.game_buttons:
            button.show()

    def hide_game_buttons(self):
        for button in self.game_buttons:
            button.hide()

    def handle_event(self, event):
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_game_button:
                self.show_new_player_dialog()
            elif event.ui_element == self.continue_button:
                self.show_continue_dialog()
            elif self.name_entry_window and event.ui_element == self.name_entry_line:
                pass  # handled below
            elif self.player_select_window and event.ui_element == self.player_dropdown:
                pass  # handled below
            elif event.ui_element == self.options_button:
                self.show_options()
            elif event.ui_element == self.quit_button:
                self.quit_game()
            elif event.ui_element == self.back_to_map_button:
                self.return_to_map()
            elif event.ui_element == self.show_deck_button:
                self.show_card_list_window(deck_type="deck")
            elif event.ui_element == self.show_discard_button:
                self.show_card_list_window(deck_type="discard")
            elif self.game_world._game_state == "options" and self.options_setting:
                self.options_setting.handle_events(event)
                self.options_setting.draw(self.screen)

        # Handle text entry for new player
        if self.name_entry_line and event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.name_entry_line:
                player_name = event.text
                self.startgame.create_new_player(player_name)
                print(f"Created new player: {player_name}")
                self.name_entry_window.kill()
                self.name_entry_window = None
                self.name_entry_line = None
                self.game_world._game_state = "map"

        # Handle dropdown selection for continue
        if self.player_dropdown and event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.player_dropdown:
                player_id = int(event.text.split(":")[0])
                self.startgame.continue_game(player_id)
                print(f"Continuing game for player id: {player_id}")
                self.player_select_window.kill()
                self.player_select_window = None
                self.player_dropdown = None
                self.game_world._game_state = "map"
                
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(self, "save_slot_buttons"):
                for btn in self.save_slot_buttons:
                    if event.ui_element == btn:
                        player_id = btn.player_id
                        self.startgame.continue_game(player_id)
                        print(f"Continuing game for player id: {player_id}")
                        if self.player_select_window:
                            self.player_select_window.kill()
                            self.player_select_window = None
                        for b in self.save_slot_buttons:
                            b.kill()
                        self.save_slot_buttons = []
                        self.game_world._game_state = "map"

    def show_new_player_dialog(self):
        if self.name_entry_window:
            self.name_entry_window.kill()
        self.name_entry_window = pygame_gui.elements.UIWindow(
            pygame.Rect((self.screen.get_width()/2-150, self.screen.get_height()/2-50), (300, 100)),
            manager=self.ui_manager,
            window_display_title="Enter Player Name"
        )
        self.name_entry_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 10), (280, 30)),
            manager=self.ui_manager,
            container=self.name_entry_window
        )
        self.name_entry_line.set_text_length_limit(20)

    def show_continue_dialog(self):
        # Destroy previous window if it exists
        if self.player_select_window:
            self.player_select_window.kill()
            self.player_select_window = None
        # Remove old slot buttons if they exist
        if hasattr(self, "save_slot_buttons"):
            for btn in self.save_slot_buttons:
                btn.kill()
        self.save_slot_buttons = []

        players = self.startgame.database.fetch_players()
        if not players:
            print("No players found.")
            return

        # Limit to 10 slots
        players = players[:10]
        self.player_select_window = pygame_gui.elements.UIWindow(
            pygame.Rect((self.screen.get_width()/2-200, self.screen.get_height()/2-200), (400, 600)),
            manager=self.ui_manager,
            window_display_title="Select Save Slot"
        )

        for idx, player in enumerate(players):
            player_id, player_name, player_gold = player[:3]
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((20, 20 + idx*55, 360, 50)),
                text=f"Slot {idx+1}: {player_name} (Gold: {player_gold})",
                manager=self.ui_manager,
                container=self.player_select_window
            )
            btn.player_id = player_id  # Attach player_id for later reference
            self.save_slot_buttons.append(btn)

    def update(self, delta_time):
        self.ui_manager.update(delta_time)

    def draw(self, screen):
        self.ui_manager.draw_ui(screen)
        if self.game_world._game_state == "options" and self.options_setting:
            self.options_setting.draw(self.screen)



    def start_game(self):
        print("Starting Game")
        self.game_world._game_state = "map"  # Transition to the map state
        self.play_button.hide()
        self.options_button.hide()
        self.quit_button.hide()

    def start_new_game(self):
        print("Starting New Game")
        self.game_world._game_state = "map"
        
    def quit_game(self):
        print("Quitting Game")
        self.game_world._running = False

    def return_to_map(self):
        print("Returning to Map")
        self.game_world._game_state = "map"
        self.back_to_map_button.hide()
        self.game_world._fight_initialized = False
    
    def show_options(self):
        print("Showing Options")
        self.options_setting = OptionsSettings(self.sound_manager, self.game_world)
        self.game_world._game_state = "options"
            
        

    def deck_tracker(self):
        print("Showing Deck Tracker")
        self.deck_tracker_button.show()

    def show_end_turn_button(self):
        self.end_turn_button.show()

    def hide_end_turn_button(self):
        self.end_turn_button.hide()

    def show_card_list_window(self, deck_type="deck"):
        # Remove previous window if it exists
        if hasattr(self, "card_list_window") and self.card_list_window:
            self.card_list_window.kill()
            self.card_list_window = None

        # Get the deck from the player
        player = Player.get_instance()
        deck = getattr(player, "deck", None)
        if deck is None:
            print("No deck found!")
            return

        if deck_type == "deck":
            card_list = deck.draw_pile
            title = "Cards in Deck"
        else:
            card_list = deck.discarded_cards
            title = "Discarded Cards"

        card_names = [getattr(card, "name", str(card)) for card in card_list]
        card_text = "\n".join(card_names) if card_names else "No cards."

        self.card_list_window = pygame_gui.elements.UIWindow(
            pygame.Rect((self.screen.get_width()/2-200, self.screen.get_height()/2-200), (400, 400)),
            manager=self.ui_manager,
            window_display_title=title
        )
        text_box = pygame_gui.elements.UITextBox(
            html_text=card_text.replace("\n", "<br>"),
            relative_rect=pygame.Rect((10, 10), (380, 340)),
            manager=self.ui_manager,
            container=self.card_list_window
        )
