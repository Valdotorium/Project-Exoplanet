import random
import pymunk

def Noise(obj, scale, variability, randomnoise):
        #main  terrain generator function
        print("----------------------------------------------------------------")
        x = 0
        #Height_Change = random.uniform(-obj.CFG_Terrain_Scale * scale, obj.CFG_Terrain_Scale * scale)
        Height_Change = 0
        Terrain_Direction = 0
        #should be renamed flatness, the higher, the flatter the terrain
        steepness = obj.Environment["Terrain"]["Flatness"]
        
        while x < len(obj.Terrain):
            if x > 70:
                r = random.uniform(0,100)
                if r < variability:
                    Terrain_Direction += random.randint(-1,1)
                #keeping Terrain_Direction within valid area (-3 to 3)
                if Terrain_Direction > 3:
                    Terrain_Direction = 3
                elif Terrain_Direction < -3:
                    Terrain_Direction = -3
                if randomnoise:
                    if Terrain_Direction > 0:
                        Height_Change += random.uniform(0, ((obj.CFG_Terrain_Scale * scale) / 50) * (Terrain_Direction / steepness))
                    elif Terrain_Direction < 0:
                        Height_Change += random.uniform(-((obj.CFG_Terrain_Scale * scale )/ 50) * (-Terrain_Direction / steepness), 0)
                else:
                    Height_Change +=( ((obj.CFG_Terrain_Scale * scale) / 80) * (Terrain_Direction / steepness) )
                    if Terrain_Direction > 0:
                        Height_Change += random.uniform(0, ((obj.CFG_Terrain_Scale * scale) / 600) * (Terrain_Direction / steepness))
                    elif Terrain_Direction < 0:
                        Height_Change += random.uniform(-((obj.CFG_Terrain_Scale * scale )/ 600) * (-Terrain_Direction / steepness), 0)
            Height_Change * scale

            obj.Terrain[x] += Height_Change
            obj.Terrain[x] = round(obj.Terrain[x])
            if obj.Terrain[x] < -50000:
                obj.Terrain[x] = -50000
                Height_Change = 0
                Terrain_Direction = 1
            if obj.Terrain[x] > 50000:
                obj.Terrain[x] = 50000
                Height_Change = 0
                Terrain_Direction = -1
            
            x += 1
            difficultyFactor = obj.Environment["Terrain"]["Difficulty"]
            difficultyFactor /= 10000
            steepness -= difficultyFactor + steepness * (difficultyFactor / 10)
            if steepness > 20:
                steepness = 20
            if steepness < 0.2:
                steepness = 0.2
            #1 screen = around 40 m
            if x == 4000:
               print("steepness at 280000px:",steepness)
            if x == 8000:
               print("steepness at 560000px:",steepness)
            if x == 12000:
               print("steepness at 740000px:",steepness)
        print("steepness at end:",steepness)
def setup(obj):
    obj.Terrain = []
    obj.TerrainAssets = []
    AssetChance = obj.Environment["Visuals"]["AssetFrequency"]
    AssetCount = len(obj.Environment["Visuals"]["Assets"])
    x = 0
    obj.Terrain.append(-90000)
    while x < 50000:
        r = random.uniform(0,100)
        if r < AssetChance and x > 40:
            if AssetCount != 0:
                obj.TerrainAssets.append(random.randint(0, AssetCount - 1))
            else:
                obj.TerrainAssets.append(None)
        else:
            obj.TerrainAssets.append(None)
        obj.Terrain.append(650)
        x += 1

def generate_chunk(obj):
    c = 1
    while c < obj.Environment["Terrain"]["Layers"] + 1:
        #scaling the variability and scale values by the upscalefactor by the terrain and generating noise woth the new values
        Noise(obj, round(obj.Environment["Terrain"]["StartScale"] / (obj.Environment["Terrain"]["UpscaleFactor"] * c)), obj.Environment["Terrain"]["StartVariability"] * (obj.Environment["Terrain"]["UpscaleFactor"] * c), obj.Environment["Terrain"]["RandomNoise"][c-1])
        c += 1
    print("total terrain length:", len(obj.Terrain) * obj.Environment["Terrain"]["Scale"])

    
def WritePolygonPositions(obj):
    
    #making tuples (x,y) out of the y positions of the future polygon vertices stored in obj.Terrain
    x = round((obj.X_Position + obj.Environment["Terrain"]["Scale"] * 8) /obj.Environment["Terrain"]["Scale"])
    endx = round((obj.X_Position + obj.dimensions[0]*2.2)/ obj.Environment["Terrain"]["Scale"])
    obj.EndItemOfRendering = endx
    PolygonPoints = []
    obj.StaticPolygon = []
    #Edge point
    if x < 0: 
        x = 0
    if endx < 2:
        endx = 2
    #the polygon points between x and enx get rendered
    while x < round(endx):
        Point = obj.Terrain[x]
        PolygonPoints.append(((x - 10) * round(obj.Environment["Terrain"]["Scale"]) - obj.X_Position, Point))
        obj.StaticPolygon.append(((x - 10) * round(obj.Environment["Terrain"]["Scale"]) , obj.Terrain[x]))
        x += 1
    #edge point
    obj.GroundRelief = PolygonPoints#provisorisch

    #print("THE GROUND POLYGON IS AT:", PolygonPoints)
    #print(f"drawing poly from terrain item {startx} to terrain item {x}")
    obj.MinimapPolygon = []
    x = round((obj.X_Position - obj.Environment["Terrain"]["Scale"] * 8) /obj.Environment["Terrain"]["Scale"])
    endx = round((obj.X_Position + obj.dimensions[0]*25)/ obj.Environment["Terrain"]["Scale"])
    PolygonPoints = []
    PolygonAssets = []
    #Edge point
    if x < 0: 
        x = 0
    if endx < 2:
        endx = 2
    #the polygon points between x and enx get rendered
    while x < round(endx) and endx < len(obj.Terrain):
        Point = obj.Terrain[x]
        Asset = obj.TerrainAssets[x]
        PolygonPoints.append(((x - 10) * round(obj.Environment["Terrain"]["Scale"]) - obj.X_Position, Point))
        PolygonAssets.append(Asset)
        #PolygonAssets format: [None, None, [AssetData], None...]
        x += 1
    obj.MinimapPolygon = PolygonPoints
    obj.PolygonAssets = PolygonAssets