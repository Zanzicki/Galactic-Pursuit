from Components.card import Card
from Components.component import SpriteRenderer
from gameobject import GameObject
import pygame
from FactoryPatterns.factorypattern import Factory
from Components.cardhoverhandler import CardHoverHandler

class CardFactory(Factory):
    def create_component(self):
        go = GameObject(pygame.math.Vector2(250, 250))
        go.add_component(Card("Card", 0, "Card", "Common", "A simple card", 67))
        go.add_component(SpriteRenderer("Cards/floppycard.png"))
        go.add_component(CardHoverHandler())
        go.get_component("SpriteRenderer").sprite_image = pygame.transform.scale(go.get_component("SpriteRenderer").sprite_image, (150, 150))

        return go
    
    def create_component(self, card):
        go = GameObject(pygame.math.Vector2(250, 250))
        go.add_component(card)
        go.add_component(SpriteRenderer(("Cards/floppycard.png")))
        go.add_component(CardHoverHandler())
        go.get_component("SpriteRenderer").sprite_image = pygame.transform.scale(go.get_component("SpriteRenderer").sprite_image, (150, 150))
        return go