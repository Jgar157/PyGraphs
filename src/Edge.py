"""
Edge class containing all functions regarding edges
"""
from pygame import gfxdraw
import Vertex


class Edge:
    """
    An edge connects two vertices together.
    Without one of the vertices, the edge cannot exist.
    """

    screen = None
    black = (0, 0, 0)

    def __init__(self, vertexOne, vertexTwo, color=black):
        self.vertexOne = vertexOne
        self.vertexTwo = vertexTwo
        self.color = color

    def getVertexOne(self):
        """
        Returns vertexOne
        """
        return self.vertexOne

    def getVertexTwo(self):
        """
        Returns vertexTwo
        """
        return self.vertexTwo

    def areVerticesCorrect(self, one, two):
        """
        Checks if inputted vertices are the vertices of the edge
        one: The first vertex
        two: The second vertex
        """
        if self.vertexOne == one and self.vertexTwo == two:
            return True
        elif self.vertexOne == two and self.vertexTwo == one:
            return True
        else:
            return False

    def draw(self):
        """
        Draws the edge from vertexOne to vertexTwo
        """
        gfxdraw.line(getScreen(), self.vertexOne.getPosX(),
                     self.vertexOne.getPosY(), self.vertexTwo.getPosX(),
                     self.vertexTwo.getPosY(), self.color)

    def setColor(self, color):
        """
        Sets the color for the edge
        """
        self.color = color

    def getDefaultColor(self):
        """
        Returns the default color of the edge
        """
        return self.black

    def setColorDefault(self):
        """
        Sets the color to the default color
        """
        self.setColor(self.getDefaultColor())


def setScreen(tempScreen):
    """
    Sets the screen for the edges to be drawn on
    """
    Edge.screen = tempScreen


def getScreen():
    """
    Returns the screen the edge class is using
    """
    return Edge.screen
