import gym
import exercise1.car_maze as cm
import random as rnd
import time

env = cm.CarMazeEnv()

#####################################
# You code starts here
#####################################

for i_episode in range(1):
    observation = env.reset()
    for t in range(200000):
        env.render()

        # --------------------------------------------
        # example code
        # --------------------------------------------
        # #action = env.action_space.sample()
        # time.sleep(0.1)
        # avalableActions = [x[0] for x in enumerate(observation) if x[1] == 1]
        # action = avalableActions[rnd.randint(0, len(avalableActions)-1)]
        # observation, reward, done, info = env.step(action)

        # if done:
        #     print("Episode finished after {} timesteps".format(t+1))
        #     print("Reward - " + reward)
        #     break
        # --------------------------------------------
        # end of example code
        # --------------------------------------------

#####################################
# You code ends here
#####################################


env.close()
