import random
from .event_generator import RandomEventGenerator


class ExplorationService:
    def __init__(self, game_data, battle_service=None):
        self.game_data = game_data
        self.battle_service = battle_service
        self.event_generator = RandomEventGenerator(game_data)

    def explore(self, player):
        """处理探索事件"""
        if player.hp <= 0:
            raise ValueError("你已经死亡，请休息恢复")

        # 时间流逝
        age_result = player.pass_time(random.randint(1, 3))
        time_str = self.get_time_string(player)

        # 使用事件生成器生成随机事件
        event = self.event_generator.generate_event(player, player.location)

        messages = []

        if age_result:
            messages.append(
                f"[{time_str}] 岁月如流水，你已经{age_result['new_age']}岁了。随着年龄的增长，你的实力也在发生变化...")

        # 处理不同类型的事件
        event_result = self._process_event(event, player, time_str, messages)

        return event_result

    def _process_event(self, event, player, time_str, messages):
        """处理生成的事件"""
        event_type = event['type']
        rarity = event['rarity']

        # 添加事件标题和稀有度信息
        rarity_text = {
            'common': '',
            'uncommon': ' [稀有]',
            'rare': ' [罕见]',
            'epic': ' [史诗]',
            'legendary': ' [传说]'
        }.get(rarity, '')

        messages.append(f"[{time_str}] {event['title']}{rarity_text}")
        messages.append(event['description'])

        # 根据事件类型处理效果
        if event_type == 'combat':
            enemy = event['effects']['enemy']

            if self.battle_service:
                # 使用 battle_service 处理战斗
                battle_enemy = self.battle_service.start_battle(player)
                # 保持生成的敌人属性
                battle_enemy.update(enemy)
                return {
                    'type': 'enemy',
                    'messages': messages,
                    'enemy': battle_enemy,
                    'rarity': rarity
                }
            else:
                # 向后兼容的处理方式
                return {
                    'type': 'enemy',
                    'messages': messages,
                    'enemy': enemy,
                    'rarity': rarity
                }

        elif event_type == 'treasure':
            gold_found = event['effects']['gold']
            player.gold += gold_found

            result = {
                'type': 'treasure',
                'messages': messages,
                'gold_gained': gold_found,
                'rarity': rarity
            }

            # 添加额外奖励
            if 'bonus' in event['effects']:
                result['bonus'] = event['effects']['bonus']
                messages.append("你还获得了一些特殊的收获！")

            return result

        elif event_type == 'story':
            exp_gained = event['effects']['exp']
            player.exp += exp_gained

            # 检查升级
            level_up_msg = ""
            if player.level_up():
                level_up_msg = f" 恭喜！你升级到了{player.level}级！"

            messages.append(f"你获得了{exp_gained}点经验。{level_up_msg}")

            return {
                'type': 'story',
                'messages': messages,
                'exp_gained': exp_gained,
                'rarity': rarity
            }

        elif event_type == 'merchant':
            return {
                'type': 'merchant',
                'messages': messages,
                'merchant_type': event['effects']['merchant_type'],
                'choices': event['choices'],
                'rarity': rarity
            }

        elif event_type == 'encounter':
            return {
                'type': 'encounter',
                'messages': messages,
                'special': event['effects']['special'],
                'rarity': rarity
            }

        elif event_type == 'trap':
            damage = event['effects']['damage']
            player.hp = max(0, player.hp - damage)

            messages.append(f"你受到了{damage}点伤害。")

            if player.hp <= 0:
                messages.append("你伤势过重，需要休息恢复！")

            return {
                'type': 'trap',
                'messages': messages,
                'damage': damage,
                'rarity': rarity
            }

        elif event_type == 'training':
            stat_bonus = event['effects']['stat_bonus']
            # 随机提升属性
            if random.choice([True, False]):
                player.max_hp += stat_bonus
                player.hp += stat_bonus
                stat_name = "生命值"
            else:
                player.attack += stat_bonus
                stat_name = "攻击力"

            messages.append(f"你的{stat_name}提升了{stat_bonus}点！")

            return {
                'type': 'training',
                'messages': messages,
                'stat_bonus': stat_bonus,
                'stat_name': stat_name,
                'rarity': rarity
            }

        else:
            return {
                'type': 'nothing',
                'messages': messages
            }

    def get_time_string(self, player):
        """获取时间字符串"""
        time = player.game_time
        return f"武林历{time['year']}年{time['month']}月{time['day']}日"
