# Architecture Deployment Guide

指导 AI 如何部署 Harness Engineering 架构文件和文档先行运行时门禁到项目目录。

---

## 核心理念

**Skill 是"安装器"，项目文件是"运行时"**

```
AI 读取 skill（一次性）→ 部署架构文件和文档门禁 → 后续只读项目文件自驱动
```

---

## 部署检查

检查项目根目录是否存在以下文件：

| 文件 | 必须存在 | 检查逻辑 |
|------|----------|----------|
| `AGENTS.md` | ✅ | 导航入口，AI 新对话首先读取 |
| `WORKFLOW.md` | ✅ | 工作流程指南和 Documentation Gate |
| `PROJECT.md` | ⚠️ | 项目状态，software-dev 项目应存在 |
| `docs/requirements.md` | ⚠️ | 行为和范围要求，software-dev 项目应存在 |
| `docs/design.md` | ⚠️ | 模块设计和接口契约，software-dev 项目应存在 |
| `architecture.md` | ✅ | 架构约束 |
| `task.json` | ⚠️ | 任务定义和文档引用，可使用模板 |
| `progress.txt` | ⚠️ | 开发历史、文档更新、测试证据，可使用模板 |

---

## 部署流程

### Step 1: 收集项目信息

向用户询问（如未提供）：

1. **项目名称** - 用于 AGENTS.md 标题
2. **项目目标** - 1-2 句话描述
3. **技术栈** - Frontend/Backend/Database/Auth
4. **核心功能** - 主要功能点
5. **约束条件** - 禁止事项、必须遵守的规则
6. **文档来源** - 是否已有 `PROJECT.md`、`docs/requirements.md`、`docs/design.md`

### Step 2: 部署 AGENTS.md

使用模板 `assets/templates/AGENTS.md`：

- 填充项目名称
- 填充项目描述
- 填充目录结构（根据技术栈）
- 填充关键约定
- 保留 Documentation Gate 和读取顺序
- 控制在 ~60 行

### Step 3: 部署 WORKFLOW.md

使用模板 `assets/templates/WORKFLOW.md`：

- 直接复制，无需修改
- 包含完整工作流程和 Documentation Gate

### Step 4: 部署 architecture.md

使用模板 `assets/templates/architecture.md`：

- 填充 Overview
- 填充 Tech Stack 表格（含选择理由）
- 填充 Directory Structure
- 填充 Data Model
- 填充 API Design
- 填充 Key Constraints（必须遵守 + 禁止事项）

### Step 5: 部署 task.json（如不存在）

使用模板 `assets/templates/task.json`：

- 填充项目名称和描述
- 每个任务必须包含 `requirement_ref`、`design_ref`、`docs_updated`
- 可保留示例任务或清空

### Step 6: 部署 progress.txt（如不存在）

使用模板 `assets/templates/progress.txt`：

- 初始化为空或添加第一条记录
- 保留文档更新、跳过文档风险、测试证据的记录格式

### Step 7: 验证部署

运行验证脚本：

```bash
python scripts/validate_architecture.py --architecture-file architecture.md
```

确保所有必需章节存在。

---

## 模板文件位置

所有模板位于 `skills/coding-workflow/assets/templates/`：

| 模板 | 用途 | 部署后位置 |
|------|------|------------|
| `AGENTS.md` | 导航入口 | `<project-root>/AGENTS.md` |
| `WORKFLOW.md` | 工作流程和 Documentation Gate | `<project-root>/WORKFLOW.md` |
| `architecture.md` | 架构约束 | `<project-root>/architecture.md` |
| `task.json` | 任务定义和文档引用 | `<project-root>/task.json` |
| `progress.txt` | 进度记录、文档更新、测试证据 | `<project-root>/progress.txt` |

---

## AGENTS.md 智能生成策略

根目录必须生成，子目录根据复杂度判断：

**判断规则**：

- 目录有 3+ 子目录 或 5+ 文件 → 生成
- 目录有明确职责边界（如 `src/components/`）→ 生成
- 目录是叶子目录（只有代码文件）→ 不生成

**示例**：

```
src/                    → 生成（有多个子目录）
src/app/                → 生成（职责明确）
src/app/api/            → 生成（有多个路由）
src/app/api/users/      → 不生成（叶子目录）
src/components/         → 生成（组件库）
src/lib/                → 生成（工具库）
src/lib/db/             → 不生成（叶子目录）
```

---

## 完成提示

部署完成后告诉用户：

```
项目已初始化完成。部署的文件：
- AGENTS.md（导航入口）
- WORKFLOW.md（工作流程和 Documentation Gate）
- architecture.md（架构约束）
- task.json（任务模板和文档引用）
- progress.txt（进度记录、文档更新、测试证据）

后续开发：
- 新对话时，AI 先读取 AGENTS.md，再按 WORKFLOW.md 通过 Documentation Gate
- AI 会按渐进式披露原则，按需读取其他文件
- 不需要再次调用 coding-workflow skill
```

---

## 已初始化项目处理

如果项目已有完整架构文件：

```
项目已初始化，架构文件完整。

后续开发：
- 新对话时读取 AGENTS.md 即可
- AI 会自动读取 WORKFLOW.md、architecture.md、task.json 和相关 docs
- 源码修改前必须通过 WORKFLOW.md 中的 Documentation Gate
- 按渐进式披露原则，按需读取必要文件
```

---

## 验证脚本

| 脚本 | 用途 |
|------|------|
| `scripts/validate_architecture.py` | 验证 architecture.md 必需章节 |
| `scripts/validate_iteration.py` | 验证迭代一致性 |
| `scripts/plan_batches.py` | 分析任务依赖和并行批次 |
