# Code Review

Code review catches bugs early, shares knowledge, and enforces standards.

**Checklist:**

```markdown
### Functionality
- [ ] Does the code do what it's supposed to?
- [ ] Are edge cases handled?

### Readability
- [ ] Are names descriptive?
- [ ] Is there unnecessary duplication?

### Testing
- [ ] Are there tests for new functionality?
- [ ] Do tests cover edge cases?

### Security
- [ ] Is user input validated and sanitized?
- [ ] Are secrets handled securely?

### Performance
- [ ] Are there unnecessary computations?
- [ ] Is memoization used where needed?
```

**Feedback guidelines:**

| Approach | Example |
| --- | --- |
| Be specific | "Consider using `map` instead of `forEach` here" |
| Explain why | "Using `const` prevents accidental reassignment" |
| Suggest alternatives | "This could use a reducer pattern" |
| Acknowledge good code | "Great solution for this edge case!" |
| Ask questions | "What was the reasoning behind this approach?" |
