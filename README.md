# Vanko Skill

A Claude Code skills marketplace containing personal AI development utilities.

## Available Skills

### task-driven-ai-dev

Turn a repository into a task-driven AI delivery loop with durable planning artifacts, guarded single-task execution, progress logging, and validation gates.

**Features:**
- **Architecture Documentation**: Maintain system overview, constraints, and integration boundaries
- **Task Management**: Track backlog with dependencies, blocked state, and validation notes
- **Progress Logging**: Dated execution log with testing evidence
- **Project Configuration**: Repo-specific commands and artifact paths
- **Git Integration**: Automatic commit after task completion

### coding-workflow

A structured development workflow for fullstack projects with verification gates, persistent state, and browser testing integration.

**Features:**
- **Task Selection**: Automatically select next incomplete task from task.json
- **Implementation Guidance**: Follow existing code patterns and conventions
- **Testing Gates**: Lint, build, and browser testing with MCP Playwright
- **Progress Documentation**: Persistent session history in progress.txt
- **Blocking Protocol**: Clear handling of tasks that require human intervention
- **Rollback Support**: Clean recovery from failed implementations

### interactive-learning

Interactive learning system based on Bloom's "2 Sigma Problem" and mastery learning principles.

**Features:**
- **Dialog-Based Verification**: AI generates questions dynamically, asks follow-up questions to verify understanding
- **Mastery Learning**: Only proceed when truly understanding (L3 application level)
- **Branch Exploration**: Dive deep into concepts that interest you, return to main path anytime
- **Progress Tracking**: Resume learning across conversations, never lose context
- **Feynman Method**: Learn by explaining, AI helps you find knowledge gaps
- **Error Correction**: Correct AI mistakes, make learning a collaborative process
- **Source Citations**: Generate courses based on your documents, books, or websites with proper citations
- **Obsidian Integration**: Auto-add `^block-id` for precise note references

## Installation

### From GitHub Marketplace

```shell
/plugin marketplace add zhaohuanke123/vanko-skill
```

### Install Specific Skills

```shell
# Task-driven AI development
/plugin install task-driven-ai-dev@zhaohuanke123-vanko-skill

# Coding workflow
/plugin install coding-workflow@zhaohuanke123-vanko-skill

# Interactive learning
/plugin install interactive-learning@zhaohuanke123-vanko-skill
```

### Local Development

```bash
git clone https://github.com/zhaohuanke123/vanko-skill.git
claude --plugin-dir ./vanko-skill
```

## Usage

```shell
# Task-driven AI development
/task-driven-ai-dev:task-driven-ai-dev

# Coding workflow
/coding-workflow:coding-workflow

# Interactive learning
/interactive-learning:interactive-learning
```

## Required Artifacts

### For task-driven-ai-dev

| File | Purpose |
|------|---------|
| `architecture.md` | System overview, constraints, integration boundaries |
| `task.json` | Backlog source of truth with task definitions |
| `progress.txt` | Dated execution log with evidence |
| `project-config.json` | Repo-specific commands and artifact paths |

### For coding-workflow

| File | Purpose |
|------|---------|
| `task.json` | Task definitions with steps and completion status |
| `progress.txt` | Session history and context |
| `architecture.md` | System design decisions |
| `init.sh` | Environment setup script |

### For interactive-learning

| File | Purpose |
|------|---------|
| `进度.md` | Learning progress and current state |
| `知识图谱.md` | Learning path and concept relationships |
| `参考资料.md` | Source materials library for the topic |
| `books/` | Local books and documents (PDF, MD, TXT) |
| `XX_标题.md` | Course files with content and checkpoint records |
| `config.json` | Learning directory and teaching settings |

**Source Materials (Optional):**
| Type | Example |
|------|---------|
| Local files | `./books/guide.pdf` |
| Obsidian notes | `[[notes/topic]]` |
| Websites | `https://example.com/article` |
| Books | `《Book Name》Chapter X` |

## License

MIT
