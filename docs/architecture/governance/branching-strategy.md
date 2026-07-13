# Enterprise AI Knowledge & Operations Platform (EAKOP)

# Branching Strategy

| Property             | Value                                                 |
| -------------------- | ----------------------------------------------------- |
| **Project Name**     | Enterprise AI Knowledge & Operations Platform (EAKOP) |
| **Project Codename** | Project AURA                                          |
| **Document**         | Branching Strategy                                    |
| **Version**          | 1.0                                                   |
| **Status**           | Approved                                              |
| **Author**           | Pankaj Jagdaley                                       |
| **Date**             | July 2025                                             |

---

# 1. Purpose

This document defines the Git branching strategy for the Enterprise AI Knowledge & Operations Platform (EAKOP).

The strategy provides a consistent approach for source code management, feature development, bug fixes, releases, and hotfixes while supporting Continuous Integration and Continuous Deployment (CI/CD).

---

# 2. Objectives

The branching strategy aims to:

* Maintain a stable production codebase.
* Enable parallel development.
* Simplify code reviews.
* Support automated testing.
* Reduce merge conflicts.
* Facilitate controlled releases.

---

# 3. Branching Model

The project follows a simplified GitHub Flow with dedicated release branches.

The primary branches are:

```text
main
develop
feature/*
release/*
hotfix/*
```

---

# 4. Branch Descriptions

## main

Purpose:

* Production-ready code.
* Protected branch.
* Always deployable.

Rules:

* Direct commits are not permitted.
* Changes are merged only through Pull Requests.
* All automated tests must pass before merging.

---

## develop

Purpose:

* Primary integration branch.
* Contains completed features awaiting release.

Rules:

* Feature branches are merged into develop.
* CI pipeline executes automatically.

---

## feature/*

Purpose:

Development of new functionality.

Naming Convention:

```text
feature/document-upload
feature/rag-pipeline
feature/chat-service
feature/langgraph-orchestration
feature/mcp-integration
feature/security-enhancements
```

Rules:

* Created from develop.
* Merged back into develop through Pull Requests.
* Deleted after successful merge.

---

## release/*

Purpose:

Prepare a production release.

Naming Convention:

```text
release/v1.0.0
release/v1.1.0
release/v2.0.0
```

Activities:

* Final testing.
* Documentation updates.
* Version updates.
* Bug fixes only.

After approval:

* Merge into main.
* Merge back into develop.
* Tag the release.
* Delete the release branch.

---

## hotfix/*

Purpose:

Urgent production fixes.

Naming Convention:

```text
hotfix/security-fix
hotfix/chat-timeout
hotfix/rag-bug
```

Rules:

* Created from main.
* Merged into both main and develop.
* Tagged after deployment.
* Deleted after merge.

---

# 5. Branch Lifecycle

```text
main
  │
  ├──────────────┐
  │              │
develop          │
  │              │
  ├── feature/*  │
  │       │      │
  │       ▼      │
  └──── develop  │
          │      │
          ▼      │
     release/*   │
          │      │
          ▼      │
         main ◄──┘
          │
     production

main
 │
 ▼
hotfix/*
 │
 ├──► main
 └──► develop
```

---

# 6. Pull Request Process

Every Pull Request shall include:

* Description of the change.
* Related issue or requirement.
* Test results.
* Documentation updates (if applicable).
* Reviewer approval.

No Pull Request shall be merged until:

* CI pipeline passes.
* Code review is completed.
* No critical security issues remain.

---

# 7. Commit Message Convention

The project follows the Conventional Commits specification.

Examples:

```text
feat(auth): implement Firebase authentication

feat(rag): add hybrid search support

fix(chat): resolve conversation context issue

docs(api): update API architecture document

refactor(search): simplify retrieval service

test(upload): add integration tests for document upload

chore(deps): update LangGraph dependency
```

Commit types:

* feat
* fix
* docs
* refactor
* test
* chore
* perf
* ci
* build

---

# 8. Release Process

1. Complete feature development in develop.
2. Create a release branch.
3. Perform testing and validation.
4. Update documentation and version numbers.
5. Merge release into main.
6. Create Git tag.
7. Deploy to production.
8. Merge release back into develop.

---

# 9. Branch Protection Rules

The following protection rules apply to the main branch:

* Pull Requests required.
* Direct pushes disabled.
* Successful CI checks required.
* Review approval required.
* Linear history preferred.
* Signed commits encouraged.

---

# 10. Version Tagging

Production releases shall be tagged using Semantic Versioning.

Examples:

```text
v1.0.0
v1.1.0
v1.2.0
v2.0.0
```

Tags shall correspond to production deployments.

---

# 11. Merge Strategy

Preferred merge strategy:

* Squash and Merge for feature branches.
* Merge Commit for release branches.
* Merge Commit for hotfix branches.

This keeps feature history concise while preserving release history.

---

# 12. Continuous Integration

Every commit to:

* develop
* feature/*
* release/*
* hotfix/*

shall automatically trigger:

* Code formatting checks.
* Static analysis.
* Unit tests.
* Integration tests (where applicable).
* Security scanning.

---

# 13. Branch Cleanup

After successful merge:

* Feature branches shall be deleted.
* Release branches shall be deleted.
* Hotfix branches shall be deleted.

The main and develop branches are permanent.

---

# 14. Exceptions

Any deviation from this branching strategy shall be documented and approved by the project architect before implementation.

---

# 15. Review

The branching strategy shall be reviewed periodically as the project evolves. Changes shall be documented through an Architecture Decision Record (ADR) where they significantly affect the development workflow.
