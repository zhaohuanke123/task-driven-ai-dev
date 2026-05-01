# Development Workflow

完整工作流程指南，AI 自驱动开发时遵循此流程。

---

## 多代理架构

```
Orchestrator（主代理）
  ├── 读取 task.json，分析依赖图
  ├── 创建 git worktrees 用于并行任务
  ├── spawn Executor 子代理（一个任务一个，并行执行）
  ├── spawn Verifier 子代理（一个任务一个，并行验证）
  ├── 合并 worktree 分支回 main
  └── 提交 task.json + progress.txt 更新
```

**三种角色**：
- **Orchestrator** — 协调批次、管理 worktrees、合并结果
- **Executor** — 在隔离 worktree 中实现单个任务
- **Verifier** — 独立审查和测试 executor 的输出

---

## 工作模式

### Mode 1: Continue（默认）

当用户说 "继续"、"下一个任务"、"开发"：

1. 读取 `PROJECT.md`（如存在）获取阶段、版本、恢复上下文
2. 读取 `task.json` 获取任务列表和文档引用
3. 读取 `progress.txt` 了解当前进度
4. 运行依赖分析选择可执行任务
5. 执行 Documentation Gate
6. 执行任务（见下方执行流程）

### Mode 2: Status

当用户说 "状态"、"进度"：

1. 读取 `task.json` 和 `progress.txt`
2. 汇报：已完成/剩余/阻塞的任务
3. 显示哪些任务可并行执行

### Mode 3: Specific Task

当用户指定任务 ID 或描述：

1. 在 `task.json` 中定位任务
2. 检查任务的 `requirement_ref`、`design_ref`、`docs_updated`
3. 作为单任务批次执行

### Mode 4: Bug / Behavior Fix

当用户说 "bug"、"有问题"、"不对"、"修一下"、"改成..."：

1. 读取 `PROJECT.md`（如存在）、`task.json`、`progress.txt`
2. 定位相关需求、设计、架构文档
3. 判断类型：
   - 文档已定义正确行为但代码不符：记录为 implementation bug
   - 用户请求新行为或变更：先更新需求/设计/架构文档
   - 没有对应文档：先创建或补齐最小文档说明
4. Documentation Gate 通过后才进入源码修改

---

## Orchestrator 执行流程

### Step 1: Documentation Gate

**源码修改前必须通过**。如果未通过，禁止创建 executor 或编辑源码。

必须读取：

```
1. PROJECT.md（如存在）- 当前阶段、版本、恢复上下文
2. task.json - 任务、依赖、requirement_ref、design_ref
3. progress.txt - 已完成工作、测试证据、跳过文档记录
4. docs/requirements.md - 行为和范围要求（如存在）
5. docs/design.md - 模块设计和接口契约（如存在）
6. docs/architecture.md 或 architecture.md - 架构边界
```

通过条件：

| 检查项 | 通过标准 |
|--------|----------|
| 任务文档引用 | 当前任务有 `requirement_ref` 和 `design_ref`，或有明确的等价文档章节 |
| 行为定义 | bug/feature/behavior change 的预期行为已写入需求或设计 |
| 文档更新 | 如果行为变化，相关文档已先更新，任务 `docs_updated` 为 `true` |
| 跳过记录 | 如果用户确认跳过文档，`PROJECT.md` 或 `progress.txt` 记录了原因、风险、待补文档 |

未通过时：

1. 不进入源码实现。
2. 先更新相关文档或记录显式跳过。
3. 在 `progress.txt` 记录 Documentation Gate 的状态。

### Step 2: 架构约束检查

**编码前必须读取**：

```
1. docs/architecture.md 或 architecture.md - 获取技术栈、目录结构、禁止事项
2. 确认理解关键约束
```

从 `architecture.md` 提取：

| 约束类型 | 章节 | 确认内容 |
|----------|------|----------|
| 技术栈 | `## Tech Stack` | 框架、语言、库 |
| 目录结构 | `## Directory Structure` | 代码放置位置 |
| 禁止事项 | `## Key Constraints` | 什么不能做 |

### Step 3: 任务选择

使用依赖分析：

```bash
python scripts/plan_batches.py --task-file task.json --format json
```

选择规则：
- 所有依赖任务必须已完成（`passes: true`）
- 当前任务必须通过 Documentation Gate
- 同批次任务无文件冲突
- 同批次任务无 `conflict_groups` 冲突

### Step 4: Worktree 创建

为每个任务创建隔离工作树：

```bash
git worktree add .worktrees/task-<ID> -b feature/task-<ID>
```

### Step 5: Spawn Executor 子代理

为每个任务 spawn 一个 executor 子代理，**所有 executor 并行运行**。

