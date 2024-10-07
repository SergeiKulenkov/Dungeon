import pygame
from Game.Game import Game

pygame.init()

def main():
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()