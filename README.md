# Connect-4 Game (CS 7319 Final Project)

A fully-featured desktop Connect-4 game built in **Python** using **Tkinter**, supporting both two-player mode and AI mode powered by a Monte Carlo search algorithm.

> Final project for *CS 7319 - Software Architecture and Design*
> Final Project Group 10
- Mays Nael Abdel Rahman: CS 7319 | Off Campus |  SMU ID: 49711409
- Bohan Dong: CS 7319 | On Campus |  SMU ID: 49347343
- Ian Walton: CS 7319 | Off Campus |  SMU ID: 49351490

---

## Features

- Two-player mode
- AI opponent using Monte Carlo Tree Search
- Real-time move validation
- Automatic win/draw detection
- Restart and new game options
- Customizable board color and settings
- Implemented with **two architectural styles**:
  - Blackboard Architecture
  - Layered Architecture (final choice)

---

##  Architecture Overview

### Option 1: Blackboard Architecture
- Decouples components via a shared data space (blackboard)
- Allows parallel processing (e.g., UI, AI, win checker)
- Supports modularity and easy component reuse

### Option 2: Layered Architecture  *(Final Implementation)*
- Separates UI, logic, and data layers
- Promotes readability, maintainability, and testability
- Ideal for collaborative development and future expansion

---

##  Functional Requirements

- Players can choose to play against two players or against AI.
- Real-time location legitimacy judgment.
- Automatically recognize victory conditions or tie status.
- The game supports restarting or starting a new game.
- Provides Settings interface, can customize the board color and game appearance.
- Game progress and status are automatically tracked and updated in the background.
- AI opponents are based on Monte Carlo search algorithms with certain intelligent strategies.

###  Non-Functional Requirements

- Cross-platform compatibility: Runs on multiple desktop operating systems ( Windows, macOS).
- Fast response speed: the drop response and AI calculation are completed in an acceptable time.
- User friendly: The interface is interactive and intuitive, suitable for players of all ages.
- High stability: it will not crash or stall during long-term operation.
- Scalability: The architecture supports future extensions, such as adding new AI strategies and new chessboard modes.
- Testability: Each component can be tested and debugged individually

---

## Tech Stack

- Python 3.x
- Tkinter (GUI)
- Object-Oriented Programming
- Monte Carlo Search Algorithm
- UML & Software Architecture (Blackboard & Layered)


---

## Running the Implementations

### Install Dependencies

* tkinter
* numpy

### Blackboard

To run the Blackboard architecture Connect4 game:

  * cd to the project root directory
  * run `python unselected/Connect4App.py`

### Layered


To run the Layered architecture Connect4 game:

  * cd to the project root directory
  * run `python selected/main.py`
