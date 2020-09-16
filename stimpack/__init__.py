import logging
import sys
from functools import partial
from typing import get_type_hints, Any, Callable, Dict, Sequence, Type, TypeVar


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


T = TypeVar("T")


class Component(object):

    def __init__(self, comp_type: Type[T], init: Sequence[Any] = None):
        self._comp_type = comp_type
        self._init = init

    @property
    def comp_type(self) -> type:
        return self._comp_type

    @property
    def dependencies(self) -> Sequence[Any]:
        return tuple(get_type_hints(self.comp_type.__init__).values())

    def new_instance(self, component_pool: Dict[type, Any] = {}) -> T:
        if self._init is not None:
            return self.comp_type(*self._init)
        if not self.dependencies:
            return self.comp_type()
        return self.comp_type(*(component_pool[dep_type] for dep_type in self.dependencies))


class Container(object):

    def __init__(self, *components: Component):
        self._components: Dict[type, Component] = {}
        self._component_pool: Dict[type, Any] = {}
        self._register_components(components)

    def get(self, component_type: Type[T]) -> T:
        return self._component_pool[component_type]

    def inject(self, **types: type) -> Callable:
        def decorated(fn: Callable) -> Callable:
            for key in types:
                del fn.__annotations__[key]
            return partial(fn, **{key: self._component_pool[value] for (key, value) in types.items()})
        return decorated

    def _register_components(self, components: Sequence[Component]):
        for component in components:
            self._components[component.comp_type] = component
            logger.info(f"Registered Component[{component.comp_type}]")
            instance = self._components[component.comp_type].new_instance(self._component_pool)
            logger.info(f"Created a new Component[{component.comp_type}] instance")
            self._component_pool[component.comp_type] = instance

