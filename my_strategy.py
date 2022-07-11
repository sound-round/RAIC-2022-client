from debugging.color import Color
from model.game import Game
from model.order import Order
from model.unit_order import UnitOrder
from model.constants import Constants
from model.vec2 import Vec2
from model.action_order import ActionOrder
from typing import Optional
from debug_interface import DebugInterface
import sys, math


SHOOT_DISTANCE_TO_ENEMY = 20

class MyStrategy:
    def __init__(self, constants: Constants):
        pass
    def get_order(self, game: Game, debug_interface: Optional[DebugInterface]) -> Order:
        orders = {}
        for unit in game.units:
            if unit.player_id != game.my_id:
                continue
            

            my_unit = unit
            velocity = Vec2(-unit.position.x, -unit.position.y)
            direction = Vec2(-unit.direction.y, unit.direction.x)  # просто крутится взглядом
            shoot = False
            ranked_enemies = self.sort_enemies(my_unit, game.units, game)
            # print("\033[91m ranked_enemies \033[0m", Constants.unit_radius)
            potion = None
            possibleTarget = None
            if my_unit.shield_potions <= 1:
                potion = self.find_shield_potion(game.loot, my_unit)
            if not potion:
                possibleTarget = self.find_enemy(ranked_enemies)
            if possibleTarget:
                direction = possibleTarget.position.copy().minus(unit.position)
                velocity = direction
                distance = self.find_distance(my_unit, possibleTarget)
                if distance < SHOOT_DISTANCE_TO_ENEMY:
                    velocity = Vec2(0, 0)

                shoot = True

                if debug_interface:
                    self.show_target(debug_interface, unit, possibleTarget)

            action = ActionOrder.Aim(shoot)

            if potion:
                distance = self.find_distance(potion, my_unit)
                if distance < 1:
                    action = ActionOrder.Pickup(potion.id)
                direction = potion.position.copy().minus(unit.position)
                velocity = direction

                if debug_interface:
                        self.show_target(debug_interface, unit, potion)

            if my_unit.shield < 60 and my_unit.shield_potions:
                action = ActionOrder.UseShieldPotion()

            orders[unit.id] = UnitOrder(
                velocity,
                direction,
                action,
            )
        return Order(orders)

    @staticmethod
    def find_distance(entity1, entity2):
        return math.hypot(
            entity1.position.x - entity2.position.x,
            entity1.position.y - entity2.position.y,
            )

    def find_enemy(self, enemies):
        if enemies:
            return enemies[0][1]
        return

    def find_shield_potion(self, loot, my_unit):
        potions = []
        for obj in loot:
            if obj.item.TAG == 1:
                distance = self.find_distance(obj, my_unit)
                potions.append((distance, obj))
        if not potions:
            return
        potions.sort()
        return potions[0][1]

    # def pickup_loot(self, loot):


    def sort_enemies(self, my_unit, units, game):
        enemies = []
        for unit in units:
            if (unit.player_id != game.my_id):
                distance = self.find_distance(my_unit, unit)
                enemies.append((distance, unit))
        enemies.sort()
        return enemies

    @staticmethod
    def show_target(debug_interface, unit, target):
        debug_interface.add_poly_line([unit.position, target.position], 0.5, Color(1.0, 0.0, 0.0, 1.0))

    def debug_update(self, displayed_tick: int, debug_interface: DebugInterface):
        pass
    def finish(self):
        pass