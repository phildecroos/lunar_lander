# Import and initialize needed modules
import pygame
import os
import random

pygame.init()
pygame.font.init()

# Set the screen and caption
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lunar Lander")

# Set the different fonts to be used
small_font = pygame.font.SysFont('courier', 15)
medium_font = pygame.font.SysFont('courier', 20)
large_font = pygame.font.SysFont('courier', 50)
extra_large_font = pygame.font.SysFont('courier', 100)

# Set the non-object images to be used
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, 'images\\background.png'))
explosion_medium = pygame.image.load(os.path.join(current_path, 'images\explosion_medium.png'))
in_air_explosion_large = pygame.image.load(os.path.join(current_path, 'images\in_air_explosion_large.png'))
player_thrusting = pygame.image.load(os.path.join(current_path, 'images\player_thrusting.png'))

# Define needed variables
main_loop = True
start_loop = True
outer_game_loop = True
pre_game_loop = True
game_loop = True
level_win_loop = True
end_loop = True
overall_win = False
level = 1
score = 0
high_score = 0

# Define some text displays so they're available under all conditions
score_text = medium_font.render('Score: ' + str(score), False, (255, 255, 255))
overall_win_text = large_font.render('ALL MISSIONS COMPLETE', False, (0, 255, 0))

# Define the game objects class


class GameObject:
    def __init__(self, x, y, x_speed, y_speed, name):
        self.image = pygame.image.load(os.path.join(current_path, "images\\" + name + ".png"))
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.name = name
        self.rect = self.image.get_rect()

    # Change the x and y values of the object
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    # Move the object's rect and display its image
    def display(self):
        self.rect = self.image.get_rect()
        self.rect.move_ip(int(self.x), int(self.y))
        screen.blit(self.image, (int(self.x), int(self.y)))

    def collided_with(self, other_object):
        return self.rect.colliderect(other_object.rect)


# Define functions to cut down on the number of lines and make the loops easier to organize.


# Display anything at any location on the screen
def display(image, x, y):
    screen.blit(image, (int(x), int(y)))


# Display the score based on how large it is
def display_score():
    if 0 <= score < 10:
        display(score_text, 686, 5)
    if 10 <= score < 1000:
        display(score_text, 660, 5)
    if 1000 <= score < 10000:
        display(score_text, 652, 5)
    if 10000 <= score:
        display(score_text, 639, 5)


# Display the level based on how large the number is
def display_level():
    if 1 <= level < 10:
        display(level_display, 700, 30)
    if 10 <= level:
        display(level_display, 688, 30)


# Display the text display
def display_text():
    display(altitude, 10, 5)
    display(display_fuel, 10, 30)
    display(v_display, 10, 55)
    display(h_display, 10, 80)
    display_level()
    display_score()


