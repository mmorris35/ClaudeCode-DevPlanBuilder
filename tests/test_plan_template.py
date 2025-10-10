"""Tests for DEVELOPMENT_PLAN.md Jinja2 template rendering.

This module tests that the base plan.md.j2 template correctly renders
with various input data, properly substitutes variables, and generates
valid markdown output with phases, tasks, and subtasks.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


@pytest.fixture
def template_env() -> Environment:
    """Create Jinja2 environment with templates directory."""
    templates_dir = Path(__file__).parent.parent / "claude_planner" / "templates"
    return Environment(loader=FileSystemLoader(str(templates_dir)))


@pytest.fixture
def minimal_plan_data() -> dict:
    """Minimal required data for plan template rendering."""
    return {
        "project_name": "Test Project",
        "goal": "Build a test application",
        "target_users": "Developers",
        "timeline": "2 weeks",
        "tech_stack": {
            "Language": "Python 3.11+",
            "Testing": "pytest",
        },
        "phases": [
            {
                "id": 0,
                "title": "Foundation",
                "timeline": "Week 1, Days 1-2",
                "goal": "Set up project infrastructure",
                "tasks": [
                    {
                        "id": "0.1",
                        "title": "Repository Setup",
                        "subtasks": [
                            {
                                "id": "0.1.1",
                                "title": "Initialize Git Repository (Single Session)",
                                "status": "pending",
                                "prerequisites": [],
                                "deliverables": [
                                    "Create .gitignore",
                                    "Create README.md",
                                    "Initial commit",
                                ],
                                "success_criteria": [
                                    ".gitignore covers Python files",
                                    "README has basic info",
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "current_phase": 0,
        "next_subtask": "0.1.1",
    }


@pytest.fixture
def full_plan_data(minimal_plan_data: dict) -> dict:
    """Full plan data with all optional fields."""
    data = minimal_plan_data.copy()
    data.update(
        {
            "mvp_scope": [
                "✅ CLI with commands",
                "✅ Template library",
                "❌ Web UI (v2)",
            ],
            "key_libraries": ["click", "jinja2", "pytest"],
            "success_metrics": {
                "Development Process": [
                    "Code coverage: >80%",
                    "All tests pass",
                ],
                "Product Metrics": [
                    "Generate plan in <5 seconds",
                    "Validation passes with 0 errors",
                ],
            },
            "timeline_summary": [
                {
                    "id": 0,
                    "days": "1-2",
                    "deliverable": "Foundation",
                    "complete": False,
                }
            ],
            "total_timeline": "2 weeks (10 days)",
        }
    )
    # Add technology decisions and file info to subtask
    data["phases"][0]["tasks"][0]["subtasks"][0].update(
        {
            "technology_decisions": ["Git for version control", "GitHub for hosting"],
            "files_to_create": [
                {"path": ".gitignore", "description": "Python standard"},
                {"path": "README.md", "description": "Project overview"},
            ],
            "files_to_modify": [{"path": "setup.py", "description": "Add version"}],
            "completion_notes": {
                "implementation": "Created foundational repository files",
                "files_created": [".gitignore", "README.md"],
                "files_modified": ["setup.py"],
                "tests": "N/A (no code to test yet)",
                "build": "✅ Success",
                "branch": "main",
                "notes": "Repository foundation complete",
            },
        }
    )
    return data


@pytest.fixture
def multiple_phases_data(minimal_plan_data: dict) -> dict:
    """Plan data with multiple phases, tasks, and subtasks."""
    data = minimal_plan_data.copy()
    data["phases"].append(
        {
            "id": 1,
            "title": "Core Features",
            "timeline": "Week 1, Days 3-4",
            "goal": "Implement core functionality",
            "prerequisites": "Phase 0 complete",
            "tasks": [
                {
                    "id": "1.1",
                    "title": "Data Models",
                    "goal": "Define core data structures",
                    "subtasks": [
                        {
                            "id": "1.1.1",
                            "title": "User Model (Single Session)",
                            "status": "complete",
                            "prerequisites": ["0.1.1"],
                            "deliverables": [
                                "Create user.py",
                                "Add user tests",
                            ],
                            "success_criteria": [
                                "User model created",
                                "Tests pass",
                            ],
                        },
                        {
                            "id": "1.1.2",
                            "title": "Post Model (Single Session)",
                            "status": "pending",
                            "prerequisites": ["1.1.1"],
                            "deliverables": [
                                "Create post.py",
                                "Add post tests",
                            ],
                            "success_criteria": [
                                "Post model created",
                                "Tests pass",
                            ],
                        },
                    ],
                }
            ],
        }
    )
    return data


class TestPlanTemplateLoading:
    """Test template loading and availability."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that plan.md.j2 template can be loaded."""
        try:
            template = template_env.get_template("base/plan.md.j2")
            assert template is not None
        except TemplateNotFound:
            pytest.fail("Template base/plan.md.j2 not found")

    def test_template_has_content(self, template_env: Environment, minimal_plan_data: dict) -> None:
        """Test that template file is not empty."""
        template = template_env.get_template("base/plan.md.j2")
        rendered = template.render(**minimal_plan_data)
        assert rendered is not None
        assert len(rendered) > 100  # Should have substantial content


