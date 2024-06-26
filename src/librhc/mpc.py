# Copyright (c) 2019, The Personal Robotics Lab, The MuSHR Team, The Contributors of MuSHR
# License: BSD 3-Clause. See LICENSE.md file in root directory.

import threading

import librhc.utils as utils


class MPC:
    # Number of elements in the position vector
    NPOS = 3

    def __init__(self, params, logger, dtype, mvmt_model, trajgen, cost):
        self.dtype = dtype
        self.logger = logger
        self.params = params
        self.goal = None

        self.trajgen = trajgen
        self.kinematics = mvmt_model
        self.cost = cost

        self.reset(init=True)

    def reset(self, init=False):
        """
        Args:
        init [bool] -- whether this is being called by the init function
        """
        self.T = self.params.get_int("T", default=15)
        self.K = self.params.get_int("K", default=62)

        # Rollouts buffer, the main engine of our computation
        self.rollouts = self.dtype(self.K, self.T, self.NPOS)

        xy_thresh = self.params.get_float("xy_threshold", default=0.1)
        self.goal_threshold = self.dtype([xy_thresh, xy_thresh])
        self.desired_speed = self.params.get_float("trajgen/desired_speed", default=1.0)
        self.dist_horizon = utils.get_distance_horizon(self.params)

        self.goal_lock = threading.Lock()
        with self.goal_lock:
            self.goal = None

        if not init:
            self.trajgen.reset()
            self.kinematics.reset()
            self.cost.reset()

    def step(self, state, path, gear_changes, car_pose):
        """
        Args:
        state [(3,) tensor] -- Current position in "world" coordinates
        TODO
        path --
        gear_changes -- list of path indices where direction changes forward <-> reverse and the corresponding change
        car_pose --
        """
        assert state.size() == (3,)

        if self.at_goal(state, path):
            return None, None

        with self.goal_lock:
            g = self.goal

        self.rollouts.zero_()

        # For each K trial, the first position is at the current position
        self.rollouts[:, 0] = state.expand_as(self.rollouts[:, 0])

        min_cost = 1000000000
        out = None
        rollout = None
        for i in range(1):
            v = min( self.desired_speed/(i+1), self.desired_speed * (self.dist_to_goal(state, path) / (self.dist_horizon)))
            if gear_changes[0][1]:
                v *= -1  # check backwards trajectories in second loop iteration
            trajs = self.trajgen.get_control_trajectories(v)
            assert trajs.size() == (self.K, self.T, 2)

            for t in range(1, self.T):
                cur_x = self.rollouts[:, t - 1]
                self.rollouts[:, t] = self.kinematics.apply(cur_x, trajs[:, t - 1])

            costs = self.cost.apply(self.rollouts, g, path, gear_changes, car_pose)
            result, idx = self.trajgen.generate_control(trajs, costs)
            if(i < 1):
                min_cost = costs[idx]
                out = result
                rollouts = self.rollouts
            else:
                if(costs[idx] < min_cost):
                    min_cost = costs[idx]
                    out = result
                    rollouts = self.rollouts
        self.rollouts = rollouts
        result = out
        # result[0,0] = max(0.0, result[0,0]) # prevent reverse
        return result, self.rollouts[idx]

    def set_goal(self, goal):
        """
        Args:
        goal [(3,) tensor] -- Goal in "world" coordinates
        """
        assert goal.size() == (3,)

        with self.goal_lock:
            self.goal = goal
            return self.cost.set_goal(goal)

    def dist_to_goal(self, state, path):
        with self.goal_lock:
            if self.goal is None:
                return False
        return self.goal[:2].dist(state[:2]) if self.cost.target_index + 15 < len(path) else self.dist_horizon

    def at_goal(self, state, path):
        """
        Args:
        state [(3,) tensor] -- Current position in "world" coordinates
        """
        with self.goal_lock:
            if self.goal is None:
                return False
        dist = self.goal[:2].sub(state[:2]).abs_()
        return dist.lt(self.goal_threshold).min() == 1 and self.cost.target_index + 15 >= len(path)

    def get_all_rollouts(self):
        return self.rollouts
