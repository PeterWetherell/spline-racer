from stable_baselines3 import SAC
import RacingEnv

env = RacingEnv.RacingEnv()
model = SAC("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=50000)

model.save("racer_model_v5")