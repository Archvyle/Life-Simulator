import pygame
import pygame_gui
import os
from Cell import *
from Creature import *
from Plant import *
from Grid import *

path = "C:/Users/hp/OneDrive/GameOfLife/data/"

SCREENWIDTH = 1536#1920#1280
SCREENHEIGHT = 864#1080#720
CELLSIZE = 5
WIDTH = int((SCREENWIDTH)/CELLSIZE)
HEIGHT = int((SCREENHEIGHT)/CELLSIZE)

running = True
dt = 0
fps = 60

fatalHunger = 1000
plantNutritionalValue=500
reproduceCost=800
maxPlantsMult=0.4

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
number_font = pygame.font.SysFont(None, CELLSIZE+int(CELLSIZE*0.3))
fps_font = pygame.font.SysFont("consolas", 40, bold=True)

ground = pygame.Surface((WIDTH*CELLSIZE, HEIGHT*CELLSIZE))
gridSurface = pygame.Surface((WIDTH*CELLSIZE, HEIGHT*CELLSIZE), pygame.SRCALPHA)

settingsImage = pygame.image.load(os.path.abspath(path + "settings.png"))
settingsImage = pygame.transform.scale(settingsImage, (45, 45))
xImage = pygame.image.load(os.path.abspath(path + "x.png"))
xImage = pygame.transform.scale(xImage, (43, 43))

manager = pygame_gui.UIManager((SCREENWIDTH, SCREENHEIGHT))

gui_window = fps_input = fatalHunger_input = plantNV_input = reproduceCost_input = maxPlantsMult_input = None

def drawGrid():
    for column in range(WIDTH+1):
        pygame.draw.line(gridSurface, "black", [column*CELLSIZE, 0], [column*CELLSIZE, HEIGHT*CELLSIZE])
    for row in range(HEIGHT+1):
        pygame.draw.line(gridSurface, "black", [0, row*CELLSIZE], [WIDTH*CELLSIZE, row*CELLSIZE])


def drawGround(grid):
    for column in range(WIDTH):
        for row in range(HEIGHT):
            groundCell = grid.ground[column][row]
            pygame.draw.rect(ground, groundCell.color, [CELLSIZE*column, CELLSIZE*row, CELLSIZE, CELLSIZE])


def drawCells(grid):
    for column in range(WIDTH):
        for row in range(HEIGHT):
            cell = grid.grid[column][row]
            if cell.color:
                pygame.draw.rect(screen, cell.color, [CELLSIZE*column, CELLSIZE*row, CELLSIZE, CELLSIZE])


def drawNums(grid):
    for column in range(WIDTH):
        for row in range(HEIGHT):
            cell = grid.grid[column][row]
            if cell.ID in (1,2):
                number_image = number_font.render(str(int(cell.dormant)), True, "black")
                screen.blit(number_image, (5+CELLSIZE*column, 3+CELLSIZE*row))


def createGUI():
    global gui_window, fps_input, fatalHunger_input, plantNV_input, reproduceCost_input, maxPlantsMult_input
    gui_window = pygame_gui.elements.UIWindow(manager=manager,
                                            rect=pygame.Rect((100, 100), (500, 500)),
                                            window_display_title="Settings")
    fps_label = pygame_gui.elements.UILabel(manager=manager,
                                            container=gui_window,
                                            relative_rect=pygame.Rect((10, 10), (50, 20)),
                                            text="FPS")
    fps_input = pygame_gui.elements.UITextEntryLine(manager=manager,
                                                       container=gui_window,
                                                       relative_rect=pygame.Rect((20, 30), (50, 25)),
                                                       initial_text=str(fps))
    fatalHunger_label = pygame_gui.elements.UILabel(manager=manager,
                                        container=gui_window,
                                        relative_rect=pygame.Rect((20, 60), (100, 20)),
                                        text="Fatal Hunger")
    fatalHunger_input = pygame_gui.elements.UITextEntryLine(manager=manager,
                                                       container=gui_window,
                                                       relative_rect=pygame.Rect((20, 80), (50, 25)),
                                                       initial_text=str(fatalHunger))
    plantNV_label = pygame_gui.elements.UILabel(manager=manager,
                                        container=gui_window,
                                        relative_rect=pygame.Rect((20, 110), (190, 20)),
                                        text="Plant Nutritional Value")
    plantNV_input = pygame_gui.elements.UITextEntryLine(manager=manager,
                                                       container=gui_window,
                                                       relative_rect=pygame.Rect((20, 130), (50, 25)),
                                                       initial_text=str(plantNutritionalValue))
    reproduceCost_label = pygame_gui.elements.UILabel(manager=manager,
                                        container=gui_window,
                                        relative_rect=pygame.Rect((20, 160), (140, 20)),
                                        text="Cost to Reproduce")
    reproduceCost_input = pygame_gui.elements.UITextEntryLine(manager=manager,
                                                       container=gui_window,
                                                       relative_rect=pygame.Rect((20, 180), (50, 25)),
                                                       initial_text=str(reproduceCost))
    maxPlantsMult_label = pygame_gui.elements.UILabel(manager=manager,
                                        container=gui_window,
                                        relative_rect=pygame.Rect((20, 210), (175, 20)),
                                        text="Max Plants Multiplier")
    maxPlantsMult_input = pygame_gui.elements.UITextEntryLine(manager=manager,
                                                       container=gui_window,
                                                       relative_rect=pygame.Rect((20, 230), (50, 25)),
                                                       initial_text=str(maxPlantsMult))
    fps_input.set_allowed_characters('numbers')
    fatalHunger_input.set_allowed_characters('numbers')
    plantNV_input.set_allowed_characters('numbers')
    reproduceCost_input.set_allowed_characters('numbers')
    maxPlantsMult_input.set_allowed_characters(['0','1','2','3','4','5','6','7','8','9','.'])


