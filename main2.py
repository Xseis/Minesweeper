# Attempt 2
import pygame
import random

WIDTH, HEIGHT = 600, 500
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

WINDOW_CAPTION = "Hopefully optimized minesweeper"
pygame.display.set_caption(WINDOW_CAPTION)

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
    elif current_index > mine_count:
        return (1, current_index/mine_count*100)

    for mine in range(current_index, end_index): 
        if mine >= mine_count:
            print("Done generating!")
            return (1, current_index/mine_count*100)
        bytemap[mines[mine] +BYTEMAP_OFFSET] |= MINE # Place mine
        neighbouring_tiles = [
            mines[mine]-size[1]-1, mines[mine]-size[0], mines[mine]-size[1]+1,
            mines[mine]-1,                              mines[mine]+1,
            mines[mine]+size[1]-1, mines[mine]+size[1], mines[mine]+size[1]+1,
        ]
        for neighbour in neighbouring_tiles:
            if 0 <= neighbour < size[0]*size[1]:
                bytemap[neighbour +BYTEMAP_OFFSET] += 1
        current_index += 1
    return (0, current_index/mine_count*100)

def GenerateChunks(flag=None, pos=(0,0)):
    global chunks
    camera_x, camera_y = pos # Top left window
    chunksize = chunks["size"]
    chunk_columns = int.from_bytes(bytemap[0:4]) // chunksize +1
    chunk_rows = int.from_bytes(bytemap[4:8]) // chunksize +1
    TEXTURESIZE = texture["TEXTURESIZE"]

    if flag == "start":
        # Slight optimizing
        filled_chunk_template = pygame.Surface((TEXTURESIZE[0]*chunksize, TEXTURESIZE[1]*chunksize))
        for tx in range(chunksize):
                for ty in range(chunksize):
                    filled_chunk_template.blit(texture["cellup"], (tx*TEXTURESIZE[0], ty*TEXTURESIZE[1]))
        # Make all chunk surfaces
        for x in range(chunk_columns):
            for y in range(chunk_rows):
                pos = (x, y)
                worldpos = (x*zoom*chunksize, y*zoom*chunksize)
                chunks[pos] = {"normal": pygame.Surface((TEXTURESIZE[0]*chunksize, TEXTURESIZE[1]*chunksize)),}
                chunks[pos]["normal"].fill((random.randint(50, 150), 0, 0))

                width_remainder = int.from_bytes(bytemap[0:4]) % chunksize
                height_remainder= int.from_bytes(bytemap[4:8]) % chunksize
                if x == chunk_columns-1 and y != chunk_rows-1 and width_remainder != 0: # Right row
                    for tx in range(int.from_bytes(bytemap[0:4]) % chunksize):
                        for ty in range(chunksize):
                            chunks[pos]["normal"].blit(texture["cellup"], (tx*TEXTURESIZE[0], ty*TEXTURESIZE[1]))
                            chunks[pos]["scaled"] = pygame.transform.smoothscale(chunks[pos]["normal"], (zoom*chunksize, zoom*chunksize))
                elif x == chunk_columns-1 and y == chunk_rows-1 and width_remainder+height_remainder != 0: # Bottom right
                    for tx in range(int.from_bytes(bytemap[0:4]) % chunksize):
                        for ty in range(int.from_bytes(bytemap[4:8]) % chunksize):
                            chunks[pos]["normal"].blit(texture["cellup"], (tx*TEXTURESIZE[0], ty*TEXTURESIZE[1]))
                            chunks[pos]["scaled"] = pygame.transform.smoothscale(chunks[pos]["normal"], (zoom*chunksize, zoom*chunksize))
                elif x != chunk_columns-1 and y == chunk_rows-1 and height_remainder != 0: # Bottom row
                    for tx in range(chunksize):
                        for ty in range(int.from_bytes(bytemap[4:8]) % chunksize):
                            chunks[pos]["normal"].blit(texture["cellup"], (tx*TEXTURESIZE[0], ty*TEXTURESIZE[1]))
                            chunks[pos]["scaled"] = pygame.transform.smoothscale(chunks[pos]["normal"], (zoom*chunksize, zoom*chunksize))
                else: # Every chunk except edges
                    chunks[pos]["normal"].blit(filled_chunk_template, (0, 0))
                    chunks[pos]["scaled"] = pygame.transform.smoothscale(chunks[pos]["normal"], (zoom*chunksize, zoom*chunksize))

def Render():
    chunksize = chunks["size"]
    for key, chunk in chunks.items():
        if key == "size":
            continue
        else:
            x = key[0] * zoom * chunksize
            y = key[1] * zoom * chunksize
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                scaled_chunk = chunk["scaled"]
                win.blit(scaled_chunk, (x, y))
    
    pygame.display.flip()
    pygame.display.set_caption(WINDOW_CAPTION + f" - Iterating {len(chunks)} chunks - FPS: {current_fps}")
    

# Game variables
chunks = {
    "size": 16
}

current_index = 0
zoom = 5.0

pos_x = 0
pos_y = 0

NUMBERS= 0b00001111
MINE=    0b00010000
FLAG=    0b00100000
CLICKED= 0b01000000

BYTEMAP_OFFSET=12 # 0-3, 4-7, 8-11
MAP_WIDTH = 160  # 0
MAP_HEIGHT = 160 # 1
MAP_MINES = 1500 # 2
bytemap = bytearray(MAP_WIDTH*MAP_HEIGHT +BYTEMAP_OFFSET) # offset for width and height
bytemap[0:4] = MAP_WIDTH.to_bytes(4)
bytemap[4:8] = MAP_HEIGHT.to_bytes(4)
bytemap[8:12] = MAP_MINES.to_bytes(4)

# Texture Cache
texture = {
    "TEXTURESIZE": pygame.image.load("content/cell1.svg").get_size(),
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

current_fps = 0
is_generating_level = True
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.WINDOWRESIZED:
            WIDTH = event.dict["x"]
            HEIGHT= event.dict["y"]
    if is_generating_level:
        mine_count = int.from_bytes(bytemap[8:12])
        status, progress = GenerateLevel((int.from_bytes(bytemap[0:4]), int.from_bytes(bytemap[4:8])), mine_count, current_index, mine_count//100+1)
        # progress bar
        pygame.draw.rect(win, (230, 230, 230), (WIDTH/2-(progress/100*WIDTH)/2, HEIGHT/2-(progress/100*HEIGHT)/2, progress/100*WIDTH, progress/100*HEIGHT))
        pygame.display.flip()
        if status: # If finished
            generating = False
            GenerateChunks("start")
    
    Render()
    current_fps = clock.tick(60)

pygame.quit()