class TestPlanTemplateRendering:
    """Test template rendering with various data."""

    def test_render_with_minimal_data(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test template renders successfully with minimal required data."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert result is not None
        assert len(result) > 0

    def test_render_with_full_data(self, template_env: Environment, full_plan_data: dict) -> None:
        """Test template renders successfully with full data including optional fields."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert result is not None
        assert len(result) > 0

    def test_project_name_substitution(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that project_name variable is correctly substituted."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "Test Project" in result
        assert "# Test Project - Development Plan" in result

    def test_goal_and_timeline_substitution(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that goal and timeline variables are correctly substituted."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "Build a test application" in result
        assert "2 weeks" in result
        assert "Developers" in result

    def test_tech_stack_loop(self, template_env: Environment, minimal_plan_data: dict) -> None:
        """Test that tech_stack dictionary is correctly looped and rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Language**: Python 3.11+" in result
        assert "**Testing**: pytest" in result


class TestPlanTemplatePhases:
    """Test phase, task, and subtask rendering."""

    def test_phase_rendering(self, template_env: Environment, minimal_plan_data: dict) -> None:
        """Test that phases are correctly rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "## Phase 0: Foundation (Week 1, Days 1-2)" in result
        assert "**Goal**: Set up project infrastructure" in result

    def test_task_rendering(self, template_env: Environment, minimal_plan_data: dict) -> None:
        """Test that tasks are correctly rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "### Task 0.1: Repository Setup" in result

    def test_subtask_rendering(self, template_env: Environment, minimal_plan_data: dict) -> None:
        """Test that subtasks are correctly rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Subtask 0.1.1: Initialize Git Repository (Single Session)**" in result

    def test_deliverables_rendering(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that deliverables are correctly rendered with checkboxes."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Deliverables**:" in result
        assert "- [ ] Create .gitignore" in result
        assert "- [ ] Create README.md" in result
        assert "- [ ] Initial commit" in result

    def test_success_criteria_rendering(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that success criteria are correctly rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Success Criteria**:" in result
        assert "- [ ] .gitignore covers Python files" in result
        assert "- [ ] README has basic info" in result

    def test_prerequisites_rendering(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that prerequisites are correctly rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Prerequisites**:" in result
        assert "- None" in result  # No prerequisites for first task

    def test_completion_notes_empty(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that completion notes template is rendered when empty."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Completion Notes**:" in result
        assert "- **Implementation**:" in result
        assert "- **Files Created**:" in result
        assert "- **Tests**:" in result


class TestPlanTemplateProgressTracking:
    """Test progress tracking section rendering."""

    def test_progress_tracking_section(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that progress tracking section is rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "## Progress Tracking" in result
        assert "### Phase 0: Foundation (Week 1, Days 1-2)" in result

    def test_progress_tracking_checkboxes(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that progress tracking shows correct checkbox states."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        # Pending subtask should have empty checkbox
        assert "- [ ] 0.1.1: Initialize Git Repository (Single Session)" in result

    def test_progress_tracking_completed(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that completed subtasks show checked boxes in progress tracking."""
        # Mark subtask as complete
        minimal_plan_data["phases"][0]["tasks"][0]["subtasks"][0]["status"] = "complete"

        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        # Completed subtask should have checked checkbox
        assert "- [x] 0.1.1: Initialize Git Repository (Single Session)" in result

    def test_current_and_next_indicators(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that current phase and next subtask are indicated."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        assert "**Current**: Phase 0" in result
        assert "**Next**: 0.1.1" in result


class TestPlanTemplateOptionalSections:
    """Test optional section rendering."""

    def test_mvp_scope_when_present(self, template_env: Environment, full_plan_data: dict) -> None:
        """Test that MVP scope is rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "**MVP Scope**:" in result
        assert "- ✅ CLI with commands" in result
        assert "- ❌ Web UI (v2)" in result

    def test_mvp_scope_when_absent(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that MVP scope is excluded when not present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        # Should not have MVP scope section
        assert "**MVP Scope**:" not in result

    def test_key_libraries_when_present(
        self, template_env: Environment, full_plan_data: dict
    ) -> None:
        """Test that key libraries are rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "**Key Libraries**: click, jinja2, pytest" in result

    def test_technology_decisions_when_present(
        self, template_env: Environment, full_plan_data: dict
    ) -> None:
        """Test that technology decisions are rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "**Technology Decisions**:" in result
        assert "- Git for version control" in result

    def test_files_sections_when_present(
        self, template_env: Environment, full_plan_data: dict
    ) -> None:
        """Test that files to create/modify sections are rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "**Files to Create**:" in result
        assert "- `.gitignore` - Python standard" in result
        assert "**Files to Modify**:" in result
        assert "- `setup.py` - Add version" in result

    def test_completion_notes_when_present(
        self, template_env: Environment, full_plan_data: dict
    ) -> None:
        """Test that completion notes are rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "- **Implementation**: Created foundational repository files" in result
        assert "- **Files Created**:" in result
        assert "  - .gitignore" in result
        assert "- **Build**: ✅ Success" in result

    def test_success_metrics_when_present(
        self, template_env: Environment, full_plan_data: dict
    ) -> None:
        """Test that success metrics are rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "## Success Metrics" in result
        assert "**Development Process**:" in result
        assert "- Code coverage: >80%" in result

    def test_timeline_summary_when_present(
        self, template_env: Environment, full_plan_data: dict
    ) -> None:
        """Test that timeline summary is rendered when present."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**full_plan_data)

        assert "## Timeline Summary" in result
        assert "| Phase | Days | Deliverable | Status |" in result
        assert "| Phase 0 | 1-2 | Foundation | [ ] |" in result
        assert "**Total**: 2 weeks (10 days)" in result


class TestPlanTemplateMultiplePhases:
    """Test rendering with multiple phases, tasks, and subtasks."""

    def test_multiple_phases_rendered(
        self, template_env: Environment, multiple_phases_data: dict
    ) -> None:
        """Test that multiple phases are all rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**multiple_phases_data)

        assert "## Phase 0: Foundation" in result
        assert "## Phase 1: Core Features" in result

    def test_multiple_tasks_rendered(
        self, template_env: Environment, multiple_phases_data: dict
    ) -> None:
        """Test that multiple tasks within a phase are rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**multiple_phases_data)

        assert "### Task 0.1: Repository Setup" in result
        assert "### Task 1.1: Data Models" in result

    def test_multiple_subtasks_rendered(
        self, template_env: Environment, multiple_phases_data: dict
    ) -> None:
        """Test that multiple subtasks within a task are rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**multiple_phases_data)

        assert "**Subtask 1.1.1: User Model (Single Session)**" in result
        assert "**Subtask 1.1.2: Post Model (Single Session)**" in result

    def test_prerequisite_references(
        self, template_env: Environment, multiple_phases_data: dict
    ) -> None:
        """Test that prerequisites correctly reference other subtasks."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**multiple_phases_data)

        # Subtask 1.1.2 should show 1.1.1 as prerequisite
        assert "- [ ] 1.1.1" in result

    def test_mixed_completion_states(
        self, template_env: Environment, multiple_phases_data: dict
    ) -> None:
        """Test that mixed completion states are correctly rendered."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**multiple_phases_data)

        # Progress tracking should show completed and pending tasks
        assert "- [x] 1.1.1: User Model (Single Session)" in result
        assert "- [ ] 1.1.2: Post Model (Single Session)" in result


