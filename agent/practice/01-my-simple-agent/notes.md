# Hello-Agents 学习笔记

> DataWhale Hello-Agents 教程学习与实践总结
> 
> 学习时间：2026-06-09

---

## 第一部分：实践总结

### 一、实践过程中遇到的问题

#### 1. API连接与配置问题

**问题描述**：
- 初次运行时API连接失败，报错"模型不存在"
- API密钥配置不正确，导致无法调用大模型

**解决方案**：
- 检查API端点URL是否正确（豆包API：`https://ark.cn-beijing.volces.com/api/v3/`）
- 确认模型名称是否正确（`doubao-1-5-lite-32k-250115`）
- 使用配置文件管理API密钥，避免明文编码

**学习要点**：
- API配置需要严格按照服务商文档
- 使用YAML配置文件管理敏感信息
- 配置文件模板（config.example.yaml）+ 本地配置（config.yaml）的设计模式

#### 2. 工具调用解析问题

**问题描述**：
- LLM返回的工具调用格式是 `get_weather(城市="武汉")`
- 使用中文参数名，但工具函数期望英文参数名 `city`
- 正则表达式无法匹配中文参数名

**解决方案**：
- 修改正则表达式支持中文：`[\w\u4e00-\u9fa5]+`
- 添加参数名映射表：`{'城市': 'city', '天气': 'weather'}`
- 自动将中文参数名转换为英文

**学习要点**：
- LLM的输出格式可能不符合预期，需要灵活处理
- 正则表达式是解析文本的重要工具
- 参数名映射是处理多语言输入的有效方法

#### 3. Unicode编码问题

**问题描述**：
- Windows命令行使用GBK编码
- 无法显示Unicode字符（如 ✓）
- 导致程序报错 `UnicodeEncodeError`

**解决方案**：
- 使用ASCII字符替代Unicode符号
- 输出"成功 [OK]"替代"成功 ✓"

**学习要点**：
- 不同操作系统终端编码不同
- 需要考虑跨平台兼容性

#### 4. 项目结构复杂化问题

**问题描述**：
- 初期设计过于模块化（src/agent, src/tools, src/config等）
- 文件过多，不便于初学者理解
- 违背了教程"简单易懂"的原则

**解决方案**：
- 简化为3个核心文件：agent.py, tools.py, main.py
- 删除复杂的模块化文件
- 保持结构清晰，易于学习

**学习要点**：
- 初学者项目应该简单明了
- 过度工程化会增加学习负担
- 模块化应该在理解基础后逐步引入

### 二、实践中学到的核心知识

#### 1. ReAct循环（核心机制）

**概念理解**：
ReAct = Reasoning（推理）+ Acting（行动）

**工作流程**：
```
用户输入 → 思考(Thought) → 行动(Action) → 观察(Observation) → 循环
```

**代码实现**：
```python
for iteration in range(max_iterations):
    # 1. 调用LLM思考
    response = call_llm(messages)
    
    # 2. 解析Thought和Action
    parsed = parse_response(response)
    
    # 3. 执行工具（如果是Action）
    if parsed['action_type'] == 'tool':
        observation = execute_tool(...)
        messages.append({"role": "user", "content": f"Observation: {observation}"})
    
    # 4. 返回最终答案（如果是Finish）
    elif parsed['action_type'] == 'finish':
        return parsed['action_content']
```

**关键理解**：
- Thought：LLM分析当前情况，规划下一步
- Action：调用工具或给出最终答案
- Observation：工具返回的结果，作为下一轮思考的输入

#### 2. 系统提示词设计

**核心要素**：
```python
SYSTEM_PROMPT = """
你是一个智能旅行助手，可以帮助用户查询天气并推荐旅游景点。

你可以使用以下工具：
- get_weather: 查询指定城市的天气信息
- get_attraction: 根据城市和天气推荐旅游景点

请按照以下格式思考和行动：
Thought: 分析用户需求，思考下一步该做什么
Action: 调用工具：工具名(参数1="值1", 参数2="值2")
Observation: 工具返回的结果（由系统自动填充）

当你完成任务时，使用以下格式给出最终答案：
Action: Finish[最终答案内容]
"""
```

