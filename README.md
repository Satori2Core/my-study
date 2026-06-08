# 后端技术学习项目

一个系统化学习 Go 语言、MySQL、Redis、Linux、Docker 的学习项目，包含学习笔记、技能配置和学习进度管理。

## 📚 学习内容

### Agent 技能系统
- **触发机制**：关键词触发、场景触发、意图触发、组合触发
- **规则设计**：复杂规则、优先级计算、容错机制
- **身份切换**：通用 Agent 与专业 Agent 的切换机制
- **技能定义**：SKILL.md 与 prompt.md 的设计规范

### Go 语言
- 环境搭建与基础语法
- 并发编程（goroutine、channel）
- 接口与设计模式
- 微服务开发

### MySQL
- SQL 基础与高级查询
- 索引优化与性能调优
- 事务与锁机制
- 主从复制与高可用架构

### Redis
- 数据类型详解
- 持久化机制
- 集群部署
- 缓存策略与性能优化

### Linux
- 命令行操作与脚本编程
- 进程管理与性能监控
- 网络配置与安全加固
- Docker 容器基础

### Docker
- 镜像管理与容器操作
- Dockerfile 编写
- Docker Compose
- Docker Swarm 集群

## 🗂️ 项目结构

```
my-study/
├── .trae/                    # Trae IDE 技能配置
│   └── skill/
│       └── learning-coach/   # 学习教练技能
│           ├── SKILL.md      # 技能定义
│           └── prompt.md     # Agent 身份定义
├── agent/                    # Agent 技能系统学习笔记
│   ├── concepts/             # 核心概念
│   ├── config/               # 配置管理
│   └── rules/                # 规则设计
├── go/                       # Go 语言学习笔记（待学习）
├── mysql/                    # MySQL 学习笔记（待学习）
├── redis/                    # Redis 学习笔记（待学习）
├── linux/                    # Linux 学习笔记（待学习）
├── docker/                   # Docker 学习笔记（待学习）
└── study_config.json         # 学习配置文件
```

## 🚀 快速开始

### 环境要求
- Trae IDE（推荐）或 VS Code
- Go 1.21+
- MySQL 8.0+
- Redis 7.0+
- Docker 24.0+

### 使用方法

1. **克隆项目**
```bash
git clone https://github.com/your-username/my-study.git
cd my-study
```

2. **配置学习路径**
编辑 `study_config.json` 文件，配置学习笔记目录和当前学习主题。

3. **开始学习**
在 Trae IDE 中打开项目，触发学习教练技能：
- 输入"学习 Go"开始学习 Go 语言
- 输入"学习 MySQL"开始学习 MySQL
- 输入"学习 Redis"开始学习 Redis

## 🎯 学习目标

- ✅ 认识：理解核心概念和原理
- ✅ 实践：编写可运行的代码示例
- ✅ 验证：测试代码功能正确性
- ✅ 原理：深入理解底层实现机制

## 📝 笔记格式

每个学习笔记遵循以下结构：
- **知识点拆解**：核心概念解析
- **实战案例**：可运行的代码示例
- **关联知识点**：知识体系连接
- **底层原理**：深入机制分析
- **参考资源**：官方文档和权威链接

## 🔧 技能配置

### SKILL.md 配置项
- `name`：技能名称
- `version`：技能版本
- `description`：技能描述
- `triggers`：触发规则
- `execution_flow`：执行流程

### prompt.md 配置项
- `role`：Agent 角色定义
- `responsibilities`：核心职责
- `rules`：执行规则
- `learning_path`：学习路径

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**学习进度**：Agent 技能系统 ✓ | Go 语言 ⏳ | MySQL ⏳ | Redis ⏳ | Linux ⏳ | Docker ⏳
