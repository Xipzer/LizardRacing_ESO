# (ESO) Quest Automation: Lizard Racing 

This project consists of a Jupyter Notebook and a Python Program. The notebook 
is designed to allow you flexible customisation for the quest automation, as there 
are some parameters that need to be tweaked in order for the automation to execute 
correctly. The Python Program offers a more simple execution approach for once 
you've configured the automation to your system.

_DISCLAIMER: This software doesn't come with any liability or warranty. This 
automation may go against the Code of Conduct outlined by ZOS. Hence, you alone 
are responsible for your usage of this script and the implication(s) of its usage 
on your account._

## Overview

This automation interacts with the Lizard Racing NPC in Reaper's March. It fetches
the quest from the NPC, awaits the quests completion, detects whether the quest was 
successful or not and then repeats the quest.

The automation keeps track of the quest state through image recognition. These images
and their locations on your screen will be specific to your setup. The default display
coordinates and images assume a 1920x1080 display, with 100% windows scaling and the 
game running in full-screen.

Simulated organic movement has been implemented to reduce the possibility of 
detection - you'll need . Although, the Lizard Racing Quest is more abuse-able by a 
regular human than by this script. Overall, the odds of any negative repercussion 
are low/non-existent. You take the full responsibility, regardless.

## Config (Automation)

This software requires Python (Version 3.9), in order to execute. To avoid import 
issues, use the same version.

### Installation

Install Requirements:
```shell
pip install -r requirements.txt --no-index
```

### Quest Images
If your gaming configuration (monitor/game window) don't match the default 
configuration, described in the overview, you will need new screenshots and 
coordinates. Windows Snip Tool + Photoshop are ideal for this.

Using the provided screenshots as references, begin by taking fullscreen screenshots
of the monitor the game window resides on, where each of these images appear. 

We will need the isolated game elements as seen by the files provided. Either
use the selective snip tool to take these from within the game window, or take them
from the fullscreen screenshots directly. Ensure that the snippets are as closed to
the game elements as possible (try not to include unnecessary surroundings) - the
closer to just the element, the better.

If you're cutting the elements from the fullscreen screenshots, take note of the 
height, width, x and y coordinates from within Photoshop. If you're using snipped
elements, then perfectly line them up with the fullscreen screenshot and do the same.

Once complete, replace the snipped elements in the working directory with your new
ones. 

### Coordinates

_These are found in both the Jupyter Notebook (.ipynb) and Python Program (.py)._

Modify the following variables with your height, width, x and y coordinates.

For "E Talk" Prompt:
```
e_talk_region = (1062, 611, 93, 37)  # (x, y, width, height)
```
For "Goodbye" Dialogue:
```
goodbye_region = (1074, 555, 96, 32)  # (x, y, width, height)
```
For "What's Lizard Racing" Dialogue:
```
whats_lizard_racing_region = (1078, 560, 201, 24)  # (x, y, width, height)
```
For "Thanks" Dialogue:
```
thanks_region = (1072, 552, 84, 37)  # (x, y, width, height)
```
For "Try Again" Dialogue:
```
try_again_region = (1073, 555, 151, 34)  # (x, y, width, height)
```
For "Lizard Racing" Quest Name In Your Journal:
```
journal_region = (1029, 462, 125, 30)  # (x, y, width, height)
```

## Setup (In-Game)

Travel to the Lizard Racing NPC in Reaper's March. 

Once there, ensure the quest has not yet been collected - it must be in the 
"blue" icon state.

Position your player character sandwiched in the crevice between the large crucible
dish, facing towards the Lizard Racing NPC. 

Angle your camera so that it's looking diagonally at the floor - this will further
prevent the player character from moving too far from the NPC.

The race should now be to your left, the crucible to your right and the NPC directly
in front of you.

## Run

Once positioned, tab out of the game and execute the automation. It will wait for you
to re-focus the game window and dismiss the menu so it can see "E".

```shell
python .\quest_automation.py
```

###### ~Xipzer