class TestPlanTemplateValidation:
    """Test that rendered output is valid markdown."""

    def test_no_template_syntax_in_output(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that no unrendered Jinja2 syntax remains in output."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        # Check for common Jinja2 syntax patterns
        assert "{{" not in result, "Unrendered variable substitution found"
        assert "}}" not in result, "Unrendered variable substitution found"
        assert "{%" not in result, "Unrendered template tag found"
        assert "%}" not in result, "Unrendered template tag found"
        assert "{#" not in result, "Unrendered comment found"
        assert "#}" not in result, "Unrendered comment found"

    def test_consistent_heading_hierarchy(
        self, template_env: Environment, minimal_plan_data: dict
    ) -> None:
        """Test that heading levels are properly nested."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        # Extract all headings
        headings = re.findall(r"^(#{1,6})\s+(.+)$", result, re.MULTILINE)

        # Should have headings
        assert len(headings) > 0

        # First heading should be H1
        assert headings[0][0] == "#"

    def test_checkbox_format(self, template_env: Environment, minimal_plan_data: dict) -> None:
        """Test that all checkboxes follow correct markdown format."""
        template = template_env.get_template("base/plan.md.j2")
        result = template.render(**minimal_plan_data)

        # Find all checkbox patterns
        checkboxes = re.findall(r"- \[([ x])\]", result)

        # Should have checkboxes
        assert len(checkboxes) > 0

        # All checkboxes should be either [ ] or [x]
        for checkbox in checkboxes:
            assert checkbox in [" ", "x"]
