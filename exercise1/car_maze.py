#####################################################
# No code change allowed
#####################################################

import math
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding
from os import path
import exercise1.maze as mz
from gym.envs.classic_control import rendering


class CarMazeEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 30
    }

    def __init__(self, maze_mode="blind"):
        self.__maze_mode = maze_mode
        self.__viewer = None
        self.observation_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(4)
        self.__np_random = None
        self.__maze_size = (15, 15)
        self.__maze = mz.Maze(self.__maze_size[0], self.__maze_size[1])
        self.__carPosition = self.__maze.start
        self.__goldPosition = self.__maze.gold
        self.__celltrans = None
        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.__np_random, seed = seeding.np_random(seed)
        return [seed]

    # @property
    def observation(self):
        carPos = self.__carPosition
        availabeStops = [x.dest.get_id for x in self.__maze.roads if x.source.get_id == carPos.get_id]
        up = int(mz.Stop(carPos.x, carPos.y + 1).get_id in availabeStops)
        down = int(mz.Stop(carPos.x, carPos.y - 1).get_id in availabeStops)
        left = int(mz.Stop(carPos.x - 1, carPos.y).get_id in availabeStops)
        right = int(mz.Stop(carPos.x + 1, carPos.y).get_id in availabeStops)
        roads_obs = [(x.source.get_id, x.dest.get_id) for x in self.__maze.roads]
        car_obs = carPos.get_id
        gold_obs = self.__goldPosition.get_id

        if self.__maze_mode == "blind":
            return [up, down, left, right, car_obs, gold_obs]
        return [up, down, left, right, car_obs, gold_obs, roads_obs]

    def reset(self):
        return self.observation()

    def step(self, action):
        obs = self.observation()
        if obs[action] != 1:
            return obs, -100, True, {"errors": ["No road to this direction"]}
        dm = [(0, 1), (0, -1), (-1, 0), (1, 0)][action]
        desiredStop = mz.Stop(self.__carPosition.x + dm[0], self.__carPosition.y + dm[1])
        nextStop = next((x for x in self.__maze.stops if x.get_id == desiredStop.get_id), None)
        self.__carPosition = nextStop
        state = self.observation()
        if self.__carPosition.get_id == self.__goldPosition.get_id:
            reward = 100
            done = True
        else:
            reward = 0
            done = False
        return state, reward, done, {}

    def draw_maze(self, s_width, s_height):
        scale = min(s_width, s_height)
        wallSize = 10
        cellSize = (scale - wallSize) // self.__maze_size[0]
        self.maze_scales = (cellSize, wallSize)

        for stop in self.__maze.stops:
            l, r = stop.x * cellSize + wallSize, stop.x * cellSize + cellSize
            t, b = stop.y * cellSize + wallSize, stop.y * cellSize + cellSize
            # l, r, t, b = -40 / 2, 40 / 2, 20, 0
            cell = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            cell.add_attr(rendering.Transform(translation=(0, 10)))
            self.__celltrans = rendering.Transform()
            cell.add_attr(self.__celltrans)
            self.__viewer.add_geom(cell)

        for road in self.__maze.roads:
            coef = 7
            l = road.source.x * cellSize + wallSize + cellSize // coef
            r = road.dest.x * cellSize + wallSize + ((coef - 1) * cellSize // coef)
            t = road.source.y * cellSize + wallSize + cellSize // coef
            b = road.dest.y * cellSize + wallSize + ((coef - 1) * cellSize // coef)
            road = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.__viewer.add_geom(road)
            # break

    def move_car(self, action):
        pass

    def draw_car_position(self):
        carX = self.__carPosition.x * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        carY = self.__carPosition.y * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        self.__viewer.add_onetime(self.img)
        self.imgtrans.scale = (1, 1)
        self.imgtrans.set_translation(carX, carY)

    def draw_gold_position(self):
        X = self.__goldPosition.x * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        Y = self.__goldPosition.y * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        self.__viewer.add_onetime(self.imgGold)
        self.imgGoldtrans.scale = (1, 1)
        self.imgGoldtrans.set_translation(X, Y)

    def render(self, mode='human'):
        screen_width = 800
        screen_height = 800
        if self.__viewer is None:
            self.__viewer = rendering.Viewer(screen_width, screen_height)
            self.draw_maze(screen_width, screen_height)
            fname = path.join(path.dirname(__file__), "assets/car.png")
            self.img = rendering.Image(fname, 40., 20.)
            self.imgtrans = rendering.Transform()
            self.img.add_attr(self.imgtrans)
            fnamegold = path.join(path.dirname(__file__), "assets/gold.png")
            self.imgGold = rendering.Image(fnamegold, 40., 20.)
            self.imgGoldtrans = rendering.Transform()
            self.imgGold.add_attr(self.imgGoldtrans)

        self.draw_car_position()
        self.draw_gold_position()
        return self.__viewer.render(return_rgb_array=mode == 'rgb_array')


class Maze:
    pass
