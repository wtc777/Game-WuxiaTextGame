class ShopService:
    def __init__(self, game_data):
        self.game_data = game_data

    def get_shop_items(self):
        """获取商店物品列表"""
        return self.game_data.weapons

    def buy_weapon(self, player, weapon_key):
        """购买武器"""
        weapon = self.game_data.weapons.get(weapon_key)

        if not weapon:
            raise ValueError("武器不存在")

        # 简单的价格计算
        price = weapon['attack'] * 10

        if player.gold < price:
            raise ValueError(f"金币不足！需要{price}金币")

        player.gold -= price
        player.weapon = weapon_key

        return {
            'success': True,
            'weapon': weapon,
            'price': price
        }
