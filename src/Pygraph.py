"""
The main graph which contains edges and vertices.
"""
import os

import pygame
from pygame_button import Button
import Vertex
import Edge
import textbox

os.environ["SDL_VIDEO_CENTERED"] = "1"



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
        self.initInteractables()

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

                elif event.key == pygame.K_c:
                    self.createCycle()

                elif event.key == pygame.K_k:
                    self.createComplete()

                elif event.key == pygame.K_b:
                    self.createBipartite()

                pygame.display.update()

        return False

    def inputCheckerSettings(self):
        """
        The input checker for the settings loop.
        ONLY runs during the settings loop.
        Checks the event of all interactable objects during the settings loop.
        """
        ev = pygame.event.get()
        for event in ev:
            self.settingsExitButton.check_event(event)
            self.settingsAcceptButton.check_event(event)


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


    def initInteractables(self):
        """
        Initialization of buttons
        """

        # -------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------Buttons----------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------


        # Button styles are the dictionaries that hold the information on each button
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
            "clicked_color": (139,0,0),
            "font_color": pygame.Color("Black"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            }

        ACCEPT_SETTINGS_BUTTON_STLE = {
            "text": "Accept",
            "font": self.primaryFont,
            "call_on_release": True,
            "hover_color": self.BLUE,
            "clicked_color": (0,191,255),
            "font_color": pygame.Color("Black"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
        }

        # Lambdas that are passed into buttons
        openSettings = lambda: self.settingsLoop()
        closeSettings = lambda: self.closeLoop()


        self.settingsButton = Button((self.xSize - 50, 0, 50, 20),  self.WHITE, openSettings,  **BUTTON_STYLE)
        self.settingsButton.update(self.screen)
        self.screenBoundary = pygame.Rect(self.settingsButton.rect.x - 10, 0, self.settingsButton.rect.x + 10,
                                          self.ySize)

        self.settingsExitButton = Button((self.xSize - 90, 50, 40, 25), self.RED, closeSettings, **EXIT_BUTTON_STYLE)
        self.inSettingsLoop = False

        self.settingsAcceptButton = Button((self.xSize / 2 - 30, self.ySize - 70, 60, 20), self.WHITE, closeSettings,
                                           **ACCEPT_SETTINGS_BUTTON_STLE)



        # -------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------Text Box---------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

        onClearDefaultVertexColor = None
        self.setDefaultVertexColor = textbox.TextBox((self.xSize / 2 - 50, self.ySize / 2 - 50, 50, 50),
                                                     command = onClearDefaultVertexColor, clear_on_enter=True,
                                                     inactive_on_enter=False)
        # TODO Fix the command for the text box -> We want it to change vertex default colors


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
            self.primarySelected.setColorToDefault()

        if self.secondarySelected is not None:
            self.secondarySelected.setColorToDefault()

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
        self.secondarySelected.setColorToDefault()
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
        """
        This loop runs whenever the settings window is open
        :return:
        """

        self.openSettingsWindow() # Open the window
        self.inSettingsLoop = True # State that we're in the loop
        self.settingsExitButton.update(self.screen) # Draw the exit button
        self.settingsAcceptButton.update(self.screen)
        pygame.display.update() # Update the display


    def openSettingsWindow(self):
        """
        Opens the settings window
        """
        self.screen.fill(self.color) # Fill the screen white to wipe previous screen
        settingsScreen = pygame.Rect(50, 50, self.xSize - 100, self.ySize - 100) # Create the settings window
        pygame.draw.rect(self.screen, self.BLACK, settingsScreen, 2)

    def closeLoop(self):
        """
        Ends the settings loop
        """
        self.inSettingsLoop = False
        self.clearScreen()
        pygame.display.update()


#----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Algorithms---------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
    def createCycle(self):
        """
        Creates a cycle in order of vertex creation
        """
        for number in range(-1, len(self.vertices) - 1):
            tempEdge = Edge.Edge(self.vertices[number], self.vertices[number + 1])
            self.edges.append(tempEdge)
            self.vertices[number].addEdge(tempEdge)
            self.vertices[number + 1].addEdge(tempEdge)

    def createComplete(self):
        """
        Connects every vertex to every other vertex
        """
        for vertex in self.vertices:
            for secondVertex in self.vertices:
                if vertex is not secondVertex:
                    tempEdge = Edge.Edge(vertex, secondVertex)
                    self.edges.append(tempEdge)
                    vertex.addEdge(tempEdge)
                    secondVertex.addEdge(tempEdge)

    def createBipartite(self):
        numberOfVertices = len(self.vertices)
        halfOfVertices = numberOfVertices // 2

        firstPartite = self.vertices[:halfOfVertices]
        secondPartite = self.vertices[halfOfVertices:]

        for vertex in firstPartite:
            for secondVertex in secondPartite:
                tempEdge = Edge.Edge(vertex, secondVertex)
                self.edges.append(tempEdge)
                vertex.addEdge(tempEdge)
                secondVertex.addEdge(tempEdge)



