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
        self.primarySelected = None
        self.secondarySelected = None

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

                        if event.button == 1:
                            self.selectVertex(vertices[x])
                            self.drawVertices()
                            pygame.display.update()

                        elif event.button == 3:
                            self.makeVertexPrimary(vertices[x])

                        return False  # there is no new vertex

                # If a vertex has not been clicked then we add a new vertex
                vertices.append(Vertex.Vertex(pos[0], pos[1]))
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.resetScreen()

                elif event.key == pygame.K_SPACE:  # Easy way of unselecting everything
                    if self.primarySelected is not None:
                        self.unselectPrimary()
                        self.drawVertices()

                elif event.key == pygame.K_DELETE:
                    self.deleteSelected()

                pygame.display.update()

        return False

    def generateScreen(self):
        """
        Sets up the pygame screen
        """

        self.screen = pygame.display.set_mode((self.xSize, self.ySize), pygame.SCALED)
        self.screen.fill(self.color)

    def generateEdge(self):
        """
        Generates edge based on primarySelected vertices
        return: False if the edge already exists
        """
        for edges in self.primarySelected.getEdges():
            if edges.areVerticesCorrect(self.primarySelected, self.secondarySelected):
                print("Vertex already exists")
                return False  # Breaks the function from continuing

        if self.primarySelected is not None and self.secondarySelected is not None:
            tempEdge = Edge.Edge(self.primarySelected, self.secondarySelected)
            self.primarySelected.addEdge(tempEdge)
            self.secondarySelected.addEdge(tempEdge)
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

    def drawAll(self):
        """
        Draws all vertices and edges then updates the screen
        """
        self.drawVertices()
        self.drawEdges()
        pygame.display.update()

    def resetScreen(self):
        """
        Resets the screen to default
        """
        print("Good")
        self.vertices.clear()
        self.edges.clear()
        self.primarySelected = None
        self.secondarySelected = None
        self.screen.fill((255, 255, 255))
        pygame.display.update()

    def clearScreen(self):
        """
        Makes the entire screen white
        """
        self.screen.fill((255, 255, 255))
        pygame.display.update()

    def setupVerticesAndEdges(self):
        """
        Sets up the vertices and edges classes
        """
        Vertex.setScreen(self.screen)
        Edge.setScreen(self.screen)

    def selectVertex(self, selectable):
        """
        Sets the primarySelected vertex
        """
        if selectable == self.primarySelected:  # Clears all vertices if original is reclicked
            self.unselectPrimary()

        elif self.primarySelected is not None:  # Checks if original already clicked

            if self.secondarySelected is None:  # What to do if there is no secondarySelected
                self.selectSecondary(selectable)

            elif selectable == self.secondarySelected:  # If already primarySelected, unselect
                self.unselectSecondary()

            else:  # If not primarySelected, unselect
                self.unselectSecondary()
                self.selectSecondary(selectable)

        else:
            self.primarySelected = selectable
            selectable.setColor(selectable.selectedColor)

        pygame.display.update()

    def clearSelected(self):
        """
        Sets both primary selected and secondary selected to none
        """
        self.primarySelected = None
        self.secondarySelected = None

    def unselectPrimary(self):
        """
        Unselects the primary vertex
        """
        if self.primarySelected is not None:
            self.primarySelected.setColorDefault()

        if self.secondarySelected is not None:
            self.secondarySelected.setColorDefault()

        # Clears both the primary and the secondary
        self.primarySelected = None
        self.secondarySelected = None

        self.drawVertices()
        pygame.display.update()

    def makeVertexPrimary(self, selected):
        """
        Makes the primary the newly selected vertex and clears the secondary
        selected: The new primary
        """
        if self.secondarySelected is None and self.primarySelected is None:
            self.selectVertex(selected)
        else:
            print("Selecting Primary")
            self.unselectPrimary()
            self.selectVertex(selected)

        self.drawAll()

    def unselectSecondary(self):
        """
        Unselects the secondary vertex clicked
        secondary: The vertex to be unselected
        """
        self.secondarySelected.setColorDefault()
        self.secondarySelected = None

    def selectSecondary(self, selected):
        """
        Selects a secondary vertex, which means an edge has been generated.
        secondary: The vertex to be primarySelected
        """
        self.secondarySelected = selected
        self.secondarySelected.setColor(self.secondarySelected.secondarySelectedColor)
        self.generateEdge()
        self.drawEdges()

    def deleteSelected(self):
        """
        Deletes the selected object.
        Vertex: Removes vertex from vertices and then iterates over the edges of the vertex to remove those edges
        from the edges list and the edges list for both vertices of each edge.
        Finally: Unselects
        """
        if isinstance(self.primarySelected, Vertex.Vertex):
            self.vertices.remove(self.primarySelected)

            tempList = self.primarySelected.getEdges().copy()

            for edgeToBeRemoved in tempList:  # Loops over primary's edges and removes from list

                self.edges.remove(edgeToBeRemoved)
                edgeToBeRemoved.getVertexOne().removeEdge(edgeToBeRemoved)  # Removes the edge from both vertices
                edgeToBeRemoved.getVertexTwo().removeEdge(edgeToBeRemoved)

            self.unselectPrimary()

        self.clearScreen()

        self.drawEdges()
        self.drawVertices()
