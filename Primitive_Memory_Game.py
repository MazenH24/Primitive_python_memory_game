import pygame
import os
import sys
from random import randint
from time import sleep

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1280, 720

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Primitive Memory Game")

NUMBERS = [pygame.image.load(os.path.join("resources", "Numbers", str(i) + "-Number-PNG.png")) for i in range(11)]
NUMBERS = [pygame.transform.scale(NUMBERS[i], (200, 300)) for i in range(11)]

INPUT_BOX = pygame.image.load(os.path.join("resources", "Rectangle", "rectangle.png"))
INPUT_BOX = pygame.transform.scale(INPUT_BOX, (600, 150))

game_over = pygame.image.load(os.path.join("resources", "GameOver", "gameover.png"))
game_over = pygame.transform.scale(game_over, (300, 100))

empty_image = 10

input_rect = pygame.Rect((WIDTH//2 - 275, HEIGHT - 175), (600, 150))
base_font = pygame.font.Font(None, 50)
font = pygame.font.SysFont('Constantia', 50)
clock = pygame.time.Clock()


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font_style = pygame.font.SysFont('Constantia', 60)
            text = font_style.render(self.text, True, (255, 255, 255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False


def primitive_memory_game():
    run = True
    level = 1
    highest_level = 0
    with open("highest_score.txt") as file:
        highest_level = file.read()
    fps = 60
    lower_bound = 10000
    upper_bound = 99999

    def update_window_with_numbers(digit):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("highest_score.txt", 'w') as f:
                    f.write(highest_level)
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        WINDOW.fill((255, 255, 255))

        WINDOW.blit(INPUT_BOX, (WIDTH//2 - 275, HEIGHT - 175))

        level_label = font.render("Level: {}".format(level), True, (47, 150, 214))
        highest_level_label = font.render("Max Level: {}".format(highest_level), True, (47, 150, 214))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 20, 15))
        WINDOW.blit(highest_level_label, (WIDTH - level_label.get_width() - 123, 55))

        x_axis = randint(200, 900)
        y_axis = randint(75, 175)
        WINDOW.blit(NUMBERS[int(digit)], (x_axis, y_axis))

        pygame.display.update()
        sleep(1.25)

    def take_input():
        number_answered = ''
        WINDOW.fill((255, 255, 255))

        WINDOW.blit(INPUT_BOX, (WIDTH//2 - 275, HEIGHT - 175))

        level_label = font.render("Level: {}".format(level), True, (47, 150, 214))
        highest_level_label = font.render("Max Level: {}".format(highest_level), True, (47, 150, 214))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 20, 15))
        WINDOW.blit(highest_level_label, (WIDTH - level_label.get_width() - 123, 55))

        pygame.draw.rect(WINDOW, (47, 150, 214), input_rect, 5)
        submit_button = Button((0, 0, 0), WIDTH//2 - 275, HEIGHT - 227, 200, 50, "Submit:")
        while True:
            submit_button.draw(WINDOW)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    with open("highest_score.txt", 'w') as f:
                        f.write(highest_level)
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_button.is_over(pos):
                        return number_answered.strip().replace(' ', '')
                if event.type == pygame.MOUSEMOTION:
                    if submit_button.is_over(pos):
                        submit_button.color = (47, 150, 214)
                    else:
                        submit_button.color = (0, 0, 0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        number_answered = number_answered[:-1]
                        WINDOW.blit(INPUT_BOX, (WIDTH//2 - 275, HEIGHT - 175))
                    elif str(event.unicode).isdigit():
                        number_answered += event.unicode

            text_surface = base_font.render(number_answered, True, (47, 150, 214))
            WINDOW.blit(text_surface, (input_rect.x + 75, input_rect.y + 50))
            submit_button.draw(WINDOW, (0,0,0))
            pygame.display.update()

    def game_is_over():
        run = True
        again_button = Button((0, 0, 0), WIDTH//2 - 275, HEIGHT - 175, 600, 150, "Play Again?")
        while run:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    with open("highest_score.txt", 'w') as f:
                        f.write(highest_level)
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if again_button.is_over(pos):
                        with open("highest_score.txt", 'w') as f:
                            f.write(highest_level)
                        return True
                if event.type == pygame.MOUSEMOTION:
                    if again_button.is_over(pos):
                        again_button.color = (47, 150, 214)
                    else:
                        again_button.color = (0, 0, 0)

            WINDOW.fill((255, 255, 255))

            WINDOW.blit(INPUT_BOX, (WIDTH//2 - 275, HEIGHT - 175))

            level_label = font.render("Level: {}".format(level), True, (47, 150, 214))
            highest_level_label = font.render("Max Level: {}".format(highest_level), True, (47, 150, 214))
            WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 20, 15))
            WINDOW.blit(highest_level_label, (WIDTH - level_label.get_width() - 123, 55))
            again_button.draw(WINDOW, (0, 0, 0))

            x_axis = randint(200, 675)
            y_axis = randint(75, 250)
            WINDOW.blit(game_over, (x_axis, y_axis))
            pygame.display.update()
            sleep(0.25)

    def start():
        purple_button = Button((0, 0, 0), WIDTH//2 - 275, HEIGHT - 175, 600, 150, "Click Me To Start!")
        while True:
            WINDOW.fill((255, 255, 255))
            purple_button.draw(WINDOW, (0, 0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if purple_button.is_over(pos):
                        return
                if event.type == pygame.MOUSEMOTION:
                    if purple_button.is_over(pos):
                        purple_button.color = (47, 150, 214)
                    else:
                        purple_button.color = (0, 0, 0)

    start()
    while run:
        clock.tick(fps)
        num = randint(lower_bound, upper_bound)
        lower_bound = int(str(lower_bound) + '0')
        upper_bound = int(str(upper_bound) + '9')
        num = str(num)
        [update_window_with_numbers(num[i]) for i in range(len(num))]
        update_window_with_numbers(empty_image)

        answer = take_input()

        if answer != num:
            return game_is_over()
        else:
            level += 1
            if str(level) > highest_level:
                highest_level = str(level)


if __name__ == '__main__':
    condition = True
    while condition:
        condition = primitive_memory_game()
