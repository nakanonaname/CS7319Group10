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
##  Architecture Comparison & Rationale

###  Blackboard Architecture

The **Blackboard architecture** organizes components around a shared data structure — the "blackboard" — where each component can read from and write to the shared state independently. This design promotes **parallelism**, **loose coupling**, and **modularity**, making it easier to develop and test components in isolation.

**Advantages:**
- Concurrency & Parallelism:  Enables components (e.g., AI, move checker, validator) to work independently and potentially in parallel — improving responsiveness.
- Reusability: Components like MonteCarlo, WinChecker, and MoveProcessor are loosely coupled and can be reused or swapped easily.
- Modularity: Promotes modular development — each component (UI, AI, logic) can be built and tested in isolation.
- Decoupling:  Components interact only via the blackboard — they are not directly connected, reducing interdependencies.
- Scalability: The system supports easy integration of new features (e.g., new AI, advanced analytics) without altering the core logic.
- Shared Data Access: Efficient mechanism for sharing game state across all modules (e.g., AI reads from the same source as the UI).

**Drawbacks:**
- High Dependency on Shared State: Components are dependent on the integrity of the blackboard — if the data is corrupted, all logic fails.
- Concurrency & Synchronization Complexity: Parallel access to shared data requires careful synchronization to avoid race conditions or inconsistencies.
- Single Point of Failure: The Blackboard is critical — if it crashes or becomes inconsistent, the entire game breaks.
- Maintenance & Evolution Difficulty: As the system grows, managing and evolving interactions around the blackboard can become error-prone and hard to trace.
- Performance Overhead: Synchronization and indirect communication may slow down system responsiveness in more complex implementations.
- Debugging & Testing Challenges: Dynamic, indirect interactions between components and the blackboard make it hard to isolate bugs and test individual flows.

![image](https://github.com/user-attachments/assets/9f0190c9-397e-4264-916b-3869a3363a35)

---

###  Layered Architecture  *(Final Choice)*

The **Layered architecture** divides the system into separate layers. Each layer depends only on the layer directly beneath it, which ensures a clear separation of concerns and better system maintainability.

**Advantages:**
- Readability: The simplicity and modularity of this architecture styles facilitates clear code that can be easily read and maintained over time.
- Extensibility: The clear division between layers and abstraction offered through well-defined interfaces makes the architecture easy to extend and modify. For example, the Monte Carlo agent could be replaced with no impact to the UI or Game layers. Similarly, the application could be easily extended to support mobile/tablet experience by modifying the UI layer would changing the underlying services.
- Separation of concerns: This architecture allows distributed teams, such as ours, to contribute effectively and in parallel. Team members were able to utilize their distinct strengths with particular technologies with confidence due to separation of concerns offered by the well defined interfaces and isolated layer components. 

**Drawbacks:**
- Duplication of code: Sometimes it may be necessary to cache a projection of the return values in the upstream layers. For example, the UI layer had to persist a representation of the game board to draw the tkinter widget. This approach could cause out of sync issues as the system scales and number of layers increase.
- Increased complexity for simple operations: Changes to the well defined interface require some additional boilerplate that may be tedious to scale and maintain. Changes to the MoveResult response DTO, for example, may require adjusting the UI layer to adjust to the change in interface. 
- Latency between layers: If messages are passed between multiple layers, any latency introduced downstream is additive to the entire request flow. For example, if the Monte Carlo agent is prohibitively slow, the user experience will degrade due to the synchronous nature of calls between the UI and Game Session layer.

![image](https://github.com/user-attachments/assets/04f9159f-a8ea-4f6b-86c7-1022d53ae863)

---

###  Final Selection Rationale

After evaluating both architectural styles, we selected the **Layered architecture** for our final implementation. Although the Blackboard architecture offers strong modularity and concurrent processing — which is ideal for AI-driven or event-heavy applications — the simplicity and clarity of the Layered model aligned better with our project goals.

Our rationale included:

- **Maintainability**: Easier for team members to understand and modify
- **Readability**: Code structure closely matches functional responsibilities
- **Scalability**: New features (e.g., different AIs or UIs) can be added cleanly
- **Project scope fit**: For a moderately complex game like Connect-4, the overhead of Blackboard didn’t justify the complexity

The Layered architecture helped us keep the system **organized**, **testable**, and **easy to extend** — all critical factors for delivering a quality final product within our timeline.

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

* `pip install tkinter`
* `pip install numpy`

### Blackboard

To run the Blackboard architecture Connect4 game:

  * cd to the project root directory
  * run `python Unselected/Connect4App.py`

### Layered

To run the Layered architecture Connect4 game:

  * cd to the project root directory
  * run `python Selected/main.py`
