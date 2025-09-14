# 武侠文字冒险游戏 - 优化版本

## 项目结构说明

本项目采用了模块化的设计，将原有单一文件拆分为多个模块，便于维护和扩展。

### 目录结构

```
Game-WuxiaTextGame/
├── app.py                 # 应用入口
├── config.py              # 配置文件
├── requirements.txt        # 依赖列表
├── models/                # 数据模型
│   ├── __init__.py
│   ├── player.py          # 玩家模型
│   └── game_data.py       # 游戏数据模型
├── services/              # 业务逻辑
│   ├── __init__.py
│   ├── character_service.py # 角色服务
│   ├── battle_service.py   # 战斗服务
│   ├── exploration_service.py # 探索服务
│   └── shop_service.py     # 商店服务
├── api/                   # API路由
│   ├── __init__.py
│   ├── character_api.py   # 角色API
│   ├── game_api.py        # 游戏主API
│   └── shop_api.py        # 商店API
├── utils/                 # 工具函数
│   ├── __init__.py
│   └── database.py        # 数据库工具
├── templates/             # 前端模板
│   └── index.html
└── static/                # 静态资源
    ├── css/
    └── js/
```

### 主要优化点

1. **模块化设计**：将原有代码按功能拆分为多个模块
2. **数据持久化**：使用SQLite数据库存储玩家数据和游戏存档
3. **服务层分离**：将业务逻辑从路由中分离出来
4. **配置管理**：使用配置文件管理应用设置
5. **蓝图路由**：使用Flask蓝图组织API路由

### 数据库设计

本项目使用SQLite数据库存储数据，包含以下表：

1. `players`表：存储玩家基本信息
2. `saves`表：存储游戏存档数据

### 安装和运行

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用：
   ```bash
   python app.py
   ```

3. 访问应用：
   在浏览器中打开 `http://localhost:5000`

### 扩展建议

1. 添加用户认证系统
2. 增加更多游戏功能（任务系统、技能系统等）
3. 实现排行榜功能
4. 添加更多武器和敌人类型
5. 增加游戏地图系统
