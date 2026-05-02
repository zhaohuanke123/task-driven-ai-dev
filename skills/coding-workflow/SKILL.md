---
name: coding-workflow
description: |
  项目初始化器 - 部署 Harness Engineering 架构文件到项目目录，包含 CLAUDE.md、WORKFLOW.md、architecture.md、task.json、progress.txt。
  TRIGGER when: 用户说 "初始化项目"、"开始新项目"、"部署架构"；项目缺少 CLAUDE.md 或 WORKFLOW.md。
  DO NOT TRIGGER when: 项目已有完整的架构文件（CLAUDE.md + WORKFLOW.md + architecture.md）。
license: Apache-2.0
---

# Coding Workflow - 项目初始化器

部署 Harness Engineering 架构文件到项目，让 AI 后续自驱动开发，并把文档先行作为运行时门禁。

---

## 核心理念

```
Skill 是"安装器"（一次性）
项目文件是"运行时"（后续自驱动）
Memory 是"路由提示"（提醒读取项目文件，不保存项目状态）

AI 读取 skill → 部署架构文件 → 后续只读项目文件
```

## Memory Is Routing, Not State

Memory can remind an agent to read `CLAUDE.md`, `WORKFLOW.md`, `task.json`, and
`progress.txt`, but it cannot replace those files.

Rules:
- `CLAUDE.md` and `WORKFLOW.md` are runtime entry points.
- `task.json` is the source of truth for task state.
- `progress.txt` is the source of truth for execution history, testing evidence, and blocks.
- `PROJECT.md` and `docs/*` win for lifecycle, requirements, design, and version context.
- If memory conflicts with repo files, trust repo files.

Recommended memory:

```text
For projects using software-dev/coding-workflow: read CLAUDE.md first, then PROJECT.md and WORKFLOW.md. Memory is only a routing hint; repo files are the source of truth. Pass the Documentation Gate before source edits.
```

Conflict examples:
- Memory says a task is complete, but `task.json` says `passes=false` → the task is incomplete.
- Memory says direct source edits are allowed, but `WORKFLOW.md` requires Documentation Gate → pass the gate first.
- Memory recalls an old design, but `docs/design.md` differs → follow `docs/design.md`.

---

## 触发条件

- 用户说 "初始化项目"、"开始新项目"、"部署架构"
- 项目缺少 `CLAUDE.md` 或 `WORKFLOW.md`

---

## 安装流程

### Step 1: 检查项目状态

**输入**：项目根目录路径

**操作**：检查以下文件是否存在：
- `CLAUDE.md`
- `WORKFLOW.md`
- `architecture.md`
- `PROJECT.md`（如项目使用 software-dev 生命周期）
- `docs/requirements.md`、`docs/design.md`（如项目使用文档先行）

**输出**：文件存在状态列表

**检查点 1**：如果检测到部分文件已存在：
1. 列出已存在的文件及其修改时间
2. 询问用户：「检测到已有架构文件，选择操作：[覆盖/跳过已存在/取消]」
3. 根据用户选择执行对应操作

### Step 2: 收集项目信息

**输入**：用户回答（可选，可能已在初始 prompt 中提供）

**操作**：向用户收集以下信息：
- 项目目标（一句话描述）
- 技术栈（语言、框架、数据库等）
- 核心功能（3-5 个主要功能点）
- 特殊约束（如有）

**智能处理**：如果用户在初始 prompt 中已提供部分信息（如 "这是一个博客系统，使用 React + Node.js"），则：
1. 提取已提供的信息，跳过对应询问
2. 只询问未提供的信息项
3. 确认提取的信息是否正确

**输出**：项目信息对象

**检查点 2**：逐项询问（或让用户一次性提供）。如果用户选择跳过，使用占位符模板，后续可手动填充。

### Step 3: 部署架构文件

**前置检查**：确认 skill 的模板和脚本目录存在：
- `assets/templates/` 目录存在
- `scripts/` 目录存在

如果缺失，报错并终止。