**设计要点**：
- 明确角色定位（智能旅行助手）
- 列出可用工具及其功能
- 规定输出格式（Thought/Action/Observation）
- 指明结束条件（Finish）

#### 3. 工具函数设计

**核心原则**：
- 工具函数应该简单、单一职责
- 清晰的函数签名和文档字符串
- 支持降级机制（真实API失败时使用模拟数据）

**示例**：
```python
def get_weather(city: str, use_real: bool = False) -> str:
    """
    查询指定城市的天气信息
    
    Args:
        city: 城市名称（中文）
        use_real: 是否使用真实API（默认False使用模拟数据）
        
    Returns:
        str: 天气描述字符串
    """
    if use_real:
        # 尝试调用真实API
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            return parse_weather(response.json())
        except:
            pass  # 降级到模拟数据
    
    # 使用模拟数据
    return f"{city}当前天气：晴朗，气温25摄氏度"
```

#### 4. 配置化管理

**总开关设计**：
```yaml
# 总开关：控制真实API还是模拟数据
use_real_api: false

# 大模型配置
model:
  api_key: "your-api-key"
  base_url: "https://ark.cn-beijing.volces.com/api/v3/"
  model_name: "doubao-1-5-lite-32k-250115"

# 搜索API配置（可选）
search:
  tavily_api_key: "your-tavily-api-key"
```

**设计要点**：
- 一个参数控制所有（use_real_api）
- API密钥不明文编码
- 配置模板 + 本地配置的设计模式

#### 5. 降级机制

**实现方式**：
```python
def get_attraction(city, weather, use_real=False, api_key=""):
    if use_real and api_key:
        # 尝试真实搜索
        try:
            from tavily import TavilyClient
            tavily = TavilyClient(api_key=api_key)
            response = tavily.search(query=f"{city}景点推荐")
            return response["answer"]
        except:
            pass  # 网络错误，降级
    
    # 使用模拟数据
    return f"推荐{city}的著名景点"
```

**关键理解**：
- 真实API可能失败（网络、密钥无效等）
- 降级机制保证程序不会崩溃
- 模拟数据适合学习和测试

---

## 第二部分：第一章知识提炼（小白认知学习笔记）

### 一、什么是智能体？

#### 1. 核心定义

**智能体（Agent）** 是任何能够：
- 通过**传感器（Sensors）** 感知**环境（Environment）**
- **自主** 地通过**执行器（Actuators）** 采取**行动（Action）**
- 以达成特定目标的实体

**四个基本要素**：
1. **环境**：智能体所处的外部世界（如道路、金融市场）
2. **传感器**：感知环境的工具（如摄像头、API）
3. **执行器**：改变环境的工具（如机械臂、代码执行）
4. **自主性**：独立决策的能力（不是被动响应）

#### 2. 传统智能体的演进

**演进路径**：简单 → 复杂 → 学习

| 类型 | 特点 | 示例 |
|------|------|------|
| **反射智能体** | 条件-动作规则，无记忆 | 恒温器（温度高→制冷） |
| **模型智能体** | 有内部世界模型，有记忆 | 自动驾驶（隧道中仍知道前方有车） |
| **目标智能体** | 主动规划，有预见性 | GPS导航（规划最优路径） |
| **效用智能体** | 多目标权衡，最大化效用 | 交易算法（时间、成本、风险权衡） |
| **学习智能体** | 通过经验自我改进 | AlphaGo（自我对弈学习） |

**关键理解**：
- 从被动反应 → 主动规划 → 自我学习
- 智能体的"智能"体现在自主决策能力

#### 3. LLM驱动的新范式

**核心区别**：

| 维度 | 传统智能体 | LLM智能体 |
|------|-----------|----------|
| **核心引擎** | 规则/模型/效用函数 | 大语言模型 |
| **知识来源** | 人类显式编程 | 海量数据预训练 |
| **交互方式** | 结构化指令 | 自然语言对话 |
| **能力边界** | 确定且有边界 | 灵活且通用 |

