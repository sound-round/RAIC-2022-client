import muffin
from debugging.color import Color
from model.game import Game
from model.order import Order
from model.unit_order import UnitOrder
from model.constants import Constants
from model.vec2 import Vec2
from model.action_order import ActionOrder
from typing import Optional
from debug_interface import DebugInterface
import math, random


SHOOT_DISTANCE_TO_ENEMY = 5
# MIN_RANDOM_COORDINATE = -60
# MAX_RANDOM_COORDINATE = 60
MIN_TIME_FOR_ZIGZAG = 30
MAX_TIME_FOR_ZIGZAG = 60
RANDOM_VALUE = 60

random_xy = (0, 0)
counter = 0

class MyStrategy:
    def __init__(self, constants: Constants, counter=counter, random_xy=random_xy):
        self.counter = counter
        self.random_xy = random_xy

    def get_order(self, game: Game, debug_interface: Optional[DebugInterface]) -> Order:
        orders = {}

        if self.counter == 0:
            self.random_xy = self.find_random_xy(RANDOM_VALUE)
            self.counter = random.randint(MIN_TIME_FOR_ZIGZAG, MAX_TIME_FOR_ZIGZAG)
        self.counter -= 1

        for unit in game.units:
            if unit.player_id != game.my_id:
                continue
            # TODO: 1. оборачиваться на звуки 
            # 2. Уворачиваться 
            # 4. Не стрелять через стены, которые не простреливаются
            # 5  Научить бегать зигзагами (научил кое-как)
            # 6. зона сужается, нужно учесть (не собирать лут, бежать центр безопасной зоны)
            # TODO: queue = [], куда записывать очередность действий

            # sounds = game.sounds
            my_unit = unit
            velocity = Vec2(-unit.position.x, -unit.position.y)
            direction = Vec2(-unit.direction.y, unit.direction.x)  # просто крутится взглядом
            shoot = False

            max_distance_to_enemy = 30
            if my_unit.weapon == 2:
                max_distance_to_enemy = 40
            if my_unit.weapon == 1:
                max_distance_to_enemy = 20

            ranked_enemies = self.sort_enemies(my_unit, game.units, game)


            loot_item = None
            possibleTarget = None
            if my_unit.shield_potions == 0:
                loot_item = self.find_shield_potion(game.loot, my_unit)
            if not loot_item and my_unit.weapon == 0:
                loot_item = self.find_weapon(game.loot, my_unit)
            if not loot_item and my_unit.ammo[my_unit.weapon] == 0:
                loot_item = self.find_ammo(game.loot, my_unit)
            # if not loot_item:
            possibleTarget = self.find_enemy(ranked_enemies)
            if possibleTarget:
                distance = self.find_distance(my_unit, possibleTarget)
                # direction = possibleTarget.position.copy().minus(unit.position)
                # velocity = direction
                velocity = Vec2(direction.x + self.random_xy[0], direction.y + self.random_xy[1])
                

                # if distance < SHOOT_DISTANCE_TO_ENEMY:
                #     velocity = Vec2(0, 0)
                
                if distance < max_distance_to_enemy:
                    direction = possibleTarget.position.copy().minus(unit.position)
                    velocity = Vec2(direction.x + self.random_xy[0], direction.y + self.random_xy[1])
                    shoot = True 

                if debug_interface:
                    self.show_target(debug_interface, unit, possibleTarget)

            action = None

            if loot_item:
                shoot = False
                distance = self.find_distance(loot_item, my_unit)
                if distance < 1:
                    action = ActionOrder.Pickup(loot_item.id)
                direction = loot_item.position.copy().minus(unit.position)
                velocity = Vec2(direction.x * 2000, direction.y * 2000)

                if debug_interface:
                        self.show_target(debug_interface, unit, loot_item)

            if not action and shoot:
                action = ActionOrder.Aim(shoot)

            if my_unit.shield < 90 and my_unit.shield_potions and not action and not shoot:
                action = ActionOrder.UseShieldPotion()
            print(action)
            orders[unit.id] = UnitOrder(
                velocity,
                direction,
                action,
            )
        return Order(orders)

    def find_random_xy(self, value):
        x = random.choice((value, - value))
        y = random.choice((value, - value))
        return (x, y)

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

    def find_ammo(self, loot, my_unit):
        ammos = []
        for obj in loot:
            if obj.item.TAG == 2 and obj.item.weapon_type_index == my_unit.weapon:
                distance = self.find_distance(obj, my_unit)
                ammos.append((distance, obj))
        if not ammos:
            return
        ammos.sort()
        return ammos[0][1]

    def find_weapon(self, loot, my_unit):
        weapons = []
        for obj in loot:
            if obj.item.TAG == 0 and obj.item.type_index == 2:
                distance = self.find_distance(obj, my_unit)
                weapons.append((distance, obj))
        if not weapons:
            return
        weapons.sort()
        return weapons[0][1]

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