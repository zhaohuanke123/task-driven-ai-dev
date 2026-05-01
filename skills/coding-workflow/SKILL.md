---
name: coding-workflow
description: |
  项目初始化器 - 部署 Harness Engineering 架构文件和文档先行运行时门禁到项目目录。
  TRIGGER when: 用户说 "初始化项目"、"开始新项目"、"部署架构"；项目缺少 AGENTS.md 或 WORKFLOW.md。
  DO NOT TRIGGER when: 项目已有完整的架构文件（AGENTS.md + WORKFLOW.md + architecture.md）。
license: Apache-2.0
---

# Coding Workflow - 项目初始化器

部署 Harness Engineering 架构文件到项目，让 AI 后续自驱动开发，并把文档先行作为运行时门禁。

---

## 核心理念

```
Skill 是"安装器"（一次性）
项目文件是"运行时"（后续自驱动）

AI 读取 skill → 部署架构文件 → 后续只读项目文件
```

---

## 触发条件

- 用户说 "初始化项目"、"开始新项目"、"部署架构"
- 项目缺少 `AGENTS.md` 或 `WORKFLOW.md`

---

## 安装流程

### Step 1: 检查项目状态

检查项目根目录是否存在以下文件：
- `AGENTS.md`
- `WORKFLOW.md`
- `architecture.md`
- `PROJECT.md`（如项目使用 software-dev 生命周期）
- `docs/requirements.md`、`docs/design.md`（如项目使用文档先行）

### Step 2: 部署架构文件

如果文件缺失，按以下顺序部署：

1. **AGENTS.md** - 项目导航入口（~60行）
   - 使用模板：`assets/templates/AGENTS.md`
   - 根据项目信息填充

2. **WORKFLOW.md** - 完整工作流程指南和 Documentation Gate
   - 使用模板：`assets/templates/WORKFLOW.md`
   - 包含文档门禁、执行、验证、合并流程

3. **architecture.md** - 架构约束
   - 使用模板：`assets/templates/architecture.md`
   - 向用户收集：项目目标、技术栈、核心功能

4. **task.json** - 任务定义模板（如不存在）
   - 使用模板：`assets/templates/task.json`
   - 每个任务包含 `requirement_ref`、`design_ref`、`docs_updated`

5. **progress.txt** - 开发历史（如不存在）
   - 使用模板：`assets/templates/progress.txt`
   - 记录文档更新、测试证据、跳过文档风险

### Step 3: 验证部署

运行验证脚本：
```bash
python scripts/validate_architecture.py --architecture-file architecture.md
```

### Step 4: 完成提示

告诉用户：
```
项目已初始化完成。部署的文件：
- AGENTS.md（导航入口）
- WORKFLOW.md（工作流程和 Documentation Gate）
- architecture.md（架构约束）
- task.json（任务模板和文档引用）

后续开发：
- 新对话时，AI 先读取 AGENTS.md，再按 WORKFLOW.md 通过 Documentation Gate
- 不需要再次调用此 skill
```

---

## 已初始化项目

如果项目已有完整的架构文件，告诉用户：

```
项目已初始化，架构文件完整。

后续开发：
- 新对话时读取 AGENTS.md 即可
- AI 会自动读取 WORKFLOW.md、architecture.md、task.json 和相关 docs
- 源码修改前必须通过 WORKFLOW.md 中的 Documentation Gate
- 按渐进式披露原则，按需读取必要文件
```

---

## 部署文件说明

| 文件 | 职责 | AI 读取时机 |
|------|------|-------------|
| `AGENTS.md` | 导航入口，指向所有文件 | 新对话首先读取 |
| `WORKFLOW.md` | 工作流程（Orchestrator）和 Documentation Gate | 需要执行任务时 |
| `executor.md` | Executor 子代理指令 | spawn executor 时 |
| `verifier.md` | Verifier 子代理指令 | spawn verifier 时 |
| `architecture.md` | 技术栈、目录结构、约束 | 编码前读取 |
| `task.json` | 任务定义、依赖、需求/设计引用 | 需要知道做什么时 |
| `progress.txt` | 开发历史、文档更新、测试证据 | 需要了解上下文时 |

---

## 模板文件

所有模板位于 `assets/templates/`：
- `AGENTS.md` - 导航入口模板
- `WORKFLOW.md` - 工作流程模板（Orchestrator）
- `executor.md` - Executor 子代理指令模板
- `verifier.md` - Verifier 子代理指令模板
- `architecture.md` - 架构约束模板
- `task.json` - 任务定义模板
- `progress.txt` - 进度记录模板

---

## 验证脚本

- `scripts/validate_architecture.py` - 验证 architecture.md 完整性
- `scripts/validate_iteration.py` - 验证迭代一致性
- `scripts/plan_batches.py` - 分析任务依赖和并行批次
