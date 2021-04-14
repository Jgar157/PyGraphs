"""
The main graph which contains edges and vertices.
"""

import pygame
from pygame_button import Button
import Vertex
import Edge



class Pygraph:

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 180, 0)

    pygame.font.init()
    primaryFont = pygame.font.SysFont("Comic Sans", 16)


    def __init__(self, color=(255, 255, 255), xSize=500, ySize=300):



        self.color = color
        self.xSize = xSize
        self.ySize = ySize
        self.clock = pygame.time.Clock()


        self.screen = None
        self.primarySelected = None
        self.secondarySelected = None


        self.vertices = []
        self.edges = []
        self.generateScreen()
        self.setupVerticesAndEdges()
        self.initButtons()

        # Sets up the pygame window
        pygame.init()
        pygame.display.update()

    def run(self):
        """
        The running loop of the graph
        """
        # Loop
        while True:

            if self.inSettingsLoop:
                self.settingsLoop()
                self.inputCheckerSettings()


            else:
                self.inputChecker(self.vertices, self.edges, self.screen)
                self.drawEdges()
                self.drawVertices()
                self.settingsButton.update(self.screen)




            pygame.display.update()

            self.clock.tick(60)

    def inputChecker(self, vertices, edges, screen):
        """
        Checks for inputs
        Returns whether or not a new vertex was added
        """
        ev = pygame.event.get()

        for event in ev:

            self.settingsButton.check_event(event)

            if event.type == pygame.QUIT: # Quits the program
                pygame.quit()


            # Creates a vertex based on where was clicked
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if not self.screenBoundary.collidepoint(pos):
                    for x in range(len(vertices)):  # Scan over all vertices
                        if vertices[x].isInBounds(pos[0], pos[1]):

                            if event.button == 1:
                                self.selectVertex(vertices[x])
                                self.drawVertices()
                                pygame.display.update()

                            elif event.button == 3:
                                self.makeVertexPrimary(vertices[x])

                            return False  # there is no new vertex
                    self.addVertex(pos)


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

    def inputCheckerSettings(self):
        ev = pygame.event.get()
        for events in ev:
            self.settingsExitButton.check_event(events)


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


    def initButtons(self):

        BUTTON_STYLE = {
            "text": "Settings",
            "font": self.primaryFont,
            "call_on_release": True,
            "hover_color": self.BLUE,
            "clicked_color": self.GREEN,
            "font_color": pygame.Color("Black"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            }

        EXIT_BUTTON_STYLE = {
            "text": "X",
            "font": self.primaryFont,
            "call_on_release": True,
            "hover_color": self.RED,
            "clicked_color": (255,0,200),
            "font_color": pygame.Color("Black"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            }

        openSettings = lambda: self.settingsLoop()
        closeSettings = lambda: self.closeLoop()


        self.settingsButton = Button((self.xSize - 50, 0, 50, 20),  self.WHITE, openSettings,  **BUTTON_STYLE)
        self.settingsButton.update(self.screen)
        self.screenBoundary = pygame.Rect(self.settingsButton.rect.x - 10, 0, self.settingsButton.rect.x + 10,
                                          self.ySize)

        self.settingsExitButton = Button((self.xSize - 90, 50, 40, 25), self.WHITE, closeSettings, **EXIT_BUTTON_STYLE)
        self.inSettingsLoop = False


    def addVertex(self, pos):
        if (pos[0] + Vertex.getBuffer() < self.screenBoundary.x):
            # If a vertex has not been clicked then we add a new vertex
            self.vertices.append(Vertex.Vertex(pos[0], pos[1]))
            return True


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
        pygame.display.update()
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

    def settingsLoop(self):

        self.openSettingsWindow()
        self.inSettingsLoop = True
        self.settingsExitButton.update(self.screen)
        pygame.display.update()


    def openSettingsWindow(self):
        self.screen.fill(self.color)
        settingsScreen = pygame.Rect(50, 50, self.xSize - 100, self.ySize - 100)
        pygame.draw.rect(self.screen, self.BLACK, settingsScreen, 2)

    def closeLoop(self):
        self.inSettingsLoop = False
        self.clearScreen()
        pygame.display.update()




