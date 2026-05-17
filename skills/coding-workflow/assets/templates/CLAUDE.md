# [项目名]

[1-2 句话描述项目是什么，解决什么问题]

本项目使用 coding-workflow 架构，多代理编排 + 文档先行。

---

## 新对话读取顺序

```
1. 本文件（CLAUDE.md）    ← 导航入口，自动读取
2. PROJECT.md             ← 项目阶段、版本（如存在）
3. task.json              ← 任务列表和依赖
4. progress.txt           ← 进度历史
5. 任务相关 docs/*        ← 需求、设计
6. 源码                   ← Documentation Gate 通过后
```

---

## Documentation Gate

编码前必须：

1. 确认任务的目标行为有文档定义（任务 `docs` 字段或 `docs/requirements.md`）
2. 读取 `architecture.md` 确认技术栈和禁止事项
3. 如果用户请求新行为，先更新文档再改代码
4. 如果确认跳过文档，在 `progress.txt` 记录原因和风险

---

## Memory 规则

Memory 只能提醒 agent 读取本文件，不能替代项目状态文件。

冲突优先级：

```text
用户最新明确指令
> PROJECT.md / docs/* / task.json / progress.txt
> CLAUDE.md / architecture.md
> skill instructions
> memory hints
```

---

## 文件导航

| 文件 | 用途 | 何时读取 |
|------|------|----------|
| [PROJECT.md](PROJECT.md) | 项目阶段、版本 | 新对话（如存在） |
| [architecture.md](architecture.md) | 技术栈、目录结构、约束 | 编码前 |
| [task.json](task.json) | 任务定义和依赖 | 需要知道做什么时 |
| [progress.txt](progress.txt) | 进度历史和测试证据 | 需要了解上下文时 |
| [docs/requirements.md](docs/requirements.md) | 行为要求 | 需求/bug/行为变更 |
| [docs/design.md](docs/design.md) | 模块设计和接口 | 编码前 |

---

## 目录结构

```
/
├── CLAUDE.md              ← 导航入口
├── architecture.md        ← 架构约束
├── task.json              ← 任务定义
├── progress.txt           ← 进度历史
├── PROJECT.md             ← 项目状态（如存在）
├── docs/                  ← 生命周期文档（如存在）
│   ├── requirements.md
│   ├── design.md
│   └── architecture.md
├── src/
│   ├── app/               ← [职责说明]
│   ├── components/        ← [职责说明]
│   ├── lib/               ← [职责说明]
│   └── types/             ← [职责说明]
└── public/                ← 静态资源
```

---

## 关键约定

所有约束（命名规范、禁止事项等）定义在 [architecture.md](architecture.md)，编码前 workflow 会自动读取。
