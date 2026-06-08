# Learning Coach Skill

## 技能定义

### 基本信息
- **名称**: learning-coach
- **版本**: 1.0.0
- **描述**: 后端开发者专属学习教练，支持 Go、MySQL、Redis、Linux、Docker 等技术栈的系统化学习
- **作者**: Trae AI
- **创建时间**: 2024-01-01

### 功能特性
1. **知识点拆解**: 将复杂技术概念拆解为易于理解的知识点
2. **实战案例**: 提供可运行的代码示例
3. **关联知识点**: 建立知识体系连接
4. **自动笔记**: 生成可归档的 Markdown 学习笔记

### 支持的学习主题
| 主题 | 标识 | 章节数 | 状态 |
|------|------|--------|------|
| Go语言 | go | 20 | 进行中 |
| MySQL | mysql | 15 | 待学习 |
| Redis | redis | 10 | 待学习 |
| Linux | linux | 15 | 待学习 |
| Docker | docker | 10 | 待学习 |

## 技能配置

### 配置文件路径
```
E:\Yang\learn\my-study\study_config.json
```

### 配置结构
```json
{
  "notes_directory": "E:\\Yang\\learn\\my-study",
  "current_topic": "go",
  "topics": [
    {
      "name": "go",
      "title": "Go语言",
      "completed_chapters": 0,
      "total_chapters": 20
    }
  ]
}
```

### 配置字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| notes_directory | string | Markdown笔记输出目录 |
| current_topic | string | 当前学习主题标识 |
| topics | array | 学习主题列表 |
| topics[].name | string | 主题标识（小写） |
| topics[].title | string | 主题显示名称 |
| topics[].completed_chapters | number | 已完成章节数 |
| topics[].total_chapters | number | 总章节数 |

## 触发规则

### 关键词触发
- "学习"、"教程"、"课程"、"入门"
- "Go"、"golang"、"MySQL"、"Redis"、"Linux"、"Docker"
- "笔记"、"总结"、"文档"

### 场景触发
- 用户询问技术知识点时
- 用户请求代码示例时
- 用户要求生成学习笔记时

## 执行流程

```
用户提问 → 意图识别 → 知识点拆解 → 生成案例 → 关联知识 → 输出笔记
    ↓              ↓              ↓
  配置读取      主题匹配      内容生成
```

## 输出格式

### 学习笔记格式
```markdown
# 章节标题

## 一、知识点拆解
- 核心概念1
- 核心概念2

## 二、实战案例
```go
// 代码示例
```

## 三、关联知识点
- 前置知识: xxx
- 后续知识: xxx
- 相关技术: xxx
```

### 配置更新格式
自动更新 `study_config.json` 中的 `completed_chapters` 字段

## 错误处理

### 配置文件不存在
- 自动创建默认配置文件

### 目录不存在
- 自动创建输出目录

### 主题不存在
- 返回支持的主题列表供用户选择
