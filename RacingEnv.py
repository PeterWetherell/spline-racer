import gym
from gym import spaces
import numpy as np
import Racer
import TrackManager

n = 5
start = 0
end = 1

class RacingEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.track = TrackManager.TrackManager()
        self.racer = Racer.Racer()
        
        # Action space: throttle and turn, both in [-1, 1]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        # [x velocty, angular velocity, curvature, 5x(spline x,y,h for t + 0.0-1)]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(3+n*3,), dtype=np.float32)

    def reset(self):
        self.track = TrackManager.TrackManager()
        self.racer = Racer.Racer()
        return self._get_obs()

    def step(self, action):
        throttle, turn = action
        self.racer.update(throttle, turn)
        self.track.update(self.racer.delta)

        distance = max(self.track.closestPoint.mag()-80,0)
        progress = self.track.deltaT * self.track.getVel()
        angle_diff = self._clip_angle(self.track.closestPoint.h - self.racer.pos.h)

        self.prev_action = getattr(self, 'prev_action', np.array([0.0, 0.0]))
        jerk_penalty = np.sum(np.square(action - self.prev_action))
        self.prev_action = action.copy()

        reward = 15.0*progress + 3.0*self.racer.relVel.x - 0.04*distance - 0.004*abs(angle_diff / np.pi) - 0.05*jerk_penalty

        done = False
        if distance > 250:
            reward -= 20
            done = True
        elif not self.racer.hasTraction:
            reward -= 10
            done = True

        return self._get_obs(), reward, done, {}
    
    def get_observation_from_state(self, racer, track):
        points = [
            track.get_point(start + (end - start) * i / (n - 1)).rotate(-racer.pos.h)
            for i in range(n)
        ]
        point_features = [np.array([p.x, p.y, self._clip_angle(p.h)]) for p in points]
        return np.concatenate([
            np.array([racer.relVel.x, racer.relVel.h, track.curvature], dtype=np.float32),
            *point_features
        ]).astype(np.float32)

    def _get_obs(self):
        points = [
            self.track.get_point(start + (end - start) * i / (n - 1)).rotate(-self.racer.pos.h)
            for i in range(n)
        ]
        point_features = [np.array([p.x, p.y, self._clip_angle(p.h)]) for p in points]
        return np.concatenate([
            np.array([self.racer.relVel.x, self.racer.relVel.h, self.track.curvature], dtype=np.float32),
            *point_features
        ]).astype(np.float32)
    
    def _clip_angle(self, a):
        return (a + np.pi)%(2*np.pi) - np.pi
    
    def _angle_difference(self, a, b):
        return self._clip_angle(a-b)
