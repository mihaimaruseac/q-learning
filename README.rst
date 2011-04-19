Reinforcement learning
======================

A. About
........

This is a homework for the Machine Learning Course that I am taking right now
at my University.

The homework simulates a robot in a rectangular grid learning to navigate
within a certain area on the the grid. The robot has only 4 sensors describing
his position as values for the distances between his position and the walls.
The sensors are limited, they can provide a maximum distance of D.

The robot most navigate in a trigonometric orientation in a small corridor
contained between d1 and d2 from the nearest wall. In order to learn this, it
should receive various rewards depending on his position.

The assignment is done in Python.

B. Usage
........

Run ``./ql`` to start the main part of the application. The GUI is pretty
simple to use.

The plot shows a red point for the 0 value and a green dot for the current
total reward that the robot has gained in the current simulation epoch.

Save plots if you want to compare the effect of the parameters or the
differences between SARSA and Q-learning or ε-greedy and softmax action
selection.

You can compare them by using::

	./ql.py cmp file1 file2 ...

where each ``file`` is a saved plot. This will output a simple table with all
data.

If you want to see a nice plot use the ``cmp.sh`` script::

	./cmp.sh out_file file1 file1_title file2 file2_title ...

C. Some implementation details
..............................

The robot and the world are separated in two different classes. The rewards are
given according to the sensor values.

At each position, the robot must choose between going forward or turning left
or right. Each selection is based on the rewards given until that point.

The rewards are given like this:
* -100 if closer than d1 or facing the exterior of the grid
* -50 if farther than d2
* a value between -15 and 5 depending on the desired orientation

