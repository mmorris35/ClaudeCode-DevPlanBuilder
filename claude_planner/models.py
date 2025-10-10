"""Data models for claude-code-project-planner.

This module defines the core data structures used throughout the application,
including the ProjectBrief dataclass that represents a parsed PROJECT_BRIEF.md file,
and Phase/Task/Subtask models for representing development plans.
"""

import re
from dataclasses import dataclass, field


@dataclass
class ProjectBrief:
    """Represents a parsed PROJECT_BRIEF.md file with all project requirements.

    This dataclass holds all the information extracted from a PROJECT_BRIEF.md file,
    which will be used to generate claude.md and DEVELOPMENT_PLAN.md files.

    Attributes:
        project_name: The name of the project
        project_type: Type of project (e.g., "CLI Tool", "Library", "Web App")
        primary_goal: The main objective/purpose of the project
        target_users: Who will use this project
        timeline: Expected development timeline
        team_size: Number of developers on the team
        key_features: List of must-have features for MVP
        nice_to_have_features: List of features for future versions
        must_use_tech: Required technologies/frameworks
        cannot_use_tech: Prohibited technologies/frameworks
        deployment_target: Where the project will be deployed
        budget_constraints: Budget limitations (if any)
        performance_requirements: Performance metrics and targets
        security_requirements: Security considerations
        scalability_requirements: Scalability needs
        availability_requirements: Availability/uptime requirements
        team_composition: Team structure and skill levels
        existing_knowledge: Technologies team already knows
        learning_budget: Time allocated for learning new technologies
        infrastructure_access: Available infrastructure and tools
        success_criteria: How success will be measured
        external_systems: List of external systems to integrate with
        data_sources: Input data sources
        data_destinations: Output data destinations
        known_challenges: Identified risks and challenges
        reference_materials: Links to documentation and resources
        questions_and_clarifications: Open questions and decisions made
        architecture_vision: High-level architecture description
        use_cases: Example usage scenarios
        deliverables: Expected project deliverables

    Example:
        >>> brief = ProjectBrief(
        ...     project_name="My API",
        ...     project_type="API",
        ...     primary_goal="Build a REST API",
        ...     target_users="Developers",
        ...     timeline="2 weeks"
        ... )
        >>> print(brief.project_name)
        My API
    """

    # Basic Information
    project_name: str
    project_type: str
    primary_goal: str
    target_users: str
    timeline: str
    team_size: str = "1"

    # Functional Requirements
    key_features: list[str] = field(default_factory=list)
    nice_to_have_features: list[str] = field(default_factory=list)

    # Technical Constraints
    must_use_tech: list[str] = field(default_factory=list)
    cannot_use_tech: list[str] = field(default_factory=list)
    deployment_target: str | None = None
    budget_constraints: str | None = None

    # Quality Requirements
    performance_requirements: dict[str, str] = field(default_factory=dict)
    security_requirements: dict[str, str] = field(default_factory=dict)
    scalability_requirements: dict[str, str] = field(default_factory=dict)
    availability_requirements: dict[str, str] = field(default_factory=dict)

    # Team & Resources
    team_composition: str | None = None
    existing_knowledge: list[str] = field(default_factory=list)
    learning_budget: str | None = None
    infrastructure_access: list[str] = field(default_factory=list)

    # Success Criteria
    success_criteria: list[str] = field(default_factory=list)

    # Integration Requirements
    external_systems: list[dict[str, str]] = field(default_factory=list)
    data_sources: list[dict[str, str]] = field(default_factory=list)
    data_destinations: list[dict[str, str]] = field(default_factory=list)

    # Known Challenges
    known_challenges: list[str] = field(default_factory=list)

    # Reference Materials
    reference_materials: list[str] = field(default_factory=list)
    questions_and_clarifications: list[str] = field(default_factory=list)

    # Architecture
    architecture_vision: str | None = None
    use_cases: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        """Validate the ProjectBrief has all required fields.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> brief = ProjectBrief(project_name="", project_type="API",
            ...                      primary_goal="Build", target_users="Devs",
            ...                      timeline="1 week")
            >>> errors = brief.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Required fields
        if not self.project_name or not self.project_name.strip():
            errors.append("project_name is required and cannot be empty")

        if not self.project_type or not self.project_type.strip():
            errors.append("project_type is required and cannot be empty")

        if not self.primary_goal or not self.primary_goal.strip():
            errors.append("primary_goal is required and cannot be empty")

        if not self.target_users or not self.target_users.strip():
            errors.append("target_users is required and cannot be empty")

        if not self.timeline or not self.timeline.strip():
            errors.append("timeline is required and cannot be empty")

        return errors

    def is_valid(self) -> bool:
        """Check if the ProjectBrief is valid.

        Returns:
            True if valid (no validation errors), False otherwise.

        Example:
            >>> brief = ProjectBrief(project_name="API", project_type="API",
            ...                      primary_goal="Build", target_users="Devs",
            ...                      timeline="1 week")
            >>> brief.is_valid()
            True
        """
        return len(self.validate()) == 0


@dataclass
class Subtask:
    """Represents a single subtask in a development plan.

    A subtask is a unit of work that should be completable in a single session.
    Each subtask has an ID, title, deliverables, prerequisites, and status.

    Attributes:
        id: Subtask ID in format "X.Y.Z" (e.g., "1.2.3")
        title: Short descriptive title (should include "Single Session")
        deliverables: List of deliverable items
        prerequisites: List of prerequisite subtask IDs
        files_to_create: List of files to be created
        files_to_modify: List of files to be modified
        success_criteria: List of success criteria
        technology_decisions: List of technology choices made
        status: Current status (pending, in_progress, completed)
        completion_notes: Notes added when subtask is completed

    Example:
        >>> subtask = Subtask(
        ...     id="1.1.1",
        ...     title="Create models (Single Session)",
        ...     deliverables=["Create models.py", "Add tests"]
        ... )
        >>> print(subtask.id)
        1.1.1
    """

    id: str
    title: str
    deliverables: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    files_to_create: list[str] = field(default_factory=list)
    files_to_modify: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    technology_decisions: list[str] = field(default_factory=list)
    status: str = "pending"
    completion_notes: dict[str, str] = field(default_factory=dict)

    def validate(self) -> list[str]:
        """Validate the subtask follows best practices.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> subtask = Subtask(id="invalid", title="Test",
            ...                   deliverables=["Only one"])
            >>> errors = subtask.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Validate ID format (X.Y.Z)
        if not re.match(r"^\d+\.\d+\.\d+$", self.id):
            errors.append(f"Subtask ID '{self.id}' must be in format X.Y.Z")

        # Validate title has "(Single Session)" suffix
        if "(Single Session)" not in self.title:
            errors.append("Subtask title should include '(Single Session)' suffix")

        # Validate deliverables count (3-7 recommended)
        if len(self.deliverables) < 3:
            errors.append(
                f"Subtask has {len(self.deliverables)} deliverables, recommended minimum is 3"
            )
        elif len(self.deliverables) > 7:
            errors.append(
                f"Subtask has {len(self.deliverables)} deliverables, recommended maximum is 7"
            )

        # Validate status
        valid_statuses = ["pending", "in_progress", "completed", "blocked"]
        if self.status not in valid_statuses:
            errors.append(
                f"Status '{self.status}' is invalid. Must be one of: {', '.join(valid_statuses)}"
            )

        return errors

    def is_valid(self) -> bool:
        """Check if the subtask is valid.

        Returns:
            True if valid (no validation errors), False otherwise.
        """
        return len(self.validate()) == 0


