# Safety and Approvals

## Read-only actions
The initial audit may inspect relevant files, list installed capabilities, read configuration key names, and run non-mutating validators.

## Approval groups
Keep these approvals separate:

1. Workspace folders and templates.
2. Memory and identity files (`MEMORY.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`).
3. Goal and project files.
4. Skills and references.
5. Connector authentication.
6. Automations and schedules (cron jobs, hooks).
7. External sends and publication (email, messages, posts, files shared outside the workspace).
8. Deletes and destructive cleanup.

Approval for one group does not approve another.

## Never implicit
- Deleting existing user work.
- Replacing an existing file without a reviewed diff.
- Reading or recording secret values.
- Trusting a hook.
- Installing third-party code.
- Authenticating an account.
- Sending messages or publishing content.
- Spending money.
- Expanding paths or permissions during a running goal or scheduled task.