# Run the start screen, game, and end screen loops
while main_loop:

    # Make the game loops run
    outer_game_loop = True
    pre_game_loop = True
    game_loop = True
    overall_win = False

    # Show the start screen
    while start_loop:

        # Reset the score to 0
        score = 0

        # Display the background images on the screen
        screen.fill((100, 100, 100))
        display(background, 0, -524)

        # Set the text displays on the start screen
        lunar_lander_text = extra_large_font.render('LUNAR LANDER', False, (255, 255, 255))
        high_score_text = medium_font.render('High Score: ' + str(high_score), False, (255, 255, 255))
        enter_text = small_font.render('Press enter to play.', False, (255, 255, 255))
        overall_win_text = large_font.render('ALL MISSIONS COMPLETE', False, (0, 255, 0))

        # Display the end screen text
        display(lunar_lander_text, 35, 190)
        display(high_score_text, 310, 170)
        display(enter_text, 310, 300)

        # Look for inputs from the keyboard or mouse
        for event in pygame.event.get():

            # Stop each loop to end the program when the user clicks the X in the top-right corner
            if event.type == pygame.QUIT:
                start_loop = False
                outer_game_loop = False
                end_loop = False
                main_loop = False

            # Start the game when the user presses enter
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_loop = False

        # Update the display
        pygame.display.update()

    # Put the user at level 1
    level = 1

    # Run the game
    while outer_game_loop:

        # Make the game loop run for this level
        game_loop = True

        # Reset the environmental objects lists to only include objects in this level
        env_objects = []
        falling_objects = []

        # Define the player and target
        player = GameObject(380, -30, 0, 1, "player")
        target = GameObject(random.randint(0, 736), 513, 0, 0, "target")
        player_y_acceleration = 0.05
        player_x_acceleration = 0
        fuel_value = 100

        # Base the level's setup on what level it is
        if level == 1:
            # Define the environmental objects
            dish1 = GameObject(150, 505, 0, 0, "dish_large")
            dish2 = GameObject(550, 537, 0, 0, "dish")
            dish3 = GameObject(650, 537, 0, 0, "dish")
            # Add the environmental objects to the main collision list
            env_objects.append(dish1)
            env_objects.append(dish2)
            env_objects.append(dish3)
            # Define the target
            target = GameObject(350, 513, 0, 0, "target")
            # Define the player
            player = GameObject(360, -30, 0, 0.5, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 2:
            # Define the environmental objects
            dish1 = GameObject(650, 505, 0, 0, "dish_large")
            rover1 = GameObject(350, 505, -0.25, 0, "rover_one")
            # Add the environmental objects to the main collision list
            env_objects.append(dish1)
            env_objects.append(rover1)
            # Define the target
            target = GameObject(500, 513, 0, 0, "target")
            # Define the player
            player = GameObject(360, -30, 0, 0.75, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 3:
            # Define the environmental objects
            rocket1 = GameObject(150, 505, 0, 0, "rocket")
            lander1 = GameObject(600, -30, 0, 1, "other_lander")
            dish1 = GameObject(450, 537, 0, 0, "dish")
            # Add the environmental objects to the main collision list
            env_objects.append(rocket1)
            env_objects.append(lander1)
            env_objects.append(dish1)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(lander1)
            # Define the target
            target = GameObject(250, 513, 0, 0, "target")
            # Define the player
            player = GameObject(360, -30, 0, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 4:
            # Define the environmental objects
            rocket1 = GameObject(200, 505, 0, 0, "rocket")
            rocket2 = GameObject(50, 505, 0, 0, "rocket")
            rover1 = GameObject(350, 505, 0.25, 0, "rover_one")
            lander1 = GameObject(350, -30, 0, 1, "other_lander")
            # Add the environmental objects to the main collision list
            env_objects.append(rocket1)
            env_objects.append(rocket2)
            env_objects.append(rover1)
            env_objects.append(lander1)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(lander1)
            # Define the target
            target = GameObject(115, 513, 0, 0, "target")
            # Define the player
            player = GameObject(500, -30, 0, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 5:
            # Define the environmental objects
            rocket1 = GameObject(700, 505, 0, 0, "rocket")
            lander1 = GameObject(200, -80, 0, 1, "other_lander")
            meteor1 = GameObject(500, -330, 0, 1.2, "meteor_small")
            meteor2 = GameObject(400, -730, 0, 1.5, "meteor_small")
            meteor3 = GameObject(675, -1030, 0, 1.5, "meteor_small")
            meteor4 = GameObject(150, -730, 0, 1, "meteor_small")
            dish1 = GameObject(300, 537, 0, 0, "dish")
            dish2 = GameObject(50, 505, 0, 0, "dish_large")
            # Add the environmental objects to the main collision list
            env_objects.append(rocket1)
            env_objects.append(lander1)
            env_objects.append(meteor1)
            env_objects.append(meteor2)
            env_objects.append(meteor3)
            env_objects.append(meteor4)
            env_objects.append(dish1)
            env_objects.append(dish2)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(lander1)
            falling_objects.append(meteor1)
            falling_objects.append(meteor2)
            falling_objects.append(meteor3)
            falling_objects.append(meteor4)
            # Define the target
            target = GameObject(600, 513, 0, 0, "target")
            # Define the player
            player = GameObject(300, -30, 0, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 6:
            # Define the environmental objects
            rocket1 = GameObject(25, 505, 0, 0, "rocket_construction")
            rocket2 = GameObject(175, 505, 0, 0, "rocket_construction")
            rocket3 = GameObject(250, 505, 0, 0, "rocket_construction")
            rocket4 = GameObject(325, 505, 0, 0, "rocket_construction")
            rocket5 = GameObject(400, 505, 0, 0, "rocket_construction")
            rocket6 = GameObject(475, 505, 0, 0, "rocket_construction")
            rocket7 = GameObject(550, 505, 0, 0, "rocket_construction")
            rocket8 = GameObject(625, 505, 0, 0, "rocket_construction")
            rocket9 = GameObject(700, 505, 0, 0, "rocket_construction")
            satellite1 = GameObject(900, 100, -1, 0, "satellite_one")
            satellite2 = GameObject(-500, 300, 1, 0, "satellite_three")
            satellite3 = GameObject(-150, 200, 1, 0, "satellite_two")
            satellite4 = GameObject(-800, 450, 1.25, 0, "satellite_one")
            satellite5 = GameObject(1300, 400, -1, 0, "satellite_three")
            # Add the environmental objects to the main collision list
            env_objects.append(rocket1)
            env_objects.append(rocket2)
            env_objects.append(rocket3)
            env_objects.append(rocket4)
            env_objects.append(rocket5)
            env_objects.append(rocket6)
            env_objects.append(rocket7)
            env_objects.append(rocket8)
            env_objects.append(rocket9)
            env_objects.append(satellite1)
            env_objects.append(satellite2)
            env_objects.append(satellite3)
            env_objects.append(satellite4)
            env_objects.append(satellite5)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(satellite1)
            falling_objects.append(satellite2)
            falling_objects.append(satellite3)
            falling_objects.append(satellite4)
            falling_objects.append(satellite5)
            # Define the target
            target = GameObject(100, 513, 0, 0, "target")
            # Define the player
            player = GameObject(360, -30, 0, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 7:
            # Define the environmental objects
            dish1 = GameObject(330, 505, 0, 0, "dish_large")
            dish2 = GameObject(460, 505, 0, 0, "dish_large")
            rover1 = GameObject(200, 505, -0.25, 0, "rover_one")
            rover2 = GameObject(600, 505, 0.1, 0, "rover_two")
            # Add the environmental objects to the main collision list
            env_objects.append(dish1)
            env_objects.append(dish2)
            env_objects.append(rover1)
            env_objects.append(rover2)
            # Define the target
            target = GameObject(400, 513, 0, 0, "target")
            # Define the player
            player = GameObject(300, -30, -0.25, 1.5, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 8:
            # Define the environmental objects
            lander1 = GameObject(75, -100, 0, 1, "other_lander")
            lander2 = GameObject(275, -300, 0, 1, "other_lander")
            lander3 = GameObject(400, -150, 0, 1, "other_lander")
            lander4 = GameObject(650, -400, 0, 1, "other_lander")
            # Add the environmental objects to the main collision list
            env_objects.append(lander1)
            env_objects.append(lander2)
            env_objects.append(lander3)
            env_objects.append(lander4)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(lander1)
            falling_objects.append(lander2)
            falling_objects.append(lander3)
            falling_objects.append(lander4)
            # Define the target
            target = GameObject(500, 513, 0, 0, "target")
            # Define the player
            player = GameObject(200, -30, 0, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 100

        if level == 9:
            # Define the environmental objects
            dish1 = GameObject(550, 537, 0, 0, "dish")
            dish2 = GameObject(675, 537, 0, 0, "dish")
            meteor1 = GameObject(25, -50, 0, 1, "meteor_large")
            meteor2 = GameObject(100, -350, 0, 1, "meteor_large")
            meteor3 = GameObject(175, -575, 0, 1, "meteor_large")
            meteor4 = GameObject(250, -275, 0, 1, "meteor_large")
            meteor5 = GameObject(325, -450, 0, 1, "meteor_large")
            meteor6 = GameObject(400, -650, 0, 1, "meteor_large")
            meteor7 = GameObject(400, -100, 0, 1, "meteor_large")
            meteor8 = GameObject(450, -300, 0, 1, "meteor_large")
            meteor9 = GameObject(500, -600, 0, 1, "meteor_large")
            meteor10 = GameObject(750, -500, 0, 1, "meteor_large")
            # Add the environmental objects to the main collision list
            env_objects.append(dish1)
            env_objects.append(dish2)
            env_objects.append(meteor1)
            env_objects.append(meteor2)
            env_objects.append(meteor3)
            env_objects.append(meteor4)
            env_objects.append(meteor5)
            env_objects.append(meteor6)
            env_objects.append(meteor7)
            env_objects.append(meteor8)
            env_objects.append(meteor9)
            env_objects.append(meteor10)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(meteor1)
            falling_objects.append(meteor2)
            falling_objects.append(meteor3)
            falling_objects.append(meteor4)
            falling_objects.append(meteor5)
            falling_objects.append(meteor6)
            falling_objects.append(meteor7)
            falling_objects.append(meteor8)
            falling_objects.append(meteor9)
            falling_objects.append(meteor10)
            # Define the target
            target = GameObject(600, 513, 0, 0, "target")
            # Define the player
            player = GameObject(100, -30, 0.25, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 75

        if level == 10:
            # Define the environmental objects
            rocket1 = GameObject(700, 505, 0, 0, "rocket")
            meteor0 = GameObject(600, -50, 0, 0.5, "meteor_large")
            meteor1 = GameObject(0, -133, 0, 1, "meteor_large")
            meteor2 = GameObject(33, -166, 0, 1, "meteor_large")
            meteor3 = GameObject(66, -200, 0, 1, "meteor_large")
            meteor4 = GameObject(100, -233, 0, 1, "meteor_large")
            meteor5 = GameObject(133, -266, 0, 1, "meteor_large")
            meteor6 = GameObject(166, -300, 0, 1, "meteor_large")
            meteor7 = GameObject(200, -333, 0, 1, "meteor_large")
            meteor8 = GameObject(233, -366, 0, 1, "meteor_large")
            meteor9 = GameObject(266, -400, 0, 1, "meteor_large")
            meteor10 = GameObject(300, -433, 0, 1, "meteor_large")
            meteor11 = GameObject(333, -466, 0, 1, "meteor_large")
            meteor12 = GameObject(366, -500, 0, 1, "meteor_large")
            meteor13 = GameObject(400, -533, 0, 1, "meteor_large")
            meteor14 = GameObject(433, -566, 0, 1, "meteor_large")
            meteor15 = GameObject(466, -600, 0, 1, "meteor_large")
            meteor16 = GameObject(500, -633, 0, 1, "meteor_large")
            meteor17 = GameObject(533, -666, 0, 1, "meteor_large")
            meteor18 = GameObject(566, -700, 0, 1, "meteor_large")
            meteor19 = GameObject(600, -733, 0, 1, "meteor_large")
            meteor20 = GameObject(633, -766, 0, 1, "meteor_large")
            meteor21 = GameObject(666, -800, 0, 1, "meteor_large")
            meteor22 = GameObject(700, -833, 0, 1, "meteor_large")
            meteor23 = GameObject(733, -866, 0, 1, "meteor_large")
            meteor24 = GameObject(766, -900, 0, 1, "meteor_large")
            meteor25 = GameObject(800, -933, 0, 1, "meteor_large")
            # Add the environmental objects to the main collision list
            env_objects.append(rocket1)
            env_objects.append(meteor0)
            env_objects.append(meteor1)
            env_objects.append(meteor2)
            env_objects.append(meteor3)
            env_objects.append(meteor4)
            env_objects.append(meteor5)
            env_objects.append(meteor6)
            env_objects.append(meteor7)
            env_objects.append(meteor8)
            env_objects.append(meteor9)
            env_objects.append(meteor10)
            env_objects.append(meteor11)
            env_objects.append(meteor12)
            env_objects.append(meteor13)
            env_objects.append(meteor14)
            env_objects.append(meteor15)
            env_objects.append(meteor16)
            env_objects.append(meteor17)
            env_objects.append(meteor18)
            env_objects.append(meteor19)
            env_objects.append(meteor20)
            env_objects.append(meteor21)
            env_objects.append(meteor22)
            env_objects.append(meteor23)
            env_objects.append(meteor24)
            env_objects.append(meteor25)
            # Add falling environmental objects to the ground collision list
            falling_objects.append(meteor0)
            falling_objects.append(meteor1)
            falling_objects.append(meteor2)
            falling_objects.append(meteor3)
            falling_objects.append(meteor4)
            falling_objects.append(meteor5)
            falling_objects.append(meteor6)
            falling_objects.append(meteor7)
            falling_objects.append(meteor8)
            falling_objects.append(meteor9)
            falling_objects.append(meteor10)
            falling_objects.append(meteor11)
            falling_objects.append(meteor12)
            falling_objects.append(meteor13)
            falling_objects.append(meteor14)
            falling_objects.append(meteor15)
            falling_objects.append(meteor16)
            falling_objects.append(meteor17)
            falling_objects.append(meteor18)
            falling_objects.append(meteor19)
            falling_objects.append(meteor20)
            falling_objects.append(meteor21)
            falling_objects.append(meteor22)
            falling_objects.append(meteor23)
            falling_objects.append(meteor24)
            falling_objects.append(meteor25)
            # Define the target
            target = GameObject(742, 513, 0, 0, "target")
            # Define the player
            player = GameObject(-30, -30, 0.5, 1, "player")
            player_x_acceleration = 0
            player_y_acceleration = 0.005
            fuel_value = 50

        # Set the text displays on the game screen
        score_text = medium_font.render('Score: ' + str(score), False, (255, 255, 255))
        initial_level_display = large_font.render('Level ' + str(level), False, (255, 255, 255))
        enter_text = small_font.render('Press enter to play.', False, (255, 255, 255))
        level_display = medium_font.render('Level ' + str(level), False, (255, 255, 255))
        v_display = medium_font.render('Descent: ' + str(round(player.y_speed, 1)) + 'm/s', False, (0, 255, 0))
        h_display = medium_font.render('Speed: ' + str(round(abs(player.x_speed), 1)) + 'm/s', False, (0, 255, 0))
        display_fuel = medium_font.render('Fuel: ' + str(int(fuel_value)) + '%', False, (0, 255, 0))
        game_lose = large_font.render('MISSION FAILED', False, (255, 0, 0))
        game_win = large_font.render('MISSION SUCCESS', False, (0, 255, 0))

        # Display the background images on the screen
        screen.fill((100, 100, 100))
        display(background, 0, -524)

        # Pre-level loop
        while pre_game_loop:

            # Update the enter text
            enter_text = small_font.render('Press enter to start.', False, (255, 255, 255))

            # Display the text on the screen
            display(initial_level_display, 290, 200)
            display(enter_text, 300, 260)

            # Update the display
            pygame.display.update()

            # Look for inputs from the user
            for event in pygame.event.get():

                # Stop each loop to end the program when the user clicks the X in the top-right corner
                if event.type == pygame.QUIT:
                    pre_game_loop = False
                    game_loop = False
                    outer_game_loop = False
                    end_loop = False
                    main_loop = False

                # Start the game when the user presses enter
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pre_game_loop = False

        # Make the pre-game loop run for the next level
        pre_game_loop = True

        # Set the value for the explosion clearing timer
        delay = 0

        # Run the level
        while game_loop:

            # Display the background images on the screen
            screen.fill((100, 100, 100))
            display(background, 0, -524)

            # Look for inputs from the user
            for event in pygame.event.get():

                # Stop each loop to end the program when the user clicks the X in the top-right corner
                if event.type == pygame.QUIT:
                    game_loop = False
                    outer_game_loop = False
                    end_loop = False
                    main_loop = False

                # Change the acceleration of the player when the user presses the arrow keys, if they have fuel
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and fuel_value > 0:
                        player_x_acceleration = -0.005
                    if event.key == pygame.K_RIGHT and fuel_value > 0:
                        player_x_acceleration = 0.005
                    if event.key == pygame.K_UP and fuel_value > 0:
                        player_y_acceleration = -0.005
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_x_acceleration = 0
                    if event.key == pygame.K_UP:
                        player_y_acceleration = 0.005

            # Use fuel when the player is accelerating with an arrow key
            if player_y_acceleration != 0.005 or player_x_acceleration != 0:
                fuel_value -= 0.1
                if fuel_value <= 0:
                    player_y_acceleration = 0.005
                    player_x_acceleration = 0

            # Change the player's speeds and location based on its acceleration and speed
            player.x_speed += player_x_acceleration
            player.y_speed += player_y_acceleration
            player.move()

            # Move and display the environmental objects
            for anything in env_objects:
                anything.move()
                anything.display()

            # Display the target
            target.display()

            # Update the altitude text display
            altitude = medium_font.render('Altitude: ' + str(int((530 - player.y))) + 'm', False, (255, 255, 255))
            if int(530 - player.y < 0):
                altitude = medium_font.render('Altitude: 0m', False, (255, 255, 255))

            # Update the fuel text display
            display_fuel = medium_font.render('Fuel: ' + str(int(fuel_value)) + '%', False, (0, 255, 0))
            if fuel_value < 25:
                display_fuel = medium_font.render('Fuel: ' + str(int(fuel_value)) + '%', False, (255, 255, 0))
            if fuel_value <= 0:
                display_fuel = medium_font.render('Fuel: 0%', False, (255, 0, 0))

            # Update the descent display
            if round(player.y_speed, 1) < 1.5:
                v_display = medium_font.render('Descent: ' + str(round(player.y_speed, 1)) + 'm/s', False, (0, 255, 0))
            if 1.5 <= round(player.y_speed, 1) < 2:
                v_display = medium_font.render('Descent: ' + str(round(player.y_speed, 1)) + 'm/s', False,
                                               (255, 255, 0))
            if round(player.y_speed, 1) >= 2:
                v_display = medium_font.render('Descent: ' + str(round(player.y_speed, 1)) + 'm/s TOO FAST', False,
                                               (255, 0, 0))

            # Update the speed text display
            if round(abs(player.x_speed), 1) < 0.7:
                h_display = medium_font.render('Speed: ' + str(round(abs(player.x_speed), 1)) + 'm/s', False,
                                               (0, 255, 0))
            if 0.7 <= round(abs(player.x_speed), 1) < 1:
                h_display = medium_font.render('Speed: ' + str(round(abs(player.x_speed), 1)) + 'm/s', False,
                                               (255, 255, 0))
            if round(abs(player.x_speed), 1) >= 1:
                h_display = medium_font.render('Speed: ' + str(round(abs(player.x_speed), 1)) + 'm/s TOO FAST', False,
                                               (255, 0, 0))

            # Display the text display
            display_text()

            # Display the player (either the thrusting or non-thrusting image)
            if player_x_acceleration == 0 and player_y_acceleration == 0.005:
                player.display()
            else:
                player.rect = player.image.get_rect()
                player.rect.move_ip(int(player.x), int(player.y))
                screen.blit(player_thrusting, (int(player.x), int(player.y)))

            # Detect collisions between two env objects or between one env object and the player
            for anything in env_objects:
                if player.collided_with(anything):
                    # Display the explosion and the game_lose text, update the display, and end the game loop
                    display(in_air_explosion_large, player.x - 17, player.y - 18)
                    display(game_lose, 200, 200)
                    game_loop = False
                    outer_game_loop = False
                    end_loop = True
                for anything_else in env_objects:
                    if anything.collided_with(anything_else) and anything != anything_else:
                        display(in_air_explosion_large, anything.x - 16, anything.y - 16)
                        anything.x_speed = 0
                        anything.y_speed = 0
                        anything_else.x_speed = 0
                        anything_else.y_speed = 0
                        delay += 1
                        if delay >= 100:
                            if anything in env_objects:
                                env_objects.remove(anything)
                            if anything in falling_objects:
                                falling_objects.remove(anything)
                            if anything_else in env_objects:
                                env_objects.remove(anything_else)
                            if anything_else in falling_objects:
                                falling_objects.remove(anything_else)
                            delay = 0

            # Detect collisions between falling environmental objects and the ground
            for anything in falling_objects:
                if anything.y >= 530:
                    anything.x_speed = 0
                    anything.y_speed = 0
                    if anything.name == "meteor_small" or anything.name == "meteor_large":
                        display(explosion_medium, anything.x - 16, anything.y - 30)
                        delay += 1
                    if delay >= 100 and (anything.name == "meteor_small" or anything.name == "meteor_large"):
                        falling_objects.remove(anything)
                        env_objects.remove(anything)
                        delay = 0

            # End the game loop when the player hits the ground
            if player.y >= 530:
                # Win if the player is touching the target and not going too fast
                if player.collided_with(target) == 1 and round(player.y_speed, 1) < 2 and round(abs(player.x_speed),
                                                                                                1) < 1:
                    # Give them a score based on their location, speeds, and remaining fuel
                    score += int(
                        1000 - 40 * abs(player.x - (target.x + 13)) + 10 * fuel_value + 1000 * (2 - player.y_speed)
                        + 1000 * (1 - abs(player.x_speed)))

                    # Update the score text display
                    score_text = medium_font.render('Score: ' + str(score), False, (255, 255, 255))

                    # Display the background images on the screen
                    screen.fill((100, 100, 100))
                    display(background, 0, -524)

                    # Display the text display
                    display_text()

                    # Set the high score
                    if score >= high_score:
                        high_score = score

                    # Update the enter text
                    enter_text = small_font.render('Press enter to go to the next level.', False, (255, 255, 255))

                    if level == 10:
                        level_win_loop = False
                        game_loop = False
                        outer_game_loop = False
                        end_loop = True
                        overall_win = True

                    # Level win loop
                    while level_win_loop:

                        # Display the target, player, game_win text, and update the display
                        display(game_win, 180, 200)
                        display(enter_text, 250, 270)
                        target.display()
                        player.display()
                        pygame.display.update()

                        # Look for inputs from the user
                        for event in pygame.event.get():

                            # Stop each loop to end the program when the user clicks the X in the top-right corner
                            if event.type == pygame.QUIT:
                                level_win_loop = False
                                game_loop = False
                                outer_game_loop = False
                                end_loop = False
                                main_loop = False

                            # End the level win loop when the user presses enter
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    level_win_loop = False
                                    game_loop = False

                    # Make the level win loop run for the next level
                    level_win_loop = True

                    # End the level win loop and proceed to the next level
                    level += 1

                # Lose in all other circumstances
                else:
                    # Display the explosion, display the game_lose text, update the display, and end the game loop
                    display(explosion_medium, player.x - 17, player.y - 30)
                    display(game_lose, 200, 200)
                    game_loop = False
                    outer_game_loop = False
                    end_loop = True

            # Update the display
            pygame.display.update()

    # Run the end screen until the player returns to the start screen, or closes the game window
    while end_loop:

        # Set the text displays on the end screen
        high_score_text = medium_font.render('High Score: ' + str(high_score), False, (255, 255, 255))
        enter_text = small_font.render('Press enter to return to the start screen.', False, (255, 255, 255))

        # Display the end screen text
        if overall_win:
            display(overall_win_text, 100, 200)
        display(high_score_text, 300, 170)
        display(score_text, 340, 260)
        display(enter_text, 220, 300)

        # Look for inputs from the keyboard or mouse
        for event in pygame.event.get():

            # Stop each loop to end the program when the user clicks the X in the top-right corner
            if event.type == pygame.QUIT:
                end_loop = False
                main_loop = False

            # Return the home screen when the user presses enter
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    end_loop = False
                    start_loop = True

        # Update the display
        pygame.display.update()
