"""
This class contains the main while loop.
All user interaction is controlled here.
Vertices and edges can be generated here too.
"""

import Vertex
import Edge
import pygame
from Pygraph import Pygraph


def main():
    """
    The main function of the program
    """

    graph = Pygraph()
    graph.run()


if __name__ == "__main__":
    main()
