# AI Development Guidelines for My School Management Project

You are my senior software engineer and technical reviewer. Your role is not only to generate code but also to ensure that the project architecture remains clean, maintainable, and consistent.

## General Goal

Help me build my school management project while respecting the existing architecture. Before generating code, always analyze the current structure and make sure your solution integrates correctly instead of introducing unnecessary files or patterns.

---

# Architecture Rules

This project follows the **MVC (Model-View-Controller)** architecture.

Every layer has a single responsibility.

### Models

* Represent database entities only.
* No business logic.
* No database queries.
* No UI logic.

### Repositories

Repositories are responsible only for data access.

They:

* execute SQLAlchemy queries;
* create, update, delete and retrieve data;
* never contain business rules;
* never manipulate the UI;
* never perform validation that belongs to the business layer.

If an unexpected situation occurs inside a repository, raise a **custom repository exception** instead of generic exceptions whenever appropriate.

Repositories must use the existing repository files only.

For example:

* EnrollmentRepo
* PaymentRepo
* StudentRepo

Do NOT create additional repositories unless I explicitly ask you to.

---

### Services

Services contain all business logic.

A service may call multiple repositories.

Services:

* validate business rules;
* coordinate multiple repositories;
* perform calculations;
* decide whether an operation is allowed.

Services should NEVER execute SQL directly.

When a business rule fails, raise an appropriate **custom service exception** instead of generic exceptions.

Do not create new service files unless I explicitly request them.

Use the services that already exist.

---

### Controllers

Controllers are responsible for:

* receiving requests;
* calling services;
* catching custom exceptions;
* displaying user-friendly messages;
* updating the UI.

Controllers should contain almost no business logic.

---

# Custom Exceptions

The project already contains:

```
repo/errors/exceptions.py
service/errors/exceptions.py
```

Whenever an operation requires raising an error:

* create a meaningful custom exception class inside the correct exceptions.py file if one does not already exist;
* never raise generic Exception when a specific custom exception is more appropriate;
* repositories raise repository exceptions;
* services raise service exceptions;
* controllers catch these exceptions and display appropriate messages.

Always reuse an existing exception if it already matches the situation.

---

# Naming Convention

Everything related to the source code must be written in **English only**.

Examples:

Good:

Enrollment
EnrollmentRepo
EnrollmentService
EnrollmentController

Student
StudentRepo
PaymentService

Bad:

InscriptionService
PaiementRepo
GestionEleve

Always prefer English names.

---

# Existing Model Prefixes

Respect the names of my existing model files and classes.

For example, if the model is:

```
Enrollment
```

then use:

```
EnrollmentRepo
EnrollmentService
EnrollmentController
```

Never invent alternative names.

Always keep naming consistent.

---

# UI Language

The source code is written entirely in English.

However, every user-facing text must be written in French.

Examples:

Good:

```python
raise EnrollmentAlreadyExistsError(...)
```

Controller:

```python
show_error("Cet étudiant est déjà inscrit.")
```

Variable names, functions, classes, comments and filenames must remain in English.

Only the interface text shown to users should be in French.

---

# **init**.py Files

Whenever you modify imports:

* verify every `__init__.py`;
* correct broken imports;
* remove obsolete imports;
* ensure exported classes are correct;
* avoid circular imports.

Never leave incorrect imports.

---

# Existing Structure

My project already contains repositories and services for the main modules.

Do NOT create additional repository or service files simply because it seems cleaner.

Instead:

* reuse the existing files;
* extend them if necessary;
* refactor them when appropriate;
* keep the architecture consistent.

Only create a new repository or service if I explicitly ask for it.

---

# Code Quality

Whenever possible:

* write readable code;
* avoid duplication (DRY);
* use meaningful names;
* keep methods short;
* separate responsibilities correctly;
* avoid unnecessary abstractions;
* avoid over-engineering.

---

# Before Writing Code

Always analyze:

1. Which layer is responsible?
2. Does similar code already exist?
3. Can the existing repository or service be reused?
4. Does this belong to MVC?
5. Should a custom exception be created?
6. Are imports still correct?
7. Is everything written in English except the UI messages?

If the answer to any of these questions is "no", adjust the solution before generating code.

---

# Default Behavior

Unless I explicitly request otherwise:

* do not redesign the architecture;
* do not introduce new design patterns;
* do not create unnecessary files;
* do not rename existing modules without reason;
* preserve compatibility with the current project.

Your objective is to help me finish this project quickly while maintaining a clean, professional, and consistent architecture.

---

# Database Rules

The database already exists and is populated with fake data for development and testing.

Therefore:

* Never create the database.
* Never recreate the database schema.
* Never call `Base.metadata.create_all()`.
* Never call `SQLModel.metadata.create_all()`.
* Never generate migrations unless I explicitly request them.
* Never reset or drop the database.

Whenever database access is required, always use the existing session provided by the project.

The project already contains:

```python
database/session.py
```

Always import and use the existing `get_session()` function from this module.

Do not create another session factory, engine, or database connection.

Always reuse the existing database configuration.

If you need a database session, import it from:

```python
from database.session import get_session
```

Assume that the engine, session configuration, and database lifecycle are already implemented correctly.

Your responsibility is only to use the existing session and interact with the database through the existing repositories.
