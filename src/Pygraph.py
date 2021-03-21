"""
The main graph which contains edges and vertices.
"""

import pygame
import Vertex
import Edge


class Pygraph:

    def __init__(self, color=(255, 255, 255), xSize=500, ySize=300):
        self.color = color
        self.xSize = xSize
        self.ySize = ySize

        self.screen = None
        self.selected = None
        self.secondarySelected = []

        self.vertices = []
        self.edges = []
        self.generateScreen()
        self.setupVerticesAndEdges()

        # Sets up the pygame window
        pygame.init()
        pygame.display.update()

    def run(self):
        """
        The running loop of the graph
        """
        # Loop
        while True:

            foundVertex = self.inputChecker(self.vertices, self.edges, self.screen)

            self.drawEdges()
            self.drawVertices()

            if foundVertex:
                pygame.event.wait()
                pygame.display.update()

    def inputChecker(self, vertices, edges, screen):
        """
        Checks for inputs
        Returns whether or not a new vertex was added
        """
        ev = pygame.event.get()

        for event in ev:

            # Creates a vertex based on where was clicked
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for x in range(len(vertices)):  # Scan over all vertices
                    if vertices[x].isInBounds(pos[0], pos[1]):
                        self.select(vertices[x])
                        self.drawVertices()
                        pygame.display.update()
                        return False  # there is no new vertex

                # If a vertex has not been clicked then we add a new vertex
                vertices.append(Vertex.Vertex(pos[0], pos[1]))
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.resetScreen()

                if event.key == pygame.K_e:
                    self.generateEdges()
                    self.drawEdges()
                    self.drawVertices()

                if event.key == pygame.K_SPACE:  # Easy way of unselecting everything
                    if self.selected is not None:
                        self.unselectPrimary()
                        self.drawVertices()

                pygame.display.update()

        return False

    def generateScreen(self):
        """
        Sets up the pygame screen
        """

        self.screen = pygame.display.set_mode((self.xSize, self.ySize), pygame.SCALED)
        self.screen.fill(self.color)

    def generateEdges(self):
        """
        Generates edge based on selected vertices
        """
        if self.selected is not None:
            for secondaryVertex in self.secondarySelected:
                tempEdge = Edge.Edge(self.selected, secondaryVertex)
                self.selected.addEdge(tempEdge)
                secondaryVertex.addEdge(tempEdge)
                self.edges.append(tempEdge)

    def drawVertices(self):
        """
        Draws all the vertices based on the list of vertices
        """
        for x in self.vertices:
            x.draw()

    def drawEdges(self):
        """
        Draws all the edges based on the list of edges
        """
        for edge in self.edges:
            edge.draw()

    def resetScreen(self):
        """
        Resets the screen to default
        """
        print("Good")
        self.vertices.clear()
        self.edges.clear()
        self.selected = None
        self.secondarySelected.clear()
        self.screen.fill((255, 255, 255))
        pygame.display.update()

    def setupVerticesAndEdges(self):
        """
        Sets up the vertices and edges classes
        """
        Vertex.setScreen(self.screen)
        Edge.setScreen(self.screen)

    def select(self, selectable):
        """
        Sets the selected vertex
        """
        if selectable == self.selected:  # Clears all vertices if original is reclicked
            self.unselectPrimary()

        elif self.selected is not None:  # Checks if original already clicked

            if selectable in self.secondarySelected:  # If already selected, unselect
                self.unselectSecondary(selectable)
            else:  # If not selected, unselect
                self.selectSecondary(selectable)

        else:
            self.selected = selectable
            selectable.setColor(selectable.selectedColor)

        pygame.display.update()

    def unselectPrimary(self):
        """
        Unselects the primary vertex
        """
        self.selected.setColorDefault()

        for selected in self.secondarySelected:
            selected.setColorDefault()

        self.secondarySelected.clear()
        self.selected = None

        self.drawVertices()

    def unselectSecondary(self, secondary):
        """
        Unselects the secondary vertex clicked
        secondary: The vertex to be unselected
        """
        secondary.setColorDefault()
        self.secondarySelected.remove(secondary)

    def selectSecondary(self, secondary):
        """
        Selects a secondary vertex
        secondary: The vertex to be selected
        """
        self.secondarySelected.append(secondary)
        secondary.setColor(secondary.secondarySelectedColor)
        print(self.secondarySelected)
