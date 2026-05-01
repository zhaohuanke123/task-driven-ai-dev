# Project Architecture

> 本文档定义项目的架构约束。所有代码变更必须符合这些约束。

---

## Overview

<!-- 必填：1-2 段话描述系统要解决什么问题 -->

[项目描述和核心功能]

---

## Tech Stack

<!-- 必填：使用表格格式，包含选择理由 -->

| Layer | Technology | Reason |
|-------|------------|--------|
| Frontend | [例如: Next.js 14+ (App Router) + TypeScript + Tailwind CSS] | [为什么选择] |
| Backend | [例如: Next.js API Routes] | [为什么选择] |
| Database | [例如: PostgreSQL/Supabase] | [为什么选择] |
| Auth | [例如: Supabase Auth] | [为什么选择] |

---

## Directory Structure

<!-- 必填：目录树 + 每个目录的职责说明 -->

```
/
├── AGENTS.md              # 导航入口（subagent 首先读取）
├── WORKFLOW.md            # 工作流程和 Documentation Gate
├── PROJECT.md             # 项目状态（如使用 software-dev）
├── docs/                  # 文档先行体系（如使用 software-dev）
│   ├── requirements.md    # 行为和范围要求
│   ├── design.md          # 模块设计和接口契约
│   └── architecture.md    # 系统架构和数据流
├── architecture.md        # 本文件 - 架构约束
├── task.json              # 任务定义和文档引用
├── progress.txt           # 开发历史、文档更新、测试证据
├── init.sh                # 环境初始化脚本
├── src/
│   ├── app/               # [例如: Next.js App Router 页面]
│   │   ├── api/           # API 路由
│   │   └── (routes)/      # 页面组件
│   ├── components/        # 可复用组件
│   │   ├── ui/            # 基础 UI 组件
│   │   └── features/      # 功能特定组件
│   ├── lib/               # 工具和辅助函数
│   │   ├── db/            # 数据库访问层
│   │   └── utils.ts       # 通用工具
│   ├── hooks/             # 自定义 React hooks
│   └── types/             # TypeScript 类型定义
└── public/                # 静态资源
```

---

## Data Model

<!-- 必填：核心实体、字段、关系 -->

### 核心实体

| Entity | Fields | Relations |
|--------|--------|-----------|
| [Entity1] | [字段列表] | [与其他实体的关系] |
| [Entity2] | [字段列表] | [与其他实体的关系] |

### Schema

<!-- 数据库 schema 定义 -->

```sql
-- 示例
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Design

<!-- 必填：端点表格 + 命名规范 -->

### 端点列表

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/[resource] | [描述] |
| POST | /api/[resource] | [描述] |
| GET | /api/[resource]/:id | [描述] |
| PATCH | /api/[resource]/:id | [描述] |
| DELETE | /api/[resource]/:id | [描述] |

### 命名规范

- [API 命名约定，如：使用复数名词、kebab-case]

---

## Key Constraints

<!-- 必填：必须遵守的约束和禁止事项 -->

### 必须遵守

1. **[约束1]**: [原因和后果]
2. **[约束2]**: [原因和后果]

### 禁止事项

1. **[禁止事项1]**: [原因]
2. **[禁止事项2]**: [原因]

---

## Environment Variables

<!-- 推荐：环境变量清单 -->

```env
# Required
DATABASE_URL=
NEXT_PUBLIC_API_URL=

# Optional
DEBUG=
```

---

## Key Design Decisions

<!-- 推荐：重要设计决策及理由 -->

1. **[决策1]**: [理由]
2. **[决策2]**: [理由]
