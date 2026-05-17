# Project Architecture

## Overview

Fullstack blog platform with React frontend and Express backend.

## Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| Frontend | React + TypeScript + Tailwind | Component model, static typing, utility-first CSS |
| Backend | Node.js + Express | JavaScript ecosystem, simple REST API |
| Database | PostgreSQL | Relational data, strong consistency |
| Auth | JWT | Stateless auth, simple implementation |

## Directory Structure

```
/
├── CLAUDE.md
├── architecture.md
├── task.json
├── progress.txt
├── src/
│   ├── frontend/
│   │   ├── components/
│   │   └── pages/
│   ├── backend/
│   │   ├── routes/
│   │   └── models/
│   └── lib/
└── public/
```

## Key Constraints

### 必须遵守
1. 所有 API 使用 RESTful 约定
2. 前端组件使用函数式组件 + hooks

### 禁止事项
1. 禁止使用 any 类型
2. 禁止直接操作 DOM
