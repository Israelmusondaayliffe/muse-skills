# Review Checklist

Quality gates for code review. Check every applicable item.

## Plan Compliance
- [ ] Every plan checklist item is implemented
- [ ] No items were silently skipped
- [ ] Implementation matches plan specifications (not just "done" but "done correctly")
- [ ] Folder structure matches plan

## Code Completeness
- [ ] Every file is complete (no TODOs, no placeholders, no "add here" comments)
- [ ] Code is runnable as-is (no missing imports, no undefined references)
- [ ] Entry point exists and works
- [ ] No dead code or commented-out blocks

## Defensive Coding
- [ ] All user inputs are validated (type, range, format)
- [ ] Null/undefined guards on all data access
- [ ] Try-catch around external calls (API, file, database)
- [ ] Default values for optional parameters
- [ ] Error messages are user-friendly (plain English, not stack traces)

## Edge Cases
- [ ] Empty state handled (no data yet)
- [ ] Loading state handled (data being fetched)
- [ ] Error state handled (something failed, user sees a message)
- [ ] Boundary conditions validated (zero, negative, very large, empty string)
- [ ] Concurrent access considered (if multi-user)

## Code Quality
- [ ] Meaningful variable and function names
- [ ] Functions do one thing (single responsibility)
- [ ] No function exceeds ~30 lines
- [ ] No duplicated logic across files
- [ ] No magic numbers (named constants used)
- [ ] Consistent formatting throughout

## Security Basics
- [ ] No hardcoded passwords, API keys, or secrets
- [ ] User input validated before use
- [ ] No eval() or equivalent
- [ ] SQL uses parameterized queries (if applicable)
- [ ] No sensitive data in client-side code (if applicable)

## Performance Basics
- [ ] No N+1 query patterns (database call inside loop)
- [ ] No unnecessary re-renders (React: proper keys, no inline objects in props)
- [ ] No unbounded data fetching (pagination/limits on queries)
- [ ] No synchronous blocking on heavy operations
- [ ] Event listeners cleaned up (no memory leaks)

## Delivery
- [ ] Usage instructions written in plain English
- [ ] Steps assume zero technical knowledge
- [ ] "What to do if something goes wrong" section included
- [ ] All files saved to output directory
- [ ] Confidence level stated

## Severity Definitions

**Critical (must fix before delivery):**
- Code doesn't run
- Missing core functionality from plan
- Security vulnerability (hardcoded secrets, SQL injection)
- Data loss risk

**Warning (should fix, user decides):**
- Missing edge case handling
- Performance concern for large data
- Code duplication
- Inconsistent error handling

**Note (nice to have):**
- Naming could be clearer
- Comments could be added
- Minor style inconsistency
- Optimization opportunity
