# 武侠文字冒险游戏 - 安装和运行指南

## 🎮 游戏简介
这是一个基于Python Flask开发的武侠题材文字冒险游戏，支持在浏览器中游玩。游戏包含角色创建、探索、战斗、升级、装备购买等经典RPG元素。

## 📋 系统要求
- Python 3.7 或更高版本
- PyCharm IDE (推荐)
- 现代浏览器 (Chrome、Firefox、Safari、Edge)

## 🚀 安装步骤

### 1. 创建项目文件夹
```bash
mkdir wuxia_game
cd wuxia_game
```

### 2. 创建虚拟环境 (推荐)
```bash
python -m venv venv

# Windows激活虚拟环境
venv\Scripts\activate

# macOS/Linux激活虚拟环境
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install flask
```

### 4. 创建项目结构
```
wuxia_game/
├── app.py                  # 主应用文件
├── templates/
│   └── index.html         # 游戏界面模板
└── requirements.txt       # 依赖列表 (可选)
```

### 5. 复制代码文件
- 将第一个代码块保存为 `app.py`
- 创建 `templates` 文件夹
- 将模板代码保存为 `templates/index.html`

### 6. 创建requirements.txt (可选)
```text
Flask==2.3.3
```

## 🎯 在PyCharm中运行

### 方法1: 直接运行
1. 用PyCharm打开项目文件夹
2. 确保已安装Flask: `File → Settings → Project → Python Interpreter`
3. 右键点击 `app.py` → `Run 'app'`
4. 在浏览器中访问 `http://localhost:5000`

### 方法2: 配置运行配置
1. 点击 `Run → Edit Configurations`
2. 点击 `+` → `Python`
3. 配置如下：
   - Name: `Wuxia Game`
   - Script path: 选择你的 `app.py` 文件
   - Working directory: 项目根目录
4. 点击 `Apply` 和 `OK`
5. 选择配置并点击运行按钮

## 🎮 游戏特性

### 角色系统
- **武学流派**: 剑宗、拳法、内功、轻功
- **属性**: 生命值、攻击力、等级、经验值、金币
- **升级系统**: 击败敌人获得经验值，升级提升属性

### 探索系统
- **随机事件**: 遇敌、寻宝、剧情事件
- **多种敌人**: 山贼、恶狼、刺客、虎王
- **战斗机制**: 回合制战斗，可攻击或逃跑

### 装备系统
- **武器商店**: 购买更强大的武器
- **武器种类**: 木剑、铁剑、钢剑、屠龙刀
- **价格机制**: 根据武器攻击力计算价格

### 游戏功能
- **存档系统**: 使用Session自动保存游戏进度
- **休息系统**: 花费金币恢复生命值
- **实时更新**: 动态显示角色状态和战斗信息
- **响应式界面**: 适配不同屏幕尺寸

## 🎯 游戏玩法

### 开始游戏
1. 输入角色姓名
2. 选择武学流派（影响初始属性）
3. 点击"开始冒险"

### 基本操作
- **🗺️ 探索**: 随机遇到事件，获得经验和金币
- **💤 休息**: 花费10金币完全恢复生命值
- **🏪 商店**: 购买更强大的武器装备

### 战斗系统
- **⚔️ 攻击**: 对敌人造成伤害
- **🏃 逃跑**: 70%概率成功逃离战斗
- **胜利奖励**: 获得经验值和金币
- **升级**: 达到经验要求自动升级

### 策略提示
1. **合理分配资源**: 平衡休息费用和武器购买
2. **选择战斗**: 生命值过低时及时逃跑或休息
3. **装备升级**: 优先购买攻击力更高的武器
4. **经验积累**: 多探索获得经验值快速升级

## 🛠️ 故障排除

### 常见问题

**问题1: 无法启动Flask应用**
```bash
# 检查Python版本
python --version

# 检查Flask是否安装
pip list | grep Flask

# 重新安装Flask
pip install --upgrade flask
```

**问题2: 浏览器无法访问游戏**
- 确保Flask应用正在运行
- 检查端口5000是否被占用
- 尝试访问 `http://127.0.0.1:5000`

**问题3: 游戏数据丢失**
- 游戏使用Session存储，关闭浏览器会丢失数据
- 如需持久化存储，可以改用数据库

**问题4: PyCharm中无法运行**
- 确保选择了正确的Python解释器
- 检查项目结构是否正确
- 尝试重启PyCharm

### 端口配置
如果5000端口被占用，可以修改 `app.py` 最后一行：
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # 改为8080端口
```

## 🔧 扩展功能

### 可以添加的功能
1. **数据库存储**: 使用SQLite持久化保存游戏数据
2. **更多敌人**: 增加Boss战和特殊敌人
3. **技能系统**: 根据武学流派添加特殊技能
4. **地图系统**: 增加不同的探索区域
5. **任务系统**: 添加NPC和任务线
6. **多人功能**: 支持多玩家排行榜

### 代码扩展示例
```python
# 添加新武学流派
martial_arts = {
    "剑宗": {"attack_bonus": 5, "hp_bonus": 0},
    "拳法": {"attack_bonus": 3, "hp_bonus": 20},
    "内功": {"attack_bonus": 2, "hp_bonus": 30},
    "轻功": {"attack_bonus": 4, "hp_bonus": 10}
}

# 添加新敌人
new_enemies = {
    "dragon": {"name": "青龙", "hp": 200, "attack": 40, "exp": 200, "gold": 100}
}
```

## 📝 开发说明

### 技术栈
- **后端**: Python Flask
- **前端**: HTML + CSS + JavaScript
- **数据存储**: Flask Session
- **开发环境**: PyCharm

### 代码结构
- `Player类`: 管理角色数据和行为
- `GameData类`: 存储游戏静态数据
- `Flask路由`: 处理前后端交互
- `JavaScript`: 处理用户界面交互

### 安全注意事项
- 当前版本使用简单的Session存储
- 生产环境建议使用数据库和用户认证
- 添加输入验证和错误处理

## 🎊 开始游戏

完成以上步骤后：
1. 在PyCharm中运行 `app.py`
2. 打开浏览器访问 `http://localhost:5000`
3. 创建你的武侠角色
4. 开始你的江湖冒险之旅！

---

**祝你在武侠世界中获得无穷乐趣！如有问题，请检查代码和配置。**