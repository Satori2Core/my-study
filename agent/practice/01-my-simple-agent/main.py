"""
智能旅行助手 - 主程序入口
简化版：按照教程结构，加入配置化和降级能力
"""

import yaml
from pathlib import Path
from agent import SimpleAgent, create_agent
from tools import create_tools, test_model_api, test_tavily_api


def load_config():
    """加载配置文件"""
    # 查找配置文件
    config_path = Path("config.yaml")
    example_path = Path("config.example.yaml")
    
    if not config_path.exists():
        if example_path.exists():
            print("提示: 未找到 config.yaml，使用示例配置（模拟模式）")
            with open(example_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            # 强制使用模拟模式
            config['use_real_api'] = False
        else:
            print("错误: 未找到配置文件")
            return None
    else:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    
    return config


def main():
    """主程序"""
    print("=" * 60)
    print("智能旅行助手 - DataWhale Hello-Agents实践")
    print("=" * 60)
    print()
    
    # 加载配置
    config = load_config()
    if not config:
        return
    
    # 获取配置参数
    use_real_api = config.get('use_real_api', False)
    model_config = config.get('model', {})
    search_config = config.get('search', {})
    agent_config = config.get('agent', {})
    
    api_key = model_config.get('api_key', '')
    base_url = model_config.get('base_url', '')
    model_name = model_config.get('model_name', '')
    tavily_api_key = search_config.get('tavily_api_key', '')
    
    # 检查API密钥是否有效
    if api_key.startswith('your-') or not api_key:
        print("警告: API密钥未配置或无效")
        print("请复制 config.example.yaml 为 config.yaml 并填入真实API密钥")
        print()
        if use_real_api:
            print("真实模式需要有效的API密钥，已自动切换到模拟模式")
            use_real_api = False
        # 即使模拟模式也需要大模型API进行思考
        print("注意: Agent的思考过程需要大模型API")
        print("请配置有效的豆包API密钥后运行")
        return
    
    # ==================== API测试检查 ====================
    if use_real_api:
        print("模式: 真实API调用")
        print()
        
        # 测试大模型API
        print("正在测试大模型API...")
        if not test_model_api(api_key, base_url, model_name):
            print("\n大模型API不可用，将降级到模拟模式")
            use_real_api = False
        else:
            print("大模型API测试成功 [OK]")
        
        # 测试Tavily API（如果配置了）
        if tavily_api_key and not tavily_api_key.startswith('your-'):
            print("\n正在测试Tavily搜索API...")
            if test_tavily_api(tavily_api_key):
                print("Tavily API测试成功 [OK]")
            else:
                print("Tavily API不可用，景点推荐将使用模拟数据")
                tavily_api_key = ""
        
        print()
    else:
        print("模式: 模拟数据（适合学习和测试）")
        print()
    
    # ==================== 创建工具和Agent ====================
    tools = create_tools(use_real=use_real_api, tavily_api_key=tavily_api_key)
    
    agent = create_agent(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        tools=tools,
        max_iterations=agent_config.get('max_iterations', 5),
        verbose=agent_config.get('verbose', True)
    )
    
    # ==================== 运行Agent ====================
    user_request = "你好，请帮我查询一下今天武汉的天气，然后根据天气推荐一个合适的旅游景点。"
    
    result = agent.run(user_request)
    
    if result:
        print(f"\n运行成功！")


if __name__ == "__main__":
    main()