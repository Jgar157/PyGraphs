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
    defaultColor = black
    selectedColor = (0, 0, 255)
    secondarySelectedColor = (255, 0, 0)

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
        self.edges = []

    def draw(self):
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
        x: Position x
        y: Position y
        """
        if (self.getPosX() + self.getRadius() + self.buffer >= x >=
            self.getPosX() -
            self.getRadius() - self.buffer) \
                and \
                (self.getPosY() + self.getRadius() + self.buffer >= y >=
                 self.getPosY() - self.getRadius() - self.buffer):
            return True

        return False

    def addEdge(self, edge):
        """
        Adds an edge to the vertex's list of edges
        vertex: the vertex to be added
        """
        if edge in self.edges:
            print("Vertex already contains the given edge")
        else:
            self.edges.append(edge)

    def removeEdge(self, edge):
        """
        Removes the given edge from the list of edges
        edge: The edge to be removed
        """
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("Edge does not exist in list of edges")

    def getEdges(self):
        """
        Returns the edge list of the vertex
        """
        return self.edges

    def setColor(self, color):
        """
        Changes the color of a given vertex
        """
        self.color = color

    def setDefaultColor(self, color):
        """
        Sets the default color
        :param color: The new default color
        """
        Vertex.defaultColor = color

    def getDefaultColor(self):
        """
        Returns the default color
        """
        return Vertex.defaultColor


    def setColorToDefault(self):
        """
        Sets the color to the default color
        """
        self.setColor(self.getDefaultColor())

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

def getRadius():
    return Vertex.radius

def getBuffer():
    """
    Gets the value of the buffer
    :return: buffer
    """
    return Vertex.buffer
