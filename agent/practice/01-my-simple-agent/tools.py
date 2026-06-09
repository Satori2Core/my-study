"""
工具定义 - 天气查询和景点推荐
支持真实API调用和模拟数据降级
"""

import requests
from typing import Dict


# ==================== 模拟数据（降级用） ====================

_MOCK_WEATHER_DATA: Dict[str, str] = {
    "北京": "晴朗",
    "上海": "多云",
    "广州": "晴朗",
    "成都": "小雨",
    "厦门": "晴朗",
}

_MOCK_ATTRACTION_DATA: Dict[str, Dict[str, str]] = {
    "北京": {
        "晴朗": "推荐您去颐和园或天安门广场，天气好适合户外活动",
        "多云": "推荐您去故宫或国家博物馆",
        "小雨": "推荐您去国家大剧院或博物馆",
        "阴天": "推荐您去798艺术区或三里屯",
    },
    "上海": {
        "晴朗": "推荐您去外滩或东方明珠塔",
        "多云": "推荐您去豫园或田子坊",
        "小雨": "推荐您去上海博物馆或科技馆",
    },
    "广州": {
        "晴朗": "推荐您去广州塔或白云山",
        "多云": "推荐您去陈家祠或沙面岛",
    },
    "成都": {
        "晴朗": "推荐您去都江堰或青城山",
        "小雨": "推荐您去杜甫草堂或宽窄巷子",
    },
    "厦门": {
        "晴朗": "推荐您去鼓浪屿或厦门大学",
        "多云": "推荐您去南普陀寺或中山路步行街",
    },
}


# ==================== 工具函数 ====================

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
        # 尝试调用真实天气API
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data["current_condition"][0]
                weather_desc = current.get("weatherDesc", [{}])[0].get("value", "未知")
                temp_c = current.get("temp_C", "未知")
                return f"{city}当前天气：{weather_desc}，气温{temp_c}摄氏度"
        except Exception as e:
            # 网络错误，降级到模拟数据
            pass
    
    # 使用模拟数据
    weather = _MOCK_WEATHER_DATA.get(city, "晴朗")
    return f"{city}当前天气：{weather}，气温25摄氏度"


def get_attraction(city: str, weather: str, use_real: bool = False, tavily_api_key: str = "") -> str:
    """
    根据城市和天气推荐旅游景点
    
    Args:
        city: 城市名称（中文）
        weather: 天气状况
        use_real: 是否使用真实搜索API（默认False使用模拟数据）
        tavily_api_key: Tavily API密钥（真实模式需要）
        
    Returns:
        str: 景点推荐信息
    """
    if use_real and tavily_api_key:
        # 尝试调用真实搜索API
        try:
            from tavily import TavilyClient
            
            tavily = TavilyClient(api_key=tavily_api_key)
            query = f"{city} 在{weather}天气下最值得去的旅游景点推荐及理由"
            
            response = tavily.search(
                query=query,
                search_depth="basic",
                include_answer=True
            )
            
            if response.get("answer"):
                return response["answer"]
        except ImportError:
            # 未安装tavily库，降级
            pass
        except Exception as e:
            # 网络错误，降级
            pass
    
    # 使用模拟数据
    # 提取天气关键词
    weather_key = weather
    if "，" in weather_key:
        weather_key = weather_key.split("，")[0]
    if "：" in weather_key:
        weather_key = weather_key.split("：")[1]
    
    city_attractions = _MOCK_ATTRACTION_DATA.get(city, {})
    
    # 精确匹配
    if weather_key in city_attractions:
        return city_attractions[weather_key]
    
    # 模糊匹配
    for w, recommendation in city_attractions.items():
        if w in weather_key or weather_key in w:
            return recommendation
    
    # 默认推荐
    return f"在{city}的{weather}天气下，推荐您参观当地著名景点"


# ==================== 工具注册 ====================

def create_tools(use_real: bool = False, tavily_api_key: str = "") -> Dict[str, callable]:
    """
    创建工具字典
    
    Args:
        use_real: 是否使用真实API（总开关）
        tavily_api_key: Tavily API密钥
        
    Returns:
        Dict: 工具字典 {工具名: 函数}
    """
    # 使用lambda包装函数，传递use_real参数
    weather_tool = lambda city: get_weather(city, use_real=use_real)
    weather_tool.__doc__ = get_weather.__doc__  # 保持docstring
    
    attraction_tool = lambda city, weather: get_attraction(
        city, weather, use_real=use_real, tavily_api_key=tavily_api_key
    )
    attraction_tool.__doc__ = get_attraction.__doc__  # 保持docstring
    
    return {
        "get_weather": weather_tool,
        "get_attraction": attraction_tool,
    }


# ==================== API测试函数 ====================

def test_model_api(api_key: str, base_url: str, model_name: str) -> bool:
    """
    测试大模型API是否可用
    
    Args:
        api_key: API密钥
        base_url: API基础URL
        model_name: 模型名称
        
    Returns:
        bool: API是否可用
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "测试"}],
            max_tokens=10
        )
        return True
    except Exception as e:
        print(f"模型API测试失败: {str(e)}")
        return False


def test_tavily_api(api_key: str) -> bool:
    """
    测试Tavily搜索API是否可用
    
    Args:
        api_key: Tavily API密钥
        
    Returns:
        bool: API是否可用
    """
    try:
        from tavily import TavilyClient
        
        tavily = TavilyClient(api_key=api_key)
        response = tavily.search(query="测试", search_depth="basic")
        return True
    except ImportError:
        print("警告: 未安装tavily-python库，请运行: pip install tavily-python")
        return False
    except Exception as e:
        print(f"Tavily API测试失败: {str(e)}")
        return False