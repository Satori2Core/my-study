# 本地部署开源大语言模型实践

> Hello-Agents 第三章《调用开源大语言模型》实践指南
> 
> 参考教程：https://datawhalechina.github.io/hello-agents/#/./chapter3/%E7%AC%AC%E4%B8%89%E7%AB%A0%20%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80?id=_323-%e8%b0%83%e7%94%a8%e5%bc%80%e6%ba%90%e5%a4%a7%e8%af%ad%e8%a8%80%e6%a8%a1%e5%9e%8b

---

## 概述

在第一章中，我们通过 API 来驱动智能体。但在处理敏感数据、需要离线运行或精细控制成本的场景下，将大模型**私有化部署**到本地电脑是 Agent 开发者的必备技能。

本实践将带你动手，使用 **Hugging Face Transformers** 库在自己的电脑上运行一个真实的开源大模型。

---

## 环境配置

### 1. 安装依赖

```bash
pip install transformers torch
```

### 2. 选择模型

我们选择教程中推荐的小规模但功能强大的模型：

| 属性 | 值 |
|------|-----|
| **模型名称** | Qwen/Qwen1.5-0.5B-Chat |
| **出品方** | 阿里巴巴达摩院 |
| **参数量** | 约 5 亿 (0.5B) |
| **特点** | 体积小、性能优异，适合入门学习和本地部署 |

---

## 实践步骤

### 步骤 1：加载模型与分词器

创建 `run_local_llm.py` 文件：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 指定模型 ID
model_id = "Qwen/Qwen1.5-0.5B-Chat"

# 设置设备，优先使用 GPU (CUDA)，否则使用 CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 加载模型，并将其移动到指定设备
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
print("模型和分词器加载完成！")
```

### 步骤 2：准备对话输入

Qwen1.5-Chat 模型遵循特定的对话模板。我们需要构建包含 `system` 和 `user` 的消息列表：

```python
# 准备对话输入
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你好，请介绍你自己。"}
]

# 使用分词器的模板格式化输入
# tokenize=False 表示先只获取格式化后的文本字符串
# add_generation_prompt=True 表示添加模型开始生成的引导符
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# 编码输入文本，转换为 Tensor 并移动到设备
model_inputs = tokenizer([text], return_tensors="pt").to(device)
print("编码后的输入文本 (Token IDs):")
print(model_inputs)
```

### 步骤 3：生成与解码

调用模型的 `generate()` 方法生成回答：

```python
# 生成回答
with torch.no_grad():
    outputs = model.generate(
        **model_inputs,
        max_new_tokens=512,  # 最大生成 token 数
        do_sample=True,      # 是否采样
        temperature=0.7,     # 温度参数，控制随机性
        top_p=0.9            # 核采样参数
    )

# 解码输出，移除特殊 token
response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
print("\n模型输出:")
print(response[0])
```

### 步骤 4：完整代码

将以上步骤整合到完整的脚本中。

---

## 运行方式

```bash
python run_local_llm.py
```

首次运行会自动从 Hugging Face Hub 下载模型文件（约 1GB），请耐心等待。

---

## 预期输出

```
使用设备: cuda
模型和分词器加载完成！
编码后的输入文本 (Token IDs):
{'input_ids': tensor([[151643,  ...]]), 'attention_mask': tensor([[1, 1, ...]])}

模型输出:
你好！我是 Qwen1.5，由阿里巴巴达摩院开发的大语言模型。我可以帮助你回答问题、生成文本等。
```

---

## 扩展练习

1. **尝试不同的模型**：修改 `model_id` 使用其他模型，如 `Qwen/Qwen1.5-1.8B-Chat`
2. **调整生成参数**：修改 `temperature`、`max_new_tokens` 等参数观察效果
3. **多轮对话**：扩展代码支持多轮对话
4. **量化优化**：使用 `bitsandbytes` 库进行 4-bit 量化

---

## 常见问题

### 显存不足

如果遇到 CUDA 显存不足的问题，可以：
1. 使用更小的模型（如 0.5B 参数模型）
2. 启用量化：安装 `bitsandbytes` 并使用 `load_in_4bit=True`
3. 切换到 CPU 模式

### 下载速度慢

可以设置 Hugging Face 国内镜像：
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

---

## 参考资料

- [Hello-Agents 官方教程](https://datawhalechina.github.io/hello-agents/)
- [Hugging Face Transformers 文档](https://huggingface.co/docs/transformers/)
- [Qwen 模型官方页面](https://huggingface.co/Qwen)