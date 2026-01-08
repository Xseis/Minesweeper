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

def RenderScreen(level, position):
    global game_surface, failed
    surface = pygame.Surface((WIDTH, HEIGHT))
    for x in range(tile_columns):
        if x >= level["width"]: break
        for y in range(tile_rows):
            if y >= level["height"]: break
            tile_position = (x*zoom-position[0], y*zoom-position[1])
            surface.blit(scaled_texture["cellup"], tile_position)
    for x, y in level["progress"]["clicks"]:
        tile_position = (x*zoom-position[0], y*zoom-position[1])
        surrounding_tiles = [
            (x-1, y-1),(x, y-1),(x+1, y-1),
            (x-1, y),             (x+1, y),
            (x-1, y+1),(x, y+1),(x+1, y+1),
        ]
        bomb_count = 0
        for tile in surrounding_tiles:
            if tile in level["mines"]:
                bomb_count += 1
        if (x, y) in level["mines"]: # Clicked mine
            failed = True
        elif bomb_count > 0: # If surrounding bombs
            surface.blit(scaled_texture[f"cell{bomb_count}"], tile_position)
        else:
            surface.blit(scaled_texture["celldown"], tile_position)
    for x, y in level["progress"]["flags"]:
        tile_position = (x*zoom-position[0], y*zoom-position[1])
        surface.blit(scaled_texture["cellflag"], tile_position)
    
    if failed: # Game end
        for x, y in level["mines"]:
            tile_position = (x*zoom-position[0], y*zoom-position[1])
            if (x, y) in level["progress"]["clicks"]:
                surface.blit(scaled_texture["blast"], tile_position) # Clicked mine
            else:
                surface.blit(scaled_texture["cellmine"], tile_position) # Normal mine

    game_surface = surface
    return surface


# Game variables
Level1 = CreateLevel((10, 10))
print(Level1)

zoom = 47
tile_rows = HEIGHT // zoom + 1
tile_columns = WIDTH // zoom + 1

posx, posy = 0, 0

failed = False

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

game_surface = RenderScreen(Level1, (posx, posy))

running = True
while running:
    # Selected Tile
    mousepos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    selected_tile = ((mousepos[0]+posx)//zoom, (mousepos[1]+posy)//zoom)

    # Hover selected tile
    if mouse_pressed[0]:
        RenderScreen(Level1, (posx, posy))
        if 0 <= selected_tile[0] < Level1["width"] and 0 <= selected_tile[1] < Level1["height"]: # If selected_tile is inside level
            if selected_tile not in Level1["progress"]["flags"] and selected_tile not in Level1["progress"]["clicks"]: # If the tile isnt already a flag or not already clicked
                if not failed: game_surface.blit(scaled_texture["celldown"], (selected_tile[0]*zoom-posx, selected_tile[1]*zoom-posy))
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.WINDOWRESIZED:
            WIDTH, HEIGHT = event.dict["x"], event.dict["y"]
            RefreshScaledTexture()
            RenderScreen(Level1, (posx, posy))

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            if event.dict["button"] == 1: # Left click
                if 0 <= selected_tile[0] < Level1["width"] and 0 <= selected_tile[1] < Level1["height"]: # If selected_tile is inside level
                    if selected_tile not in Level1["progress"]["clicks"] and selected_tile not in Level1["progress"]["flags"]:
                        if not failed: Level1["progress"]["clicks"].append(selected_tile)
                        print("pressed")
            elif event.dict["button"] == 3:
                if 0 <= selected_tile[0] < Level1["width"] and 0 <= selected_tile[1] < Level1["height"]: # If selected_tile is inside level
                    if selected_tile not in Level1["progress"]["clicks"] and selected_tile not in Level1["progress"]["flags"]:
                        if not failed: Level1["progress"]["flags"].add(selected_tile)
                    elif selected_tile in Level1["progress"]["flags"]:
                        if not failed: Level1["progress"]["flags"].remove(selected_tile)
            RenderScreen(Level1, (posx, posy))
    
        if event.type == pygame.MOUSEWHEEL:
            previous_zoom = zoom
            zoom *= 1.2 if event.dict["y"] == 1 else 1/1.2
            zoom = round(zoom)
            if zoom == previous_zoom: # If zoom is really small
                zoom += event.dict["y"]
            zoom = max(min(zoom, 160), 3) # sets min and max zoom
            RefreshScaledTexture()

            print(f"Distance zoomed: {tile_columns}")
            
            RenderScreen(Level1, (posx, posy))

        # if event.type == pygame.MOUSEMOTION:
        #     if mouse_pressed:
        #         pressed_location = (-1, -1) # Prevent tile click
        #         dirx, diry = event.dict["rel"]
        #         posx -= dirx
        #         posy -= diry
        #         RenderScreen(Level1, (posx, posy))

    win.blit(game_surface, (0,0))

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()