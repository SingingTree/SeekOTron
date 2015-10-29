# SeekOTron

SeekOTron is a game about programming a robot to collect loot.

## Requirements

- [Python](https://www.python.org/) - SeekOTron should work in both Python 3 and Python 2. It is primarily tested in 3, but if there are issues with either let me know.
- [Pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home) - You can install it using pip with the following command: `pip install pyglet`

## How to Play

This game is played by writing instructions for the robot in the `instructions.sk` file, you then load and run these commands in the game with the space bar. If your code was well formed the robot will hurry off to comply with your orders! The goal is to move the robot around the grid and to the treasure!

For the sake of grid coordinates, the bottom left space in the grid is x: 0 and y: 0, moving to the right increases the x value, moving up increases the y value.

### Writing Seek Lang

Seek lang(guage) is a simple programming language created for telling the robot in the game to move around. The language has only a few concepts to wrangle:

#### Movement Statements

Seek lang uses 4 different statements to tell the robot to move:

- `right`
- `left`
- `up`
- `down`

Each of these tells the robot to move a single space in the grid in the appropriate direction. The robot can't walk through walls, so if told to do so, it will ignore that instruction.

So if I wanted to tell the robot to move up twice then left I'd write a program like this:

```
up
up
left
```

Seek lang will let you write multiple statements on the same line using semicolons:

```
up; up; left
```

You can even have trailing semicolons if you like:

```
up; up; left;
```

Anywho! That's all there is to controlling the robot. You can solve puzzles with just this, and the game will randomly generate a puzzle each time you start it! Neat! But there's more tools you can use!

Note there a limit to how many commands that game will do before it stops, to stop you accidentally setting up tons of moves and having to wait ages for the friendly robot to follow them all through. Info on how to change this is in the Haxxing the Game section of this readme.

#### Arithmetic expressions

Seek lang supports simple arithmetic: addition, subtraction, multiplication, division. Seek lang only uses integers, so be aware some rounding may take place behind the scenes.

#### Variables

Seek lang has simple variables: all variables have to be integers (and by default are 0). A variable is made up of a name, which has to start with a letter, and then can be any number of letters and numbers, and a value -- an integer, a number. To assign a variable I'd do something like this:

```
myVar = 5
```

Which would set the value of the variable `myVar` to 5.

I could use arithmetic if I really wanted when setting `myVar`:

```
myVar = 2 + 3
```

Being able to set variables will useful with a couple of the other structures in Seek lang.

##### Special Variables

There are a few special variables in Seek lang. These variables come preloaded with certain special values. You can use them just like any other variable, but using the preloaded values in them can be useful for problem solving, these variables are:

- `robot_x` is the x coordinate of the robot
- `robot_y` is the y coordinate of the robot
- `loot_x` is the x coordinate of the loot
- `loot_y` is the y coordinate of the loot

The values of these variables will be set as you evaluate a script (hit space bar), and may be different by the the space bar is next pressed.

For example, if the robot is in the bottom left corner of the grid, it has an x coordinate of 0, and a y coordinate of 0. If I run a script, the value of `robot_x` will be 0 and `robot_y` will be 0. However if I also move the robot right twice in the script, the next time I run the script `robot_x` will be 2 (`robot_y` is still 0), because the robot is now 2 units to the right.

Note, setting the values of these special variables won't change the robot or loot locations in the game, so feel free to change them if you want. They'll be correctly reset by the game the next time a script is evaluated.

#### If Statements

Seek lang has support for if statements that check on boolean expressions. That all means I can do something like this:

```
if myVar > 1 do
    up
end
```

Which says 'if the value of myVar is greater than 1 move the robot up'. That's kinda neat. We can also have stuff happen if condition is not true:


```
if myVar > 1 do
    up
else
    down
end
```

Which says 'if the value of myVar is greater than 1 move the robot up, otherwise move it down'. Pretty rad huh?

You can combine the special variables noted above with if statements to make some pretty sweet scripts for the robot.

#### For Statements

The last piece of Seek lang is the for statement (for loop). Seek lang has a really simple for loop, you tell it you want to do something a certain number of times, like this:

```
for 5 do
    up
end
```

Which will issue the up statement to the robot 5 times. Which is pretty neat. However, we can get even more exciting:

```
for myVar do
    left
end
```

Now the robot is going to move left a certain number of times based on what the value of myVar is. Wowza!

Things can get even more exciting in that fors and ifs can be nested inside each other. It's time to cook with gas!

#### Go Go Go!

That's it! Write your code in the `instructions.sk`, the game will look there for them there. There's some default code in there as an example, but you can blow it away! So go and collect loot! Can you write a program that collects the loot without needing any changes, for any level?

### Keyboard Commands

- `q` quits the game
- `space bar` loads and runs the code from instructions.sk

### Special Keyboard Commands

- `d` prints to standard out simple game debug information
- `k` toggles the use of the arrow keys to move the robot (off by default)

### Haxxing the game

The seek_o_tron.py file contains the SeekOTron class, this class has a few special variables that control the game and can be tweaked:

- `BOARD_WIDTH` sets the width of the board to be generated
- `BOARD_HEIGHT` sets the height of the board to be generated
- `MAX_MOVES` sets the max number of moves that will be processed before stopping

Width and height need not be the same.

## Design Details

### Seek Interperator

Seek interperator code is based on Jay Conrad's tutorial [here](http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1)
