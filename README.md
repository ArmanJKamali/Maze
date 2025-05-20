# Maze Solver with Pathfinding Algorithms

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

A Python application that solves mazes with obstacles and collectible numbers using combinatorial optimization and pathfinding algorithms.

## Features

- **Hybrid Solver** combining:
  - Brute-force search with bitmasking
  - Breadth-First Search (BFS) pathfinding
  - Greedy distance heuristics
- **Customizable Mazes**:
  - Adjustable start/end positions
  - Tree obstacles
  - Collectible numbered items
- **Visualization**:
  - Path highlighting
  - Step-by-step solving

## Algorithms Implemented

| Algorithm | Purpose | Location |
|-----------|---------|----------|
| Brute-Force + Bitmasking | Tests all number collection combinations | `bruteforce()` |
| Breadth-First Search (BFS) | Finds shortest path segments | `bfs()` |
| Greedy Sorting | Orders numbers by proximity | `check_state()` |
| Parent Pointer Reconstruction | Backtracks optimal path | `bfs()` |

## Requirements

- Python 3.8+
- CustomTkinter
- ttkBootstrap

## Installation

```bash
git clone https://github.com/yourusername/maze-solver.git
cd maze-solver
pip install -r requirements.txt
