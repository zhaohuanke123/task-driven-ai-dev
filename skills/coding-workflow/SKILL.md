---
name: coding-workflow
description: |
  项目初始化和多代理编排工作流。部署架构文件（CLAUDE.md、architecture.md、task.json、progress.txt）到目标项目，
  然后作为 Orchestrator 协调 executor/verifier 子代理完成文档门禁的开发迭代。
  TRIGGER when: 用户说 "初始化项目"、"开始新项目"、"部署架构"；项目缺少 CLAUDE.md 或 WORKFLOW.md。
  DO NOT TRIGGER when: 项目已有完整的架构文件。
license: Apache-2.0
---

# Coding Workflow

项目初始化 + 多代理编排。一次性部署架构文件，后续 AI 自驱动开发。

---

## 核心理念

```
install.py 是"安装器"（一次性部署 4 个项目文件）
SKILL.md 是"Orchestrator 剧本"（后续自驱动）
Memory 是"路由提示"（提醒读取项目文件，不保存项目状态）
```

---

## Memory Is Routing, Not State

Memory 只能提醒 agent 读取 `CLAUDE.md`、`task.json`、`progress.txt`，不能替代这些文件。

冲突优先级：

```text
用户最新明确指令
> PROJECT.md / docs/* / task.json / progress.txt
> CLAUDE.md / architecture.md
> skill instructions
> memory hints
```

- memory 说任务完成，但 `task.json` 里 `done: false` → 任务未完成
- memory 说可以跳过文档，但 architecture.md 要求 Documentation Gate → 先过 gate
- memory 记得旧设计，但 `docs/design.md` 已更新 → 以 docs 为准

---

## 安装

```bash
python install.py --target <project-dir> --name "Project Name" \
  --description "Brief description" \
  --tech-frontend "React+TypeScript+Tailwind" \
  --tech-backend "Node.js" \
  --tech-database "PostgreSQL"
```

部署 4 个文件到目标项目：
- `CLAUDE.md` — 导航入口，新对话自动读取
- `architecture.md` — 技术栈、目录结构、约束
- `task.json` — 任务定义和依赖
- `progress.txt` — 进度日志和测试证据

已有项目只需运行一次。后续开发 AI 自动读取这些文件。

---

## 工作模式

### Mode 1: Continue（默认）

用户说 "继续"、"下一个任务"、"开发"：

1. 读取 `task.json` 获取任务列表
2. 读取 `progress.txt` 了解当前进度
3. 选择下一个可执行任务（依赖已满足且 `done: false`）
4. 执行 Documentation Gate
5. Spawn executor → verifier → 合并

### Mode 2: Status

用户说 "状态"、"进度"：

1. 读取 `task.json` 和 `progress.txt`
2. 汇报：已完成 / 剩余 / 阻塞的任务

### Mode 3: Specific Task

用户指定任务 ID：

1. 在 `task.json` 中定位任务
2. 检查依赖是否满足
3. 作为单任务执行

### Mode 4: Bug / Behavior Fix

用户说 "bug"、"有问题"、"修一下"：

1. 定位相关文档
2. 判断类型：
   - 文档已定义正确行为但代码不符 → 记录为 implementation bug
   - 用户请求新行为 → 先更新文档
   - 没有对应文档 → 先创建最小文档
3. Documentation Gate 通过后才进入源码修改

---

## Orchestrator 执行流程

### Step 1: 任务选择

读取 `task.json`，选第一个 `dependencies` 全部 `done: true` 且自身 `done: false` 的任务。

### Step 2: Documentation Gate

源码修改前必须确认：

| 检查项 | 条件 |
|--------|------|
| 行为定义 | 任务的预期行为有文档定义（任务 `docs` 字段 或 `docs/requirements.md`） |
| 架构约束 | 已读取 `architecture.md`，确认技术栈和禁止事项 |
| 文档更新 | 行为变化时文档已先更新 |

不通过 → 先补文档，不进入编码。

### Step 3: Worktree 创建

```bash
git worktree add .worktrees/task-<id> -b feature/task-<id>
```

### Step 4: Spawn Executor

```
Agent(subagent_type: "executor", isolation: "worktree", prompt: """
在 worktree .worktrees/task-<id>/ 中实现以下任务。

=== 任务 ===
- Task ID: <id>
- Title: <title>
- Steps: <步骤列表>
- Docs: <docs 引用，如无则为 "docs/requirements.md">

启动协议：
1. 读取 CLAUDE.md、architecture.md
2. 读取任务的 docs
3. Documentation Gate 自检
4. 编码并提交
""")
```

### Step 5: 处理 Executor 结果

**completed**: 进入验证。
**blocked**: 清理 worktree，记录到 progress.txt，报告用户。

### Step 6: Spawn Verifier

```
Agent(subagent_type: "verifier", isolation: "worktree", prompt: """
验证 worktree .worktrees/task-<id>/ 中的实现。

=== 验证目标 ===
- Task ID: <id>
- Title: <title>
- Steps: <步骤列表>
- Docs: <docs 引用>
- Files changed: <executor 报告的文件列表>
""")
```

### Step 7: 处理 Verifier 结果

**PASS**: 合并 worktree，更新 `task.json`（`done: true`），记录 `progress.txt`。
**FAIL/PARTIAL**: 清理 worktree（不合并），记录失败原因。

合并命令：

```bash
git merge feature/task-<id> --no-edit
git worktree remove .worktrees/task-<id>
git branch -d feature/task-<id>
```

### Step 8: 提交

```bash
git add task.json progress.txt
git commit -m "complete task #<id>: <title>"
```

---

## 阻塞处理

任务无法完成时：

1. 清理 worktree（不合并）
2. 写入 `progress.txt`：
   ```
   ## [YYYY-MM-DD] - Task #N: [Title] - BLOCKED
   ### Block reason:
   - [具体原因]
   ### Human action needed:
   1. [步骤]
   ```
3. 报告用户

---

## Guardrails

1. **文档先行** — 编码前必须通过 Documentation Gate
2. **Repo 文件优先于 memory** — 冲突时以项目文件为准
3. **架构优先** — 编码前必须读取 `architecture.md`
4. **Worktree 隔离** — 每个任务独立 worktree
5. **验证先于合并** — verifier PASS 才能合并
6. **阻塞不伪造** — 无法完成时报告阻塞，不标记 done
7. **并行执行** — 同批次 executor/verifier 可并行 spawn

---

## 项目文件说明

部署到目标项目的 4 个文件：

| 文件 | 职责 | AI 读取时机 |
|------|------|-------------|
| `CLAUDE.md` | 导航入口 | 新对话自动读取 |
| `architecture.md` | 技术栈、目录、约束 | 编码前 |
| `task.json` | 任务定义和依赖 | 需要知道做什么时 |
| `progress.txt` | 进度历史和测试证据 | 需要了解上下文时 |

## 验证脚本

```bash
python scripts/validate_architecture.py --architecture-file architecture.md
```

机械化检查 architecture.md 是否有所有必需章节。
