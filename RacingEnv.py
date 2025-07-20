import gym
from gym import spaces
import numpy as np
import Racer
import TrackManager

class RacingEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.track = TrackManager.TrackManager()
        self.racer = Racer.Racer()
        
        # Action space: throttle and turn, both in [-1, 1]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        # [x velocty, angular velocity, curvature, 5x(spline x,y,h for t + 0.0-1)]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(18,), dtype=np.float32)

    def reset(self):
        self.track = TrackManager()
        self.racer = Racer()
        return self._get_obs()

    def step(self, action):
        throttle, turn = action
        self.racer.update(throttle, turn)
        self.track.update(self.racer.delta)

        distance = self.track.closestPoint.mag()
        progress = self.track.deltaT
        angle_diff = self._clip_angle(self.track.closestPoint.h - self.racer.pos.h)

        reward = 10.0*progress + 0.005*self.racer.relVel.x - 0.04*distance - 0.005*abs(angle_diff / np.pi)

        done = False
        if not self.racer.hasTraction or distance > 200:
            reward -= 50
            done = True

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        points = []
        n = 5
        start = 0
        end = 1
        for i in range(n):
            points.append(self.track.get_point(start + (end-start)*i/(n-1)).rotate(-self.racer.pos.h)) # The relative positions of the points on the track
            points[-1].h = self._clip_angle(points[-1].h)

        return np.array([
            self.racer.relVel.x,
            self.racer.relVel.h,
            self.track.curvature,
            points[0].x,
            points[0].y,
            points[0].h,
            points[1].x,
            points[1].y,
            points[1].h,
            points[2].x,
            points[2].y,
            points[2].h,
            points[3].x,
            points[3].y,
            points[3].h,
            points[4].x,
            points[4].y,
            points[4].h
        ], dtype=np.float32)
    
    def _clip_angle(self, a):
        return (a + np.pi)%(2*np.pi) - np.pi
    
    def _angle_difference(self, a, b):
        return self._clip_angle(a-b)
