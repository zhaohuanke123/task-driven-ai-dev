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

## Installation

### From GitHub Marketplace

```shell
/plugin marketplace add zhaohuanke123/vanko-skill
/plugin install task-driven-ai-dev@zhaohuanke123-vanko-skill
```

### Local Development

```bash
git clone https://github.com/zhaohuanke123/vanko-skill.git
claude --plugin-dir ./vanko-skill
```

## Usage

```shell
/task-driven-ai-dev:task-driven-ai-dev
```

## Required Artifacts (for task-driven-ai-dev)

The skill expects the following files in your project:

| File | Purpose |
|------|---------|
| `architecture.md` | System overview, constraints, integration boundaries |
| `task.json` | Backlog source of truth with task definitions |
| `progress.txt` | Dated execution log with evidence |
| `project-config.json` | Repo-specific commands and artifact paths |

## Workflow

1. **Assess repo state** - Check for existing artifacts
2. **Select one task** - Choose next ready task with satisfied dependencies
3. **Implement** - Execute the chosen task
4. **Validate** - Run required validation commands
5. **Update artifacts** - Mark task passed, write progress entry
6. **Commit to git** - Preserve changes with version control
7. **Stop** - End iteration after completion

## Directory Structure

```
your-project/
├── architecture.md      # System architecture
├── task.json           # Task backlog
├── progress.txt        # Progress log
├── project-config.json # Project configuration
└── .claude/
    └── settings.json   # Claude Code settings
```

## License

MIT
