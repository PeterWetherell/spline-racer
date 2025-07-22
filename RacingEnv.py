import gym
from gym import spaces
import numpy as np
import Racer
import TrackManager

n = 7
start = 0
end = 0.75
maxDist = 250
targetDist = 120

class RacingEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.track = TrackManager.TrackManager()
        self.racer = Racer.Racer()
        
        # Action space: throttle and turn, both in [-1, 1]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        # [prev throttle, prev turn, x velocty, angular velocity, curvature, 5x(spline x,y,h for t + 0.0-1)]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5+n*3,), dtype=np.float32)

    def reset(self):
        self.track = TrackManager.TrackManager()
        self.racer = Racer.Racer()
        return self._get_obs()

    def step(self, action):
        throttle, turn = action
        self.racer.update(throttle, turn)
        self.track.update(self.racer.delta)

        distance = self.track.closestPoint.mag()
        distance_penalty = 0.002*max(targetDist - distance,0)/targetDist - 0.03*max(distance-targetDist,0)/(maxDist - targetDist)
        angle_diff_penalty = -0.04*abs(self._clip_angle(self.track.closestPoint.h - self.racer.pos.h)/np.pi)
        progress_reward = 14.0*self.track.deltaT * self.track.getVel()
        speed_reward = abs(self.racer.relVel.x)/100.0 + 2.0*((self.racer.relVel.x)/200.0)**2
        sliding_penalty = -0.04 * abs(self.racer.relVel.y)

        self.prev_action = getattr(self, 'prev_action', np.array([0.0, 0.0]))
        jerk_penalty = -15*np.sum(np.square(action - self.prev_action))
        self.prev_action = action.copy()

        reward = progress_reward + speed_reward + angle_diff_penalty + distance_penalty + jerk_penalty + sliding_penalty

        done = False
        if self.track.kill:
            reward -= 100
            done = True
        elif distance > 250:
            reward -= 10
            done = True
        elif not self.racer.hasTraction:
            reward -= 8
            done = True

        return self._get_obs(), reward, done, {}
    
    def get_observation_from_state(self, racer, track, throttle, turn):
        points = [
            track.get_point(start + (end - start) * i / (n - 1)).rotate(-racer.pos.h)
            for i in range(n)
        ]
        point_features = [np.array([p.x, p.y, self._clip_angle(p.h)]) for p in points]
        return np.concatenate([
            np.array([throttle, turn, racer.relVel.x, racer.relVel.h, track.curvature], dtype=np.float32),
            *point_features
        ]).astype(np.float32)

    def _get_obs(self):
        points = [
            self.track.get_point(start + (end - start) * i / (n - 1)).rotate(-self.racer.pos.h)
            for i in range(n)
        ]
        point_features = [np.array([p.x, p.y, self._clip_angle(p.h)]) for p in points]
        self.prev_action = getattr(self, 'prev_action', np.array([0.0, 0.0]))
        return np.concatenate([
            np.array([self.prev_action[0], self.prev_action[1], self.racer.relVel.x, self.racer.relVel.h, self.track.curvature], dtype=np.float32),
            *point_features
        ]).astype(np.float32)
    
    def _clip_angle(self, a):
        return (a + np.pi)%(2*np.pi) - np.pi
    
    def _angle_difference(self, a, b):
        return self._clip_angle(a-b)
