---
name: coding-workflow
description: |
  项目初始化和多代理编排工作流。部署架构文件（CLAUDE.md、architecture.md、task.json、progress.txt）到目标项目，
  然后作为 Orchestrator 协调 planner/executor/verifier 子代理完成 PEV（Plan-Execute-Verify）三层分离的开发迭代。
  TRIGGER when: 用户说 "初始化项目"、"开始新项目"、"部署架构"；项目缺少 CLAUDE.md 或 WORKFLOW.md。
  DO NOT TRIGGER when: 项目已有完整的架构文件。
license: Apache-2.0
---

# Coding Workflow

项目初始化 + PEV 多代理编排。一次性部署架构文件，后续 AI 自驱动开发。

---

## 核心理念

```
install.py 是"安装器"（一次性部署 4 个项目文件）
SKILL.md 是"Orchestrator 剧本"（后续自驱动）
Memory 是"路由提示"（提醒读取项目文件，不保存项目状态）
PEV 是"三层分离"（Planner 规划 → Executor 执行 → Verifier 验证）
```

---

## PEV 三层架构

```
Orchestrator (SKILL.md)
    │
    ▼
┌─ Layer 1: Planner ─────────────────────┐
│  分析代码库 + 需求 → 生成实现计划        │
│  输出: Implementation Plan + 验收标准    │
│  权限: 只读（不写任何文件）              │
└────────────────────────────────────────┘
    │ ready
    ▼
┌─ Layer 2: Executor ────────────────────┐
│  按 Planner 计划写代码（worktree 隔离）  │
│  验证: 只跑 lint + build，不跑 test     │
└────────────────────────────────────────┘
    │ completed
    ▼
┌─ Layer 3: Verifier ────────────────────┐
│  写测试 + 跑测试 + 独立审查              │
│  FAIL 时提供修复建议打回 executor        │
└────────────────────────────────────────┘
    │ PASS → merge | FAIL → retry (max 2)
```

**为什么三层分离：**
- **Planner 独立** — 避免执行者"边想边写"导致上下文膨胀
- **Executor 不跑 test** — 对抗自我评估的乐观偏见，测试由独立验证者编写和运行
- **Verifier 独立审查** — 类似 GAN 的生成对抗架构，验证者独立于生成者

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

部署项目文件和 PEV Agent 定义到目标项目：

**项目文件（4 个）：**
- `CLAUDE.md` — 导航入口，新对话自动读取
- `architecture.md` — 技术栈、目录结构、约束
- `task.json` — 任务定义和依赖
- `progress.txt` — 进度日志和测试证据

**PEV Agent 定义（3 个）：**
- `.agents/planner.md` — 规划层：分析需求、生成实现计划
- `.agents/executor.md` — 执行层：按计划编写代码
- `.agents/verifier.md` — 验证层：编写测试、独立审查

已有项目只需运行一次。后续开发 AI 自动读取这些文件。

---

## 工作模式

### Mode 1: Continue（默认）

用户说 "继续"、"下一个任务"、"开发"：

1. 读取 `task.json` 获取任务列表
2. 读取 `progress.txt` 了解当前进度
3. 选择下一个可执行任务（依赖已满足且 `done: false`）
4. 执行 Documentation Gate
5. PEV 三层流程：Spawn planner → executor → verifier → 合并

### Mode 2: Status

用户说 "状态"、"进度"：

1. 读取 `task.json` 和 `progress.txt`
2. 汇报：已完成 / 剩余 / 阻塞的任务

### Mode 3: Specific Task

用户指定任务 ID：

1. 在 `task.json` 中定位任务
2. 检查依赖是否满足
3. 作为单任务执行 PEV 流程

### Mode 4: Bug / Behavior Fix

用户说 "bug"、"有问题"、"修一下"：

1. 定位相关文档
2. 判断类型：
   - 文档已定义正确行为但代码不符 → 记录为 implementation bug
   - 用户请求新行为 → 先更新文档
   - 没有对应文档 → 先创建最小文档
3. Documentation Gate 通过后进入 PEV 流程
4. 如果确认不需要改文档（纯 bug fix），在 `progress.txt` 写入 `[DOC-GATE-BYPASS] Task #<id>: 纯 bug fix，文档已定义正确行为` 以绕过 Hook 拦截

---

## Orchestrator 执行流程（10 步）

### Step 1: 任务选择

读取 `task.json`，选第一个 `dependencies` 全部 `done: true` 且自身 `done: false` 的任务。

### Step 2: Documentation Gate

源码修改前必须确认：

| 检查项 | 条件 |
|--------|------|
| 行为定义 | 任务的预期行为有文档定义（任务 `docs` 字段 或 `docs/requirements.md`） |
| 架构约束 | 已读取 `architecture.md`，确认技术栈和禁止事项 |
| 文档更新 | 行为变化时文档已先更新 |

不通过 → 先补文档，不进入 PEV 流程。

**机械化执行：** PreToolUse Hook（`.claude/hooks/doc-gate.sh`）会在 Edit/Write 源码文件时自动检查 git diff 中是否有文档变更。无文档变更且无 BYPASS 记录 → 拦截（exit 2）。BYPASS 通过 `progress.txt` 中 `[DOC-GATE-BYPASS] Task #<id>: <原因>` 绕过，绑定当前任务 ID。

