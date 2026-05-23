# Skill 模板

> **重要**：以下模板仅作为参考和引导，其中的格式和制作范式符合最佳规范。实际制作 Skill 时，必须根据具体需求和内容做必要的调整，而不是往模板中硬填。模板中的内容并不一定符合实际 Skill 需求，如果填入不当导致模板内容残留，可能导致 Skill 的能力漂移（执行了与目标无关的动作）。

---

## 模板一：引用型（规范/知识库）

**适用**：为 Claude 提供编码规范、设计模式、领域知识等参考。

### 模板

```yaml
---
name: {skill-name}
description: {功能描述}。触发：{关键词1、关键词2、关键词3}
---
```

```markdown
# {规范/知识名称}

{1-2 句概述}

---

## {主题一}

- 规则一
- 规则二

## {主题二}

| 分类 | 规则 | 示例 |
|------|------|------|
| ... | ... | ... |
```

### 完整示例：UITask 组件规范

```yaml
---
name: coding-standards-uitask-comp
description: UITask 中 Tofu/Comp 组件的拆分与通信规范。涵盖组件职责边界、通信方式选择、生命周期管理。触发：Tofu 拆分、Comp 设计、组件通信、UITask 组件。
---
```

```markdown
# UITask 组件规范

Tofu（Comp）是 UITask 内部的功能组件，每个 Tofu 承担单一职责。

---

## 拆分原则

- 每个 Tofu 只负责一个功能域（如：列表渲染、金币显示、按钮交互）
- Tofu 之间通过事件或 Task 中转通信，禁止直接引用其他 Tofu 的成员
- 数据源统一从 Task 层获取，Tofu 不直接访问 DS/DC

## 通信方式选择

| 场景 | 方式 | 示例 |
|------|------|------|
| 一对多通知 | 事件（EventOn） | `EventOnGoldUpdate` |
| 一对一调用 | 直接方法调用 | `m_listComp.RefreshList()` |
| 共享状态 | 通过 Task 中转 | Task 持有共享数据，各 Tofu 通过 Task 读写 |

## 生命周期

- Tofu 在 Task 的 Init 阶段创建和注册
- Task Running 时通过 Tick 或事件驱动更新
- Task Stopped 时统一清理，Tofu 自身不应持有需要手动释放的外部引用
```

---

## 模板二：任务型（操作流程）

**适用**：执行有明确步骤的操作，通常有副作用。

### 模板

```yaml
---
name: {skill-name}
description: {功能描述}。触发：{关键词}
disable-model-invocation: true
allowed-tools: {预授权工具列表}
---
```

```markdown
# {操作名称}

{简述目的}

## 步骤

1. 步骤一
2. 步骤二
3. ...
```

### 完整示例：协议代码生成

```yaml
---
name: proto-gen
description: 根据协议定义文件生成 C# 数据类代码。触发：生成协议、proto 代码、协议生成、生成 DS/DC
disable-model-invocation: true
allowed-tools: Bash(python *)
---
```

```markdown
# 协议代码生成

根据协议定义生成 C# DataSection 和 DataContainer 代码。

## 步骤

1. 确认协议定义文件路径（用户指定或从 `$ARGUMENTS` 获取）
2. 读取并解析协议结构：字段名、类型、注释
3. 生成 DS 类：字段命名使用 `m_` 前缀，属性使用 PascalCase 封装
4. 生成 DC 类：提供增删改查方法，修改后调用 `SetDirty`
5. 输出到用户指定目录，文件名与类名一致

## 命名规则

- DS 类名：`{ProtoName}DataSection`
- DC 类名：`{ProtoName}DataContainer`
- 字段：`m_{camelCaseFieldName}`
- 属性：`{PascalCaseName}`（去掉 `m_` 前缀）
```

---

## 模板三：子代理型（隔离研究/分析）

**适用**：需要隔离执行上下文、使用特定代理类型的深度任务。

### 模板

```yaml
---
name: {skill-name}
description: {功能描述}。触发：{关键词}
context: fork
agent: {Explore|Plan|自定义}
allowed-tools: {可用工具}
---
```

```markdown
# {任务名称}

{任务描述}

## 任务

1. 步骤一
2. 步骤二

## 输出格式

- 要求一
- 要求二
```

### 完整示例：模块架构分析

```yaml
---
name: analyze-module
description: 深度分析指定模块的代码架构和依赖关系。触发：分析模块、架构分析、依赖梳理、模块结构
context: fork
agent: Explore
---
```

