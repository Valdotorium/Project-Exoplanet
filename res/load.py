import pygame
import time
import os
from .fw import fw as utils
import json
import pyglet.media
def respond(obj):
    """This script is responsible for loading the games assets, such as images and parts. it will load everything in the folder it finds.
    WARNING: In py2app, the assets folder must be included TWICE in several locations of the app, see py2app.txt"""
    print("ive loaded from the source package!")
    #getting the window size
    obj.dimensions = utils.getScreenSize()
    print("LOG: screen dimensions are:", obj.dimensions)
    if obj.S_Fitscreen:
        if obj.S_Fullscreen:
            #makes it fullscreen
            obj.screen = pygame.display.set_mode(obj.dimensions[0], pygame.FULLSCREEN)
        else:
            #makes it windowed, but with the size of the full screen
            obj.screen = pygame.display.set_mode(obj.dimensions[0])
        obj.screen.fill((100, 100, 100))
        pygame.display.set_caption("Project Exoplanet") 
    else:
        #smol version
        screensize = obj.CFG_Default_Screen_Size
        obj.screen = pygame.display.set_mode(screensize)
        obj.screen.fill((100, 100, 100))
        obj.dimensions[0] = screensize
        pygame.display.set_caption("Project Exoplanet")
    obj.dimensions = obj.dimensions[0]
    utils.displayTextCenter(obj,"finding files")
    #locating the game assets

    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    gamefiles = os.listdir(CurrentPath)

    print("LOG: found gamefiles in:", gamefiles)
    utils.displayTextCenter(obj,"checking for necessary files")
    if "assets" in gamefiles:
        print("file loader path is: ", CurrentPath)
        utils.displayTextCenter(obj,"found assets folder")
        #loading images from the images folder
        if "images" in os.listdir(CurrentPath+"/assets"):
            imagefiles = os.listdir(CurrentPath+"/assets/images")
            textures = {}
            #loading all the images into the game
            for image in imagefiles:
                if image != ".DS_Store":
                    print("loaded image: ", image)
                    loadedimage = pygame.image.load(CurrentPath+"/assets/images/"+image)

                    utils.clear(obj.screen)
                    #center the text

                    utils.displayTextCenter(obj,f"loaded image {image}")
                    textures[image] = loadedimage
            print("LOG: loaded all images into:", textures)
            obj.textures = textures

            #loading all the parts into the game
            partfiles = os.listdir(CurrentPath+"/assets/parts")
            for part in partfiles:
                loadedpart = json.load(open(CurrentPath+"/assets/parts/"+part))
                utils.DecodePart(loadedpart, obj)
                utils.clear(obj.screen)
                utils.displayTextCenter(obj,f"loaded part {part}")
            print("all parts loaded to game: ", obj.partdict)
            print("all parts loaded to shop: ", obj.shopdict)
            try:
                EnvironmentFile = open(CurrentPath+"/assets/environment.json")
                obj.Environment = json.load(EnvironmentFile)
                print(f"loaded environment: ", obj.Environment)
            except:
                raise ImportError("Environment File not found")
            soundfiles = os.listdir(CurrentPath+"/assets/sounds")
            sounds = {}
            #loading all the sounds into the game
            for sound in soundfiles:
                loadedsound = pyglet.media.StaticSource(pyglet.media.load(CurrentPath+"/assets/sounds/"+sound))

                utils.clear(obj.screen)
                #center the text

                utils.displayTextCenter(obj,f"loaded sound {sound}")
                sounds[sound] = loadedsound
            print("LOG: loaded all sounds into:", sounds)
            obj.sounds = sounds
            biomefiles = os.listdir(CurrentPath+"/assets/biomes")
            biomes = {}
            #loading all the biomes into the game
            for biome in biomefiles:
                loadedbiome = json.load(open(CurrentPath+"/assets/biomes/"+biome))

                utils.clear(obj.screen)
                utils.displayTextCenter(obj,f"loaded sound {sound}")
                biomes[loadedbiome["Name"]] = loadedbiome
            print("LOG: loaded all biomes into:", biomes)
            obj.biomes = biomes
        else:
            exit
    else:
        utils.displayTextCenter(obj,"ERROR: no textures folder found")
        print("ERRNO_02: No textures or assets folder found in " + CurrentPath)
        exit
    if obj.CFG_Reload_Latest_Vehicle:
        print("loading latest vehicle")
        try:
            VehicleFile = open(CurrentPath+"/assets/saves/latest_vehicle.json")
            obj.Vehicle = json.load(VehicleFile)
            print(f"loaded vehicle: ", obj.Vehicle)
            VehicleJointFile = open(CurrentPath+"/assets/saves/latest_vehicle_joints.json")
            obj.VehicleJoints = json.load(VehicleJointFile)
            print(f"loaded vehicle joints: ", obj.VehicleJoints)
            VehicleHitboxFile = open(CurrentPath+"/assets/saves/latest_vehicle_hitboxes.json")
            obj.VehicleHitboxes = json.load(VehicleHitboxFile)
            print(f"loaded vehicle hitboxes: ", obj.VehicleHitboxes)
        except:
            raise ImportError("Vehicle File not found")
    #TODO: #8 
    #implement scalability by scaling all size values of parts by scaleX before starting in building mode

    utils.displayTextCenter(obj, "All Done!")