# Error Catalog

Common coding errors by language, their fixes, and plain English translations for non-coders. Load during building, fixing, or when explaining errors to the user.

## Table of Contents
1. JavaScript/TypeScript Errors
2. Python Errors
3. React-Specific Errors
4. API/Network Errors
5. Database Errors
6. Plain English Translations

---

## 1. JavaScript/TypeScript Errors

### Null/Undefined Access
**Pattern:** `Cannot read property 'x' of undefined`
**Cause:** Accessing a property on something that doesn't exist yet.
**Fix:** Add optional chaining (`obj?.property`) or null checks (`if (obj) { ... }`).
**Prevention:** Always initialize variables. Check API responses before accessing nested data.

### Type Coercion Bugs
**Pattern:** `"5" + 3` gives `"53"` instead of `8`
**Cause:** JavaScript converts types silently.
**Fix:** Use `Number()`, `parseInt()`, or `parseFloat()` explicitly. Use strict equality `===`.
**Prevention:** Validate and convert types at input boundaries.

### Async/Await Mistakes
**Pattern:** Function returns Promise instead of value.
**Cause:** Missing `await` keyword, or forgetting to make function `async`.
**Fix:** Add `await` before async calls. Mark containing function as `async`.
**Prevention:** Every function that calls an async function must itself be async.

### Scope Issues
**Pattern:** Variable is undefined inside callback/loop.
**Cause:** Using `var` (function scoped) instead of `let`/`const` (block scoped).
**Fix:** Replace `var` with `let` or `const`.
**Prevention:** Never use `var`. Always `const` first, `let` only when reassignment is needed.

### Event Listener Leaks
**Pattern:** Memory grows over time, duplicate handlers.
**Cause:** Adding event listeners without removing them.
**Fix:** Store listener reference, remove in cleanup.
**Prevention:** In React, clean up in useEffect return. In vanilla JS, remove listeners when element is removed.

---

## 2. Python Errors

### IndentationError
**Pattern:** `IndentationError: unexpected indent`
**Cause:** Mixing tabs and spaces, or wrong indentation level.
**Fix:** Use consistent indentation (4 spaces standard).
**Prevention:** Configure editor for spaces-only.

### Mutable Default Arguments
**Pattern:** Function behavior changes across calls unexpectedly.
**Cause:** Using mutable default like `def f(items=[])`.
**Fix:** Use `None` as default, create inside function: `def f(items=None): items = items or []`
**Prevention:** Never use lists, dicts, or sets as default arguments.

### Import Errors
**Pattern:** `ModuleNotFoundError: No module named 'x'`
**Cause:** Package not installed, or wrong virtual environment.
**Fix:** `pip install package-name`. Check you're in the right environment.
**Prevention:** Maintain requirements.txt. Document setup steps.

### Off-by-One Errors
**Pattern:** Loop processes one too many or too few items.
**Cause:** Confusion between 0-indexed and 1-indexed, or `range(n)` vs `range(1, n+1)`.
**Fix:** Check loop boundaries carefully. Use `enumerate()` when index matters.
**Prevention:** Prefer iteration (`for item in list`) over index access (`for i in range(len(list))`).

### File Handling
**Pattern:** `FileNotFoundError` or resource leaks.
**Cause:** Wrong path, or not closing files.
**Fix:** Use `with open(path) as f:` (auto-closes). Use `os.path` for path construction.
**Prevention:** Always use context managers (`with`). Always use `pathlib` or `os.path`.

---

## 3. React-Specific Errors

### Infinite Re-render
**Pattern:** "Too many re-renders" error.
**Cause:** Setting state inside render body, or useEffect without proper dependency array.
**Fix:** Move state updates into event handlers or useEffect with correct deps.
**Prevention:** Never call setState directly in component body. Always specify useEffect dependencies.

### Stale Closure
**Pattern:** State value is outdated inside callback.
**Cause:** Callback captures old state value from previous render.
**Fix:** Use functional state update: `setState(prev => prev + 1)`. Or use useRef for latest value.
**Prevention:** Use functional updates when new state depends on previous state.

