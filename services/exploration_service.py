import random


class ExplorationService:
    def __init__(self, game_data):
        self.game_data = game_data

    def explore(self, player):
        """处理探索事件"""
        if player.hp <= 0:
            raise ValueError("你已经死亡，请休息恢复")

        # 时间流逝
        age_result = player.pass_time(random.randint(1, 3))
        time_str = self.get_time_string(player)

        # 随机事件
        event_type = random.choice(['enemy', 'treasure', 'story', 'nothing'])

        messages = []

        if age_result:
            messages.append(
                f"[{time_str}] 岁月如流水，你已经{age_result['new_age']}岁了。随着年龄的增长，你的实力也在发生变化...")

        if event_type == 'enemy':
            enemy_key = random.choice(list(self.game_data.enemies.keys()))
            enemy = self.game_data.enemies[enemy_key].copy()
            
            messages.append(f"[{time_str}] 你遇到了{enemy['name']}！")

            return {
                'type': 'enemy',
                'messages': messages,
                'enemy': enemy
            }

        elif event_type == 'treasure':
            gold_found = random.randint(5, 20)
            player.gold += gold_found

            messages.append(f"[{time_str}] 你发现了一个宝箱，获得了{gold_found}金币！")

            return {
                'type': 'treasure',
                'messages': messages,
                'gold_gained': gold_found
            }

        elif event_type == 'story':
            stories = [
                "你遇到了一位神秘的老者，他传授给你一些武学心得。",
                "你发现了一座古老的石碑，上面刻着前人的武功感悟。",
                "一只受伤的小鸟落在你面前，你温柔地为它包扎了伤口，内心感到平静。",
                "你路过一处风景秀丽的地方，观察山川流水，对武学有了新的理解。",
                "你遇到了一位同道中人，与他切磋武艺，互有收获。",
                "在一处客栈中，你听到了江湖传说，心中对武道的追求更加坚定。"
            ]

            # 随机获得少量经验
            exp_gained = random.randint(5, 15)
            player.exp += exp_gained

            # 检查升级
            level_up_msg = ""
            if player.level_up():
                level_up_msg = f" 恭喜！你升级到了{player.level}级！"

            messages.append(f"[{time_str}] {random.choice(stories)}你获得了{exp_gained}点经验。{level_up_msg}")

            return {
                'type': 'story',
                'messages': messages,
                'exp_gained': exp_gained
            }

        else:
            messages.append(f"[{time_str}] 你在周围探索了一番，但什么都没有发现。时间悄悄流逝...")

            return {
                'type': 'nothing',
                'messages': messages
            }

    def get_time_string(self, player):
        """获取时间字符串"""
        time = player.game_time
        return f"武林历{time['year']}年{time['month']}月{time['day']}日"
