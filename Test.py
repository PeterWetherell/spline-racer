import Racer
import TrackManager
import numpy as np
import random
import RacingEnv
from stable_baselines3 import PPO

env = RacingEnv.RacingEnv()
model = PPO.load("./PPO/racer_model_v13")

num_completed = 0
num_offtrack = 0
num_spinout = 0

dist_traveled = 0
path_length = 0

for i in range(1000):    
    track = TrackManager.TrackManager()
    racer = Racer.Racer()

    throttle = 0
    turn = 0
    
    running = True

    num_splines = random.randint(5, 15)

    while running:
        obs = env.get_observation_from_state(racer, track, throttle, turn)
        action, _ = model.predict(obs)
        throttle = float(action[0])
        turn = float(action[1])
        racer.update(throttle, turn)
        track.update(racer.delta)
        if track.num_splines >= num_splines:
            num_completed += 1
            dist_traveled += track.dist_traveled
            path_length += track.path_length
            running = False
        elif not racer.has_traction:
            num_spinout += 1
            dist_traveled += track.dist_traveled
            path_length += track.path_length
            running = False
        elif track.kill or track.closest_point.mag() > RacingEnv.maxDist:
            num_offtrack += 1
            dist_traveled += track.dist_traveled
            path_length += track.path_length
            running = False

    if (i+1) % 50 == 0:
        print(f"{i+1} tracks: {100*num_completed/(num_spinout + num_offtrack + num_completed):5.2f}% success and {100*dist_traveled/path_length:5.2f}% efficiency")
    
print(num_completed)
print(num_spinout)
print(num_offtrack)
print(dist_traveled)
print(path_length)