**Executor 提示模板**：

```
读取 executor.md 获取你的指令。

=== 必须首先执行 ===
1. 读取 AGENTS.md、WORKFLOW.md、PROJECT.md（如存在）
2. 读取任务的 requirement_ref 和 design_ref
3. 读取 docs/architecture.md 或 architecture.md 获取架构约束
4. 如果 Documentation Gate 未通过，报告 BLOCKED，不要修改源码

=== 你的任务 ===
- Task ID: <id>
- Title: <title>
- Requirement ref: <requirement_ref>
- Design ref: <design_ref>
- Docs updated: <docs_updated>
- Steps:
  <步骤列表>

=== 你的环境 ===
- Worktree: .worktrees/task-<id>/
- Branch: feature/task-<id>

读取 executor.md 后，按启动协议执行任务。
```

### Step 6: 处理 Executor 结果

**如果 completed**：
- 记录变更文件
- 进入验证阶段

**如果 blocked**：
- 写入 `progress.txt` 阻塞信息
- 清理 worktree：
  ```bash
  git worktree remove .worktrees/task-<ID> --force
  git branch -D feature/task-<ID>
  ```
- 报告阻塞给用户

### Step 7: Spawn Verifier 子代理

为每个完成的任务 spawn 一个 verifier 子代理，**所有 verifier 并行运行**。

**Verifier 提示模板**：

```
读取 verifier.md 获取你的指令。

=== 验证目标 ===
- Task ID: <id>
- Title: <title>
- Steps: <步骤列表>
- Requirement ref: <requirement_ref>
- Design ref: <design_ref>
- Docs updated: <docs_updated>
- Worktree: .worktrees/task-<id>/
- Files changed: <文件列表>

读取 verifier.md 后，按验证流程检查 docs/code/tests 是否一致。
```

### Step 8: 处理 Verifier 结果

**如果 PASS**：
- 合并 worktree
- 更新 task.json 和 progress.txt
- 将 `docs_updated`、`implementation_done`、`verified`、`passes` 设为 `true`

**如果 FAIL 或 PARTIAL**：
- 记录失败原因到 progress.txt
- 清理 worktree（不合并）

### Step 9: 合并或回滚

**验证通过**：

```bash
git merge feature/task-<ID> --no-edit
git worktree remove .worktrees/task-<ID>
git branch -d feature/task-<ID>
```

**验证失败**：

```bash
git worktree remove .worktrees/task-<ID> --force
git branch -D feature/task-<ID>
```

记录失败原因到 `progress.txt`。

### Step 10: 记录和提交

更新 `progress.txt`：

```
## [YYYY-MM-DD] - Task #N: [Title]

### What was done:
- [变更列表]

### Documentation:
- Requirement ref: [docs/requirements.md#...]
- Design ref: [docs/design.md#...]
- Docs updated: yes/no/skipped
- Skip risk and follow-up docs: [如适用]

### Testing:
- [测试结果]

### Notes:
- [备注]
```

更新 `task.json`：将 `docs_updated`、`implementation_done`、`verified`、`passes` 改为 `true`

提交：

```bash
git add .
git commit -m "complete task #N: [Title]"
```

---

## 阻塞处理

当任务无法完成：

1. **不合并** worktree
2. 清理 worktree 和分支
3. 写入 `progress.txt`：

```
## [YYYY-MM-DD] - Task #N: [Title] - BLOCKED

### Block reason:
- [具体原因]

### Human action needed:
1. [步骤1]
2. [步骤2]
```

4. 报告给用户

---

## Guardrails

1. **文档先行** - bug、功能、行为变更必须先通过 Documentation Gate
2. **架构优先** - 编码前必须读取 `docs/architecture.md` 或 `architecture.md`
3. **Worktree 隔离** - 每个任务在独立 worktree 中执行
4. **验证先于合并** - 验证通过才能合并
5. **单批次执行** - 每次处理一个批次，汇报结果
6. **阻塞不伪造** - 无法完成时报告阻塞，不标记完成
7. **清理 Worktree** - 完成后移除 worktree 和分支
8. **并行执行** - 同批次任务的 executor 和 verifier 并行运行

---

## 子代理指令文件

| 文件 | 用途 |
|------|------|
| `executor.md` | Executor 子代理指令 |
| `verifier.md` | Verifier 子代理指令 |

---

## 脚本工具

| 脚本 | 用途 |
|------|------|
| `scripts/plan_batches.py` | 分析依赖，输出并行批次 |
| `scripts/validate_iteration.py` | 验证迭代一致性 |
| `scripts/validate_architecture.py` | 验证架构文档完整性 |
