import random
import copy
from perlin_noise import PerlinNoise
from Creature import *
from Plant import *
from Obstruction import *

class Grid:

    def __init__(self, width, height, cellsize=20, fatalHunger=1000, plantNutritionalValue=500, reproduceCost=800, maxPlantsMult=0.4):
        self.ground = []
        self.grid = []
        self.water = []
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.fatalHunger = fatalHunger
        self.plantNutritionalValue = plantNutritionalValue
        self.reproduceCost = reproduceCost
        self.maxPlants = self.width*self.height*maxPlantsMult

        self.groundNoise = PerlinNoise(octaves=8/self.cellsize*20, seed=random.getrandbits(8))
        self.waterNoise = PerlinNoise(octaves=2/self.cellsize*20, seed=random.getrandbits(8))

        for column in range(width):
            x = []
            for row in range(height):
                
                rgb_value = self.generateGround(column, row, 0.19)

                x.append(Cell(color = pygame.Color(rgb_value)))
            self.ground.append(x)
        #fill grid with random cells
        for column in range(width):
            x = []
            for row in range(height):
                water = self.generateWater(column, row, 1.5)
                randomNum = random.randint(0, 1000)
                if water:
                    randomB = random.randint(138, 158)
                    x.append(Obstruction(color = pygame.Color(10, 97, randomB)))
                elif randomNum > 977 and randomNum <= 980:
                    x.append(Creature())
                elif randomNum > 990:
                    x.append(Plant())
                else:
                    x.append(Cell())
            self.grid.append(x)

    # called to change the variables to what the gui has (every frame cuz I don't know how else)
    def setVariables(self, fatalHunger=1000, plantNutritionalValue=500, reproduceCost=800, maxPlantsMult=0.4):
        self.fatalHunger = fatalHunger
        self.plantNutritionalValue = plantNutritionalValue
        self.reproduceCost = reproduceCost
        self.maxPlants = self.width*self.height*maxPlantsMult


    def generateGround(self, column , row, roughness):
        randomColor = self.groundNoise([column/self.width, row/self.height])*0.707

        # rounds noise valie to neares multiple of roughness
        randomColor = round(randomColor/ roughness) * roughness

        min_val = -1
        max_val = 1
        start_color = (145, 99, 58)
        end_color = (84, 45, 10)

        # interpolate start and end according to randomColor
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ((randomColor - min_val) / (max_val - min_val)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ((randomColor - min_val) / (max_val - min_val)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ((randomColor - min_val) / (max_val - min_val))) 
        rgb_value = (r, g, b)

        return rgb_value


    def generateWater(self, column , row, scale):
        randomWater = self.waterNoise([column/self.width*scale, row/self.height*scale])*0.707
        if randomWater < -0.1:
            return True
        else:    
            return False


    def isOutOfRange(self, x, y) -> bool:
        return (x < 0 or x >= len(self.grid) or y < 0  or y >= len(self.grid[0]))


    def getNeighbours(self, x, y) -> int:
        neighbours = 0

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 or j == 0:
                    if not (i == 0 and j == 0):
                        # don't check out of range
                        if self.isOutOfRange(x+i, y+j): # counts out of range as occupied cells
                            neighbours += 1
                        elif self.grid[x+i][y+j].ID != 0:
                            neighbours += 1
        return neighbours


    def getNeighboursByType(self, x, y, IDs) -> int:
        neighbours = 0

        if not isinstance(IDs, list):
            IDs = [IDs]  # Convert to list if a single ID is provided

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 or j == 0:
                    if not (i == 0 and j == 0):
                        if self.isOutOfRange(x+i, y+j):
                            neighbours += 1
                            continue
                        if self.grid[x+i][y+j].ID in IDs:
                            neighbours += 1
        return neighbours


    def getNeighboursWithType(self, x, y) -> dict:
        neighbours = {}

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 or j == 0:
                    if not (i == 0 and j == 0):
                        if self.isOutOfRange(x+i, y+j):
                            neighbours[(i, j)] = None
                        else:
                            neighbours[(i, j)] = self.grid[x+i][y+j].ID
        return neighbours


    def awakenNeighbours(self, x, y):
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 or j == 0:
                    if not (i == 0 and j == 0):
                        if self.isOutOfRange(x+i, y+j):
                            continue
                        self.grid[x+i][y+j].awaken()


    def killCell(self, x, y):
        if self.grid[x][y].ID == 2:
            Plant.plantAmount -= 1
        self.grid[x][y] = Cell()


    def moveCell(self, x, y, xDirection, yDirection):
        oldX = x
        oldY = y
        x = x + xDirection
        y = y + yDirection

        # kills cell to occupy
        if self.grid[x][y].ID != 0:
            self.killCell(x, y)

        # copies the old cell to the new place
        self.grid[x][y] = self.grid[oldX][oldY]
        # empties the old cell
        self.grid[oldX][oldY] = Cell()

        return True


    def reproduceCell(self, x, y) -> bool:

        ID = self.grid[x][y].ID

        neighbours = self.getNeighboursWithType(x, y)
        availableNeighbours = []
        for neighboursPos, neighbourID in neighbours.items():
            match ID:
                case 1:
                    # IF is creature reproduce to empty cells and plants
                    if neighbourID==0 or neighbourID==2:
                        availableNeighbours.append(neighboursPos)
                case 2:
                    # IF is plant reproduce to empty cells
                    if neighbourID==0:
                        availableNeighbours.append(neighboursPos)

        newPos = random.choice(availableNeighbours)
        newX = newPos[0]
        newY = newPos[1]

        oldX = x
        oldY = y
        x = x + newX
        y = y + newY

        # kills cell to occupy
        if self.grid[x][y].ID != 0:
            self.killCell(x, y)

        # copies the old cell to the new place
        self.grid[x][y] = copy.copy(self.grid[oldX][oldY])

        # resets hunger and age
        self.grid[x][y].hunger = 0
        self.grid[x][y].age = 0
        self.grid[x][y].sexTimeLeft = 0

        return True


    def updateCreature(self, cell, column, row) -> bool:

        if cell.hunger >= self.fatalHunger: # if hunger too high die
            self.killCell(column, row)
            return True
        
        if not cell.update(): # skip cell if cell timer is not 0
            return None
        if self.getNeighboursByType(column, row, [-1, 1]) >= 4:
            return False

        # IF is hungry and has plant close eats them
        neighbours = self.getNeighboursWithType(column, row)
        for pos, ID in neighbours.items():
            if ID == 2 and cell.hunger >= 0:
                self.killCell(column+pos[0], row+pos[1])    # kill the plant
                cell.hunger -= self.plantNutritionalValue   # lower hunger
                return True

        # IF belly full
        # AND maturity reached
        # THEN try to reproduce and IF succeded gain hunger
        if (cell.hunger < 0) and (cell.age >= 300):
            if cell.sexTimeLeft <= 0:
                if self.reproduceCell(column, row):
                    cell.sexTimeLeft = cell.updateRate*20
                    cell.hunger += self.reproduceCost
                    return True
        
        neighbours = self.getNeighboursWithType(column, row)
        availableNeighbours = []
        for neighboursPos, neighbourID in neighbours.items():
            match cell.ID:
                case 1:
                    # IF is creature move to empty cells and plants
                    if neighbourID==0 or neighbourID==2:
                        availableNeighbours.append(neighboursPos)

        newPos = random.choice(availableNeighbours)

        return self.moveCell(column, row, newPos[0], newPos[1])


    def updatePlant(self, cell, column, row) -> bool:
        if not cell.update(): # skip cell if cell timer is not 0
            return None

        if self.getNeighbours(column, row) >= 4:
            return False

        # IF total plants more than 2.5*grid space then return (None because so it doesn't count towards failedUpdateAttempts)
        if Plant.plantAmount > self.maxPlants:
            return None

        Plant.plantAmount += 1
        return self.reproduceCell(column, row)


    def updateCells(self):
        updatedCells = []
        widthRange = range(self.width)
        heightRange = range(self.height)
        for column in widthRange:
            for row in heightRange:
                cell = self.grid[column][row]

                # if cell is empty (0) don't update no-no-nothing
                if cell.ID in (-1, 0):
                    continue

                # avoid updating the same cell twise
                if cell in updatedCells:
                    continue

                updatedCells.append(self.grid[column][row])
                cell.age += 1

                match cell.ID:
                    case 1: # creature
                        updated = self.updateCreature(cell, column, row)
                    case 2: # plant
                        updated = self.updatePlant(cell, column, row)
                if updated == False:
                    cell.failedUpdateAttempts += 1
                elif updated:
                    self.awakenNeighbours(column, row)