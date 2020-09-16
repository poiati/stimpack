import sys

sys.path.append("../")

import stimpack
from fastapi import FastAPI
from stimpack import Container, Component


class Renderer(object):
    def render(self):
        return "Rendered!"


app = FastAPI()

container = Container(
    Component(comp_type=Renderer)
)


@app.get("/")
@container.inject(renderer=Renderer)
def index(renderer: Renderer):
    return renderer.render()