### Step 3: Worktree 创建

```bash
git worktree add .worktrees/task-<id> -b feature/task-<id>
```

### Step 4: Spawn Planner（Layer 1）

```
Agent(subagent_type: "planner", prompt: """
分析以下任务并生成实现计划。

=== 任务 ===
- Task ID: <id>
- Title: <title>
- Steps: <步骤列表>
- Docs: <docs 引用>

请按 Implementation Plan 格式返回分析结果。
""")
```

### Step 5: 处理 Planner 结果

- **ready** → 将 Implementation Plan 存入变量，进入 Step 6
- **blocked** → 清理 worktree，记录 `progress.txt`，报告用户

### Step 6: Spawn Executor（Layer 2）

```
Agent(subagent_type: "executor", isolation: "worktree", prompt: """
在 worktree .worktrees/task-<id>/ 中实现以下任务。

=== 任务 ===
- Task ID: <id>
- Title: <title>

=== Planner 的 Implementation Plan ===
<Planner 返回的完整 Implementation Plan>

严格按此计划执行。只修改 File Ownership Map 中的文件。
""")
```

### Step 7: 处理 Executor 结果

- **completed** → 进入验证（Step 8）
- **blocked** → 清理 worktree，记录 `progress.txt`，报告用户

### Step 8: Spawn Verifier（Layer 3）

```
Agent(subagent_type: "verifier", isolation: "worktree", prompt: """
验证 worktree .worktrees/task-<id>/ 中的实现。

=== 验证目标 ===
- Task ID: <id>
- Title: <title>
- Files changed: <executor 报告的文件列表>

=== Planner 的 Acceptance Criteria ===
<Planner 返回的 Acceptance Criteria>

=== Planner 的 Test Scenarios ===
<Planner 返回的 Test Scenarios>

请编写测试用例（如果需要），运行全量验证，报告结果。
""")
```

### Step 9: 处理 Verifier 结果 + 反馈循环

**PASS** → 合并 worktree，更新 `task.json`（`done: true`），记录 `progress.txt`，进入 Step 10。

**FAIL** → 进入反馈循环：

```
retry_count = 0
max_retries = 2

while retry_count < max_retries:
    retry_count += 1

    1. 清理 worktree（git reset --hard）
    2. 重新 Spawn Executor，附加 Verifier 反馈：
       Agent(subagent_type: "executor", isolation: "worktree", prompt: """
       [原有 prompt]

       === Verifier 反馈（必须修复） ===
       <Verifier 的 Failures 列表>

       === Retry Recommendation ===
       <Verifier 的 Retry Recommendation>

       请修复以上问题并重新提交。
       """)
    3. Executor 修复后 → 重新 Spawn Verifier
    4. Verifier PASS → break → merge
    5. Verifier FAIL → continue retry loop

如果 max_retries 用尽仍 FAIL:
    - 放弃当前任务
    - 清理 worktree（不合并）
    - 在 progress.txt 记录 BLOCKED，附上失败摘要
    - 报告用户
```

合并命令：

```bash
git merge feature/task-<id> --no-edit
git worktree remove .worktrees/task-<id>
git branch -d feature/task-<id>
```

### Step 10: 提交

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

1. **PEV 三层分离** — 规划、执行、验证由独立 Agent 完成
2. **文档先行** — 编码前必须通过 Documentation Gate
3. **Repo 文件优先于 memory** — 冲突时以项目文件为准
4. **架构优先** — 编码前必须读取 `architecture.md`
5. **Worktree 隔离** — 每个任务独立 worktree
6. **文件所有权** — 任何文件只能有一个 owner，两个 Agent 不能同时修改同一文件
7. **验证先于合并** — verifier PASS 才能合并
8. **测试由验证者编写** — executor 不跑 test，verifier 独立编写和运行测试
9. **阻塞不伪造** — 无法完成时报告阻塞，不标记 done
10. **反馈循环有界** — 最多 2 轮重试，超出则报告用户
11. **Documentation Gate 机械化执行** — PreToolUse Hook（`.claude/hooks/doc-gate.sh`）拦截未经文档更新的源码修改。BYPASS 通过 `progress.txt` 中 `[DOC-GATE-BYPASS] Task #<id>: <原因>` 绑定当前任务

---

## 项目文件说明

部署到目标项目的文件：

| 文件 | 职责 | AI 读取时机 |
|------|------|-------------|
| `CLAUDE.md` | 导航入口 | 新对话自动读取 |
| `architecture.md` | 技术栈、目录、约束 | 编码前 |
| `task.json` | 任务定义和依赖 | 需要知道做什么时 |
| `progress.txt` | 进度历史和测试证据 | 需要了解上下文时 |
| `.agents/planner.md` | PEV 规划层 Agent 定义 | 被 Orchestrator spawn 时 |
| `.agents/executor.md` | PEV 执行层 Agent 定义 | 被 Orchestrator spawn 时 |
| `.agents/verifier.md` | PEV 验证层 Agent 定义 | 被 Orchestrator spawn 时 |

## 验证脚本

```bash
python scripts/validate_architecture.py --architecture-file architecture.md
```

机械化检查 architecture.md 是否有所有必需章节。
