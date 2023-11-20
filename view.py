from controller import GameController
from abc import ABC, abstractmethod
from model import Grid
import pygame

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class View(ABC):
    @abstractmethod
    def draw(self):
        pass


class Renderer(View, Observer):
    def __init__(self, grid: Grid, width: int, height: int, controller: GameController, screen: any) -> None:
        self.grid: Grid = grid
        self.controller: GameController = controller
        self.cell_width: int = width / grid.width
        self.cell_height: int = height / grid.height
        self.screen = screen
        self.width = width
        self.height = height

    def draw(self) -> None:
        self.draw_grid()
        self.draw_cells()

        if self.controller.paused:
            self.screen.blit(self.create_pause_overlay(), (0, 0))
        pygame.display.flip() 

    def update(self) -> None:
        self.draw()

    def draw_grid(self) -> None:
        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, white, cell)

    def draw_cells(self) -> None:
        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.grid.cells[x][y].alive:
                    pygame.draw.rect(self.screen, black, cell) 

    def create_pause_overlay(self):
        pause_overlay = pygame.Surface((self.width, self.height))
        pause_overlay.fill((0, 0, 0))
        pause_overlay.set_alpha(90)

        return pause_overlay

