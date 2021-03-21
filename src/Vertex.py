import pygame
from pygame import gfxdraw
from Edge import Edge


class Vertex:
    """
    Vertices are points on a graph.
    They can be labeled and placed.
    Vertices can have edges connecting to other vertices.
    """

    # The screen is where the vertices are drawn on.
    screen = None

    # Default color of a vertex if black.
    black = (0, 0, 0)

    # Default radius of vertex is 2.
    radius = 5

    # Buffer around the vertices that prevents other vertices from being
    # added too closely
    buffer = radius * 2

    def __init__(self, posX, posY, color=black):
        # posX and posY are the centers of each vertex
        self.posX = posX
        self.posY = posY
        self.color = color

    def drawVertex(self):
        """
        Draws a vertex onto a screen
        """
        gfxdraw.aacircle(self.screen, self.posX, self.posY, self.radius,
                         self.color)
        gfxdraw.filled_circle(self.screen, self.posX, self.posY, self.radius,
                              self.color)

    def isInBounds(self, x, y):
        """
        Checks if a given position is within the boundary of a vertex
        """
        if (self.getPosX() + self.getRadius() + self.buffer >= x >=
            self.getPosX() -
            self.getRadius() - self.buffer) \
                and \
                (self.getPosY() + self.getRadius() + self.buffer >= y >=
                 self.getPosY() - self.getRadius() - self.buffer):
            return True

        return False

    def setColor(self, color):
        """
        Changes the color of a given vertex
        """
        if self.color != self.black:
            self.color = self.black
        else:
            self.color = color

    def getPosX(self):
        """
        Returns the posX
        """
        return self.posX

    def getPosY(self):
        """
        Returns the posY
        """
        return self.posY

    def getColor(self):
        """
        Returns the color of the vertices
        """
        return self.color

    def getRadius(self):
        """
        Gets the value of the radius for each vertex
        """
        return self.radius


def getScreen():
    """
    Returns the screen used for all vertices
    """
    return Vertex.screen


def setScreen(tempScreen):
    """
    Sets the screen for all vertices, only needs to be done once.
    :param tempScreen: The main screen
    """
    Vertex.screen = tempScreen


def setColor(color):
    """
    Sets the color of all vertices.
    :param color: Color of all vertices.
    """
    Vertex.color = color
