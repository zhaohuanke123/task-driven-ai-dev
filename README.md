# Vanko Skill

Claude Code 个人技能集合，包含开发工作流、交互式学习、Skill 制作等实用工具。

## Skills 概览

| Skill | 类型 | 说明 |
|-------|------|------|
| [task-driven-ai-dev](#task-driven-ai-dev) | 任务驱动 | 任务驱动的 AI 开发循环，持久化规划文档 + 单任务执行 + 验证门 |
| [coding-workflow](#coding-workflow) | 开发流程 | 项目初始化 + PEV 三层 Agent 编排（Planner → Executor → Verifier） |
| [software-dev](#software-dev) | 开发流程 | 10 阶段全生命周期，文档驱动 + 阶段门控 |
| [interactive-learning](#interactive-learning) | 交互学习 | Bloom 掌握学习 + 盲点诊断 + 骨架精读 + 费曼验证 + 艾宾浩斯复习 |
| [skill-creator](#skill-creator) | Skill 制作 | 指导创建符合 Claude Code 规范的 Skill |

---

## Skill 详情

### task-driven-ai-dev

将仓库变为任务驱动的 AI 交付循环，通过持久化规划文档、受保护的单任务执行、进度日志和验证门来确保交付质量。

**Features:**
- **架构文档管理**：维护系统概览、约束条件和集成边界
- **任务管理**：追踪带依赖关系、阻塞状态和验证记录的待办列表
- **进度日志**：按日期记录执行日志及测试证据
- **项目配置**：仓库级命令和产物路径配置
- **Git 集成**：任务完成后自动提交

### coding-workflow

面向全栈项目的结构化开发工作流，包含文档门、验证门、持久状态和浏览器测试集成。采用 PEV（Plan-Execute-Verify）三层 Agent 架构。

**Features:**
- **任务选择**：自动从 task.json 选取下一个未完成任务
- **文档门**：实现前要求任务级需求/设计参考
- **Memory 路由规则**：Memory 仅作路由提示，仓库文件为事实来源
- **实现引导**：遵循已有文档、代码模式和约定
- **测试门**：Lint、构建、浏览器测试、文档/代码/测试一致性检查
- **进度文档**：持久化会话历史、文档更新、跳过风险记录
- **阻塞协议**：清晰处理需要人工介入的任务
- **回滚支持**：从失败实现中干净恢复

### software-dev

10 阶段全生命周期指导：问题定义 → 需求 → 规划 → 架构 → 设计 → 编码 → 单元测试 → 集成 → 系统测试 → 交付。适用于需要快速迭代且有纪律交付的小型/演示项目。

**Features:**
- **10 阶段生命周期**：完整的阶段门控流程
- **文档优先**：实现前先更新文档；Bug 修复和行为变更必须通过文档门；文档、代码、测试必须一致
- **渐进加载**：紧凑的主文件 + 按需加载的参考文件
- **跨会话持久化**：`PROJECT.md`、`CLAUDE.md`、`AGENTS.md`、`WORKFLOW.md` 跨会话保持上下文
- **Memory 适配策略**：Memory 可提醒起始点，但不替代项目状态或文档
- **Git 集成**：每个阶段内置提交、标签和回滚
- **恢复协议**：处理文件缺失、脏工作树和废弃项目

### interactive-learning

基于 Bloom "2 Sigma 问题"理论和掌握学习原则的交互式学习系统。

**Features:**
- **盲点诊断**：开始前用诊断题探测"以为懂其实不懂"，按盲点重排学习路径（L1-L5 分级）
- **骨架精读**：整本书 / 长文档等大材料自动精读成带原文回溯的骨架
- **对话式验证**：AI 动态生成问题，追问验证理解程度
- **掌握学习**：真正理解（L3 应用级）后才继续
- **分支探索**：深入感兴趣的概念，随时回到主线
- **跨会话进度**：新对话也能恢复学习上下文
- **费曼方法**：通过解释来学习，AI 帮你发现知识盲点
- **纠错机制**：纠正 AI 错误，让学习成为协作过程
- **来源引用**：基于文档、书籍或网站生成课程
- **Obsidian 集成**：自动添加 `^block-id` 精确笔记引用
- **艾宾浩斯复习**：间隔重复复习系统（20min, 1h, 1d, 2d, 6d, 31d）

### skill-creator

指导创建符合 Claude Code 规范的 Skill，包含完整的开发工作流、合规检查清单、语言优化规范和多类型模板。

**Features:**
- **6 步工作流**：需求确认 → Frontmatter 设计 → 正文编写 → 合规检查 → 辅助文件 → 输出
- **合规检查**：12 项验证清单确保 Skill 规范
- **语言优化**：8 类冗余消除规则，确保高信息密度
- **模板参考**：引用型、任务型、子代理型、参数化型、动态注入型 5 种模板
- **详细参考**：完整字段说明、作用域优先级、生命周期管理

---

## 安装

### 方式一：通过 skills 安装器（推荐）

使用 [vercel-labs/skills](https://github.com/vercel-labs/skills) 一行命令安装单个 skill，无需手动复制：

```bash
# 安装单个 skill（以 interactive-learning 为例）
npx skills add zhaohuanke123/vanko-skill@interactive-learning

# 全局安装（所有项目可用，-g）；-y 跳过确认
npx skills add zhaohuanke123/vanko-skill@interactive-learning -g -y
```

> 也可用 `npx add-skill zhaohuanke123/vanko-skill`。

### 方式二：git clone + 手动复制

```bash
git clone https://github.com/zhaohuanke123/vanko-skill.git

# 复制需要的 skill 到个人目录（所有项目可用）
cp -r vanko-skill/skills/task-driven-ai-dev ~/.claude/skills/
cp -r vanko-skill/skills/coding-workflow ~/.claude/skills/
cp -r vanko-skill/skills/interactive-learning ~/.claude/skills/
cp -r vanko-skill/skills/software-dev ~/.claude/skills/
cp -r vanko-skill/skills/skill-creator-gd ~/.claude/skills/skill-creator
```

### 方式三：复制到项目 Skills 目录

```bash
# 复制到特定项目的 .claude/skills/ 目录（仅该项目可用）
cp -r vanko-skill/skills/interactive-learning /your-project/.claude/skills/
```

### 方式四：通过 --add-dir 加载

```bash
claude --add-dir /path/to/vanko-skill/skills/interactive-learning
```

## 使用

安装后在 Claude Code 对话中通过 `/skill-name` 调用：

```
/task-driven-ai-dev          # 任务驱动 AI 开发
/coding-workflow             # 编码工作流（PEV 编排）
/software-dev                # 软件开发全生命周期
/interactive-learning        # 交互式学习（含盲点诊断、骨架精读）
/skill-creator               # Skill 开发制作
```

每个 Skill 也会根据描述中的触发条件被 Claude 自动加载。

## 产物文件

### software-dev

| 文件 | 用途 |
|------|------|
| `PROJECT.md` | 项目状态、阶段、版本的事实来源 |
| `CLAUDE.md` | 跨会话持久化的通用 Agent 入口 |
| `AGENTS.md` | 未来 Agent 的运行时导航入口 |
| `WORKFLOW.md` | 执行工作流和文档门 |
| `docs/problem-definition.md` | 问题描述和成功标准 |
| `docs/requirements.md` | 功能和非功能需求 |
| `docs/plan.md` | 技术栈、里程碑、风险、版本策略 |
| `docs/architecture.md` | 组件和数据流 |
| `docs/design.md` | 模块设计和契约 |
| `docs/test-results.md` | 验证结果 |
| `docs/version-history.md` | 发布和回滚历史 |
| `docs/lessons-learned.md` | 可复用的经验教训 |

### task-driven-ai-dev

| 文件 | 用途 |
|------|------|
| `architecture.md` | 系统概览、约束、集成边界 |
| `task.json` | 待办列表事实来源 |
| `progress.txt` | 按日期的执行日志及证据 |
| `project-config.json` | 仓库级命令和产物路径 |

### coding-workflow

| 文件 | 用途 |
|------|------|
| `AGENTS.md` | 运行时导航入口 |
| `WORKFLOW.md` | 执行工作流和文档门 |
| `task.json` | 任务定义（步骤、状态、文档引用） |
| `progress.txt` | 会话历史、文档更新、跳过风险记录 |
| `architecture.md` | 系统设计决策 |

### interactive-learning

| 文件 | 用途 |
|------|------|
| `诊断报告.md` | 盲点诊断结果（可选，非纯新手时生成） |
| `骨架/` | 大材料（整本书/长文档）精读骨架（可选） |
| `进度.md` | 学习进度和当前状态 |
| `知识图谱.md` | 学习路径和概念关系 |
| `复习计划.md` | 艾宾浩斯复习计划 |
| `参考资料.md` | 主题的来源材料库 |
| `XX_标题.md` | 课程文件（含内容和检查站记录） |
| `config.json` | 学习目录和教学设置 |

## License

MIT
