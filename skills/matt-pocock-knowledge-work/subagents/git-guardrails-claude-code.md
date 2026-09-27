---
name: git-guardrails-claude-code
description: "Use when the user wants to prevent destructive git operations, add git safety hooks, or block git push or reset in Claude Code."
---

Invocation: model or user

# Setup Git Guardrails

Trigger: the user wants to block dangerous git commands in Claude Code.

Procedure: ask scope first: this project only (.claude/settings.json) or all projects (~/.claude/settings.json). Then copy the bundled script bin/block-dangerous-git.sh to the matching hooks directory (.claude/hooks/block-dangerous-git.sh for project scope, ~/.claude/hooks/block-dangerous-git.sh for global) and make it executable with chmod +x. Finally add a PreToolUse hook entry to the corresponding settings file with matcher Bash and a command-type hook pointing at the copied script. Once installed, the hook blocks git push (all variants including force), git reset --hard, git clean -f / -fd, git branch -D, and git checkout . / git restore . before they execute, and Claude sees a message saying it does not have authority to run those commands.
