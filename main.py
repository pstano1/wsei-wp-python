import pygame
from model import Grid
from view import Renderer
from controller import GameController

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('The game of life')


def main():
    grid = Grid(40, 30)
    controller = GameController(grid)
    renderer = Renderer(grid, width, height, controller, screen)
    controller.attach(renderer)
    controller.run_game()

if __name__ == '__main__':
    main()


pygame.quit()  

