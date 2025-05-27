import pygame
from Components.component import Component
from Components.player import Player

# made by Erik

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
        card_component = self.gameObject.get_component("Card")
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
        card_damage = getattr(get_card_component, "damage", 0)

        
        if card_type == "Attack":
            print(f"[card activated] {card_type} activated")        
            if target: 
                
                enemy_component = target.get_component("Enemy")
                if enemy_component:
                    card_damage= 10
                    enemy_component.take_damage(card_damage)
                    print(f"[card activated] {card_type} dealt {card_damage} to {enemy_component.name}")
                else:
                    print("[error] Target does not have an Enemy component.")

        else:
            print("you missed the target")       

    
    def block_card_activated(self, game_world, target=None):
        get_card_component = self.get_card_component()

        card_type = getattr(get_card_component, "_type", "")
        
        if card_type == "Block":
            print("Block activated")

            player = None
            for obj in game_world._gameObjects:
                player_component = obj.get_component("Player")
                if player_component:
                    player = player_component
                    break
            if player:
                player.block_points += 2
                print(f"[card activated] {card_type} activated, block points: {player.block_points}")


    def update(self, delta_time):
        #  Local import to avoid circular dependency
        from gameworld import GameWorld

        sprite_renderer = self.gameObject.get_component("SpriteRenderer")
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

            card_info = self.gameObject.get_component("Card")
            if not card_info:
                return

            info_text = f"Name: {getattr(card_info, '_name', '???')} - rarity: {getattr(card_info, '_rarity', '???')} - value: {getattr(card_info, '_value', '???')}"
            description = f"Description: {getattr(card_info, '_description', '???')}"

            text_surface_1 = self.font.render(info_text, True, (255, 255, 255))
            text_surface_2 = self.font.render(description, True, (200, 200, 200))

             # Center the text in the middle of the screen
            screen_center = self._game_world.screen.get_rect().center
            text_x = screen_center[0] - (max(text_surface_1.get_width(), text_surface_2.get_width()) // 2)
            text_y = screen_center[1] - 100  # slightly above center

            text_bg_rect = pygame.Rect(
                text_x - 5,
                text_y - 5,
                max(text_surface_1.get_width(), text_surface_2.get_width()) + 10,
                60
            )
            pygame.draw.rect(self._game_world.screen, (0, 0, 0), text_bg_rect)
            pygame.draw.rect(self._game_world.screen, (255, 255, 255), text_bg_rect, 1)

            self._game_world.screen.blit(text_surface_1, (text_x, text_y))
            self._game_world.screen.blit(text_surface_2, (text_x, text_y + 25))
            
            if pygame.mouse.get_pressed()[0]:  # Left click
                if not self.clicked:
                    self.clicked = True
                    print(f"Card clicked!")                 
                enemy_target = None
                for obj in self._game_world._gameObjects:
                    enemy_component = obj.get_component("Enemy")
                    if enemy_component and enemy_component.is_alive:
                        enemy_target = obj
                        break

                self.card_type_activated(self._game_world, target=enemy_target) 
                self.player.deck.discarded_cards.append(self.gameObject.get_component("Card"))
                self._game_world.card_pool.release(self.gameObject)  # Add to pool instead of just destroying
                self.gameObject.is_destroyed = True  # Mark for removal from game world

        else:
            self.clicked = False
