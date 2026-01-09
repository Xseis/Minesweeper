# Attempt 2
import pygame
import random

WIDTH, HEIGHT = 600, 500
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

pygame.display.set_caption("Hopefully optimized minesweeper")

def GenerateLevel(size:tuple=(10,10), mine_count:int=15, current_index_val=0, index_steps=100):
    '''
    Generates slice of level, implemented in main loop to prevent bottleneck
    '''
    global bytemap, current_index, mines
    current_index = current_index_val
    end_index = current_index + index_steps
    if current_index == 0: # Generate empty bytemap first iteration
        print(f"Generating level ({size[0]}x{size[1]}) with {mine_count} mines")
        mines = random.sample(range(size[0]*size[1]), mine_count)
        bytemap = bytearray(size[0]*size[1])
    elif current_index > mine_count:
        return 1

    for mine in range(current_index, end_index): 
        if mine >= mine_count:
            print("Done generating!")
            return 1
        bytemap[mines[mine]] |= MINE # Place mine
        neighbouring_tiles = [
            mines[mine]-size[1]-1, mines[mine]-size[0], mines[mine]-size[1]+1,
            mines[mine]-1,                              mines[mine]+1,
            mines[mine]+size[1]-1, mines[mine]+size[1], mines[mine]+size[1]+1,
        ]
        for neighbour in neighbouring_tiles:
            if 0 <= neighbour < size[0]*size[1]:
                bytemap[neighbour] += 1
        current_index += 1
    print(f"Progress: {current_index/mine_count*100}%")
    return 0

# Game variables
current_index = 0
zoom = 40.0

NUMBERS= 0b00001111
MINE=    0b00010000
FLAG=    0b00100000
CLICKED= 0b01000000


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
    global scaled_texture, tile_rows, tile_columns
    tile_rows = int(HEIGHT // zoom + 1)
    tile_columns = int(WIDTH // zoom + 1)
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

generating = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if generating:
        mine_count = 150000
        if GenerateLevel((10000, 10000), mine_count, current_index, mine_count//100):
            generating = False
    
    clock.tick(60)

pygame.quit()