**输入**：Step 1 检查结果 + Step 2 项目信息

**操作**：根据检查结果，按顺序部署文件：

| 序号 | 文件 | 模板路径 | 说明 |
|------|------|----------|------|
| 1 | `CLAUDE.md` | `assets/templates/CLAUDE.md` | 如已存在，询问合并或覆盖 |
| 2 | `WORKFLOW.md` | `assets/templates/WORKFLOW.md` | 直接复制 |
| 3 | `architecture.md` | `assets/templates/architecture.md` | 填充项目信息 |
| 4 | `task.json` | `assets/templates/task.json` | 如不存在则创建 |
| 5 | `progress.txt` | `assets/templates/progress.txt` | 如不存在则创建 |

**输出**：部署的文件列表

### Step 4: 验证部署

**输入**：`architecture.md` 文件路径

**操作**：运行验证脚本
```bash
python scripts/validate_architecture.py --architecture-file architecture.md
```

**输出**：验证结果（通过/失败 + 错误日志）

**检查点 3**：如果验证失败：
1. 展示错误日志
2. 询问用户：「验证失败，选择操作：[查看详情并修复/跳过验证/取消]」
3. 根据选择执行对应操作

### Step 5: 完成提示

**输入**：部署结果

**输出**：用户提示信息
```
项目已初始化完成。部署的文件：
- CLAUDE.md（项目配置和导航入口）
- WORKFLOW.md（工作流程和 Documentation Gate）
- architecture.md（架构约束）
- task.json（任务模板和文档引用）

后续开发：
- 新对话时，AI 自动读取 CLAUDE.md，再按 WORKFLOW.md 通过 Documentation Gate
- 不需要再次调用此 skill
```

---

## 已初始化项目

如果项目已有完整的架构文件，告诉用户：

```
项目已初始化，架构文件完整。

后续开发：
- 新对话时 AI 自动读取 CLAUDE.md
- AI 会自动读取 WORKFLOW.md、architecture.md、task.json 和相关 docs
- 源码修改前必须通过 WORKFLOW.md 中的 Documentation Gate
- 按渐进式披露原则，按需读取必要文件
```

---

## 部署文件说明

| 文件 | 职责 | AI 读取时机 |
|------|------|-------------|
| `CLAUDE.md` | 项目配置和导航入口 | 新对话自动读取 |
| `WORKFLOW.md` | 工作流程（Orchestrator）和 Documentation Gate | 需要执行任务时 |
| `executor.md` | Executor 子代理指令 | spawn executor 时 |
| `verifier.md` | Verifier 子代理指令 | spawn verifier 时 |
| `architecture.md` | 技术栈、目录结构、约束 | 编码前读取 |
| `task.json` | 任务定义、依赖、需求/设计引用 | 需要知道做什么时 |
| `progress.txt` | 开发历史、文档更新、测试证据 | 需要了解上下文时 |

---

## 模板文件

所有模板位于 `assets/templates/`：

| 模板 | 用途 |
|------|------|
| `CLAUDE.md` | 项目配置和导航入口模板 |
| `WORKFLOW.md` | 工作流程模板（Orchestrator） |
| `executor.md` | Executor 子代理指令模板 |
| `verifier.md` | Verifier 子代理指令模板 |
| `architecture.md` | 架构约束模板 |
| `task.json` | 任务定义模板 |
| `progress.txt` | 进度记录模板 |
| `init.sh` | 项目初始化脚本 |
| `project-config.json` | 项目配置模板 |

---

## 验证脚本

所有脚本位于 `scripts/`：

| 脚本 | 用途 |
|------|------|
| `validate_architecture.py` | 验证 architecture.md 完整性 |
| `validate_iteration.py` | 验证迭代一致性 |
| `plan_batches.py` | 分析任务依赖和并行批次 |
| `select_next_task.py` | 选择下一个可执行任务 |

---

## 参考文档

| 文档 | 用途 |
|------|------|
| `references/frontend-best-practices.md` | 前端开发最佳实践 |
