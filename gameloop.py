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


game_start = int(sys.argv[1])
game_end = int(sys.argv[2])

start = dt.datetime.now()
controller.run_games(game_start, game_end)
end = dt.datetime.now()

print('Start: ' + str(start))
print('End: ' + str(end))