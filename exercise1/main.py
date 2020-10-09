import gym
import exercise1.car_maze2 as cm
import random as rnd
import time

env = cm.CarMazeEnv()

for i_episode in range(1):
    observation = env.reset()
    for t in range(20000):
        env.render()
        #action = env.action_space.sample()

        time.sleep(0.1)
        avalableActions = [x[0] for x in enumerate(observation) if x[1] == 1]
        action = avalableActions[rnd.randint(0, len(avalableActions)-1)]

        observation, reward, done, info = env.step(action)
        # print(reward)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

env.close()
