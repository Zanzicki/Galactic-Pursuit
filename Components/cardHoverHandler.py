import pygame
from Components.card import Card
from Components.component import Component
from Components.player import Player
from soundmanager import SoundManager
from Components.card import Card
# mad by Erik

class CardHoverHandler(Component):  
    def __init__(self):
        super().__init__()
        self._hovered = False
        self.clicked = False
        self.font = pygame.font.Font(None, 36)
        self.player = Player.get_instance()  # Get the Singleton Player instance

    def awake(self, game_world):
        self._game_world = game_world

    def start(self):
        pass
    
    def get_card_component(self):
        card_component = self.gameObject.get_component("CardDisplay").card_data
        if not card_component:
            print("[error] No Card component found on this GameObject.")
            return None
        return card_component

    # method to see wich type has been activated
    # and call the right method
    def card_type_activated(self, game_world, target=None):
        get_card_component = self.get_card_component()

        card_type = getattr(get_card_component, "_type", "")

        if card_type == "Attack":
                self.attack_card_activated(game_world, target)

        elif card_type == "Block":
            self.block_card_activated(game_world, target)
        elif card_type == "Deck":
            print("Deck activated")

    def attack_card_activated(self, game_world, target=None):      
        get_card_component = self.get_card_component()
        card_type = getattr(get_card_component, "_type", "")
        card_damage = getattr(get_card_component, "_value", 0)  # Use _value from card

        if card_type == "Attack":
            print(f"[card activated] {card_type} activated")        
            if target: 
                enemy_component = target.get_component("Enemy") or target.get_component("Boss")
                if enemy_component:
                    enemy_component.take_damage(card_damage)
                    print(f"[card activated] {card_type} dealt {card_damage} to {enemy_component.name}")
                    SoundManager().play_sound("laser")
                else:
                    print("[error] Target does not have an Enemy component.")
        else:
            print("you missed the target")       

    
    def block_card_activated(self, game_world, target=None):
        get_card_component = self.get_card_component()
        card_type = getattr(get_card_component, "_type", "")
        card_block = getattr(get_card_component, "_value", 0)  # Use _value from card

        if card_type == "Block":
            print("Block activated")

            player = None
            for obj in game_world._gameObjects:
                player_component = obj.get_component("Player")
                if player_component:
                    player = player_component
                    break
            if player:
                player.add_temp_health(card_block)
                print(f"[card activated] {card_type} activated, block points: {player.temp_health}")
                SoundManager().play_sound("shield_up")


    def update(self, delta_time):
        sprite_renderer = self.gameObject.get_component("SpriteRenderer")
        card_component = self.gameObject.get_component("Card")
        if not sprite_renderer:
            return

        rect = pygame.Rect(
            self.gameObject.transform.position[0],
            self.gameObject.transform.position[1],
            sprite_renderer.sprite_image.get_width(),
            sprite_renderer.sprite_image.get_height()
        )

        mouse_pos = pygame.mouse.get_pos()
        self._hovered = rect.collidepoint(mouse_pos)

        if self._hovered:
             pygame.draw.rect(self._game_world.screen, (255, 0, 0), rect, 2)

        card_info = self.gameObject.get_component("CardDisplay").card_data
        if not card_info:
                return


        info_text = f"Name: {getattr(card_info, '_name', '???')} - rarity: {getattr(card_info, '_rarity', '???')} - value: {getattr(card_info, '_value', '???')}"
        description = f"Description: {getattr(card_info, '_description', '???')}"

        text_surface_1 = self.font.render(info_text, True, (255, 255, 255))
        text_surface_2 = self.font.render(description, True, (200, 200, 200))

            # Background box for text
        text_bg_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], max(text_surface_1.get_width(), text_surface_2.get_width()) + 10, 40)
        pygame.draw.rect(self._game_world.screen, (0, 0, 0), text_bg_rect)
        pygame.draw.rect(self._game_world.screen, (255, 255, 255), text_bg_rect, 1)

            # Draw text on top of the background box
        self._game_world.screen.blit(text_surface_1, (mouse_pos[0] + 5, mouse_pos[1] + 2))
        self._game_world.screen.blit(text_surface_2, (mouse_pos[0] + 5, mouse_pos[1] + 20))


        if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if not self.clicked:
                    self.clicked = True
                    print(f"Card clicked!")                 
                enemy_target = None
                for obj in self._game_world._gameObjects:
                    boss_component = obj.get_component("Boss")
                    if boss_component and boss_component._is_alive:
                        enemy_target = obj
                        break
                    enemy_component = obj.get_component("Enemy")
                    if enemy_component and enemy_component.is_alive:
                        enemy_target = obj
                        break

                if enemy_target:
                    self.card_type_activated(self._game_world, target=enemy_target)
                    self.play_card()

        else:
            self.clicked = False

    def play_card(self):
        card = self.gameObject.get_component("CardDisplay").card_data
        self.player.deck.play_card(card)
        self._game_world.card_pool.release(self.gameObject)
        self.gameObject.is_destroyed = True
