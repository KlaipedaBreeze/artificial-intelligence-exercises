import gym
import exercise1.car_maze as cm
import random as rnd
import time

env = cm.CarMazeEnv("open")

#################################################
# Observation space value meanings by list index:
# 0 - up       (values: 0 - road blocked,  1 - road available)
# 1 - down
# 2 - left
# 3 - right
# 4 - ID position of car
# 5 - ID position of gold
# 6 - roads / possible moves of the maze. Tuple of two ID values (from, to)
#
###########################
# Action space values
# 0 - up
# 1 - down
# 2 - left
# 3 - right

#####################################
# You code starts here
#####################################

for i_episode in range(10):
    observation = env.reset()
    for t in range(200000):
        env.render()

        # # --------------------------------------------
        # # example code
        # # --------------------------------------------
        # #action = env.action_space.sample()
        # time.sleep(0.3)
        # avalableActions = [x[0] for x in enumerate(observation) if x[1] == 1]
        # action = avalableActions[rnd.randint(0, len(avalableActions)-1)]
        #
        # observation, reward, done, info = env.step(action)
        # print(observation[6])
        #
        # if done:
        #     print("Episode finished after {} timesteps".format(t+1))
        #     print("Reward - " + reward)
        #     break
        # # --------------------------------------------
        # # end of example code
        # # --------------------------------------------

#####################################
# You code ends here
#####################################


env.close()
