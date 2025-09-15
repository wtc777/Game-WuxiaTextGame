from flask import session
import random, copy

class BattleService:
    def __init__(self, game_data):
        self.game_data = game_data

    def start_battle(self, player, *, force=False):
        # 若玩家已死亡，禁止开战
        if int(player.hp) <= 0:
            raise ValueError("你已经死亡，请休息恢复")
        # 不能重复开战
        if not force and session.get('current_enemy'):
            raise ValueError("战斗尚未结束，不能开始新的战斗")
        if not self.game_data.enemies:
            raise ValueError("没有可用的敌人数据")

        enemy_key = random.choice(list(self.game_data.enemies.keys()))
        enemy = copy.deepcopy(self.game_data.enemies[enemy_key])
        enemy['hp'] = int(enemy.get('hp', 0))
        enemy['attack'] = int(enemy.get('attack', 0))

        session['current_enemy'] = {'key': enemy_key, 'data': enemy}
        session.modified = True
        return enemy

    def process_attack(self, player, action):
        # 若本就没有战斗，抛错
        if 'current_enemy' not in session:
            raise ValueError("没有正在战斗的敌人")

        # 若玩家已是 0 HP，直接结束战斗（兜底）
        if int(player.hp) <= 0:
            # 清理战斗状态
            session.pop('current_enemy', None)
            session.modified = True
            # 返回统一的 battle_over 信号 + defeat
            return {
                'battle_over': True,
                'defeat': True,
                'battle_log': [f'[{self.get_time_string(player)}] 你体力不支，倒地不起！'],
                'player_hp': 0
            }

        enemy = session['current_enemy']['data']
        time_str = self.get_time_string(player)
        log = []

        def clamp_damage(base, low, high):
            return max(0, int(base) + random.randint(low, high))

        if action == 'attack':
            # 玩家出手
            weapon_info = self.game_data.weapons.get(player.weapon, {})
            base = int(player.attack) + int(weapon_info.get('attack', 0))
            player_damage = clamp_damage(base, -3, 3)

            enemy['hp'] = max(0, int(enemy['hp']) - player_damage)
            log.append(f'[{time_str}] 你对{enemy["name"]}造成了{player_damage}点伤害！')

            # 敌人死亡 -> 胜利，战斗结束
            if enemy['hp'] == 0:
                exp_gained = int(enemy.get('exp', 0))
                gold_gained = int(enemy.get('gold', 0))
                player.exp += exp_gained
                player.gold += gold_gained
                log += [
                    f'[{time_str}] {enemy["name"]}被击败了！',
                    f'[{time_str}] 获得{exp_gained}经验值和{gold_gained}金币！'
                ]
                if player.level_up():
                    log.append(f'[{time_str}] 恭喜！你升级到了{player.level}级！')
                age_result = player.pass_time(1)
                if age_result:
                    log.append(f'[{time_str}] 经过激烈的战斗，你已经{age_result["new_age"]}岁了。')

                # 清理战斗状态（非常关键）
                session.pop('current_enemy', None)
                session.modified = True

                return {
                    'battle_over': True,
                    'victory': True,
                    'battle_log': log,
                    'exp_gained': exp_gained,
                    'gold_gained': gold_gained,
                    'player_hp': int(player.hp),
                    'enemy_hp': 0
                }

            # 敌人反击（仅在敌人未死时）
            enemy_damage = clamp_damage(enemy['attack'], -2, 2)
            player.hp = max(0, int(player.hp) - enemy_damage)
            log.append(f'[{time_str}] {enemy["name"]}对你造成了{enemy_damage}点伤害！')

            # 玩家死亡 -> 失败，战斗结束
            if player.hp == 0:
                log.append(f'[{time_str}] 你被击败了！')

                # 清理战斗状态（非常关键）
                session.pop('current_enemy', None)
                session.modified = True

                return {
                    'battle_over': True,
                    'defeat': True,
                    'battle_log': log,
                    'player_hp': 0,
                    'enemy_hp': int(enemy['hp'])
                }

            # 战斗继续：写回敌人
            session['current_enemy']['data'] = enemy
            session.modified = True

            return {
                'continue': True,
                'battle_log': log,
                'player_hp': int(player.hp),
                'enemy_hp': int(enemy['hp'])
            }

        elif action == 'flee':
            # 逃跑成功 -> 战斗结束
            if random.random() < 0.7:
                session.pop('current_enemy', None)
                session.modified = True
                log.append(f'[{time_str}] 你成功脱身了！')
                return {
                    'battle_over': True,
                    'fled': True,
                    'battle_log': log,
                    'player_hp': int(player.hp)
                }

            # 逃跑失败，敌人攻击
            enemy_damage = clamp_damage(enemy['attack'], -2, 2)
            player.hp = max(0, int(player.hp) - enemy_damage)
            log.append(f'[{time_str}] 逃跑失败！{enemy["name"]}趁势出手，造成{enemy_damage}点伤害！')

            # 玩家死亡 -> 失败，战斗结束
            if player.hp == 0:
                log.append(f'[{time_str}] 你被击败了！')
                session.pop('current_enemy', None)
                session.modified = True
                return {
                    'battle_over': True,
                    'defeat': True,
                    'battle_log': log,
                    'player_hp': 0,
                    'enemy_hp': int(enemy['hp'])
                }

            # 战斗未结束：保持敌人状态
            session['current_enemy']['data'] = enemy
            session.modified = True

            return {
                'flee_failed': True,
                'battle_log': log,
                'player_hp': int(player.hp),
                'enemy_hp': int(enemy['hp'])
            }

        else:
            raise ValueError(f"未知动作: {action}")

    def get_time_string(self, player):
        t = getattr(player, 'game_time', None) or {}
        y, m, d = t.get('year', '?'), t.get('month', '?'), t.get('day', '?')
        return f"武林历{y}年{m}月{d}日"
