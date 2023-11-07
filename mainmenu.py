import pygame
import sys
import subprocess

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mi Juego Pygame")

# Cargar fondos
backgrounds = {
    "world1": pygame.image.load("img/background_world1.png"),
    "world2": pygame.image.load("img/background_world2.jpg"),
    "world3": pygame.image.load("img/background_world3.png"),
}

# Cargar música de fondo
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Cargar fuentes
menu_font = pygame.font.Font(None, 36)  # Ajusta el tamaño de la fuente según tus necesidades

# Función para mostrar el menú principal
def main_menu():
    selected_option = 0
    options = ["Seleccionar Mundo", "Instrucciones", "Salir"]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        # Opción "Seleccionar Mundo"
                        run_level1()  # Ejecuta "level1.py"
                    elif selected_option == 1:
                        show_instructions()
                        pass
                    elif selected_option == 2:
                        # Opción "Salir"
                        pygame.quit()
                        sys.exit()

        # Dibuja el fondo
        screen.blit(backgrounds["world1"], (0, 0))

        # Dibuja el menú y resalta la opción seleccionada
        for i, option in enumerate(options):
            text_color = (255, 255, 255)  # Color blanco
            if i == selected_option:
                text_color = (255, 0, 0)  # Color rojo para la opción seleccionada
            text_surface = menu_font.render(option, True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (width // 2, height // 2 + i * 50)
            screen.blit(text_surface, text_rect)

        pygame.display.update()

def show_instructions():
    # Fuente para mostrar las instrucciones
    instructions_font = pygame.font.Font(None, 28)

    instructions = [
        "Instrucciones:",
        "1. Moverte hacia los lados: Flechas IZQUIERDA",
        " y DERECHA.",
        "2. Disparar: Tecla ESPACIO.",
        "3. Derrota a 10 enemigos para pasar al siguiente",
        "nivel.",
        "4. En el siguiente nivel, usa las flechas (ARRIBA,",
        " ABAJO, IZQUIERDA, DERECHA) para volar y dispara ",
        "con ESPACIO.",
        "5. Derrota a 5 enemigos en el segundo nivel para ",
        "ganar el juego.",
        "6. ¡Diviértete!",
        "",
        "Presiona ENTER para volver al menú principal."
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Volver al menú principal
                    return

        screen.fill((0, 0, 0))  # Rellena la pantalla de negro
        y = 100  # Posición vertical inicial
        for line in instructions:
            text_surface = instructions_font.render(line, True, (255, 255, 255))  # Texto blanco
            text_rect = text_surface.get_rect()
            text_rect.center = (width // 2, y)
            screen.blit(text_surface, text_rect)
            y += 30  # Espacio vertical entre líneas

        pygame.display.update()


# Función para ejecutar "level1.py"
def run_level1():
    subprocess.run(["python", "level1.py"])

if __name__ == "__main__":
    main_menu()
