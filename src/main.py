"""
This class contains the main while loop.
All user interaction is controlled here.
Vertices and edges can be generated here too.
"""

import Vertex
import Edge
import pygame


def main():
    """
    The main function of the program
    """

    white = (255, 255, 255)
    screen = pygame.display.set_mode((500, 300), pygame.SCALED)
    screen.fill(white)

    # sets the screen and color for all vertices
    Vertex.setScreen(screen)
    Edge.setScreen(screen)
    Vertex.setColor([0, 0, 0])

    vertices = []
    edges = []

    pygame.init()

    pygame.display.update()

    # Loop
    while True:

        foundVertex = inputChecker(vertices, edges, screen)

        # Draws edges from each vertex to each other vertex
        for x in range(len(vertices) - 1):
            for y in range(len(vertices)):
                if x != y:
                    edges.append(Edge.Edge(vertices[x], vertices[y]))

        for x in edges:
            x.drawEdge()

        # Draws circles based on list of vertices
        for x in vertices:
            x.drawVertex()

        if foundVertex:
            pygame.event.wait()
            pygame.display.update()


def inputChecker(vertices, edges, screen):
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
                    vertices[x].setColor((0, 0, 255))
                    vertices[x].drawVertex()
                    pygame.display.update()
                    return False  # there is no new vertex

            # If a vertex has not been clicked then we add a new vertex
            vertices.append(Vertex.Vertex(pos[0], pos[1]))
            return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                print("Good")
                vertices.clear()
                edges.clear()
                screen.fill((255, 255, 255))
                pygame.display.update()
    return False


if __name__ == "__main__":
    main()
