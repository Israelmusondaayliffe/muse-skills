# Architecture Patterns Reference

Common architecture patterns, folder conventions, and data flow designs. Load when making structural decisions during planning or building.

## Deep-module test

Prefer modules whose small interface hides meaningful complexity. A boundary is useful when callers need to know less after it exists. Avoid adding layers that only forward arguments, split a coherent rule across files, or expose internal sequencing. During architecture improvement, change one boundary at a time, preserve observable behavior, and run focused proof before widening the migration.

## Table of Contents
1. Frontend Patterns
2. Backend Patterns
3. Full-Stack Patterns
4. Folder Structure Conventions
5. Data Flow Patterns
6. State Management Patterns

---

## 1. Frontend Patterns

### Single-File App (Simplest)
When: Browser-only, no build step, quick tools/utilities.
```
index.html          # Everything: HTML, CSS, JS in one file
```

### Component-Based (React/Vue)
When: Interactive UI with reusable parts.
```
src/
├── components/     # Reusable UI pieces
│   ├── Button.jsx
│   ├── Card.jsx
│   └── Modal.jsx
├── pages/          # Full page views
│   ├── Home.jsx
│   └── Settings.jsx
├── hooks/          # Shared logic (React)
│   └── useAuth.js
├── utils/          # Helper functions
│   └── format.js
├── styles/         # Global styles
│   └── globals.css
└── App.jsx         # Root component
```

### Feature-Based (Scaled React)
When: Larger apps where features are self-contained.
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.js
│   │   └── index.js
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       ├── api.js
│       └── index.js
├── shared/
│   ├── components/
│   ├── hooks/
│   └── utils/
└── App.jsx
```

---

## 2. Backend Patterns

### Simple Script
When: One-off task, data processing, automation.
```
script.py           # Single file with clear sections
# or
script.js
```

### Route-Handler (Express/Flask)
When: Simple API with a few endpoints.
```
src/
├── routes/         # URL → handler mapping
│   ├── users.js
│   └── posts.js
├── middleware/      # Request processing (auth, logging)
│   └── auth.js
├── utils/          # Shared helpers
│   └── validate.js
├── db.js           # Database connection
└── server.js       # Entry point
```

### MVC (Model-View-Controller)
When: Data-driven app with clear CRUD operations.
```
src/
├── models/         # Data shape and database interaction
│   ├── User.js
│   └── Post.js
├── controllers/    # Business logic
│   ├── userController.js
│   └── postController.js
├── routes/         # URL mapping to controllers
│   ├── userRoutes.js
│   └── postRoutes.js
├── middleware/
│   └── auth.js
├── config/
│   └── db.js
└── server.js
```

### Clean Architecture (Layered)
When: Complex business logic, long-lived codebase, multiple interfaces.
```
src/
├── domain/         # Business rules (no framework deps)
│   ├── entities/
│   └── useCases/
├── infrastructure/ # External concerns
│   ├── database/
│   ├── api/
│   └── cache/
├── interface/      # Delivery mechanism
│   ├── controllers/
│   ├── routes/
│   └── presenters/
└── config/
```

**Key rule:** Dependencies point inward. Domain depends on nothing. Infrastructure depends on domain. Interface depends on both.

---

## 3. Full-Stack Patterns

### Monolith (Simplest Full-Stack)
When: Small to medium app, single team, rapid development.
```
project/
├── client/         # Frontend
│   ├── src/
│   └── public/
├── server/         # Backend
│   ├── routes/
│   ├── models/
│   └── controllers/
├── shared/         # Types, constants, utils used by both
├── package.json
└── README.md
```

### API + Client (Separated)
When: Different teams for frontend/backend, or multiple clients (web, mobile).
```
api/                # Backend (its own repo/project)
├── src/
├── tests/
└── package.json

client/             # Frontend (its own repo/project)
├── src/
├── tests/
└── package.json
```

---

## 4. Folder Structure Conventions

**Universal rules:**
- `src/` for source code
- `tests/` or `__tests__/` for test files
- `config/` for configuration
- `utils/` or `lib/` for shared helpers
- `public/` or `static/` for static assets
- `scripts/` for build/deploy scripts

**Naming:**
- Files: camelCase (JS) or snake_case (Python)
- Components: PascalCase (React, Vue)
- Directories: lowercase with hyphens (kebab-case)
- Constants: UPPER_SNAKE_CASE

**Index files:**
- Use index.js/index.ts to re-export module public API
- Keeps imports clean: `import { Button } from './components'`

---

## 5. Data Flow Patterns

### Unidirectional (React Model)
```
User Action → State Update → Re-render → Display
     ↑                                      │
     └──────────────────────────────────────┘
```
Data flows one direction. State is the single source of truth. UI reacts to state changes.

### Request-Response (API Model)
```
Client Request → Validate → Process → Respond
                    │           │
                    ↓           ↓
                  Error     Database
```
Every request is validated, processed, and responded to. Errors short-circuit the flow.

### Event-Driven
```
Event Emitted → Queue → Handler → Side Effect
                         │
                         ↓
                     Next Event (if any)
```
Loose coupling. Components communicate through events. Good for notifications, logging, async processing.

### Pub-Sub (Real-Time)
```
Publisher → Topic → Subscriber A
                 → Subscriber B
                 → Subscriber C
```
One-to-many communication. Good for chat, live updates, collaborative editing.

---

## 6. State Management Patterns

### Local State (Simplest)
When: State belongs to one component.
React: useState, useReducer.
Vanilla: Variables in closure scope.

### Lifted State
When: Two sibling components share state.
Move state to their nearest common parent. Pass down as props.

### Context/Store (Global)
When: Many components across the tree need the same data.
React: useContext + useReducer.
Vue: Pinia/Vuex.
Pattern: Create store → provide at top → consume anywhere.

### Server State
When: Data comes from an API and needs caching, refetching, synchronization.
Pattern: Fetch on mount → cache response → refetch on stale → handle loading/error states.
Libraries: React Query, SWR, Apollo (GraphQL).

---

## Decision Quick Reference

| Situation | Pattern |
|-----------|---------|
| Quick tool, no server | Single-file HTML |
| Interactive UI | Component-based React |
| Large frontend app | Feature-based React |
| Simple API | Route-Handler |
| CRUD app | MVC |
| Complex business logic | Clean Architecture |
| Small full-stack | Monolith |
| Multiple client types | API + Client separated |
| One component's data | Local state |
| Shared across app | Context/Store |
| API data | Server state pattern |
