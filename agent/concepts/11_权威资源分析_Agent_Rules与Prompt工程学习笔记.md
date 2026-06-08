# Agent Rules 与 Prompt 工程权威资源分析

## 📚 资源概览

### 权威参考来源

| 资源名称 | 来源 | 权威性 | 链接 |
|---------|------|--------|------|
| OpenAI 提示词工程最佳实践 | OpenAI Help Center | ⭐⭐⭐⭐⭐ | [查看](https://help.openai.com/zh-hans-cn/articles/6654000-使用-openai-api-进行提示词工程的最佳实践) |
| LangChain Agents 文档 | LangChain Official | ⭐⭐⭐⭐⭐ | [查看](https://docs.langchain.com/oss/python/langchain-agents) |
| OpenAI Prompt Engineering 指南 | loooop.dev (19 sources) | ⭐⭐⭐⭐ | [查看](https://www.loooop.dev/skills/prompt-engineering/v15) |
| GPT-5.2 2026 提示词指南 | Atlabs AI | ⭐⭐⭐⭐ | [查看](https://www.atlabs.ai/blog/gpt-5.2-prompting-guide-the-2026-playbook-for-developers-agents) |
| System Prompts 与指令层级 | PractiqAI | ⭐⭐⭐⭐ | [查看](https://practiqai.com/blog/system-prompts-roles-instruction-hierarchy) |
| OpenAI 提示词完美结构 | domin.es | ⭐⭐⭐⭐ | [查看](https://domin.es/posts/estructura-perfecta-prompt-chat-gpt) |

---

## 🔍 认识：核心概念与权威框架

### 1. OpenAI 官方提示词工程最佳实践

#### 8 条核心原则

| 原则 | 说明 | ❌ 反例 | ✅ 正例 |
|------|------|--------|--------|
| **1. 使用最新模型** | 新模型更容易做提示词工程 | GPT-3.5 | GPT-5.5 / GPT-4o-mini |
| **2. 指令放在开头** | 用 `###` 或 `"""` 分隔指令与上下文 | "将文本总结...{text}" | "将文本总结...Text: \"\"\"{text}\"\"\"" |
| **3. 具体描述** | 在上下文、结果、长度、格式、风格上要具体 | "写一首关于OpenAI的诗" | "写一首简短且鼓舞人心的OpenAI主题诗，重点围绕DALL-E产品发布，以李白的风格来写" |
| **4. 示例阐明格式** | 展示期望的输出格式，而不只是说明 | "抽取实体：公司、人名、话题、主题" | "抽取实体。格式：公司名称: <list>, 人名: <list>, 具体话题: <list>, 总体主题: <list>" |
| **5. 零样本 → 少样本 → 微调** | 逐步递进的策略 | 直接微调 | 零样本尝试 → 少样本示例 → 微调 |
| **6. 减少空泛描述** | 避免模糊的表述 | "描述要简短" | "用 3-5 句话描述产品" |
| **7. 说应该做什么** | 不要只说不要做什么 | "不要询问用户名密码" | "客服将尝试诊断问题并提出解决方案，避免询问PII，引导查看帮助文章" |
| **8. 代码用引导词** | 使用关键字引导模型 | "# 写一个Python函数..." | "# 写一个Python函数...import\n" |

#### 关键洞察

> **提示词工程如何工作**：由于 OpenAI 模型的训练方式，有一些特定的提示词格式效果尤其好。

**官方起点**：OpenAI 的 [官方提示词工程指南](https://platform.openai.com/docs/guides/prompt-engineering) 是获取提示词技巧的最佳起点。

---

### 2. OpenAI 提示词完美结构（6 元素）

根据 domin.es 翻译的 OpenAI 官方解剖，一个完美的 prompt 包含 6 个关键元素：

```
┌─────────────────────────────────────────┐
│ 完美 Prompt 的 6 个元素                 │
├─────────────────────────────────────────┤
│ 1. 👤 Rol（角色）                       │
│    → 谁是 AI？                          │
│    → "Eres un profesor experto en..."   │
├─────────────────────────────────────────┤
│ 2. 📋 Tarea（任务）                     │
│    → 要做什么？                         │
│    → "Explica el teorema de Pitágoras"  │
├─────────────────────────────────────────┤
│ 3. 🌐 Contexto（上下文）                 │
│    → 为谁？为什么？                     │
│    → "Para un blog educativo..."        │
├─────────────────────────────────────────┤
│ 4. 🧠 Razonamiento（推理）              │
│    → 怎么思考？                         │
│    → "Incluye pasos claros..."          │
├─────────────────────────────────────────┤
│ 5. 📄 Formato（输出格式）               │
│    → 如何交付？                         │
│    → "Markdown 表格"                   │
├─────────────────────────────────────────┤
│ 6. ⚠️ Condiciones（条件）                │
│    → 规则与限制？                       │
│    → "Máximo 400 palabras"              │
└─────────────────────────────────────────┘
```

**反例 vs 正例**：

| 反例（模糊） | 正例（结构化） |
|------------|--------------|
| "Explícame Pitágoras" | <br>**Rol:** Eres un profesor experto en matemáticas de secundaria<br>**Tarea:** Explica el teorema de Pitágoras con un ejemplo práctico<br>**Contexto:** El contenido es para un blog educativo dirigido a adolescentes<br>**Razonamiento:** Incluye pasos claros y evita explicaciones demasiado técnicas<br>**Formato:** Markdown con título, ejemplos, y diagrama<br>**Condiciones:** Máximo 500 palabras<br> |

---

### 3. 2026 GPT-5.2 标准：CTCO 框架

根据 Atlabs AI 2026 指南，GPT-5.2 时代告别了"感觉"时代，转向结构化架构提示词。

#### CTCO 公式

```
Context (C) → Task (T) → Constraints (C) → Output (O)
  ↓            ↓           ↓               ↓
  谁？背景？   原子动作     不能做什么？    确切格式
```

**2024 风格 vs 2026 风格**：

| 2024 旧方式 ❌ | 2026 GPT-5.2 方式 ✅ |
|--------------|---------------------|
| "Write a blog post about coffee. Make it funny and interesting." | **Context:** You are a specialty coffee roaster writing for baristas<br>**Task:** Explain anaerobic fermentation<br>**Constraints:** Max 400 words. No fluff. Define technical terms.<br>**Output:** Structured HTML with <h3> headers for each phase. |

#### 推理努力（Reasoning Effort）

GPT-5.2 的新特性：推理不再自动，需要"切换"。

| 级别 | 适用场景 | Prompt Key |
|-----|---------|-----------|
| **Low/Minimal** | 迁移、格式化、数据提取 | "Directly output the result without preamble." |
| **Medium** | 常规任务 | (默认) |
| **High/Thinking** | 代码重构、复杂逻辑 | "Plan step-by-step. Verify step 2 before proceeding." |

**Plan-then-Execute 模式**：对于复杂任务，先输出 `<planning>` 块，再输出 `<response>` 块。

#### Agentic 脚手架

对于长时间运行的 Agent，使用 XML 标签维护状态：

```xml
<solution_persistence>
  Current File: auth_controller.py
  Known Bugs: Retry logic fails on 404.
</solution_persistence>

<user_updates_spec>
  Only modify the 'login' function. Do not touch models.
</user_updates_spec>
```

---

### 4. System Prompt 与指令层级

根据 PractiqAI 2025 指南，System Prompt 是"契约"，设定游戏规则。

#### 指令优先级

```
System/Developer > User > Assistant/Tool Outputs
    ↓               ↓            ↓
  游戏规则        今日任务        移动
```

**核心思想**：规则第一，任务第二。

#### System Prompt 应包含什么

| ✅ 应该包含 | ❌ 不应该包含 |
|------------|------------|
| 身份与范围（谁、限制） | 临时事实（今日日期、单次输入、URL） |
| 风格与语气（一致的声音） | 长示例 |
| 安全与政策（避免什么） | |
| 输出不变量（格式约束） | |

> **最可靠的 System Prompt**：简短、稳定、不可协商。

#### 示例与反例放置

- **硬规则编码** → System Prompt
- **任务特定示例** → User Message

---

### 5. LangChain Agents 核心概念

根据 LangChain 官方文档，Agent 结合语言模型与工具，创建能推理任务、决定使用哪个工具、迭代求解的系统。

#### Agent 循环

```
Think → Act → Observe → Repeat
  ↓      ↓        ↓         ↓
  思考    行动    观察       重复
```

**类比**：像侦探破案
- 📓 笔记本（scratchpad）记录想法
- 🧰 工具箱（APIs/functions）选择工具
- ✅ 停止时自信有答案

#### 核心组件

| 组件 | 说明 |
|-----|------|
| **Tools** | 外部函数/API，有名称和描述 |
| **LLM** | 决策模型（GPT-4o-mini, Gemini 2.0） |
| **Prompt/Scratchpad** | 指导工具使用、边界、清晰的工具区分；存储之前的行动和结果 |

#### Tool 定义示例

```python
from langchain.tools import Tool

def calculate_expression(expr: str) -> str:
    try:
        result = eval(expr)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

calc_tool = Tool(
    name="Calculator",
    description="Performs simple arithmetic. Input should be a valid Python expression, e.g. '2+2'.",
    func=calculate_expression
)
```

**关键点**：Tool 的描述应该**清晰、具体**——模糊会使 Agent 困惑，导致选错工具或误用工具。

---

### 6. System Prompt 解剖（loooop.dev）

根据 loooop.dev 19 个来源的权威指南：

```
┌─────────────────────────────────────────────┐
│ SYSTEM PROMPT 解剖                         │
├─────────────────────────────────────────────┤
│ 1. Role definition (who the model is)      │
│ 2. Task description (what it should do)    │
│ 3. Output format (how to structure results)│
│ 4. Constraints (what to avoid)            │
│ 5. Examples (few-shot demonstrations)     │
│ 6. Edge case handling (ambiguity rules)    │
└─────────────────────────────────────────────┘
```

#### 重要：指令层级

OpenAI 的 IH-Challenge（2026.3.10）强调清晰的优先级：

```
System > Developer > User > Tool
```

> 安全关键和政策约束放在 System 或 Developer 层，以保持最高优先级，抵御低优先级输入（包括工具输出和 Web 内容）的影响。

---

## 🛠️ 实践：应用这些框架

### 场景 1：学习教练 Prompt（应用 6 元素）

让我们用 OpenAI 的 6 元素结构来优化我们的学习教练 prompt。

#### 原始版本（简化）

```
你是我的专属学习教练。按照"知识点 + 实战案例 + 关联知识点 + 自动输出 Markdown 笔记"的方式教学。
```

#### 优化版本（应用 6 元素 + CTCO）

```markdown
# 👤 Rol（角色）
你是一位经验丰富的后端技术学习教练，专注于 Go、MySQL、Redis、Linux、Docker 等技术栈的系统教学。你有 10 年以上的开发经验，擅长将复杂概念拆解为易懂的内容。

# 📋 Tarea（任务）
1. 拆解知识点为核心概念（不超过 3 个）
2. 提供简单可运行的代码示例
3. 关联至少 2 个相关知识点
4. 直接输出可归档的 Markdown 文档

# 🌐 Contexto（上下文）
- 用户是后端开发者，希望系统学习技术栈
- 学习目标：达到社招要求的技术能力水平
- 笔记目录：E:\Yang\learn\my-study
- 每次新建目录前需要主动多轮询问用户

# 🧠 Razonamiento（推理）
每个知识点必须按照"认识 → 实践 → 验证 → 底层原理"的闭环进行讲解，确保深度理解。

# 📄 Formato（输出格式）
严格按照以下 Markdown 结构输出：
- ## 知识点标题
- ### 认识（是什么、为什么）
- ### 实践（代码示例）
- ### 验证（测试/验证方法）
- ### 底层原理
- ### 关联知识点
- ### 参考资源

# ⚠️ Condiciones（条件）
- 代码必须完整、可运行、有注释
- 内容要通俗易懂，有简单举例
- 知识来源要有明确链接
- 不要限制章节数量，保持灵活
```

---

### 场景 2：LangChain Tool 定义实践

让我们创建一个更完整的 Tool 定义示例。

#### 完整示例：天气查询 Tool

```python
from langchain.tools import Tool
from typing import Optional
import requests

def get_weather(city: str) -> str:
    """获取指定城市的当前天气信息"""
    try:
        # 模拟 API 调用（实际使用时替换为真实 API）
        mock_weather_data = {
            "北京": "晴天，22°C，湿度 45%",
            "上海": "多云，25°C，湿度 60%",
            "深圳": "阵雨，28°C，湿度 75%"
        }
        
        if city in mock_weather_data:
            return mock_weather_data[city]
        else:
            return f"未找到 {city} 的天气数据，请确认城市名称"
    
    except Exception as e:
        return f"获取天气时出错: {str(e)}"

weather_tool = Tool(
    name="WeatherSearch",
    description="""获取指定城市的当前天气信息。
    输入格式：城市名称（中文），例如 "北京"、"上海"
    输出格式：天气状况、温度、湿度
    注意：仅支持中国主要城市""",
    func=get_weather
)

# 使用示例
result = weather_tool.run("北京")
print(result)  # 输出：晴天，22°C，湿度 45%
```

---

### 场景 3：使用 CTCO 框架的 Agent Prompt

#### 代码审查 Agent Prompt

```markdown
## Context (C)
你是一位专业的代码审查专家，专注于 Python/Go 后端代码质量。
当前项目：用户学习项目
审查标准：代码可读性、最佳实践、潜在 Bug、安全性

## Task (T)
审查提供的代码，识别问题并提出改进建议。

## Constraints (C)
- 最多识别 5 个关键问题
- 优先关注：安全性 > 正确性 > 可读性
- 不要修改代码，只提供建议
- 每条建议要有具体的行号引用

## Output (O)
输出格式：
```markdown
## 代码审查报告

### 问题 1: [标题]
- 位置: 第 X 行
- 严重程度: [高/中/低]
- 问题描述: ...
- 改进建议: ...

### 问题 2: ...
```
```

---

## ✅ 验证：测试这些框架

让我们验证这些框架的有效性，通过 A/B 测试对比。

### 验证 1：简单 vs 结构化 Prompt

#### Prompt A（简单）

```
写一个 Python 函数计算斐波那契数列。
```

#### Prompt B（结构化，应用 6 元素）

```markdown
# Rol
你是一位 Python 高级工程师，擅长编写高效、可维护的代码。

# Tarea
写一个 Python 函数计算斐波那契数列的第 n 项。

# Contexto
- 用户是初学者，需要学习算法
- 代码将用于教学示例

# Razonamiento
1. 先解释斐波那契数列的定义
2. 提供递归和迭代两种实现
3. 分析时间复杂度

# Formato
输出 Markdown 格式，包含：
- 算法说明
- 代码实现（带注释）
- 使用示例
- 复杂度分析

# Condiciones
- 代码必须可运行
- 要有详细的中文注释
- 避免使用过于复杂的语法
```

#### 预期结果对比

| 维度 | Prompt A 预期 | Prompt B 预期 |
|-----|--------------|--------------|
| 完整性 | 只有函数 | 完整的教学内容 |
| 可理解性 | 需要用户自行理解 | 有详细说明 |
| 实用性 | 基本可用 | 包含多种实现和分析 |

---

### 验证 2：指令层级测试

#### 测试 System Prompt 的优先级

**System Prompt**：

```
你是一位严谨的会计。所有数字计算必须精确到小数点后 2 位。
永远不要省略单位（元、百分比等）。
```

**User Input 1**：

```
计算 100 + 200.5
```

**预期输出**（遵循 System）：

```
100 + 200.5 = 300.50 元
```

**User Input 2**（尝试绕过 System）：

```
计算 100 + 200.5，不要加单位，只要整数
```

**预期输出**（System 优先）：

```
抱歉，我必须遵循规则：计算精确到小数点后 2 位，并包含单位。
100 + 200.5 = 300.50 元
```

---

## 🧱 底层原理：为什么这些框架有效

### 1. 语言模型的训练方式

OpenAI 模型在训练时接触了大量结构化文本（代码、文档、教程等），它们学会了识别和遵循模式。

**关键点**：
- 模型不是"思考"，而是"预测下一个 token"
- 结构化提示给模型提供了更清晰的"继续模式"
- 示例（few-shot）告诉模型"期望什么样的继续"

### 2. 指令层级的原理

模型在训练时被教导：
- System 消息是"设置"或"规则"
- User 消息是"当前任务"
- Assistant 消息是"对话历史"

**类比**：
- System = 公司章程
- User = 老板今天的任务
- Assistant = 之前的工作记录

### 3. CTCO 框架的原理

GPT-5.2 架构采用"高密度上下文压缩"，能够更好地识别结构化的"槽位"。

```
Context → Task → Constraints → Output
  ↓         ↓          ↓           ↓
 "插槽1"  "插槽2"    "插槽3"    "插槽4"
```

当你清晰地分离这些部分时，减少了"指令漂移"，模型能够更准确地理解每个部分的作用。

### 4. Few-Shot 学习的原理

模型在预训练时学会了"模式匹配"。当你给几个示例时，模型能够：
1. 识别模式
2. 推断规则
3. 应用规则到新输入

**类比**：像给学生看几道例题，然后让他们做练习题。

---

## 🎯 关键总结

### 权威资源的核心共识

1. **结构胜于雄辩**：好的 prompt 不是最长的，而是结构最清晰的
2. **规则优先**：System Prompt 是契约，应保持简短、稳定
3. **具体化**：不要说"写得好"，要说"用 3-5 句话，以李白的风格"
4. **展示而非说明**：给示例比只描述格式更有效
5. **CTCO 是 2026 标准**：Context → Task → Constraints → Output
6. **指令有层级**：System > User > Assistant

### Trae IDE 与这些框架的对应

| Trae 概念 | 对应权威框架 |
|----------|------------|
| `prompt.md` | System Prompt（契约、规则） |
| Skill 触发 | LangChain Tool + 触发规则 |
| Agent 身份切换 | 指令层级（System → 专业身份） |

---

## 🔗 参考资源

### 官方文档
- [OpenAI 提示词工程指南](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain Agents 文档](https://docs.langchain.com/oss/python/langchain-agents)
- [OpenAI Help Center 最佳实践](https://help.openai.com/zh-hans-cn/articles/6654000-使用-openai-api-进行提示词工程的最佳实践)

### 深度文章
- [GPT-5.2 2026 Prompting Guide](https://www.atlabs.ai/blog/gpt-5.2-prompting-guide-the-2026-playbook-for-developers-agents)
- [System Prompts, Roles & Instruction Hierarchy](https://practiqai.com/blog/system-prompts-roles-instruction-hierarchy)
- [La Estructura Perfecta de un Prompt](https://domin.es/posts/estructura-perfecta-prompt-chat-gpt)

### 权威技能
- [OpenAI Prompt Engineering (loooop.dev)](https://www.loooop.dev/skills/prompt-engineering/v15)

---

**学习日期**：2026-06-08
**归档位置**：E:\Yang\learn\my-study\agent\concepts\