@dataclass
class Task:
    """Represents a task in a development plan.

    A task groups related subtasks together and belongs to a phase.

    Attributes:
        id: Task ID in format "X.Y" (e.g., "1.2")
        title: Short descriptive title
        description: Longer description of the task
        subtasks: List of Subtask objects

    Example:
        >>> task = Task(id="1.1", title="Setup", description="Setup project")
        >>> task.subtasks.append(Subtask(id="1.1.1", title="Init (Single Session)"))
        >>> len(task.subtasks)
        1
    """

    id: str
    title: str
    description: str = ""
    subtasks: list[Subtask] = field(default_factory=list)

    def validate(self) -> list[str]:
        """Validate the task follows best practices.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> task = Task(id="invalid", title="Test")
            >>> errors = task.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Validate ID format (X.Y)
        if not re.match(r"^\d+\.\d+$", self.id):
            errors.append(f"Task ID '{self.id}' must be in format X.Y")

        # Validate has at least one subtask
        if len(self.subtasks) == 0:
            errors.append(f"Task '{self.id}' must have at least one subtask")

        # Validate all subtasks
        for subtask in self.subtasks:
            subtask_errors = subtask.validate()
            errors.extend([f"Subtask {subtask.id}: {error}" for error in subtask_errors])

        return errors

    def is_valid(self) -> bool:
        """Check if the task is valid.

        Returns:
            True if valid (no validation errors), False otherwise.
        """
        return len(self.validate()) == 0


@dataclass
class Phase:
    """Represents a phase in a development plan.

    A phase groups related tasks together and represents a major milestone.

    Attributes:
        id: Phase ID (integer as string, e.g., "0", "1")
        title: Short descriptive title
        description: Longer description of the phase
        goal: What this phase aims to achieve
        days: Estimated number of days
        tasks: List of Task objects

    Example:
        >>> phase = Phase(id="0", title="Foundation",
        ...               goal="Setup project", days="1-2")
        >>> phase.tasks.append(Task(id="0.1", title="Setup"))
        >>> len(phase.tasks)
        1
    """

    id: str
    title: str
    goal: str
    days: str = ""
    description: str = ""
    tasks: list[Task] = field(default_factory=list)

    def validate(self) -> list[str]:
        """Validate the phase follows best practices.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> phase = Phase(id="X", title="Test", goal="Test goal")
            >>> errors = phase.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Validate ID is numeric
        if not self.id.isdigit():
            errors.append(f"Phase ID '{self.id}' must be a number")

        # Validate phase 0 is "Foundation" (warning)
        if self.id == "0" and "Foundation" not in self.title:
            errors.append(f"Phase 0 should be titled 'Foundation', got '{self.title}' (warning)")

        # Validate has at least one task
        if len(self.tasks) == 0:
            errors.append(f"Phase '{self.id}' must have at least one task")

        # Validate all tasks
        for task in self.tasks:
            task_errors = task.validate()
            errors.extend([f"Task {task.id}: {error}" for error in task_errors])

        return errors

    def is_valid(self) -> bool:
        """Check if the phase is valid.

        Returns:
            True if valid (no validation errors), False otherwise.
        """
        return len(self.validate()) == 0


