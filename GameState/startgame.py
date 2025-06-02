from Components.planet import Planet
from Components.player import Player
from Database.sqlrepository import SQLRepository
from FactoryPatterns.artifactFactory import ArtifactFactory
from gameobject import GameObject
from GameState.map import Map


class NewGame:
    def __init__(self, game_world):
        self._game_world = game_world
        self.repository = SQLRepository()
        self.artifact_factory = ArtifactFactory()
        
    def create_new_player(self, name):
        player = Player.get_instance()
        player._credits = 50
        player._scraps = 10
        player._health = 100
        player._max_health = 100
        # Insert player and get ID
        player._id = self.repository.insert_player(name, player._credits, player._scraps, player._health, player._max_health)
        player.name = name
        print(f"New player created: {name} (ID: {player._id})")

        self._game_world.map.generate_planets()
        planets = self._game_world.map.planets
        if not planets:
            print("[error] No planets generated.")
            return None
        for planet in planets:
            print(f"Adding planet: {planet}")
            planet_component = planet.get_component("Planet")
            self.repository.insert_planet(
                player._id,
                planet_component.name,
                planet_component.color[0],
                planet_component.color[1],
                planet_component.color[2],
                False,
                int(planet_component.position[0]),
                int(planet_component.position[1]),
                planet_component.size
            )
        return player._id

    def continue_game(self, player_id):
        player_data = self.repository.fetch_player(player_id)
        if player_data:
            player = Player.get_instance()
            player._id = player_data[0]
            player.name = player_data[1]
            player._credits = player_data[2]
            player._scraps = player_data[3]
            player._health = player_data[4]
            player._max_health = player_data[5]

        # Load planets for this player
        planet_rows = self.repository.fetch_planets_for_player(player_id)
        for row in planet_rows:
            name, r, g, b, explored, x, y, size = row
            planet = GameObject((x, y))
            planet.add_component(Planet(name, size, (r, g, b), (x, y), self._game_world))
            planet.get_component("Planet")._visited = explored
            self._game_world.map.planets.append(planet)
            self._game_world._gameObjects.append(planet)

        artifacts_rows = self.repository.fetch_player_artifacts(player_id)
        for row in artifacts_rows:
            artifact_id = row[1]
            artifact_data = self.repository.fetch_artifact_by_id(artifact_id)
            if artifact_data:
                artifact_go = self.artifact_factory.create_component(artifact_data)
                player.artifacts.append(artifact_go)
                self._game_world.instantiate(artifact_go)
        player.update_artifacts()
                

    def get_player_list(self):
        return self.repository.fetch_players()
