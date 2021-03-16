import time
import Vertex
import pygame
from pygame import gfxdraw

def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def main():
    print("temp")

    white = [255,255,255]
    screen = pygame.display.set_mode((500,300), pygame.SCALED)
    screen.fill(white)

    Vertex.setScreen(screen)
    Vertex.setColor([0,0,0])

    vertices = []




    pygame.init()

    count  = 0

    pygame.display.update()

    # Loop
    while True:

        foundNewVertex = False

        ev = pygame.event.get()

        for event in ev:

            # Creates a vertex based on where was clicked
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                vertices.append(Vertex.Vertex(pos[0],pos[1]))
                foundNewVertex = True

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_x:
                    print("SHIT")
                    vertices.clear()
                    pygame.display.update()



        # Draws circles based on list of vertices
        for x in vertices:
            draw_circle(x.getScreen(), x.getPosX(), x.getPosY(), x.getRadius(), x.getColor())

        # Draws edges from each vertex to each other vertex
        for x in range(len(vertices) - 1):
            for y in range(len(vertices)):
                if (x != y):
                    pygame.draw.line(vertices[x].getScreen(), [0,0,0], [vertices[x].getPosX(), vertices[x].getPosY()],
                                     [vertices[y].getPosX(), vertices[y].getPosY()], 1)

        if (foundNewVertex):
            pygame.event.wait()
            pygame.display.update()



if __name__ == "__main__":
    main()

