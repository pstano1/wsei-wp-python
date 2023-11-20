import os
import pygame
from model import Grid

class GameController:
    def __init__(self, grid: Grid) -> None:
        self.running: bool = True
        self.grid: Grid = grid
        self.clock = pygame.time.Clock()
        self.tick_interval: int = 1000
        self.last_update: int = 0
        self.paused: bool = False
        self.observers = []

    def attach(self, observer) -> None:
        self.observers.append(observer)

    def detach(self, observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update() 

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_META:
                    self.save_game() 
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_META: 
                    self.load_game()   

    def run_game(self) -> None:
         while self.running:
            self.handle_events()

            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.tick_interval:
                self.last_update = current_time
                if not self.paused:
                    self.grid.next_generation()
                pygame.display.flip()

            self.notify()
            pygame.display.flip()
    
    def save_game(self) -> None:
        save_directory = './saves'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        json_data = self.grid.create_snapshot()

        save_file = os.path.join(save_directory, 'game_state.json')
        with open(save_file, 'w') as file:
            file.write(json_data)
        

    def load_game(self) -> None:
        save_file = './saves/game_state.json'

        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                json_data = file.read()
                self.grid.load_from_snapshot(json_data)