```markdown
# 模块架构分析：$ARGUMENTS

## 任务

1. 使用 Glob 查找模块相关的所有 C# 文件（`*.cs`）
2. 使用 Grep 搜索类继承关系（`: UITaskBase`、`: SceneTaskBase` 等）
3. 分析模块内 Task、Tofu、PrefabController 的职责划分
4. 梳理模块与其他模块的依赖关系（引用、事件通信）

## 输出格式

- 模块概述（职责和边界）
- 类职责表（类名 → 职责 → 继承关系）
- 依赖关系图（文字描述）
- 潜在问题（职责越界、循环依赖等）
```

---

## 模板四：参数化型（Bug 修复/特定操作）

**适用**：需要接收参数执行的操作。

### 模板

```yaml
---
name: {skill-name}
description: {功能描述}。触发：{关键词}
arguments: [{arg1}, {arg2}]
disable-model-invocation: true
allowed-tools: {预授权工具}
argument-hint: [{arg1} {arg2}]
---
```

```markdown
# {操作名称}

{使用参数的指令描述}

## 步骤

1. 步骤一（使用 $arg1）
2. 步骤二（使用 $arg2）
```

### 完整示例：UITask 代码审查

```yaml
---
name: review-uitask
description: 审查指定 UITask 的代码质量和架构合规性。触发：审查 UITask、检查 Task 代码、UITask review
arguments: [task-name]
disable-model-invocation: true
argument-hint: [UITask类名]
---
```

```markdown
# UITask 代码审查：$task-name

## 审查范围

1. 定位 Task 类文件，阅读完整代码
2. 查找关联的 Tofu/Comp、PrefabController、DS/DC
3. 检查 Task 生命周期实现（Init → Running → Paused → Stopped）

## 检查清单

| 维度 | 检查项 |
|------|--------|
| MVC 职责 | Task 是否承担了 View 层工作？Tofu 是否越权访问 Model？ |
| 命名规范 | 字段 `m_` 前缀、函数 PascalCase、回调 `On` 前缀 |
| 生命周期 | Init 中创建资源、Stopped 中清理、Push/Pop 配对 |
| 事件管理 | 注册和注销是否配对？是否存在事件泄漏？ |
| Layer 使用 | StayOnTop 是否合理？Push/Pop 是否配对？ |

## 输出

按维度列出问题，每个问题附带文件路径和行号引用。
```

---

## 模板五：动态注入型（变更摘要/状态报告）

**适用**：需要实时获取当前状态的操作。

### 模板

````yaml
---
name: {skill-name}
description: {功能描述}。触发：{关键词}
---
````

````markdown
## 当前状态

!`{获取状态的命令}`

## 指令

{基于动态数据的分析和处理指令}
````

### 完整示例：变更摘要

```yaml
---
name: summarize-changes
description: 总结未提交变更并标记风险项。触发：改了什么、提交信息、审查 diff、变更摘要
---
```

````markdown
## 当前变更

!`git diff HEAD`

## 指令

用两到三个要点总结上述变更，然后列出风险项：
- 是否违反 MVC 职责边界（Task 直接操作 View？Tofu 访问 DS？）
- 事件注册/注销是否配对
- Layer Push/Pop 是否配对
- 命名是否符合规范（`m_` 前缀、PascalCase 等）

如果 diff 为空，说明没有未提交变更。
````

### 完整示例：PR 审查（子代理 + 动态注入）

```yaml
---
name: review-pr
description: 审查当前 PR 的客户端代码变更。触发：审查 PR、review PR、检查 PR、PR 代码审查
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---
```

````markdown
## PR 上下文

- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## 审查要求

1. 识别主要变更涉及的 Task、Tofu、PrefabController、DS/DC
2. 检查 MVC 职责是否清晰
3. 检查事件管理和 Layer 操作是否规范
4. 检查 C# 命名规范（m_ 前缀、PascalCase、On 回调）
5. 标注风险项：资源泄漏、事件未注销、Layer 未配对 Pop
````

---

## 辅助文件目录结构参考

当 Skill 需要辅助文件时，使用以下结构：

```
skill-name/
├── SKILL.md           # 主文件（必需，精简）
├── reference.md       # 详细参考文档（按需读取）
├── templates.md       # 模板和示例（按需读取）
├── examples/
│   └── sample.md      # 示例输出
└── scripts/
    └── helper.py      # 工具脚本
```

在 SKILL.md 中引用辅助文件：

```markdown
详细字段参考见 [reference.md](reference.md)
```

运行辅助脚本时使用 `${CLAUDE_SKILL_DIR}` 定位脚本路径（该变量会自动解析为 SKILL.md 所在目录的绝对路径）：

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/your-script.py
```
