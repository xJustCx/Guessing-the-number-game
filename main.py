import pygame, sys
from random import randint

pygame.init()
screen = pygame.display.set_mode((1000, 300))
pygame.display.set_caption('Guessing The Number')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/LittleLordFontleroyNF.ttf', 100)
q_font = pygame.font.Font('font/LittleLordFontleroyNF.ttf', 110)
out1_font = pygame.font.Font('font/Bungasai.ttf', 40)
out2_font = pygame.font.Font('font/Bungasai.ttf', 45)
input_font = pygame.font.Font(None, 50)
c_font = pygame.font.Font('font/LittleLordFontleroyNF.ttf', 30)
user_text = ''
pygame.mixer.music.load('audio/Calm Relaxing Music.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mouse.set_cursor(*pygame.cursors.arrow)

target = randint(0, 100)  # Generate a random target number between 1 and 100
guess_count = 0  # Track the total number of guesses
correct_guess = False  # Track if the guess is correct
too_high = False  # Track if the guess is too high
too_low = False  # Track if the guess is too low
out_of_range = False  # Track if the guess is out of range
game_active = False
active = False
current_screen = "intro"  # Track current screen

# Intro screen
game_name = test_font.render('Guessing The Number', False, ("#049000"))
game_name_rect = game_name.get_rect(center=(500, 80))

game_message = test_font.render('Press space to start', False, ("#c6d100"))
game_message_rect = game_message.get_rect(center=(500, 230))

# Game screen
surface_01 = pygame.image.load('pic/bunny.png').convert()
surface_02 = pygame.image.load('pic/sky.png').convert()

guess_text = q_font.render('Enter your guess: ', True, ("#c6d100"))  
guess_text_rect = guess_text.get_rect(midleft=(100, 150))

correct = out2_font.render('Congratulations, your guess is correct!', True, ("#049000"))
correct_rect = correct.get_rect(midleft=(100, 50))

high_text = out2_font.render('Sorry, your guess is too high!', True, ("#7159bf"))
high_text_rect = high_text.get_rect(midleft=(100, 240))

low_text = out2_font.render('Sorry, your guess is too low!', True, ("#7159bf"))
low_text_rect = low_text.get_rect(midleft=(100, 240))

out_of_range_text = out1_font.render('Sorry, your guess is out of range!', True, ("#7159bf"))
out_of_range_text_rect = out_of_range_text.get_rect(midleft=(100, 240))

guess_count_text = out2_font.render(f'Total number of guesses: {guess_count}', True, ("#c6d100"))
guess_count_rect = guess_count_text.get_rect(midleft=(200, 230))

# Button images
button_image = pygame.image.load("pic/b1.png")
button_surface = pygame.transform.scale(button_image, (200, 40))
restart_button_surface = pygame.transform.scale(button_image, (200, 40))

# Input box
input_rect = pygame.Rect((575, 145), (100, 40))
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = c_font.render(self.text_input, True, "#000490")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = c_font.render(self.text_input, True, "green")
        else:
            self.text = c_font.render(self.text_input, True, "#000490")

# Instantiate buttons
confirm_button = Button(button_surface, 800, 160, "Click to confirm")
restart_button = Button(restart_button_surface, 500, 150, "Restart")

def reset_game():
    global target, guess_count, correct_guess, too_high, too_low, out_of_range, user_text, active, current_screen
    target = randint(0, 100) 
    guess_count = 0
    correct_guess = False
    too_high = False
    too_low = False
    out_of_range = False
    user_text = ''
    active = False
    current_screen = "game"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_screen == "intro":
                current_screen = "game"  # Transition to game screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if confirm_button.checkForInput(pygame.mouse.get_pos()) and current_screen == "game":
                try:
                    user_guess = int(user_text)  
                    guess_count += 1  # Increment guess count
                    out_of_range = False  # Reset out_of_range flag

                    # Check if the guess is out of range
                    if user_guess < 0 or user_guess > 100:
                        out_of_range = True  # Set flag if out of range
                        too_high = False
                        too_low = False
                    elif user_guess == target:
                        correct_guess = True  # Correct guess
                        too_high = False
                        too_low = False
                    elif user_guess > target:
                        too_high = True  # Guess too high
                        too_low = False  # Reset too low flag
                    elif user_guess < target:
                        too_low = True  # Guess too low
                        too_high = False  # Reset too high flag

                    user_text = ''  # Reset input box after guess
                except ValueError:
                    pass  # Ignore if user_text is not a valid number

            if restart_button.checkForInput(pygame.mouse.get_pos()) and correct_guess:
                reset_game()  # Reset the game when "Restart" is clicked

            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    if current_screen == "intro":
        # Intro screen display
        screen.fill(("#f2f2f2"))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
    elif current_screen == "game":
        if correct_guess:
            # Show success screen if the guess is correct
            screen.blit(surface_02, (0, 0))
            screen.blit(correct, correct_rect)
            guess_count_text = out2_font.render(f'Total number of guesses: {guess_count}', True, ("#c6d100"))
            screen.blit(guess_count_text, guess_count_rect)  # Display the total number of guesses
            restart_button.update()  # Display restart button
        else:
            # Display game screen
            screen.blit(surface_01, (0, 0))
            screen.blit(guess_text, guess_text_rect)  # Use `guess_text` for the "Enter your guess" prompt
            confirm_button.update()

            if too_high:
                screen.blit(high_text, high_text_rect)  # Show "too high" message
            elif too_low:
                screen.blit(low_text, low_text_rect)  # Show "too low" message
            elif out_of_range:
                screen.blit(out_of_range_text, out_of_range_text_rect)  # Show "out of range" message

            if active:
                color = color_active
            else:
                color = color_passive
            pygame.draw.rect(screen, color, input_rect)
            text_surface = input_font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(100, text_surface.get_width() + 10)

    confirm_button.changeColor(pygame.mouse.get_pos())
    restart_button.changeColor(pygame.mouse.get_pos())
    pygame.display.flip()
    clock.tick(60)