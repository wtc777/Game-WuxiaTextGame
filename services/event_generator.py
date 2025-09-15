
import random
from typing import Dict, List, Any, Optional
from enum import Enum


class EventRarity(Enum):
    """事件稀有度"""
    COMMON = "common"      # 普通
    UNCOMMON = "uncommon"  # 稀有
    RARE = "rare"         # 罕见
    EPIC = "epic"         # 史诗
    LEGENDARY = "legendary"  # 传说


class EventType(Enum):
    """事件类型"""
    COMBAT = "combat"        # 战斗
    TREASURE = "treasure"    # 宝藏
    STORY = "story"         # 故事
    MERCHANT = "merchant"    # 商人
    ENCOUNTER = "encounter"  # 奇遇
    TRAP = "trap"          # 陷阱
    TRAINING = "training"    # 修炼
    QUEST = "quest"        # 任务


class RandomEventGenerator:
    """随机事件生成器"""
    
    def __init__(self, game_data):
        self.game_data = game_data
        self.event_templates = self._initialize_event_templates()
        self.rarity_weights = {
            EventRarity.COMMON: 50,
            EventRarity.UNCOMMON: 30,
            EventRarity.RARE: 15,
            EventRarity.EPIC: 4,
            EventRarity.LEGENDARY: 1
        }
        
    def _initialize_event_templates(self) -> Dict[EventType, List[Dict]]:
        """初始化事件模板"""
        return {
            EventType.COMBAT: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "遭遇{enemy}",
                        "{enemy}突然出现",
                        "前方出现了{enemy}",
                        "{enemy}挡住了去路"
                    ],
                    "description_templates": [
                        "你遇到了{enemy}，它看起来{enemy_description}。",
                        "一只{enemy}出现在你面前，{enemy_description}。",
                        "{enemy}向你发起了攻击，{enemy_description}。"
                    ],
                    "enemy_descriptions": [
                        "凶猛异常",
                        "眼神凶狠",
                        "气势汹汹",
                        "虎视眈眈",
                        "蓄势待发"
                    ]
                },
                {
                    "rarity": EventRarity.UNCOMMON,
                    "title_templates": [
                        "精英{enemy}",
                        "强大的{enemy}",
                        "变异{enemy}"
                    ],
                    "description_templates": [
                        "你遇到了一只异常强大的{enemy}，{enemy_description}。",
                        "这只{enemy}看起来比同类要强大得多，{enemy_description}。"
                    ],
                    "enemy_descriptions": [
                        "散发着强大的气势",
                        "眼中闪烁着危险的光芒",
                        "肌肉贲张，力量惊人"
                    ],
                    "stat_multiplier": 1.5
                },
                {
                    "rarity": EventRarity.RARE,
                    "title_templates": [
                        "传说中的{enemy}",
                        "古代{enemy}",
                        "神秘{enemy}"
                    ],
                    "description_templates": [
                        "你遇到了传说中的{enemy}，{enemy_description}。",
                        "这只神秘的{enemy}散发着古老的气息，{enemy_description}。"
                    ],
                    "enemy_descriptions": [
                        "散发着古老而强大的气息",
                        "眼中蕴含着智慧的光芒",
                        "身上有着神秘的纹路"
                    ],
                    "stat_multiplier": 2.0
                }
            ],
            
            EventType.TREASURE: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "发现宝箱",
                        "获得金币",
                        "找到财宝"
                    ],
                    "description_templates": [
                        "你发现了一个{chest_type}，里面装着{treasure_content}。",
                        "在地上找到了一个{chest_type}，{treasure_content}。",
                        "偶然间发现了{chest_type}，{treasure_content}。"
                    ],
                    "chest_types": ["普通木箱", "小铁盒", "旧布袋"],
                    "treasure_contents": [
                        "一些金币",
                        "零散的银两",
                        "少量的钱财"
                    ],
                    "gold_range": (5, 20)
                },
                {
                    "rarity": EventRarity.UNCOMMON,
                    "title_templates": [
                        "神秘宝箱",
                        "珍贵财宝",
                        "意外收获"
                    ],
                    "description_templates": [
                        "你发现了一个{chest_type}，{treasure_content}。",
                        "找到了一个精致的{chest_type}，{treasure_content}。"
                    ],
                    "chest_types": ["雕花木箱", "铜制宝箱", "精致锦盒"],
                    "treasure_contents": [
                        "不少金币和一颗宝石",
                        "一些银两和一本秘籍残页",
                        "金币和一瓶伤药"
                    ],
                    "gold_range": (20, 50),
                    "bonus_chance": 0.3
                },
                {
                    "rarity": EventRarity.RARE,
                    "title_templates": [
                        "古代宝箱",
                        "传说宝藏",
                        "天降横财"
                    ],
                    "description_templates": [
                        "你发现了一个{chest_type}，{treasure_content}。",
                        "找到了一个散发着神秘气息的{chest_type}，{treasure_content}。"
                    ],
                    "chest_types": ["古代石匣", "神秘玉盒", "龙纹宝箱"],
                    "treasure_contents": [
                        "大量金币和一本武功秘籍",
                        "珍贵的宝石和一瓶灵丹妙药",
                        "金币和一把神兵利器"
                    ],
                    "gold_range": (50, 150),
                    "bonus_chance": 0.7
                }
            ],
            
            EventType.STORY: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "江湖见闻",
                        "偶遇高人",
                        "武学感悟"
                    ],
                    "description_templates": [
                        "你{story_event}，{story_result}。",
                        "在{location}，你{story_event}，{story_result}。",
                        "{story_event}，让你{story_result}。"
                    ],
                    "story_events": [
                        "遇到了一位神秘的老者",
                        "发现了一座古老的石碑",
                        "救助了一只受伤的小动物",
                        "观察了一处美丽的风景",
                        "遇到了一位同道中人",
                        "在客栈听到了江湖传说"
                    ],
                    "story_results": [
                        "对武学有了新的理解",
                        "内心感到平静",
                        "获得了一些启发",
                        "武学境界有所提升",
                        "对江湖有了更深的认识"
                    ],
                    "exp_range": (5, 15)
                },
                {
                    "rarity": EventRarity.UNCOMMON,
                    "title_templates": [
                        "奇遇高人",
                        "武学顿悟",
                        "江湖历练"
                    ],
                    "description_templates": [
                        "你{story_event}，{story_result}。",
                        "在{location}，你{story_event}，{story_result}。"
                    ],
                    "story_events": [
                        "遇到了一位隐世高人",
                        "偶然间观看了两位高手的对决",
                        "在古寺中听高僧讲经",
                        "见证了江湖中的恩怨情仇"
                    ],
                    "story_results": [
                        "领悟了武学的精髓",
                        "内力有所精进",
                        "招式更加纯熟",
                        "心境得到了升华"
                    ],
                    "exp_range": (15, 30)
                }
            ],
            
            EventType.MERCHANT: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "遇到商人",
                        "江湖货郎",
                        "行商"
                    ],
                    "description_templates": [
                        "你遇到了一位{merchant_type}，{merchant_description}。",
                        "路边站着一位{merchant_type}，{merchant_description}。"
                    ],
                    "merchant_types": ["普通商人", "江湖货郎", "行脚商人"],
                    "merchant_descriptions": [
                        "他看起来很友善",
                        "他有很多货物",
                        "他愿意与你交易"
                    ]
                },
                {
                    "rarity": EventRarity.UNCOMMON,
                    "title_templates": [
                        "神秘商人",
                        "古董商",
                        "异域商人"
                    ],
                    "description_templates": [
                        "你遇到了一位{merchant_type}，{merchant_description}。",
                        "一位神秘的{merchant_type}出现在你面前，{merchant_description}。"
                    ],
                    "merchant_types": ["神秘商人", "古董商", "异域商人"],
                    "merchant_descriptions": [
                        "他有一些稀有的货物",
                        "他的商品看起来很珍贵",
                        "他声称有来自远方的宝物"
                    ]
                }
            ],
            
            EventType.ENCOUNTER: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "江湖偶遇",
                        "奇遇",
                        "意外发现"
                    ],
                    "description_templates": [
                        "你{encounter_event}，{encounter_result}。",
                        "在旅途中，你{encounter_event}，{encounter_result}。"
                    ],
                    "encounter_events": [
                        "遇到了一位受伤的侠客",
                        "发现了一处废弃的洞府",
                        "救助了一位被欺负的平民",
                        "看到了一场比武招亲"
                    ],
                    "encounter_results": [
                        "获得了他的感谢",
                        "在洞府中找到了一些有用的东西",
                        "得到了一些报酬",
                        "对江湖有了新的认识"
                    ]
                }
            ],
            
            EventType.TRAP: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "遭遇陷阱",
                        "危险情况",
                        "意外伤害"
                    ],
                    "description_templates": [
                        "你{trap_event}，{trap_result}。",
                        "不小心{trap_event}，{trap_result}。"
                    ],
                    "trap_events": [
                        "踩到了一个陷阱",
                        "被暗器所伤",
                        "中了埋伏",
                        "遇到了机关"
                    ],
                    "trap_results": [
                        "受到了一些伤害",
                        "损失了一些体力",
                        "幸好反应及时"
                    ],
                    "damage_range": (5, 15)
                }
            ],
            
            EventType.TRAINING: [
                {
                    "rarity": EventRarity.COMMON,
                    "title_templates": [
                        "修炼机会",
                        "武学进境",
                        "内力增长"
                    ],
                    "description_templates": [
                        "你{training_event}，{training_result}。",
                        "在{location}，你{training_event}，{training_result}。"
                    ],
                    "training_events": [
                        "找到了一处适合修炼的地方",
                        "偶然间领悟了武学要义",
                        "通过冥想提升了内力",
                        "练习招式时有所突破"
                    ],
                    "training_results": [
                        "内力有所增长",
                        "武学境界提升",
                        "招式更加纯熟",
                        "身体素质增强"
                    ],
                    "stat_bonus_range": (1, 3)
                }
            ]
        }
    
    def generate_event(self, player, location: str = None) -> Dict[str, Any]:
        """生成随机事件"""
        # 根据玩家等级和位置调整事件权重
        event_weights = self._calculate_event_weights(player, location)
        
        # 选择事件类型
        event_type = self._weighted_random_choice(event_weights)
        
        # 选择事件稀有度
        rarity = self._select_rarity(player)
        
        # 生成具体事件
        event = self._generate_specific_event(event_type, rarity, player, location)
        
        return event
    
    def _calculate_event_weights(self, player, location: str = None) -> Dict[EventType, int]:
        """计算事件权重"""
        base_weights = {
            EventType.COMBAT: 30,
            EventType.TREASURE: 25,
            EventType.STORY: 20,
            EventType.MERCHANT: 10,
            EventType.ENCOUNTER: 8,
            EventType.TRAP: 5,
            EventType.TRAINING: 2
        }
        
        # 根据玩家等级调整权重
        if player.level <= 5:
            base_weights[EventType.COMBAT] = 20
            base_weights[EventType.STORY] = 30
            base_weights[EventType.TREASURE] = 30
        elif player.level >= 20:
            base_weights[EventType.COMBAT] = 35
            base_weights[EventType.ENCOUNTER] = 15
            base_weights[EventType.TRAINING] = 10
        
        # 根据位置调整权重
        if location:
            if location == "forest":
                base_weights[EventType.COMBAT] += 10
                base_weights[EventType.TRAP] += 5
            elif location == "city":
                base_weights[EventType.MERCHANT] += 15
                base_weights[EventType.ENCOUNTER] += 10
            elif location == "temple":
                base_weights[EventType.TRAINING] += 10
                base_weights[EventType.STORY] += 10
            elif location == "desert":
                base_weights[EventType.TRAP] += 10
                base_weights[EventType.TREASURE] += 5
        
        return base_weights
    
    def _select_rarity(self, player) -> EventRarity:
        """选择事件稀有度"""
        # 根据玩家等级调整稀有度权重
        rarity_weights = self.rarity_weights.copy()
        
        if player.level <= 5:
            rarity_weights[EventRarity.COMMON] += 20
            rarity_weights[EventRarity.LEGENDARY] = 0
        elif player.level >= 15:
            rarity_weights[EventRarity.COMMON] -= 10
            rarity_weights[EventRarity.RARE] += 5
            rarity_weights[EventRarity.EPIC] += 3
            rarity_weights[EventRarity.LEGENDARY] += 2
        
        return self._weighted_random_choice(rarity_weights)
    
    def _weighted_random_choice(self, weights: Dict) -> Any:
        """加权随机选择"""
        items = list(weights.keys())
        weights_list = list(weights.values())
        return random.choices(items, weights=weights_list)[0]
    
    def _generate_specific_event(self, event_type: EventType, rarity: EventRarity, 
                               player, location: str = None) -> Dict[str, Any]:
        """生成具体事件内容"""
        templates = self.event_templates.get(event_type, [])
        
        # 筛选符合稀有度的模板
        valid_templates = [t for t in templates if t["rarity"] == rarity]
        
        if not valid_templates:
            # 如果没有符合稀有度的模板，使用该类型的第一个模板
            valid_templates = templates[:1]
        
        template = random.choice(valid_templates)
        
        event = {
            "type": event_type.value,
            "rarity": rarity.value,
            "title": "",
            "description": "",
            "effects": {},
            "choices": []
        }
        
        # 根据事件类型生成具体内容
        if event_type == EventType.COMBAT:
            self._generate_combat_event(event, template, player)
        elif event_type == EventType.TREASURE:
            self._generate_treasure_event(event, template, player)
        elif event_type == EventType.STORY:
            self._generate_story_event(event, template, player, location)
        elif event_type == EventType.MERCHANT:
            self._generate_merchant_event(event, template, player)
        elif event_type == EventType.ENCOUNTER:
            self._generate_encounter_event(event, template, player, location)
        elif event_type == EventType.TRAP:
            self._generate_trap_event(event, template, player)
        elif event_type == EventType.TRAINING:
            self._generate_training_event(event, template, player, location)
        
        return event
    
    def _generate_combat_event(self, event: Dict, template: Dict, player):
        """生成战斗事件"""
        enemy_key = random.choice(list(self.game_data.enemies.keys()))
        enemy = self.game_data.enemies[enemy_key].copy()
        
        # 应用属性倍数
        stat_multiplier = template.get("stat_multiplier", 1.0)
        if stat_multiplier > 1.0:
            enemy["hp"] = int(enemy["hp"] * stat_multiplier)
            enemy["attack"] = int(enemy["attack"] * stat_multiplier)
            enemy["exp"] = int(enemy["exp"] * stat_multiplier)
            enemy["gold"] = int(enemy["gold"] * stat_multiplier)
            enemy["name"] = f"{template['title_templates'][0].format(enemy=enemy['name'])}"
        
        event["title"] = random.choice(template["title_templates"]).format(enemy=enemy["name"])
        event["description"] = random.choice(template["description_templates"]).format(
            enemy=enemy["name"],
            enemy_description=random.choice(template["enemy_descriptions"])
        )
        event["effects"]["enemy"] = enemy
    
    def _generate_treasure_event(self, event: Dict, template: Dict, player):
        """生成宝藏事件"""
        gold_range = template["gold_range"]
        gold_found = random.randint(gold_range[0], gold_range[1])
        
        event["title"] = random.choice(template["title_templates"])
        event["description"] = random.choice(template["description_templates"]).format(
            chest_type=random.choice(template["chest_types"]),
            treasure_content=random.choice(template["treasure_contents"])
        )
        event["effects"]["gold"] = gold_found
        
        # 添加奖励机会
        if template.get("bonus_chance", 0) > random.random():
            event["effects"]["bonus"] = "special_item"
            event["description"] += " 还有一些特殊的收获！"
    
    def _generate_story_event(self, event: Dict, template: Dict, player, location: str = None):
        """生成故事事件"""
        exp_range = template["exp_range"]
        exp_gained = random.randint(exp_range[0], exp_range[1])
        
        location_text = location or self.game_data.locations.get(player.location, {}).get("name", "未知地点")
        
        event["title"] = random.choice(template["title_templates"])
        event["description"] = random.choice(template["description_templates"]).format(
            story_event=random.choice(template["story_events"]),
            story_result=random.choice(template["story_results"]),
            location=location_text
        )
        event["effects"]["exp"] = exp_gained
    
    def _generate_merchant_event(self, event: Dict, template: Dict, player):
        """生成商人事件"""
        event["title"] = random.choice(template["title_templates"])
        event["description"] = random.choice(template["description_templates"]).format(
            merchant_type=random.choice(template["merchant_types"]),
            merchant_description=random.choice(template["merchant_descriptions"])
        )
        event["effects"]["merchant_type"] = "normal"
        event["choices"] = ["查看商品", "离开"]
    
    def _generate_encounter_event(self, event: Dict, template: Dict, player, location: str = None):
        """生成奇遇事件"""
        location_text = location or self.game_data.locations.get(player.location, {}).get("name", "未知地点")
        
        event["title"] = random.choice(template["title_templates"])
        event["description"] = random.choice(template["description_templates"]).format(
            encounter_event=random.choice(template["encounter_events"]),
            encounter_result=random.choice(template["encounter_results"]),
            location=location_text
        )
        event["effects"]["special"] = True
    
    def _generate_trap_event(self, event: Dict, template: Dict, player):
        """生成陷阱事件"""
        damage_range = template["damage_range"]
        damage = random.randint(damage_range[0], damage_range[1])
        
        event["title"] = random.choice(template["title_templates"])
        event["description"] = random.choice(template["description_templates"]).format(
            trap_event=random.choice(template["trap_events"]),
            trap_result=random.choice(template["trap_results"])
        )
        event["effects"]["damage"] = damage
    
    def _generate_training_event(self, event: Dict, template: Dict, player, location: str = None):
        """生成修炼事件"""
        stat_bonus_range = template["stat_bonus_range"]
        stat_bonus = random.randint(stat_bonus_range[0], stat_bonus_range[1])
        
        location_text = location or self.game_data.locations.get(player.location, {}).get("name", "未知地点")
        
        event["title"] = random.choice(template["title_templates"])
        event["description"] = random.choice(template["description_templates"]).format(
            training_event=random.choice(template["training_events"]),
            training_result=random.choice(template["training_results"]),
            location=location_text
        )
        event["effects"]["stat_bonus"] = stat_bonus