def drawFps():
    if dt:
        fps_image = fps_font.render(str(round(1/dt)), True, pygame.Color(0, 168, 45))
        screen.blit(fps_image, (5, 5))




grid = Grid(WIDTH, HEIGHT, CELLSIZE,
            fatalHunger=fatalHunger,
            plantNutritionalValue=plantNutritionalValue,
            reproduceCost=reproduceCost,
            maxPlantsMult=maxPlantsMult)

# draws the still surfaces
drawGround(grid)
# drawGrid()

# combines the still surfaces into one tuple
ground_blit = (ground, (0, 0), (0, 0, ground.get_size()[0], ground.get_size()[1]))
grid_blit = (gridSurface, (0, 0), (0, 0, gridSurface.get_size()[0], gridSurface.get_size()[1]))

xButtonPos = (SCREENWIDTH-xImage.get_size()[0]-10, 5)
settingsButtonPos = (SCREENWIDTH-settingsImage.get_size()[0]-xImage.get_size()[0]-20, 5)

x_blit = (xImage, xButtonPos)
settings_blit = (settingsImage, settingsButtonPos)
buttons_blit = (x_blit, settings_blit)

blit_sequence = (ground_blit, grid_blit)

createGUI()
gui_window.hide()

while running:
    pygame.event.pump()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if xButtonPos[0]+xImage.get_size()[0] > mouse[0] > xButtonPos[0] and xButtonPos[1]+xImage.get_size()[1] > mouse[1] > xButtonPos[1]:
                if gui_window.alive():
                    gui_window.kill()
                else:
                    running = False
            elif settingsButtonPos[0]+settingsImage.get_size()[0] > mouse[0] > settingsButtonPos[0] and settingsButtonPos[1]+settingsImage.get_size()[1] > mouse[1] > settingsButtonPos[1]:
                createGUI()

        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

    manager.update(dt)

    mouse = pygame.mouse.get_pos()
    # adds all the still surfaces to the screen
    screen.blits(blit_sequence)
    
    drawCells(grid)
    # drawNums(grid)
    drawFps()
    grid.updateCells()

    for button in buttons_blit:
        screen.blit(button[0], button[1])

    input = fps_input.get_text()
    if input != '':
        fps = int(input)
    if fps >= 0:
        dt = clock.tick(fps) / 1000

    input = fatalHunger_input.get_text()
    if input != '':
        fatalHunger = int(input)
    
    input = plantNV_input.get_text()
    if input != '':
        plantNutritionalValue = int(input)
    
    input = reproduceCost_input.get_text()
    if input != '':
        reproduceCost = int(input)
    
    input = maxPlantsMult_input.get_text()
    if input != '':
        try:
            input = float(input)
        except Exception as e:
            print(e)
            maxPlantsMult_input.set_text(str(maxPlantsMult))
        else:
            maxPlantsMult = input
    grid.setVariables(fatalHunger=fatalHunger, plantNutritionalValue=plantNutritionalValue, reproduceCost=reproduceCost, maxPlantsMult=maxPlantsMult)

    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()