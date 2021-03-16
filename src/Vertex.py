


class Vertex:
    """
    Vertices are points on a graph.
    They can be labeled and placed.
    Vertices can have edges connecting to other vertices.
    """

    # The screen is where the vertices are drawn on.
    screen = None

    # Default color of a vertex if black.
    color = [0,0,0]

    # Default radius of vertex is 2.
    radius = 2




    def __init__(self, posX, posY):

        # posX and posY are the centers of each vertex
        self.posX = posX
        self.posY = posY

    def getPosX(self):
        return self.posX

    def getPosY(self):
        return self.posY

    def getScreen(self):
        return self.screen

    def getColor(self):
        return self.color

    def getRadius(self):
        return self.radius



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
