# File: FileEngine.py
# Author: Reticulum Team
# Date: 6-7-2018 (last edit)
# Description: This is the file where the FileEngine module is defined.
#              This module contains all code that reads and writes to and
#              from the program's data files

from RoomClass import Room
from ItemClass import Item
import json
import time
import pickle

# define the exact file name and path to where the room data is held
class _RoomFileNames:
    _room_names = ["holdingChamber.json"
                   ,"loadingDock.json"
                   ,"navControlRoom.json"
                   ,"stationControlRoom.json"
                   ,"plantLab.json"
                   ,"energyGenPlant.json"
                   ,"crewSleepingQuarters.json"
                   ,"VRChamber.json"
                   ,"escapePod.json"
                   ,"maintenanceRoom.json"
                   ,"busyHallway.json"
                   ,"EVAPrepChamber.json"
                   ,"spaceNearEscapePod.json"
                   ,"spaceNearEVAChamber.json"
                   ,"messHall.json"
                   ,"space.json"
                   ]

    _room_files_directory = "../room_data/"

# define path and filenames for saved games
class _GameFileNames:
    _game_files_directory = "../saved_games/"
    _saved_game_filename = "game.dat"

class _GameTextFileNames:
    _text_files_directory = "./"
    _text_files_filename = "gameText.json"


# saveGame -> saves current state to file
# loadGame -> loads saved state and returns game back to caller
class GameSaver:
    # use pickle module
    def saveGame(self, game):
        f = open(_GameFileNames._game_files_directory
                 + _GameFileNames._saved_game_filename,
                 "wb")

        f.write(pickle.dumps(game))
        f.close()


    # read from encoded file containing the state of a game when
    # it was saved. Set the data fields of the passed in Game object
    # to the values contained in the data file
    def loadGame(self, game):
        try:
            f = open(_GameFileNames._game_files_directory
                     + _GameFileNames._saved_game_filename,
                     "rb")
        except OSError:
            print("No Saved Game File To Load")
            return

        game = pickle.loads(f.read())
        f.close()
        return game

# return a key-value pair dict from gameText file, use for any additional game text
class TextReader:
    def getTextFromFiles(self):
        textDict = {}
        f = open(_GameTextFileNames._text_files_directory + _GameTextFileNames._text_files_filename, "r")
        textDict = json.loads(f.read())


        for keys in textDict:
            textString = ""
            for s in textDict[keys]:
                textString = textString + s + '\n'
            textDict[keys] = textString

        return textDict


# FileReader has one method 'getRoomsFromFiles' which will return
# a dictionary of Room objects with each key being the full name of the Room.
# This class will search for Room files based on the parameters defined in the
# internal class _RoomFileNames. Any change made to the names and or directory
# structure of the Room data files must be reflected in the _RoomFileNames class
class FileReader:
    def getRoomsFromFiles(self):
        rooms_dict = {}
        for fname in _RoomFileNames._room_names:
            f = open(_RoomFileNames._room_files_directory + fname, "r")
            pyDict = json.loads(f.read())

            # create a new Item for each item in inventory_list
            inventory_list = {}
            for i in range(0, len(pyDict["inventory_list"])):
                key =(pyDict["inventory_list"][i]['name'])
                #print("key:" + key)
                inventory_list[key] = (Item(pyDict["inventory_list"][i]["name"], pyDict["inventory_list"][i]["description"],
                                            pyDict["inventory_list"][i]["room_name"], pyDict["inventory_list"][i]["use_desc"],
                                            pyDict["inventory_list"][i]["room_desc"], pyDict["inventory_list"][i]["exit"]))
                #print(inventory_list[key]._room_name)
                #print(inventory_list[key].keys())
            # create the Room object
            newRoom = Room(pyDict["room_name"],
                           pyDict["long_description"],
                           pyDict["short_description"],
                           pyDict["which_short"],
                           inventory_list,
                           pyDict["exit_names"],
                           pyDict["exit_locks"],
                           pyDict["feature1_keywords"],
                           pyDict["feature2_keywords"],
                           pyDict["examinable_objects"])
            #print(newRoom._inventory_list["key"].get_description())
            # add to dict to return
            rooms_dict[newRoom.get_name()] = newRoom
            f.close()

        return rooms_dict
