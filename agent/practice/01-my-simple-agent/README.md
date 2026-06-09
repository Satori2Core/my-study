# 智能旅行助手 - Hello-Agents实践

基于 DataWhale Hello-Agents 教程的简化版智能体实现，适合初学者学习。

## 项目特点

- **简单易懂**：按照教程原始结构，核心代码只有3个文件
- **配置化**：通过配置文件控制真实API或模拟数据
- **降级机制**：API失败时自动降级到模拟数据
- **总开关设计**：一键切换真实/mock模式

## 项目结构

```
my-simple-agent/
├── agent.py          # 核心Agent循环（ReAct模式）
├── tools.py          # 工具定义（天气查询、景点推荐）
├── main.py           # 主程序入口
├── config.example.yaml  # 配置模板
├── requirements.txt  # 依赖列表
├── README.md         # 说明文档
└── QA.md             # 学习笔记
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制配置模板并填入你的API密钥：

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`，填入你的豆包API密钥：

```yaml
model:
  api_key: "your-real-api-key"  # 替换为真实密钥
```

### 3. 运行程序

```bash
python main.py
```

## 配置说明

### 总开关：use_real_api

配置文件中的 `use_real_api` 控制运行模式：

- `false`（默认）：使用模拟数据，无需API密钥，适合学习
- `true`：使用真实API调用，需要有效的API密钥

### 真实模式启动流程

当 `use_real_api: true` 时：

1. 自动测试大模型API是否可用
2. 自动测试Tavily搜索API（如果配置了）
3. API不可用时自动降级到模拟数据

## 核心代码说明

### agent.py - ReAct循环

核心流程：**思考 → 行动 → 观察 → 循环**

```python
# 系统提示词模板
SYSTEM_PROMPT = """
请按照以下格式思考和行动：
Thought: 分析用户需求，思考下一步该做什么
Action: 调用工具：工具名(参数1="值1", 参数2="值2")
Observation: 工具返回的结果

完成任务时：
Action: Finish[最终答案内容]
"""

# ReAct循环
for iteration in range(max_iterations):
    response = call_llm(messages)
    parsed = parse_response(response)
    
    if parsed['action_type'] == 'finish':
        return parsed['action_content']
    
    elif parsed['action_type'] == 'tool':
        observation = execute_tool(...)
        messages.append({"role": "user", "content": f"Observation: {observation}"})
```

### tools.py - 工具定义

两个核心工具：

1. `get_weather(city)` - 查询天气
2. `get_attraction(city, weather)` - 推荐景点

支持真实API和模拟数据降级：

```python
def get_weather(city, use_real=False):
    if use_real:
        # 尝试调用真实API
        try:
            response = requests.get(f"https://wttr.in/{city}?format=j1")
            return parse_weather(response.json())
        except:
            pass  # 降级到模拟数据
    
    # 使用模拟数据
    return f"{city}当前天气：晴朗，气温25摄氏度"
```

## 运行示例

### 模拟模式（默认）

```
============================================================
智能旅行助手 - DataWhale Hello-Agents实践
============================================================

模式: 模拟数据（适合学习和测试）

============================================================
智能旅行助手 - Agent运行中
============================================================
用户请求: 你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。

--- 第 1 轮思考 ---
Agent思考:
Thought: 首先调用get_weather工具查询北京今天的天气
Action: 调用工具：get_weather(city="北京")

执行工具: get_weather({'city': '北京'})
工具返回: 北京当前天气：晴朗，气温25摄氏度

--- 第 2 轮思考 ---
Agent思考:
Thought: 已知北京天气晴朗，调用get_attraction工具推荐景点
Action: 调用工具：get_attraction(city="北京", weather="晴朗")

执行工具: get_attraction({'city': '北京', 'weather': '晴朗'})
工具返回: 推荐您去颐和园或天安门广场，天气好适合户外活动

--- 第 3 轮思考 ---
Action: Finish[北京当前天气晴朗，气温25摄氏度。推荐您去颐和园或天安门广场游玩。]

最终答案:
北京当前天气晴朗，气温25摄氏度。推荐您去颐和园或天安门广场游玩。

============================================================
任务完成！
```

## 学习路径

推荐按照以下顺序学习：

1. 阅读 `agent.py` 理解ReAct循环
2. 阅读 `tools.py` 理解工具定义
3. 阅读 `main.py` 理解配置加载
4. 修改配置文件尝试真实API
5. 扩展新的工具函数

## 参考资料

- [Hello-Agents教程](https://datawhalechina.github.io/hello-agents/)
- [DataWhale开源项目](https://github.com/datawhalechina/hello-agents)

## API密钥获取

### 豆包API（火山引擎）

1. 注册火山引擎账号
2. 开通豆包大模型服务
3. 创建API密钥
4. 填入配置文件

### Tavily搜索API（可选）

1. 注册Tavily账号：https://tavily.com/
2. 创建API密钥
3. 填入配置文件（仅真实模式需要）