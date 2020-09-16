from stimpack import Component

class Bar(object):
    pass

class Foo(object):

    def __init__(self, bar: Bar):
        self.bar = bar

def test_component_type():
    assert Component(comp_type=Foo).comp_type == Foo

def test_component_dependencies():
    assert Component(comp_type=Foo).dependencies == (Bar,)

def test_component_new_instance():
    assert Component(comp_type=Foo).new_instance({Bar: Bar()})