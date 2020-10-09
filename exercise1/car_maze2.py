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

    def __init__(self):
        self.viewer = None
        self.observation_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(4)
        self.np_random = None
        self.maze_size = (15, 15)
        self.maze = mz.Maze(self.maze_size[0], self.maze_size[1])
        self.carPosition = self.maze.start
        self.goldPosition = self.maze.gold
        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # @property
    def observation(self):
        carPos = self.carPosition
        availabeStops = [x.dest.get_id for x in self.maze.roads if x.source.get_id == carPos.get_id]
        up = int(mz.Stop(carPos.x, carPos.y + 1).get_id in availabeStops)
        down = int(mz.Stop(carPos.x, carPos.y - 1).get_id in availabeStops)
        left = int(mz.Stop(carPos.x - 1, carPos.y).get_id in availabeStops)
        right = int(mz.Stop(carPos.x + 1, carPos.y).get_id in availabeStops)
        return [up, down, left, right]


    def reset(self):
        return self.observation()

    def step(self, action):
        obs = self.observation()
        if obs[action] != 1:
            return obs, -100, True, {"errors": ["No road to this direction"]}
        dm = [(0, 1), (0, -1), (-1, 0), (1, 0)][action]
        desiredStop = mz.Stop(self.carPosition.x + dm[0], self.carPosition.y + dm[1])
        nextStop = next((x for x in self.maze.stops if x.get_id == desiredStop.get_id), None)
        self.carPosition = nextStop
        state = self.observation()
        reward = 0
        done = False
        return state, reward, done, {}


    def draw_maze(self, s_width, s_height):
        scale = min(s_width, s_height)
        wallSize = 10
        cellSize = (scale - wallSize) // self.maze_size[0]
        self.maze_scales = (cellSize, wallSize)

        for stop in self.maze.stops:
            l, r = stop.x * cellSize + wallSize, stop.x * cellSize + cellSize
            t, b = stop.y * cellSize + wallSize, stop.y * cellSize + cellSize
            # l, r, t, b = -40 / 2, 40 / 2, 20, 0
            cell = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            cell.add_attr(rendering.Transform(translation=(0, 10)))
            self.celltrans = rendering.Transform()
            cell.add_attr(self.celltrans)
            self.viewer.add_geom(cell)

        for road in self.maze.roads:
            coef = 7
            l = road.source.x * cellSize + wallSize + cellSize // coef
            r = road.dest.x * cellSize + wallSize + ((coef - 1) * cellSize // coef)
            t = road.source.y * cellSize + wallSize + cellSize // coef
            b = road.dest.y * cellSize + wallSize + ((coef - 1) * cellSize // coef)
            road = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.viewer.add_geom(road)
            # break

    def move_car(self, action):
        pass

    def draw_car_position(self):
        carX = self.carPosition.x * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        carY = self.carPosition.y * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        self.viewer.add_onetime(self.img)
        self.imgtrans.scale = (1, 1)
        self.imgtrans.set_translation(carX, carY)

    def draw_gold_position(self):
        X = self.goldPosition.x * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        Y = self.goldPosition.y * self.maze_scales[0] + self.maze_scales[1] + self.maze_scales[0] // 2
        self.viewer.add_onetime(self.imgGold)
        self.imgGoldtrans.scale = (1, 1)
        self.imgGoldtrans.set_translation(X, Y)

    def render(self, mode='human'):
        screen_width = 800
        screen_height = 800
        if self.viewer is None:
            self.viewer = rendering.Viewer(screen_width, screen_height)
            self.draw_maze(screen_width, screen_height)
            fname = path.join(path.dirname(__file__), "assets/car.png")
            self.img = rendering.Image(fname, 40., 20.)
            self.imgtrans = rendering.Transform()
            self.img.add_attr(self.imgtrans)
            fnamegold = path.join(path.dirname(__file__), "assets/gold.png")
            self.imgGold = rendering.Image(fnamegold, 40., 20.)
            self.imgGoldtrans = rendering.Transform()
            self.imgGold.add_attr(self.imgtrans)

        self.draw_car_position()
        self.draw_gold_position()
        return self.viewer.render(return_rgb_array=mode == 'rgb_array')


class Maze:
    pass
