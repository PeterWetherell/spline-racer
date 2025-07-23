from stable_baselines3 import PPO
import RacingEnv

env = RacingEnv.RacingEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=200000)

model.save("./PPO/racer_model_v13")