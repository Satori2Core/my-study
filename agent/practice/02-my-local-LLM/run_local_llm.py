"""
Hello-Agents 第三章实践：本地部署开源大语言模型
参考教程：https://datawhalechina.github.io/hello-agents/#/./chapter3/%E7%AC%AC%E4%B8%89%E7%AB%A0%20%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80?id=_323-%e8%b0%83%e7%94%a8%e5%bc%80%e6%ba%90%e5%a4%a7%e8%af%ad%e8%a8%80%e6%a8%a1%e5%9e%8b
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model_and_tokenizer(model_id: str = "Qwen/Qwen1.5-0.5B-Chat"):
    """
    加载模型与分词器
    
    Args:
        model_id: Hugging Face 模型 ID
    
    Returns:
        tokenizer: 分词器
        model: 语言模型
        device: 使用的设备
    """
    # 设置设备，优先使用 GPU (CUDA)，否则使用 CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    
    # 加载分词器
    print(f"正在加载分词器: {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # 加载模型，并将其移动到指定设备
    print(f"正在加载模型: {model_id}")
    model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
    
    print("模型和分词器加载完成！")
    return tokenizer, model, device


def prepare_input(tokenizer, messages: list):
    """
    准备对话输入，使用模型指定的对话模板
    
    Args:
        tokenizer: 分词器
        messages: 消息列表，包含 system 和 user 角色
    
    Returns:
        model_inputs: 编码后的模型输入
        formatted_text: 格式化后的文本（用于调试）
    """
    # 使用分词器的模板格式化输入
    # tokenize=False 表示先只获取格式化后的文本字符串，方便观察
    # add_generation_prompt=True 表示添加模型开始生成的引导符
    formatted_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # 编码输入文本，转换为 Tensor 并移动到设备
    model_inputs = tokenizer([formatted_text], return_tensors="pt")
    
    print("\n格式化后的输入文本:")
    print(formatted_text)
    print("\n编码后的输入 (Token IDs 长度):", len(model_inputs["input_ids"][0]))
    
    return model_inputs, formatted_text


def generate_response(model, tokenizer, model_inputs, device, max_new_tokens=512):
    """
    生成模型响应
    
    Args:
        model: 语言模型
        tokenizer: 分词器
        model_inputs: 编码后的输入
        device: 使用的设备
        max_new_tokens: 最大生成 token 数
    
    Returns:
        response: 模型生成的回答
    """
    # 将输入移动到设备
    model_inputs = model_inputs.to(device)
    
    # 生成回答
    print("\n正在生成回答...")
    with torch.no_grad():
        outputs = model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
    
    # 解码输出，移除特殊 token
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return response[0]


def chat_with_model():
    """
    交互式对话函数
    """
    print("=" * 60)
    print("Hello-Agents 本地大模型实践")
    print("模型: Qwen/Qwen1.5-0.5B-Chat")
    print("=" * 60)
    
    # 步骤 1: 加载模型和分词器
    tokenizer, model, device = load_model_and_tokenizer()
    
    # 初始化对话历史
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    print("\n输入 'exit' 或 'quit' 退出对话")
    print("-" * 60)
    
    while True:
        # 获取用户输入
        user_input = input("你: ")
        
        # 检查是否退出
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("再见！")
            break
        
        # 添加用户消息到对话历史
        messages.append({"role": "user", "content": user_input})
        
        # 步骤 2: 准备输入
        model_inputs, _ = prepare_input(tokenizer, messages)
        
        # 步骤 3: 生成回答
        response = generate_response(model, tokenizer, model_inputs, device)
        
        # 提取模型回答（移除输入部分）
        # 使用完整的对话历史生成模板，找到回答开始的位置
        full_template = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        answer_start = response.find(full_template)
        if answer_start != -1:
            answer = response[answer_start + len(full_template):].strip()
        else:
            # 如果找不到，直接使用完整响应
            answer = response
        
        # 打印回答
        print(f"\nAI: {answer}")
        print("-" * 60)
        
        # 添加模型回答到对话历史
        messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    chat_with_model()