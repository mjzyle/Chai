#!/usr/bin/python

import gameplay_models as models
import gameplay_controller as controller
import pandas as pd
import datetime as dt
import random
import threading
import math
import sys
import os
from copy import deepcopy


#game_start = int(sys.argv[1])
#game_end = int(sys.argv[2])

game_index = int(sys.argv[1])
timeout = int(sys.argv[2])

access_key = []
access_key.append(str(sys.argv[3]))
access_key.append(str(sys.argv[4]))

start = dt.datetime.now()
#controller.run_games(game_start, game_end)
controller.play_game(game_index, timeout, access_key)
end = dt.datetime.now()

print('Start: ' + str(start))
print('End: ' + str(end))