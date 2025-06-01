from typing import Optional, List
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from game.util import get_direction

class Jeno(BaseLogic):
    static_goals: List[Position] = []
    static_temp_goal: Optional[Position] = None

    def __init__(self) -> None:
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.current_direction = 0
        self.goal_position: Optional[Position] = None

    def next_move(self, bot: GameObject, board: Board):
        self.bot = bot
        self.board = board
        self.diamonds = board.diamonds
        self.base = bot.properties.base
        self.diamond_count = bot.properties.diamonds
        self.teleporters = self.get_objects_by_type("TeleportGameObject")
        self.red_buttons = self.get_objects_by_type("DiamondButtonGameObject")
        self.red_diamonds = [d for d in self.diamonds if d.properties.points == 2]

        if bot.position in self.static_goals:
            self.static_goals.remove(bot.position)

        if bot.position == self.static_temp_goal:
            self.static_temp_goal = None

        # Prioritas: kembali ke base jika sudah 5 diamond
        if self.diamond_count >= 5:
            self.goal_position = self.base
            self.static_goals.clear()
        elif self.static_temp_goal:
            self.goal_position = self.static_temp_goal
        else:
            if not self.static_goals:
                self.evaluate_map_blocks()
            self.goal_position = self.get_closest(self.static_goals)

        if self.goal_position:
            dx, dy = get_direction(bot.position.x, bot.position.y, self.goal_position.x, self.goal_position.y)
            self.check_obstacle_path(bot.position, self.goal_position)
        else:
            dx, dy = self.directions[self.current_direction]
            self.current_direction = (self.current_direction + 1) % 4

        return dx, dy

    def get_objects_by_type(self, obj_type: str):
        return [obj for obj in self.board.game_objects if obj.type == obj_type]

    def get_closest(self, positions: List[Position]) -> Optional[Position]:
        current = self.bot.position
        return min(positions, key=lambda pos: abs(pos.x - current.x) + abs(pos.y - current.y), default=None)

    def evaluate_map_blocks(self):
        block_h, block_w = self.board.height // 3, self.board.width // 3
        blocks = [[[] for _ in range(3)] for _ in range(3)]
        values = [[0 for _ in range(3)] for _ in range(3)]

        for diamond in self.diamonds:
            if diamond.properties.points == 2 and self.diamond_count == 4:
                continue
            i = diamond.position.y // block_h
            j = diamond.position.x // block_w
            blocks[i][j].append(diamond.position)
            values[i][j] += diamond.properties.points

        best_i, best_j, best_score = 0, 0, 0
        curr_i = self.bot.position.y // block_h
        curr_j = self.bot.position.x // block_w

        for i in range(3):
            for j in range(3):
                if values[i][j] == 0:
                    continue
                distance = abs(curr_i - i) + abs(curr_j - j)
                score = values[i][j] + max(0, 5 - distance)
                if score > best_score:
                    best_i, best_j, best_score = i, j, score

        if best_score == 0 and self.red_buttons:
            self.static_goals = [self.red_buttons[0].position]
        else:
            self.static_goals = blocks[best_i][best_j]

    def check_obstacle_path(self, start: Position, goal: Position):
        for obj_list in [self.teleporters, self.red_buttons, self.red_diamonds]:
            for obj in obj_list:
                obs = obj.position
                if self.on_path(start, goal, obs):
                    new_goal = self.get_safe_detour(start, goal, obs)
                    if new_goal:
                        self.goal_position = new_goal
                        self.static_temp_goal = new_goal
                        return

    def on_path(self, start: Position, goal: Position, obs: Position) -> bool:
        # Simple straight-line detection
        if start.x == goal.x == obs.x and min(start.y, goal.y) < obs.y < max(start.y, goal.y):
            return True
        if start.y == goal.y == obs.y and min(start.x, goal.x) < obs.x < max(start.x, goal.x):
            return True
        return False

    def get_safe_detour(self, start: Position, goal: Position, obs: Position) -> Optional[Position]:
        # Simple dodge strategy: try side step
        if start.x == goal.x:
            side_x = start.x + 1 if start.x < self.board.width - 1 else start.x - 1
            return Position(start.y, side_x)
        elif start.y == goal.y:
            side_y = start.y + 1 if start.y < self.board.height - 1 else start.y - 1
            return Position(side_y, start.x)
        return None
