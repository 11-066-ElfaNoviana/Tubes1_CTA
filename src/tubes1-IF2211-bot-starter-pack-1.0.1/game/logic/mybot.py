from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from game.util import get_direction

class MyBot(BaseLogic):
    static_goals: list[Position] = []
    static_temp_goals: Optional[Position] = None

    def _init_(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        self.board = board
        self.board_bot = board_bot
        self.diamonds = board.diamonds
        self.bots = board.bots
        self.teleporter = [d for d in self.board.game_objects if d.type == "TeleportGameObject"]
        self.redButton = [d for d in self.board.game_objects if d.type == "DiamondButtonGameObject"]

        # Remove goal if already reached
        if board_bot.position in self.static_goals:
            self.static_goals.remove(board_bot.position)

        # Remove temp goal if already reached
        if board_bot.position == self.static_temp_goals:
            self.static_temp_goals = None

        # Reset temp goal if invalid
        if self.static_temp_goals and not self.is_valid_position(self.static_temp_goals.x, self.static_temp_goals.y):
            self.static_temp_goals = None

        # Analyze new state
        if props.diamonds == 5:
            self.goal_position = props.base
            self.static_goals = []
        elif self.static_temp_goals:
            self.goal_position = self.static_temp_goals
        else:
            if not self.static_goals:
                self.find_best_block()
            self.goal_position = self.find_nearest_goal()

        current_position = board_bot.position
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x, current_position.y,
                self.goal_position.x, self.goal_position.y,
            )

            if not self.static_temp_goals:
                self.obstacle_on_path('teleporter', current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            if not self.static_temp_goals:
                self.obstacle_on_path('redButton', current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            if props.diamonds == 4 and not self.static_temp_goals:
                self.obstacle_on_path('redDiamond', current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
        else:
            # Jika goal tidak ada, coba cari diamond terdekat langsung
            nearest_diamond = None
            nearest_dist = float('inf')
            pos = current_position
            for d in self.diamonds:
                dist = abs(pos.x - d.position.x) + abs(pos.y - d.position.y)
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_diamond = d.position

            if nearest_diamond:
                delta_x, delta_y = get_direction(pos.x, pos.y, nearest_diamond.x, nearest_diamond.y)
            else:
                delta_x, delta_y = self.directions[self.current_direction]
                self.current_direction = (self.current_direction + 1) % len(self.directions)

        return delta_x, delta_y

    def find_nearest_goal(self):
        current_position = self.board_bot.position
        nearest_goal = None
        nearest_distance = float("inf")
        for goal in self.static_goals:
            distance = abs(current_position.x - goal.x) + abs(current_position.y - goal.y)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_goal = goal
        return nearest_goal

    def find_best_block(self):
        self.find_best_block_around()

    def find_best_block_around(self):
        current_position = self.board_bot.position
        blockH, blockW = 3, 3
        topLeft = (current_position.y - blockH // 2 - blockH, current_position.x - blockW // 2 - blockW)

        blockAroundValue = [[0 for _ in range(3)] for _ in range(3)]
        blockAroundDiamonds = [[[] for _ in range(3)] for _ in range(3)]
        bestValue = 0
        bestBlockIndex = (0, 0)

        for diamond in self.diamonds:
            if diamond.properties.points == 2 and self.board_bot.properties.diamonds == 4:
                continue
            if topLeft[1] <= diamond.position.x < topLeft[1] + blockW * 3 and topLeft[0] <= diamond.position.y < topLeft[0] + blockH * 3:
                i = (diamond.position.y - topLeft[0]) // blockH
                j = (diamond.position.x - topLeft[1]) // blockW
                if 0 <= i < 3 and 0 <= j < 3:
                    blockAroundValue[i][j] += diamond.properties.points
                    blockAroundDiamonds[i][j].append(diamond.position)

        min_diamond = 5 - self.board_bot.properties.diamonds
        for i in range(3):
            for j in range(3):
                if blockAroundValue[i][j] < min_diamond:
                    blockAroundValue[i][j] = 0
                else:
                    dist = abs(i - 1) + abs(j - 1)  # jarak dari tengah blok
                    blockAroundValue[i][j] += max(0, 5 - dist * 2)

        for i in range(3):
            for j in range(3):
                if blockAroundValue[i][j] > bestValue:
                    bestValue = blockAroundValue[i][j]
                    bestBlockIndex = (i, j)

        if bestValue > 0:
            self.static_goals = blockAroundDiamonds[bestBlockIndex[0]][bestBlockIndex[1]]
        else:
            self.find_best_block_map()

    def find_best_block_map(self):
        current_position = self.board_bot.position
        blockH = max(1, self.board.height // 3)
        blockW = max(1, self.board.width // 3)

        blockAroundValue = [[0 for _ in range(3)] for _ in range(3)]
        blockAroundDiamonds = [[[] for _ in range(3)] for _ in range(3)]

        bestValue = 0
        bestBlockIndex = (0, 0)

        for diamond in self.diamonds:
            if diamond.properties.points == 2 and self.board_bot.properties.diamonds == 4:
                continue
            i, j = diamond.position.y // blockH, diamond.position.x // blockW
            if 0 <= i < 3 and 0 <= j < 3:
                blockAroundValue[i][j] += diamond.properties.points
                blockAroundDiamonds[i][j].append(diamond.position)
                if blockAroundValue[i][j] > bestValue:
                    bestValue = blockAroundValue[i][j]
                    bestBlockIndex = (i, j)

        if bestValue == 0:
            if self.redButton:
                self.static_goals.append(self.redButton[0].position)
            return

        minimunDiamond = 5 - self.board_bot.properties.diamonds
        currentBlock = (current_position.y // blockH, current_position.x // blockW)

        for i in range(3):
            for j in range(3):
                if blockAroundValue[i][j] == 0 or blockAroundValue[i][j] < minimunDiamond:
                    continue
                distance = abs(currentBlock[0] - i) + abs(currentBlock[1] - j)
                blockAroundValue[i][j] += max(0, 5 - distance)
                selisih = blockAroundValue[i][j] - minimunDiamond
                blockAroundValue[i][j] -= selisih

        score = 0
        for i in range(3):
            for j in range(3):
                if blockAroundValue[i][j] > score:
                    score = blockAroundValue[i][j]
                    bestBlockIndex = (i, j)

        self.static_goals = blockAroundDiamonds[bestBlockIndex[0]][bestBlockIndex[1]]

    def obstacle_on_path(self, type, current_x, current_y, dest_x, dest_y):
        if type == 'teleporter':
            objects = self.teleporter
        elif type == 'redDiamond':
            objects = [d for d in self.diamonds if d.properties.points == 2]
        elif type == 'redButton':
            objects = self.redButton
        else:
            return

        for obj in objects:
            t = obj.position

            def try_set_goal(new_y, new_x):
                if self.is_valid_position(new_x, new_y):
                    self.goal_position = Position(new_y, new_x)
                    self.static_temp_goals = Position(new_y, new_x)
                    return True
                return False

            if t.x == dest_x and (dest_y < t.y <= current_y or current_y <= t.y < dest_y):
                if try_set_goal(dest_y, dest_x - 1 if dest_x > current_x else dest_x + 1):
                    return
            elif t.y == dest_y and (dest_x < t.x <= current_x or current_x <= t.x < dest_x):
                if try_set_goal(dest_y - 1 if dest_y > current_y else dest_y + 1, dest_x):
                    return
            elif t.y == current_y and (dest_x < t.x <= current_x or current_x <= t.x < dest_x):
                if try_set_goal(dest_y, current_x):
                    return
            elif t.x == current_x and (dest_y < t.y <= current_y or current_y <= t.y < dest_y):
                new_x = current_x - 1 if current_x > 0 else current_x + 1
                if try_set_goal(dest_y, new_x):
                    return

    def is_valid_position(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x >= self.board.width or y >= self.board.height:
            return False
        for obj in self.board.game_objects:
            if obj.position.x == x and obj.position.y == y and obj.type in ['WallGameObject', 'ObstacleGameObject']:
                return False
        return True