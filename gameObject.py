from Components.component import Transform


class GameObject:

    def __init__(self, position) -> None:
        self._components = {}
        self._transform = self.add_component(Transform(position))
        self._is_destroyed = False

    @property
    def transform(self):
        return self._transform
    
    @property
    def is_destroyed(self):
        return self._is_destroyed
    
    @is_destroyed.setter
    def is_destroyed(self, value):
        self._is_destroyed = value
    
    def destroy(self):
        self._is_destroyed = True
        # self._components.clear()
    
    # Here we add a component to an object, such as transform or spriterenderer etc.
    def add_component(self, component):
        component_name = component.__class__.__name__
        self._components[component_name] = component
        component.gameObject = self
        return component
    
    # and here we remove said component, if needed
    def remove_component(self, component):
        component_name = component.__class__.__name__
        if component_name in self._components:
            print(f"{component_name} is being deleted..." )
            del self._components[component_name]
            component.gameObject = None  # Clear reference to the GameObject


    def get_component(self, component_name):
        return self._components.get(component_name, None)
    
    def awake(self, game_world):
        for component in list(self._components.values()):  
            component.awake(game_world)

    def start(self):
        for component in list(self._components.values()):  
            component.start()

    def update(self, delta_time):
        for component in list(self._components.values()):  
            component.update(delta_time)