**LLM智能体的三大能力**：
1. **规划与推理**：分解高层目标为子任务
2. **工具使用**：识别信息缺口，主动调用外部工具
3. **动态修正**：根据反馈调整行为

**示例**：智能旅行助手
- 用户："规划一次厦门之旅"
- 智能体：`[确认偏好] → [查询天气] → [制定行程] → [预订票务]`
- 工具调用：天气API、地图API、预订网站
- 动态修正：用户反馈"酒店太贵" → 重新搜索

### 二、智能体的运行原理

#### 1. PEAS模型（任务环境定义）

**PEAS = Performance + Environment + Actuators + Sensors**

**示例**：智能旅行助手

| 维度 | 描述 |
|------|------|
| **性能度量** | 用户满意度、行程合理性 |
| **环境** | 天气数据、地图数据、预订系统 |
| **执行器** | 调用API、生成推荐、发送消息 |
| **传感器** | 接收用户输入、API返回数据 |

#### 2. ReAct循环（核心运行机制）

**ReAct = Reasoning + Acting**

**工作流程**：
```
1. 用户输入："查询北京天气并推荐景点"
2. Thought: "需要先查询天气，再推荐景点"
3. Action: get_weather(city="北京")
4. Observation: "北京晴朗，25℃"
5. Thought: "已知天气晴朗，推荐户外景点"
6. Action: get_attraction(city="北京", weather="晴朗")
7. Observation: "推荐颐和园、天安门"
8. Thought: "已完成任务，给出最终答案"
9. Action: Finish[北京晴朗，推荐颐和园]
```

**关键理解**：
- Thought：思考当前状态和下一步
- Action：执行工具或给出答案
- Observation：工具结果作为下一轮输入
- 循环直到Finish

#### 3. 智能体的感知与行动

**感知（Perception）**：
- 接收用户输入（自然语言）
- 接收工具返回（结构化数据）
- 维护对话历史（上下文）

**行动（Action）**：
- 调用工具（API、函数）
- 生成回复（自然语言）
- 更新状态（对话历史）

### 三、智能体的类型

#### 1. 基于内部决策架构

- **反应式**：简单条件-动作规则
- **模型式**：有内部世界模型
- **目标式**：主动规划达成目标
- **效用式**：多目标权衡优化
- **学习式**：通过经验自我改进

#### 2. 基于时间与反应性

- **反应性智能体**：立即响应，追求速度
- **规划性智能体**：深思熟虑，追求最优
- **混合式智能体**：结合两者优点

**LLM智能体的混合模式**：
- 思考阶段：规划（审慎）
- 行动阶段：反应（快速）
- 观察阶段：反馈（即时）

#### 3. 基于知识表示

| 类型 | 知识形式 | 特点 |
|------|---------|------|
| **符号主义AI** | 显式规则、逻辑 | 可解释、脆弱 |
| **亚符号主义AI** | 隐式模式、神经网络 | 强大、黑箱 |
| **神经符号主义AI** | 混合两者 | 兼具直觉与理性 |

**LLM智能体 = 神经符号主义实践**：
- 核心：神经网络（模式识别、语言生成）
- 输出：结构化符号（Thought、Action、API调用）

### 四、动手实践：5分钟实现第一个智能体

#### 1. 准备工作

**依赖安装**：
```bash
pip install openai requests pyyaml
```

**配置文件**：
```yaml
model:
  api_key: "your-api-key"
  base_url: "https://ark.cn-beijing.volces.com/api/v3/"
  model_name: "doubao-1-5-lite-32k-250115"
```

#### 2. 核心代码结构

**三个核心文件**：
1. `agent.py`：ReAct循环实现
2. `tools.py`：工具函数定义
3. `main.py`：主程序入口

