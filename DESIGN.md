# Email Monitor Design

---

# 1. Introduction

This document describes the major design decisions made throughout the development of Email Monitor.

Rather than focusing on implementation details, this document explains the reasoning behind the architecture, the trade-offs that were considered, and the principles that guided each decision.

The primary objective of the project is to build a maintainable, extensible, AI-assisted email processing platform using modern software engineering practices.

---

# 2. Design Philosophy

The project is guided by a few fundamental principles.

- Build for maintainability rather than speed.
- Prefer simplicity over unnecessary complexity.
- Separate infrastructure from business logic.
- Design for extensibility from the beginning.
- Prefer explicit code over implicit behavior.
- Optimize readability before optimization.
- Make architectural decisions that scale with the project.

The emphasis is on creating software that remains understandable and easy to evolve as new functionality is introduced.

---

# 3. Why Python?

Although much of my professional experience has been in modern C++, Python was selected because it provides an excellent ecosystem for AI integration, rapid prototyping, and backend automation.

Python allows the project to focus on architecture and AI capabilities without introducing unnecessary implementation complexity.

---

# 4. Why Gmail API?

Several options were considered.

| Option | Reason Not Selected |
|---------|--------------------|
| IMAP | Older protocol with limited metadata and synchronization support |
| POP3 | Does not support modern email workflows |
| Gmail API | Native Google support, OAuth2, labels, threads, metadata |

The Gmail API provides a richer programming interface while following modern authentication standards.

---

# 5. Why SQLite?

The first versions of the project intentionally use SQLite.

Advantages include:

- Zero configuration
- Lightweight deployment
- ACID compliance
- Excellent reliability
- Suitable for local development
- No external infrastructure required

The persistence layer has been designed so that SQLite can later be replaced by PostgreSQL without affecting higher layers.

---

# 6. Why Layered Architecture?

The project follows a layered architecture because it naturally separates responsibilities.

```
Presentation

↓

Application

↓

Domain

↓

Repository

↓

Database
```

Benefits include:

- Easier maintenance
- Independent evolution of layers
- Better testability
- Reduced coupling
- Clear ownership of responsibilities

---

# 7. Why Repository Pattern?

The Repository Pattern isolates business logic from persistence.

Instead of allowing business code to execute SQL directly, all persistence operations are centralized within repositories.

```
Business Logic

↓

Repository

↓

SQLite
```

Benefits:

- Database independence
- Cleaner code
- Easier testing
- Single persistence abstraction
- Reduced duplication

---

# 8. Why Strong Domain Models?

The project models business concepts explicitly.

Instead of passing dictionaries throughout the application, the system uses strongly typed domain objects.

Examples include:

```
Email

EmailRecord

ProcessingStatus
```

Advantages:

- Better readability
- Type safety
- Clear ownership of data
- Easier refactoring

---

# 9. Why Separate Email and EmailRecord?

One of the earliest design decisions was separating the external email representation from the persistence model.

```
Email

↓

contains only provider data
```

```
EmailRecord

↓

Email

+

Database metadata
```

This avoids mixing infrastructure concerns with business objects.

Email represents the real-world email.

EmailRecord represents the persisted version of that email.

---

# 10. Why Composition Instead of Inheritance?

EmailRecord contains an Email instead of inheriting from it.

```
EmailRecord

contains

Email
```

Reasons:

- Better encapsulation
- Reduced coupling
- Avoids inheritance complexity
- Easier future evolution

Composition better represents the relationship between the two objects.

---

# 11. Why Exception Translation?

Infrastructure-specific exceptions should not leak outside the persistence layer.

Instead of exposing:

```
sqlite3.IntegrityError
```

the repository exposes:

```
DuplicateEmailError
```

Benefits:

- Infrastructure independence
- Cleaner APIs
- Easier database replacement
- Better abstraction boundaries

---

# 12. Why Verification Scripts Instead of Unit Tests?

During the early stages of development, each milestone is verified using dedicated verification scripts.

The goal is to validate architectural progress rather than maximize automated test coverage.

Each milestone verifies:

- Project structure
- Configuration
- Database schema
- Repository behavior
- Object mappings

As the project matures, these verification scripts will gradually evolve into a comprehensive automated test suite.

---

# 13. Why Explicit SQL?

Several ORM frameworks were considered.

Examples:

- SQLAlchemy
- Peewee
- Django ORM

The project intentionally uses handwritten SQL.

Reasons:

- Complete control over queries
- Better understanding of persistence
- Simpler debugging
- No ORM abstractions
- Easier performance optimization

Since the project is intended as an engineering exercise, explicit SQL provides greater transparency.

---

# 14. Why Incremental Development?

The project is intentionally developed in small milestones.

Each milestone satisfies three conditions:

- Builds successfully
- Passes verification
- Leaves the project in a deployable state

Benefits:

- Reduced risk
- Easier debugging
- Better architectural consistency
- Smaller review scope

---

# 15. AI Design Philosophy

Artificial Intelligence is treated as an independent processing stage rather than being embedded throughout the application.

```
Email

↓

AI Processing

↓

Structured Insights
```

This approach allows:

- Multiple LLM providers
- Prompt versioning
- Future RAG integration
- Independent AI evolution

The rest of the system remains unaware of the underlying AI implementation.

---

# 16. Future Evolution

The architecture intentionally supports future enhancements including:

- PostgreSQL
- Microsoft Outlook
- IMAP providers
- Message queues
- Distributed processing
- REST APIs
- Web dashboard
- Plugin system

These enhancements should require minimal architectural changes because appropriate abstraction boundaries already exist.

---

# 17. Trade-Offs

Every architectural decision involves trade-offs.

| Decision | Benefit | Trade-Off |
|----------|---------|-----------|
| SQLite | Simple deployment | Not intended for large-scale production workloads |
| Layered Architecture | Maintainability | Slight increase in project structure |
| Repository Pattern | Clean abstraction | Additional classes |
| Strong Domain Models | Better readability | More code than dictionaries |
| Explicit SQL | Full control | More handwritten queries |
| Composition | Flexible design | Slightly deeper object graph |

The project intentionally favors maintainability and clarity over minimizing the number of source files.

---

# 18. Lessons Learned

Several important lessons have emerged during development.

- Early architectural decisions have long-term impact.
- Explicit abstractions simplify future enhancements.
- Domain models should remain independent of persistence.
- Infrastructure should remain replaceable.
- Incremental development reduces architectural drift.
- Documentation significantly improves long-term maintainability.

---

# 19. Conclusion

The design of Email Monitor emphasizes clean architecture, explicit abstractions, and long-term maintainability.

Rather than optimizing for rapid feature development, the project prioritizes engineering quality, extensibility, and thoughtful architectural decisions.

As additional capabilities such as AI summarization, rule evaluation, and notifications are introduced, the existing design should continue to support incremental growth without requiring fundamental architectural changes.