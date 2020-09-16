import typing
from stimpack import Container, Component

class Foo(object):

    def hello(self) -> str:
        return "hello"

class Bar(object):

    def __init__(self, name: str):
        self._name = name

    def hello(self) -> str:
        return f"hello {self._name}"

class Baz(object):

    def __init__(self, bar: Bar):
        self._bar = bar

    def hello(self) -> str:
        return f"bar says {self._bar.hello()}"

container = Container(
    Component(comp_type=Foo),
    Component(comp_type=Bar, init=("world",)),
    Component(comp_type=Baz)
)

def test_usage():
    assert container.get(Foo).hello() == "hello"
    assert container.get(Foo) == container.get(Foo)

    assert container.get(Bar).hello() == "hello world"
    assert container.get(Baz).hello() == "bar says hello world"

def test_function_curry_injection():
    
    @container.inject(baz=Baz)
    def hello(prefix: str, baz: Baz = None) -> str:
        return f"{prefix} {baz.hello()}"

    assert hello("hey!") == "hey! bar says hello world"