import pygame
import random

WIDTH, HEIGHT = 600, 500

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()


def CreateLevel(size:tuple=(10, 10), mine_count:int=10):
    print(f"Creating Level ({size[0]}x{size[1]})")
    picks = random.sample(range(size[0]*size[1]), mine_count)
    mines = set()
    for i in picks:
        x = i % size[0]
        y = i // size[0]
        mines.add((x, y))
    print("Done")
    level = {
        "mines": mines,
        "mine_count": mine_count,
        "size": size,
        "width": size[0],
        "height": size[1],
        "progress": {
            "clicks": list(),
            "flags": set(),
        }
    }
    return level

def RenderScreen():
    pass

# Game variables
Level1 = CreateLevel()
print(Level1)

zoom = 37
tile_rows = HEIGHT // zoom + 1
tile_columns = WIDTH // zoom + 1

posx, posy = 0, 0

# Texture Cache
texture = {
    "cell1": pygame.image.load("content/cell1.svg"),
    "cell2": pygame.image.load("content/cell2.svg"),
    "cell3": pygame.image.load("content/cell3.svg"),
    "cell4": pygame.image.load("content/cell4.svg"),
    "cell5": pygame.image.load("content/cell5.svg"),
    "cell6": pygame.image.load("content/cell6.svg"),
    "cell7": pygame.image.load("content/cell7.svg"),
    "cell8": pygame.image.load("content/cell8.svg"),
    "celldown": pygame.image.load("content/celldown.svg"),
    "cellup": pygame.image.load("content/cellup.svg"),
    "cellflag": pygame.image.load("content/cellflag.svg"),
    "cellmine": pygame.image.load("content/cellmine.svg"),
    "falsemine": pygame.image.load("content/falsemine.svg"),
    "blast": pygame.image.load("content/blast.svg"),
}
def RefreshScaledTexture():
    global scaled_texture
    scaled_texture = {
        "cell1": pygame.transform.smoothscale(texture["cell1"], (zoom, zoom)),
        "cell2": pygame.transform.smoothscale(texture["cell2"], (zoom, zoom)),
        "cell3": pygame.transform.smoothscale(texture["cell3"], (zoom, zoom)),
        "cell4": pygame.transform.smoothscale(texture["cell4"], (zoom, zoom)),
        "cell5": pygame.transform.smoothscale(texture["cell5"], (zoom, zoom)),
        "cell6": pygame.transform.smoothscale(texture["cell6"], (zoom, zoom)),
        "cell7": pygame.transform.smoothscale(texture["cell7"], (zoom, zoom)),
        "cell8": pygame.transform.smoothscale(texture["cell8"], (zoom, zoom)),
        "celldown": pygame.transform.smoothscale(texture["celldown"], (zoom, zoom)),
        "cellup": pygame.transform.smoothscale(texture["cellup"], (zoom, zoom)),
        "cellflag": pygame.transform.smoothscale(texture["cellflag"], (zoom, zoom)),
        "cellmine": pygame.transform.smoothscale(texture["cellmine"], (zoom, zoom)),
        "falsemine": pygame.transform.smoothscale(texture["falsemine"], (zoom, zoom)),
        "blast": pygame.transform.smoothscale(texture["blast"], (zoom, zoom)),
    }
RefreshScaledTexture()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()