### Key Prop Missing
**Pattern:** "Each child in a list should have a unique key prop."
**Cause:** List rendering without stable keys.
**Fix:** Add unique, stable `key` prop. Use item ID, not array index (unless list never reorders).
**Prevention:** Always use a unique identifier from the data as key.

### Prop Drilling
**Pattern:** Passing props through many intermediate components.
**Cause:** Deep component tree sharing state from top.
**Fix:** Use React Context for widely-shared state. Or restructure component tree.
**Prevention:** Plan state location during architecture phase.

---

## 4. API/Network Errors

### CORS Errors
**Pattern:** "Access-Control-Allow-Origin" errors in browser console.
**Cause:** Browser blocks requests to different domain/port without CORS headers.
**Fix:** Add CORS headers on the server. Use cors middleware in Express.
**Prevention:** Configure CORS in server setup, not as an afterthought.

### Timeout/Connection Errors
**Pattern:** Request hangs, then fails.
**Cause:** Server is slow, unreachable, or request is too large.
**Fix:** Set reasonable timeouts. Add retry logic with exponential backoff.
**Prevention:** Always set timeouts on network requests. Always handle failure states.

### 404/500 Errors
**Pattern:** API returns error status.
**Cause:** Wrong URL (404), server crash (500), bad request (400).
**Fix:** Validate URL construction. Add try-catch on server routes. Validate request body.
**Prevention:** Log all errors server-side. Return consistent error response format.

---

## 5. Database Errors

### N+1 Query
**Pattern:** Page loads slowly, many similar queries in logs.
**Cause:** Fetching related data inside a loop instead of in one query.
**Fix:** Use JOIN queries or batch fetching. In ORMs, use eager loading.
**Prevention:** Review any database call inside a loop. Replace with batch query.

### SQL Injection
**Pattern:** User input in SQL string concatenation.
**Cause:** Building queries with string formatting instead of parameterization.
**Fix:** Use parameterized queries: `db.query("SELECT * FROM users WHERE id = ?", [userId])`
**Prevention:** Never concatenate user input into SQL. Always use parameters.

### Missing Indexes
**Pattern:** Queries on large tables are slow.
**Cause:** Database scans entire table for every query.
**Fix:** Add indexes on columns used in WHERE, JOIN, ORDER BY.
**Prevention:** Add indexes during schema design for known query patterns.

### Connection Exhaustion
**Pattern:** "Too many connections" errors under load.
**Cause:** Opening new connections without closing or pooling.
**Fix:** Use connection pooling. Set max connections.
**Prevention:** Always use a connection pool. Never open/close connections per request.

---

## 6. Plain English Translations

Use these when explaining errors to the user.

| Technical Error | Plain English |
|----------------|---------------|
| `TypeError: Cannot read property 'x' of undefined` | The code tried to use something that doesn't exist yet |
| `SyntaxError: Unexpected token` | There's a typo in the code, like a missing bracket or comma |
| `ReferenceError: x is not defined` | The code uses a name that hasn't been created yet |
| `CORS error` | The browser blocked a request because it went to a different address than the page |
| `404 Not Found` | The address the code tried to reach doesn't exist |
| `500 Internal Server Error` | Something crashed on the server side |
| `ECONNREFUSED` | The server isn't running or can't be reached |
| `OutOfMemoryError` | The program used too much computer memory |
| `TimeoutError` | The operation took too long and was stopped |
| `PermissionError` | The program doesn't have access to do what it tried |
| `Infinite loop` | The code got stuck repeating the same thing forever |
| `Stack overflow` | A function called itself too many times |
| `Race condition` | Two things happened at the same time and interfered with each other |
| `Deadlock` | Two parts of the program are waiting for each other and neither can proceed |
| `Memory leak` | The program keeps using more memory without releasing it |

### How to Explain Errors to Non-Coders

1. Say what happened in one sentence using the translations above
2. Say what caused it in one sentence (the "because")
3. Say what the fix is in one sentence
4. If relevant, say how to prevent it from happening again
5. Never show raw stack traces, error codes, or technical logs unless the user asks
