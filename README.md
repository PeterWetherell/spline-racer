# Spline Racer

Spline Racer is a 2D racing simulation environment built around cubic spline path generation. It features both a player-controlled mode and an AI agent trained to follow randomly generated spline-based race tracks.

This project is designed to explore reinforcement learning and control in a continuous environment, combining physics-based vehicle dynamics with procedurally generated tracks.

## Features

- AI agent trained to follow spline-generated race tracks
- Player-controlled mode for manual testing and debugging
- Procedural cubic spline track generation
- Automated performance testing over thousands of courses
- Visualizations of both AI and human driving

## Getting Started

### 1. **Play it yourself**  
Test the physics engine, camera system, and spline logic interactively:

```bash
python PlayerControlledRaceTest.py
```

Use this to verify game mechanics and explore generated tracks manually.

### 2. **Train the AI** 

Train the AI agent to follow the generated spline track:

```bash
python Train.py
```

Training uses reinforcement learning with PPO to teach the agent how to drive on any random spline track layout.

### 3. **Visualize the AI** 

Run the AI in a visual environment to see how it performs:

```bash
python AIControlledRaceTest.py
```

This will render the simulation as the AI navigates a track, allowing you to evaluate its driving behavior visually.

### 4. **Benchmark Performance**

To test how well the model generalizes, evaluate it over 1000 randomly generated spline tracks:

```bash
python Test.py
```

This provides statistics on completion rate, lap time, crash frequency, and more (depending on how you’ve implemented evaluation).

## Dependencies

This project relies on

- pygame
- numpy
- stable_baselines3
- gym