@dataclass
class TechStack:
    """Represents the technology stack for a project.

    This dataclass holds technology choices for different aspects of a project,
    including languages, frameworks, databases, and tools.

    Attributes:
        language: Primary programming language
        framework: Main framework (e.g., "Flask", "FastAPI", "React")
        database: Database choice (e.g., "PostgreSQL", "MongoDB")
        testing: Testing framework (e.g., "pytest", "Jest")
        linting: Linting tool (e.g., "ruff", "eslint")
        type_checking: Type checking tool (e.g., "mypy", "TypeScript")
        deployment: Deployment target (e.g., "AWS", "Heroku")
        ci_cd: CI/CD platform (e.g., "GitHub Actions", "GitLab CI")
        additional_tools: Dictionary of additional tools/libraries

    Example:
        >>> stack = TechStack(
        ...     language="Python 3.11",
        ...     framework="FastAPI",
        ...     database="PostgreSQL"
        ... )
        >>> print(stack.language)
        Python 3.11
    """

    language: str
    framework: str = ""
    database: str = ""
    testing: str = ""
    linting: str = ""
    type_checking: str = ""
    deployment: str = ""
    ci_cd: str = ""
    additional_tools: dict[str, str] = field(default_factory=dict)

    def validate(self) -> list[str]:
        """Validate the TechStack has required fields.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> stack = TechStack(language="")
            >>> errors = stack.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Language is required
        if not self.language or not self.language.strip():
            errors.append("language is required and cannot be empty")

        return errors

    def is_valid(self) -> bool:
        """Check if the TechStack is valid.

        Returns:
            True if valid (no validation errors), False otherwise.

        Example:
            >>> stack = TechStack(language="Python 3.11")
            >>> stack.is_valid()
            True
        """
        return len(self.validate()) == 0

    def to_dict(self) -> dict[str, str]:
        """Convert TechStack to a dictionary for template rendering.

        Returns:
            Dictionary with all non-empty technology choices.

        Example:
            >>> stack = TechStack(language="Python", framework="Flask")
            >>> d = stack.to_dict()
            >>> d["language"]
            'Python'
        """
        result = {"language": self.language}

        if self.framework:
            result["framework"] = self.framework
        if self.database:
            result["database"] = self.database
        if self.testing:
            result["testing"] = self.testing
        if self.linting:
            result["linting"] = self.linting
        if self.type_checking:
            result["type_checking"] = self.type_checking
        if self.deployment:
            result["deployment"] = self.deployment
        if self.ci_cd:
            result["ci_cd"] = self.ci_cd

        # Add additional tools
        result.update(self.additional_tools)

        return result
