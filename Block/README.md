# Intro To Psychology Course Project - 
# Automaticity Ranking using Stroop's Effect for Direction, Movement and Sound Stimuli

## Team Name: PsYcho

### About
Humans have variable affinity to different kinds of stimuli and on exposure to those, a response is automatically generated. However, it has long been of interest to the psychology fraternity as to how automatic and to what stimulus is the response generated when more than one stimulus is present. \
The research community has attempted to conduct studies in the past to explore the automaticity of humans to different situations, with some delving deep into unveiling the cognitive play that goes on behind the scenes. \
With this project we aim to contribute our bit to the community by trying to rank the automaticity of responses generated. For our experiment, we have chosen movement, direction and sound as the stimuli which we present to the participant in various combinations. 

We hypothesize that automaticity of reponse to stimuli is rankable using Stroop's Effect. 

### Structure of the Experiment
We have three stimuli - Movement, Direction and Sound. In accordance to the Stroop's Effect set up, we devise three tasks - Neutral, Congruent and Conflict. Furthermore, since the experiment deals with ranking of automaticity of responses, we have set up three cases: Movement-Direction, Direction-Sound, Sound-Movement. 

(*Details can be found in the `docs` folder.*)

### Designing the Experiment
We have made a game with `python` using `pygame` library. 
The code has been structured to be as modular as possibe to make it easy for the reader or the user to understand and make changes to it for self-use as deemed fit. Following is the folder structure:
```
├── README.md
├── beep_f500_dur1_amp10000.wav
├── beep_f500_dur2_amp10000.wav
├── data
│   ├── 1.csv
│   ├── 2.csv
│   └── x.csv
├── data.csv
├── main.py
├── scenes.py
├── tasks.py
├── user_ids.txt
└── utils.py
```

To run the experiment run the following command:
```
python3 main.py
```

Description of files:
1. `utils.py` consists of the helper functions that contain classes for creating scene (the game window), items to be displayed during a task, a timer to show during a scene and two classes that help with presenting text on the window and initiating pauses between scenes.
2. `tasks.py` consists of the classes for each of the **tasks** (from Neutral, Conflict and Congruent) along with other helper functions used to achieve the render a desired output scene.
3. `scenes.py` is a file that consists of the classes for **individual cases** (movement, direction and sound), each with their own set of helper functions.
4. `main.py` contains the main driver code combining classes and functions from the above files to ensure a smooth working of the game. Nothing is hard-coded thereby putting all control with the user - to change and try different combinations of parameters. 
5. `data` folder will contain the response of each participant stored as `x.csv` (`x` is the **UserID** of the participant).
6. `user_ids.txt` contains the UserIDs of the participants as and when they register for the experiment. The IDs are read from here while creating the response files.
7. `data.csv` is a temporary file that gets created while the participant is doing the experiment. It gets overwritten everytime a new participant starts the experiment.
8. `analysis.py` contains the functionns for getting the participant scores. The functions provide the user with a choice to either get per-participant scores or analyse group statistics.

Note that `requirements.txt` contains the required libraries and their versions compatible with the current set up.


(*Note: This repo is under construction and is therefore is subject to changes in the future.*)