**agent.py核心逻辑**：
```python
class SimpleAgent:
    def run(self, user_input):
        messages = [{"role": "user", "content": user_input}]
        
        for iteration in range(max_iterations):
            # 1. 调用LLM
            response = self._call_llm(messages)
            
            # 2. 解析Thought和Action
            parsed = self._parse_response(response)
            
            # 3. 执行工具
            if parsed['action_type'] == 'tool':
                observation = self._execute_tool(...)
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            
            # 4. 返回答案
            elif parsed['action_type'] == 'finish':
                return parsed['action_content']
```

#### 3. 运行示例

**用户输入**：
```
"你好，请帮我查询一下今天武汉的天气，然后根据天气推荐一个合适的旅游景点。"
```

**智能体运行**：
```
--- 第 1 轮思考 ---
Thought: 用户想了解武汉天气并获取推荐景点，首先调用get_weather
Action: get_weather(city="武汉")
Observation: 武汉当前天气：Smog，气温22摄氏度

--- 第 2 轮思考 ---
Thought: 已知武汉天气雾霾，调用get_attraction推荐景点
Action: get_attraction(city="武汉", weather="Smog")
Observation: 推荐黄鹤楼和东湖，适合雾霾天气

--- 第 3 轮思考 ---
Action: Finish[武汉雾霾，推荐黄鹤楼和东湖]
```

### 五、关键概念总结

#### 1. 核心概念

| 概念 | 定义 | 重要性 |
|------|------|--------|
| **智能体** | 感知环境、自主行动的实体 | ⭐⭐⭐⭐⭐ |
| **ReAct** | Reasoning + Acting循环 | ⭐⭐⭐⭐⭐ |
| **自主性** | 独立决策的能力 | ⭐⭐⭐⭐⭐ |
| **工具调用** | 执行外部函数获取信息 | ⭐⭐⭐⭐ |
| **降级机制** | API失败时使用模拟数据 | ⭐⭐⭐⭐ |
| **系统提示词** | 规定智能体行为规则 | ⭐⭐⭐⭐⭐ |

#### 2. 设计原则

1. **简单优先**：初学者项目应该简单明了
2. **配置化管理**：API密钥不明文编码
3. **降级机制**：保证程序不会崩溃
4. **总开关设计**：一键切换真实/mock模式
5. **清晰文档**：函数签名和文档字符串

#### 3. 学习路径

**推荐顺序**：
1. 理解智能体定义和ReAct循环
2. 阅读agent.py理解核心逻辑
3. 阅读tools.py理解工具设计
4. 运行main.py体验完整流程
5. 修改配置尝试真实API
6. 扩展新的工具函数

---

## 第三部分：实践心得

### 一、从理论到实践的跨越

**理论理解**：
- 智能体是感知环境、自主行动的实体
- ReAct循环是核心运行机制

**实践体会**：
- 理论简单，实现细节复杂
- LLM输出格式可能不符合预期
- 需要处理各种边界情况

### 二、工程化思维的重要性

**配置化管理**：
- 不明文编码API密钥
- 使用配置模板 + 本地配置
- 总开关设计简化操作

**降级机制**：
- 真实API可能失败
- 模拟数据保证可用性
- 适合学习和测试

### 三、调试与问题解决

**调试技巧**：
- 添加调试信息查看解析过程
- 分步验证每个环节
- 从简单到复杂逐步调试

**问题解决思路**：
1. 理解问题本质（中文参数名无法匹配）
2. 找到根本原因（正则表达式不支持中文）
3. 设计解决方案（参数名映射）
4. 验证修复效果（运行测试）

### 四、下一步学习方向

**短期目标**：
- 深入理解ReAct循环的实现细节
- 学习更多工具函数的设计模式
- 掌握系统提示词的优化技巧

**长期目标**：
- 学习更复杂的智能体架构（如多智能体协作）
- 探索强化学习在智能体中的应用
- 构建实际应用场景的智能体系统

---

## 参考资料

- [DataWhale Hello-Agents教程](https://datawhalechina.github.io/hello-agents/)
- [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

---

**学习日期**：2026-06-09
**实践项目**：智能旅行助手
**学习状态**：已完成第一章学习与实践