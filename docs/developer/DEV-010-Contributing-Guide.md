# DEV-010 – Contributing Guide

## 1. Purpose

This document defines the contribution process for the Enterprise AI Orchestration Platform.

The objective is to ensure that all contributions are consistent, maintainable, well-tested, and aligned with the project's architectural principles and coding standards.

All contributors are expected to follow this guide before submitting changes to the repository.

---

# 2. Contribution Principles

The project values:

- High-quality code
- Clean architecture
- Consistent coding standards
- Comprehensive testing
- Complete documentation
- Constructive code reviews
- Continuous improvement

Every contribution should improve the platform.

---

# 3. Contribution Workflow

```text
Fork / Clone Repository
          │
          ▼
Create Feature Branch
          │
          ▼
Implement Changes
          │
          ▼
Run Tests
          │
          ▼
Update Documentation
          │
          ▼
Commit Changes
          │
          ▼
Push Branch
          │
          ▼
Create Pull Request
          │
          ▼
Code Review
          │
          ▼
Merge
```

---

# 4. Branching Strategy

Use short-lived feature branches.

Recommended naming:

```text
feature/hybrid-search

feature/langgraph-agent

feature/document-upload

bugfix/chat-history

bugfix/vector-search

hotfix/security-patch

docs/update-services
```

Avoid direct commits to the main branch.

---

# 5. Keeping Branches Current

Before starting work:

```bash
git checkout main

git pull origin main
```

Update your feature branch regularly:

```bash
git checkout feature/my-feature

git merge main
```

Resolve conflicts before creating a Pull Request.

---

# 6. Commit Message Convention

Follow Conventional Commits.

Examples:

```text
feat(chat): implement conversational memory

feat(search): add hybrid retrieval

fix(firestore): correct session ordering

fix(qdrant): improve metadata filtering

docs(services): update Gemini documentation

refactor(application): simplify dependency injection

test(search): improve reranker coverage

chore(deps): upgrade FastAPI
```

---

# 7. Pull Request Requirements

Every Pull Request should include:

- Clear title
- Description of changes
- Reason for the change
- Testing performed
- Related issue (if applicable)

Large Pull Requests should be avoided.

---

# 8. Code Review Checklist

Reviewers should verify:

- Architecture compliance
- Coding standards
- Naming conventions
- Type hints
- Logging
- Error handling
- Test coverage
- Documentation updates
- Security considerations

Review comments should be constructive and actionable.

---

# 9. Testing Requirements

Before submitting a Pull Request verify:

- Unit tests pass
- Integration tests pass
- API tests pass
- No new warnings
- Existing functionality remains unchanged

Do not merge code that breaks existing tests.

---

# 10. Documentation Requirements

Documentation must be updated whenever:

- New features are added
- APIs change
- Architecture changes
- Services change
- Workflows change
- Configuration changes

Documentation is considered part of the implementation.

---

# 11. Coding Standards

Contributors must follow:

- DEV-003 – Coding Standards
- DEV-004 – Dependency Injection
- DEV-005 – Error Handling

Do not introduce new coding styles without team agreement.

---

# 12. Security Guidelines

Contributors must never:

- Commit credentials
- Commit service account keys
- Commit secrets
- Log authentication tokens
- Expose internal infrastructure details

Use environment variables for all sensitive configuration.

---

# 13. Dependency Management

When adding dependencies:

- Justify the need.
- Prefer mature libraries.
- Check license compatibility.
- Minimize transitive dependencies.
- Update documentation.

Unused dependencies should be removed.

---

# 14. AI Development Guidelines

When modifying AI functionality:

- Keep prompts configurable.
- Keep retrieval independent of generation.
- Validate prompt changes.
- Preserve deterministic behavior where possible.
- Avoid hardcoding model names.
- Test retrieval quality before merging.
- Document any AI behavior changes.

---

# 15. Code Quality Expectations

Every contribution should be:

- Readable
- Testable
- Modular
- Well documented
- Production ready
- Backward compatible where practical

Avoid unnecessary complexity.

---

# 16. Merge Criteria

A Pull Request may be merged when:

- Code review is approved.
- Tests pass.
- Documentation is updated.
- No critical issues remain.
- CI pipeline succeeds.

---

# 17. Community Guidelines

Contributors should:

- Be respectful.
- Accept constructive feedback.
- Review code objectively.
- Share knowledge.
- Help improve documentation.

The goal is long-term maintainability rather than individual ownership.

---

# 18. Related Documents

- DEV-001 – Development Environment Setup
- DEV-003 – Coding Standards
- DEV-006 – Testing Strategy
- DEV-008 – Build and Deployment
- Architecture Documentation

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-010 |
| Title | Contributing Guide |
| Category | Developer Documentation |
| Audience | Developers, Reviewers, Technical Leads |
| Version | 1.0 |
| Status | Active |