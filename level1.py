#!/usr/bin/env python
# coding: utf-8
# In[ ]:

import pygame
import sys
import os
import subprocess
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
pygame.display.set_caption("Mi Juego Pygame")

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
backgrounds = {
    "world1": load_image("img", "background_world1.png", (width, height)),
    "world2": load_image("img", "background_world2.jpg", (width, height)),
    "world3": load_image("img", "background_world3.png", (width, height)),
}

player_images = {
    "world1": load_image("img", "player_world1.png", (50, 50)),
    "world2": load_image("img", "player_world2.png", (50, 50)),
    "world3": load_image("img", "player_world3.png", (50, 50)),
}

enemy_images = {
    "world1": load_image("img", "enemy_world1.png", (50, 50)),
    "world2": load_image("img", "enemy_world2.png", (50, 50)),
    "world3": load_image("img", "enemy_world3.png", (50, 50)),
}

bullet_image = load_image("img", "bullet.png", (10, 20))

collision_sound = load_sound("sounds", "collision_sound.mp3")
game_over_sound = load_sound("sounds", "game_over_sound.mp3")
start_sound = load_sound("sounds", "start_sound.mp3")
shoot_sound = load_sound("sounds", "shoot_sound.mp3")

# Reproducir sonido de inicio
start_sound.play()

# Función para reproducir música de fondo
def play_background_music():
    pygame.mixer.music.load("sounds/background_music.mp3")  # Reemplaza con tu archivo de música
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

play_background_music()

# Función para mostrar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# ...

def select_world_menu():
    world_menu_font = pygame.font.Font(None, 36)
    worlds = ["world1", "world2", "world3"]
    selected_index = 0

    while True:
        screen.blit(backgrounds[worlds[selected_index]], (0, 0))  # Muestra el fondo del mundo actual

        draw_text("Selecciona un Mundo", world_menu_font, WHITE, screen, 250, 50)

        for i, world in enumerate(worlds):
            text = f"{i + 1}. {world}"
            text_color = WHITE
            if i == selected_index:
                # Cambiar el color del texto o dibujar un recuadro alrededor de la opción seleccionada
                text_color = PINK

            draw_text(text, world_menu_font, text_color, screen, 300, 200 + i * 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(worlds)  # Mueve hacia arriba en la lista
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(worlds)  # Mueve hacia abajo en la lista
                elif event.key == pygame.K_RETURN:
                    selected_world = worlds[selected_index]
                    return selected_world  # Devuelve el mundo seleccionado

# ...



# Función para manejar colisiones
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def show_victory_message():
    victory_font = pygame.font.Font(None, 72)
    options = ["Siguiente Nivel", "Menú Principal", "Salir del Juego"]
    selected_option = 0  # Opción seleccionada inicialmente

    while True:
        screen.blit(backgrounds[selected_world], (0, 0))
        draw_text("¡Has derrotado a 10 enemigos!", victory_font, PINK, screen, 50, 100)
        draw_text("¡Ganaste!", victory_font, PINK, screen, 150, 250)

        for i, option in enumerate(options):
            text_color = PINK if i == selected_option else WHITE
            draw_text(option, victory_font, text_color, screen, 100, 350 + i * 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)  # Mueve hacia abajo
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)  # Mueve hacia arriba
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        run_second_code()  # Siguiente Nivel
                    elif selected_option == 1:
                        main()  # Menú Principal
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()  # Salir del Juego



def game_over():
    game_over_font = pygame.font.Font(None, 72)
    game_over_sound.play()  # Reproducir sonido de Game Over
    pygame.mixer.music.stop()  # Detener la música de fondo al finalizar el juego
    options = ["Volver al Menú Principal", "Salir del Juego"]
    selected_option = 0  # Opción seleccionada inicialmente

    while True:
        screen.blit(backgrounds[selected_world], (0, 0))
        draw_text("¡Game Over!", game_over_font, PINK, screen, 250, 100)

        for i, option in enumerate(options):
            text_color = WHITE
            if i == selected_option:
                text_color = PINK
            draw_text(option, game_over_font, text_color, screen, 100, 250 + i * 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)  # Mueve hacia abajo
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)  # Mueve hacia arriba
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Volver al Menú Principal
                        main()
                    else:  # Salir del Juego
                        pygame.quit()
                        sys.exit()

    game_over_font = pygame.font.Font(None, 72)
    game_over_sound.play()  # Reproducir sonido de Game Over
    pygame.mixer.music.stop()  # Detener la música de fondo al finalizar el juego
    while True:
        screen.blit(backgrounds[selected_world], (0, 0))
        draw_text("¡Game Over!", game_over_font, PINK, screen, 250, 100)
        draw_text("Presiona Enter para", game_over_font, PINK, screen, 100, 250)
        draw_text(" volver al menú principal", game_over_font, PINK, screen, 100, 300)
        draw_text("Presiona ESC para", game_over_font,WHITE, screen, 100, 400)
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
                    main()  # Reiniciar el juego
                    
# Función para ejecutar un nivel
def run_level(player_x, player_y, enemies, player_img, enemy_img):
    player_speed = 5
    bullets = []
    enemies_defeated_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_sound.play()  # Reproducir sonido de disparo
                    bullets.append({"x": player_x + 20, "y": player_y - 20, "speed": 8})

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - 50:
            player_x += player_speed

        screen.blit(backgrounds[selected_world], (0, 0))
        screen.blit(player_img, (player_x, player_y))

        # Mover y dibujar enemigos
        for enemy in enemies:
            enemy["y"] += enemy["speed"]
            screen.blit(enemy_img, (enemy["x"], enemy["y"]))

            # Verificar colisión con el jugador
            player_rect = pygame.Rect(player_x, player_y, 50, 50)
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 50)

            if check_collision(player_rect, enemy_rect):
                collision_sound.play()  # Reproducir sonido de colisión
                game_over()

            # Eliminar enemigos que salen de la pantalla
            if enemy["y"] > height:
                enemies.remove(enemy)

        # Mover y dibujar balas
        for bullet in bullets:
            bullet["y"] -= bullet["speed"]
            screen.blit(bullet_image, (bullet["x"], bullet["y"]))

            # Verificar colisión con los enemigos
            bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 20)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 50)
                if check_collision(bullet_rect, enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    collision_sound.play()  # Reproducir sonido de colisión
                    enemies_defeated_count += 1

            # Eliminar balas que salen de la pantalla
            if bullet["y"] < 0:
                bullets.remove(bullet)

        pygame.display.update()
        clock.tick(60)

        # Añadir más enemigos
        if len(enemies) < 5:
            new_enemy = {
                "x": random.randint(0, width - 50),
                "y": -50,
                "speed": random.randint(2, 5)
            }
            enemies.append(new_enemy)

        # Verificar si el jugador ha derrotado a 5 enemigos
        if enemies_defeated_count >= 10:
            show_victory_message()
            
def run_second_code():
    subprocess.run(["python", "level2.py"])

# Función principal
def main():
    global selected_world
    selected_world = select_world_menu()

    player_x, player_y = 375, 500
    enemies = []

    for level in range(1, 4):  # Puedes ajustar la cantidad de niveles según tus necesidades
        player_img = player_images[selected_world]
        enemy_img = enemy_images[selected_world]
        run_level(player_x, player_y, enemies, player_img, enemy_img)

if __name__ == "__main__":
    main()
