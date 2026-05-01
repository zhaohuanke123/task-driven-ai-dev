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

A structured development workflow for fullstack projects with documentation gates, verification gates, persistent state, and browser testing integration.

**Features:**
- **Task Selection**: Automatically select next incomplete task from task.json
- **Documentation Gate**: Require task-level requirement/design references before implementation
- **Implementation Guidance**: Follow existing docs, code patterns, and conventions
- **Testing Gates**: Lint, build, browser testing, and docs/code/tests consistency checks
- **Progress Documentation**: Persistent session history, documentation updates, and skip-risk records in progress.txt
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
- **Spaced Repetition**: Ebbinghaus forgetting curve review system (20min, 1h, 1d, 2d, 6d, 31d)

### software-dev

Guides AI agents through the complete software development lifecycle with phase-gated, document-driven execution. Designed for small/demo projects that need fast iteration with disciplined delivery.

**Features:**
- **10-Phase Lifecycle**: Problem definition → requirements → planning → architecture → design → coding → unit testing → integration → system testing → delivery
- **Document-First**: Update documentation before implementation; bug fixes and behavior changes must pass a documentation gate; docs, code, and tests must agree
- **Progressive Loading**: Compact main file with reference files loaded on demand
- **Cross-Conversation Persistence**: `PROJECT.md`, `CLAUDE.md`, `AGENTS.md`, and `WORKFLOW.md` preserve context and runtime workflow across sessions
- **Git Integration**: Commits, tags, and rollback built into every phase
- **Recovery Protocol**: Exception handling for missing files, dirty worktrees, and abandoned projects

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

# Software development lifecycle
/plugin install software-dev@zhaohuanke123-vanko-skill
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

# Software development lifecycle
/software-dev:software-dev
```

## Required Artifacts

### For software-dev

| File | Purpose |
|------|---------|
| `PROJECT.md` | Single source of truth for project state, phase, and version |
| `CLAUDE.md` | Generic agent entry point for cross-session persistence |
| `AGENTS.md` | Runtime navigation entry for future agents |
| `WORKFLOW.md` | Execution workflow and documentation gate |
| `docs/problem-definition.md` | Problem statement and success criteria |
| `docs/requirements.md` | Functional and non-functional requirements |
| `docs/plan.md` | Stack, milestones, risks, version strategy |
| `docs/architecture.md` | Components and data flow |
| `docs/design.md` | Module design and contracts |
| `docs/test-results.md` | Verification results |
| `docs/version-history.md` | Release and rollback history |
| `docs/lessons-learned.md` | Reusable lessons |

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
| `AGENTS.md` | Runtime navigation entry |
| `WORKFLOW.md` | Execution workflow and documentation gate |
| `task.json` | Task definitions with steps, completion status, and document references |
| `progress.txt` | Session history, documentation updates, and skip-risk records |
| `architecture.md` | System design decisions |
| `init.sh` | Environment setup script |

### For interactive-learning

| File | Purpose |
|------|---------|
| `进度.md` | Learning progress and current state |
| `知识图谱.md` | Learning path and concept relationships |
| `复习计划.md` | Spaced repetition review schedule |
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

**Review Commands:**
| Command | Description |
|---------|-------------|
| `复习` | Start reviewing due courses |
| `今日复习` | View today's review tasks |
| `复习计划` | View full review schedule |

## License

MIT
