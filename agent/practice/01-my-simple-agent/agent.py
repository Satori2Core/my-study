"""
智能体核心循环 - ReAct模式（Thought → Action → Observation）
参考教程：https://datawhalechina.github.io/hello-agents/
"""

import json
import re
from openai import OpenAI
from typing import Dict, List, Callable, Optional


# 系统提示词模板
SYSTEM_PROMPT_TEMPLATE = """你是一个智能旅行助手，可以帮助用户查询天气并推荐旅游景点。

你可以使用以下工具：
{tools_desc}

请按照以下格式思考和行动：
Thought: 分析用户需求，思考下一步该做什么
Action: 调用工具：工具名(参数1="值1", 参数2="值2")
Observation: 工具返回的结果（由系统自动填充）

当你完成任务时，使用以下格式给出最终答案：
Action: Finish[最终答案内容]

注意：
1. 每次只能调用一个工具
2. 必须等待工具返回结果后再进行下一步思考
3. 完成任务后必须使用Finish给出最终答案"""


class SimpleAgent:
    """
    简单的ReAct智能体
    核心流程：思考 → 行动 → 观察 → 循环
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        tools: Dict[str, Callable],
        max_iterations: int = 5,
        verbose: bool = True
    ):
        """
        初始化智能体
        
        Args:
            api_key: 大模型API密钥
            base_url: API基础URL
            model_name: 模型名称
            tools: 工具字典 {工具名: 函数}
            max_iterations: 最大迭代次数
            verbose: 是否打印详细过程
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name
        self.tools = tools
        self.max_iterations = max_iterations
        self.verbose = verbose
        
        # 生成工具描述
        self.tools_desc = self._generate_tools_desc()
        
        # 系统提示词
        self.system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            tools_desc=self.tools_desc
        )
    
    def _generate_tools_desc(self) -> str:
        """生成工具描述文本"""
        lines = []
        for name, func in self.tools.items():
            # 从函数的docstring提取描述
            desc = func.__doc__ or f"工具: {name}"
            # 只取第一行作为简短描述
            first_line = desc.strip().split('\n')[0]
            lines.append(f"- {name}: {first_line}")
        return "\n".join(lines)
    
    def _call_llm(self, messages: List[Dict]) -> str:
        """调用大语言模型"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    def _parse_response(self, response: str) -> Dict:
        """
        解析LLM响应，提取Thought和Action
        
        Returns:
            {
                'thought': str,  # 思考内容
                'action_type': str,  # 'tool' 或 'finish'
                'action_content': str  # 工具调用或最终答案
            }
        """
        result = {
            'thought': '',
            'action_type': None,
            'action_content': ''
        }
        
        # 提取Thought
        thought_match = re.search(r'Thought:\s*(.+?)(?:\n|$)', response)
        if thought_match:
            result['thought'] = thought_match.group(1).strip()
        
        # 提取Action
        action_match = re.search(r'Action:\s*(.+?)(?:\n|$)', response)
        if action_match:
            action_text = action_match.group(1).strip()
            
            # 判断是Finish还是工具调用
            if action_text.startswith('Finish'):
                result['action_type'] = 'finish'
                # 提取Finish[内容]
                finish_match = re.search(r'Finish\[(.+?)\]', action_text)
                if finish_match:
                    result['action_content'] = finish_match.group(1).strip()
            else:
                result['action_type'] = 'tool'
                result['action_content'] = action_text
        
        return result
    
    def _parse_tool_call(self, action_content: str) -> Dict:
        """
        解析工具调用字符串
        
        示例: get_weather(city="北京") -> {'name': 'get_weather', 'args': {'city': '北京'}}
        支持中文参数名（如：城市="北京"）会自动映射为英文参数名
        """
        # 参数名映射（中文 -> 英文）
        param_mapping = {
            '城市': 'city',
            '天气': 'weather',
            '查询': 'query',
        }
        
        # 提取工具名
        match = re.match(r'(\w+)\((.+?)\)', action_content)
        if not match:
            # 尝试更宽松的匹配（处理可能的空白）
            match = re.match(r'\s*(\w+)\s*\(\s*(.+?)\s*\)\s*', action_content)
        
        if not match:
            return {'name': None, 'args': {}}
        
        tool_name = match.group(1)
        args_str = match.group(2)
        
        # 解析参数（支持中文和英文参数名）
        args = {}
        # 匹配 key="value" 或 key='value'，支持中文key
        param_matches = re.findall(r'([\w\u4e00-\u9fa5]+)\s*=\s*["\'](.+?)["\']', args_str)
        for key, value in param_matches:
            # 尝试映射参数名
            mapped_key = param_mapping.get(key, key)
            args[mapped_key] = value
        
        return {'name': tool_name, 'args': args}
    
    def _execute_tool(self, tool_name: str, args: Dict) -> str:
        """执行工具"""
        if tool_name not in self.tools:
            return f"错误：未找到工具 '{tool_name}'"
        
        try:
            result = self.tools[tool_name](**args)
            return str(result)
        except Exception as e:
            return f"错误：执行工具 '{tool_name}' 失败 - {str(e)}"
    
    def run(self, user_input: str) -> Optional[str]:
        """
        运行智能体循环
        
        Args:
            user_input: 用户输入
            
        Returns:
            最终答案或None
        """
        if self.verbose:
            print("=" * 60)
            print("智能旅行助手 - Agent运行中")
            print("=" * 60)
            print(f"用户请求: {user_input}\n")
        
        # 初始化对话历史
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # ReAct循环
        for iteration in range(1, self.max_iterations + 1):
            if self.verbose:
                print(f"--- 第 {iteration} 轮思考 ---")
            
            # 调用LLM
            response = self._call_llm(messages)
            
            # 解析响应
            parsed = self._parse_response(response)
            
            if self.verbose and parsed['thought']:
                print(f"Agent思考:\nThought: {parsed['thought']}")
            
            # 判断Action类型
            if parsed['action_type'] == 'finish':
                if self.verbose:
                    print(f"\n最终答案:\n{parsed['action_content']}\n")
                    print("=" * 60)
                    print("任务完成！")
                return parsed['action_content']
            
            elif parsed['action_type'] == 'tool':
                # 解析工具调用
                tool_call = self._parse_tool_call(parsed['action_content'])
                
                if self.verbose:
                    print(f"Action: {parsed['action_content']}")
                
                # 执行工具
                if tool_call['name']:
                    observation = self._execute_tool(
                        tool_call['name'], 
                        tool_call['args']
                    )
                    
                    if self.verbose:
                        print(f"\n执行工具: {tool_call['name']}({tool_call['args']})")
                        print(f"工具返回: {observation}\n")
                    
                    # 将结果加入对话历史
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user", 
                        "content": f"Observation: {observation}"
                    })
                else:
                    # 无法解析工具调用
                    error_msg = "无法解析工具调用格式"
                    if self.verbose:
                        print(f"错误: {error_msg}\n")
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user", 
                        "content": f"Observation: {error_msg}"
                    })
            
            else:
                # 没有Action，继续对话
                if self.verbose:
                    print("未检测到Action，继续对话...\n")
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user", 
                    "content": "请继续思考并给出下一步Action。"
                })
        
        # 达到最大迭代次数
        if self.verbose:
            print(f"\n达到最大迭代次数({self.max_iterations})，任务未完成。")
        return None


def create_agent(
    api_key: str,
    base_url: str,
    model_name: str,
    tools: Dict[str, Callable],
    **kwargs
) -> SimpleAgent:
    """
    创建智能体的便捷函数
    
    Args:
        api_key: API密钥
        base_url: API基础URL
        model_name: 模型名称
        tools: 工具字典
        **kwargs: 其他参数
        
    Returns:
        SimpleAgent实例
    """
    return SimpleAgent(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        tools=tools,
        **kwargs
    )