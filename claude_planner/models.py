"""Data models for claude-code-project-planner.

This module defines the core data structures used throughout the application,
including the ProjectBrief dataclass that represents a parsed PROJECT_BRIEF.md file.
"""

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
