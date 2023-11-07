#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import sys
import os
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 0, 255)

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Nivel de Vuelo")

clock = pygame.time.Clock()

# Función para cargar imágenes
def load_image(img_folder, img_name, size=None):
    img_path = os.path.join(img_folder, img_name)
    img = pygame.image.load(img_path)
    if size:
        img = pygame.transform.scale(img, size)
    return img

# Función para cargar sonidos
def load_sound(sound_folder, sound_name):
    sound_path = os.path.join(sound_folder, sound_name)
    return pygame.mixer.Sound(sound_path)

# Cargar fondos, imágenes y sonidos
background = load_image("img", "background_sky.jpg", (width, height))
player_image = load_image("img", "player_airplane.png", (50, 50))
enemy_image = load_image("img", "enemy_airplane.png", (50, 50))
bullet_image = load_image("img", "bullet.png", (10, 20))

collision_sound = load_sound("sounds", "collision_sound.mp3")
game_over_sound = load_sound("sounds", "game_over_sound.mp3")
shoot_sound = load_sound("sounds", "shoot_sound.mp3")

# Función para mostrar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# ... (código previo del nivel 2)

def show_victory_message():
    victory_font = pygame.font.Font(None, 72)
    selected_option = 0  # Solo hay una opción, por lo que seleccionamos 0 directamente

    while True:
        screen.blit(background, (0, 0))
        draw_text("¡Has derrotado a 5 enemigos!", victory_font, PINK, screen, 50, 100)
        draw_text("¡Ganaste!, Fin", victory_font, PINK, screen, 150, 250)

        text_color = PINK  # El color del texto de la única opción
        draw_text("Salir del Juego", victory_font, text_color, screen, 100, 350)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    # Opción "Salir del Juego"
                    pygame.quit()
                    sys.exit()


# ... (código restante del nivel 2)


# Función para ejecutar el nivel de vuelo
def run_flight_level(player_x, player_y):
    player_speed = 5
    bullets = []
    enemies_defeated = 0


    # Lista de enemigos
    enemies = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_sound.play()
                    bullets.append({"x": player_x + 20, "y": player_y - 20, "speed": 8})

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - 50:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < height - 50:
            player_y += player_speed

        screen.blit(background, (0, 0))
        screen.blit(player_image, (player_x, player_y))

        # Mover y dibujar enemigos
        for enemy in enemies:
            enemy["x"] -= enemy["speed"]
            screen.blit(enemy_image, (enemy["x"], enemy["y"]))

            # Verificar colisión con el jugador
            player_rect = pygame.Rect(player_x, player_y, 50, 50)
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 50)

            if player_rect.colliderect(enemy_rect):
                collision_sound.play()
                game_over()

            if enemy["x"] < -50:
                enemies.remove(enemy)



        # Mover y dibujar balas
        for bullet in bullets:
            bullet["y"] -= bullet["speed"]
            screen.blit(bullet_image, (bullet["x"], bullet["y"]))

            # Verificar colisión de balas con enemigos
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 50)
                bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 20)

                if enemy_rect.colliderect(bullet_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    collision_sound.play()
                    enemies_defeated += 1 
    

        # Añadir más enemigos
        if len(enemies) < 5:
            new_enemy = {
                "x": width,
                "y": random.randint(0, height - 50),
                "speed": random.randint(2, 5)
            }
            enemies.append(new_enemy)
        if enemies_defeated >= 5:
            show_victory_message()
          # Sal del bucle principal para evitar más ejecución


        pygame.display.update()
        clock.tick(60)

# Función para mostrar Game Over
def game_over():
    game_over_font = pygame.font.Font(None, 72)
    game_over_sound.play()
    while True:
        screen.blit(background, (0, 0))
        draw_text("¡Game Over!", game_over_font, PINK, screen, 250, 100)
        draw_text("Presiona Enter para", game_over_font, PINK, screen, 100, 250)
        draw_text("volver a intentarlo", game_over_font, PINK, screen, 100, 300)
        draw_text("Presiona ESC para", game_over_font, WHITE, screen, 100, 400)
        draw_text("salir del juego", game_over_font, WHITE, screen, 100, 450)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    flight_level_main()  # Reiniciar el juego

# Función principal para el nivel de vuelo
def flight_level_main():
    player_x, player_y = 375, 500
    run_flight_level(player_x, player_y)

if __name__ == "__main__":
    flight_level_main()


# In[ ]:






