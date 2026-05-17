# Test Blog

A fullstack blog platform built with React and Express.

本项目使用 coding-workflow 架构，多代理编排 + 文档先行。

---

## 新对话读取顺序

```
1. 本文件（CLAUDE.md）    ← 导航入口，自动读取
2. task.json              ← 任务列表和依赖
3. progress.txt           ← 进度历史
4. 任务相关 docs/*        ← 需求、设计
5. 源码                   ← Documentation Gate 通过后
```

---

## Documentation Gate

编码前必须：
1. 确认任务的目标行为有文档定义
2. 读取 architecture.md 确认技术栈和禁止事项
3. 如果用户请求新行为，先更新文档再改代码

---

## Memory 规则

冲突优先级：用户最新明确指令 > 项目文件 > skill instructions > memory hints

---

## 文件导航

| 文件 | 用途 |
|------|------|
| [architecture.md](architecture.md) | 技术栈、目录结构、约束 |
| [task.json](task.json) | 任务定义和依赖 |
| [progress.txt](progress.txt) | 进度历史 |

---

## 关键约定

所有约束定义在 [architecture.md](architecture.md)。
