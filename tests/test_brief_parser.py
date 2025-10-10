"""Integration tests for complete PROJECT_BRIEF.md parser pipeline."""

from pathlib import Path

import pytest

from claude_planner.generator.brief_parser import parse_project_brief
from claude_planner.models import ProjectBrief


class TestParseProjectBrief:
    """Integration test cases for parse_project_brief function."""

    def test_parse_real_project_brief(self) -> None:
        """Test parsing the actual PROJECT_BRIEF.md file from the repository."""
        # Use the real PROJECT_BRIEF.md from the project root
        brief_path = Path("PROJECT_BRIEF.md")

        # Skip if file doesn't exist (for isolated test environments)
        if not brief_path.exists():
            pytest.skip("PROJECT_BRIEF.md not found in repository root")

        result = parse_project_brief(brief_path)

        # Verify it returns a ProjectBrief instance
        assert isinstance(result, ProjectBrief)

        # Verify expected fields from our real PROJECT_BRIEF.md
        assert result.project_name == "Claude Code Project Planner"
        assert "CLI Tool" in result.project_type
        assert "Library" in result.project_type
        expected_users = (
            "Developers (including yourself) who want to quickly bootstrap "
            "new projects with Claude Code"
        )
        assert result.target_users == expected_users
        assert result.timeline == "2 weeks"
        assert result.team_size == "1 senior developer (you)"

        # Verify some key features
        assert len(result.key_features) > 0
        assert any("CLI Command" in feature for feature in result.key_features)

        # Verify tech constraints
        assert len(result.must_use_tech) > 0
        assert any("Python 3.11+" in tech for tech in result.must_use_tech)

    def test_parse_minimal_valid_brief(self, tmp_path: Path) -> None:
        """Test parsing a minimal valid PROJECT_BRIEF.md file."""
        brief_path = tmp_path / "brief.md"
        brief_content = """# Project Brief: Test Project

## Basic Information

- **Project Name**: Test Project
- **Project Type**: [x] CLI Tool
- **Primary Goal**: Test goal
- **Target Users**: Test users
- **Timeline**: 1 week
- **Team Size**: 1 developer

## Functional Requirements

### Input
- Input 1

### Output
- Output 1

### Key Features
1. Feature 1

### Nice-to-Have Features
- Nice 1

## Technical Constraints

### Must Use
- Python

### Cannot Use
- PHP

### Deployment Target
- [x] Local only

## Quality Requirements

### Performance
- **Speed**: Fast

### Security
- **Auth**: Required

### Scalability
- **Users**: 100+

## Team & Resources

### Team Composition
- [x] Senior

### Existing Knowledge
- Python

### Infrastructure Access
- [x] GitHub
"""
        brief_path.write_text(brief_content, encoding="utf-8")

        result = parse_project_brief(brief_path)

        assert isinstance(result, ProjectBrief)
        assert result.project_name == "Test Project"
        assert result.project_type == "CLI Tool"
        assert result.primary_goal == "Test goal"
        assert result.target_users == "Test users"
        assert result.timeline == "1 week"
        assert result.team_size == "1 developer"
        assert result.key_features == ["Feature 1"]
        assert result.must_use_tech == ["Python"]

    def test_parse_file_not_found(self, tmp_path: Path) -> None:
        """Test parsing a non-existent file raises FileNotFoundError."""
        brief_path = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError) as exc_info:
            parse_project_brief(brief_path)

        assert "not found" in str(exc_info.value).lower()
        assert str(brief_path) in str(exc_info.value)

    def test_parse_directory_not_file(self, tmp_path: Path) -> None:
        """Test parsing a directory raises ValueError."""
        brief_dir = tmp_path / "brief_dir"
        brief_dir.mkdir()

        with pytest.raises(ValueError) as exc_info:
            parse_project_brief(brief_dir)

        assert "not a file" in str(exc_info.value).lower()

    def test_parse_missing_required_field(self, tmp_path: Path) -> None:
        """Test parsing fails when required field is missing."""
        brief_path = tmp_path / "brief.md"
        brief_content = """# Project Brief: Test

## Basic Information

- **Project Name**: Test Project
- **Project Type**: [x] CLI Tool
- **Primary Goal**:
- **Target Users**: Test users
- **Timeline**: 1 week
"""
        brief_path.write_text(brief_content, encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            parse_project_brief(brief_path)

        # Should indicate it's a conversion error with missing field
        assert "primary_goal" in str(exc_info.value).lower()

    def test_parse_empty_file(self, tmp_path: Path) -> None:
        """Test parsing an empty file fails gracefully."""
        brief_path = tmp_path / "brief.md"
        brief_path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            parse_project_brief(brief_path)

        # Should fail during conversion due to missing required fields
        assert "failed" in str(exc_info.value).lower()

    def test_parse_malformed_markdown(self, tmp_path: Path) -> None:
        """Test parsing handles malformed markdown gracefully."""
        brief_path = tmp_path / "brief.md"
        brief_content = """Not valid markdown structure
No sections here
Just random text
"""
        brief_path.write_text(brief_content, encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            parse_project_brief(brief_path)

        # Should fail during conversion due to missing required fields
        assert "failed" in str(exc_info.value).lower()

    def test_parse_with_complex_project_type(self, tmp_path: Path) -> None:
        """Test parsing with multiple project types."""
        brief_path = tmp_path / "brief.md"
        brief_content = """# Project Brief: Multi Type

## Basic Information

- **Project Name**: Multi Project
- **Project Type**: [x] CLI Tool + [x] Library + [x] API
- **Primary Goal**: Build everything
- **Target Users**: Everyone
- **Timeline**: 3 weeks
- **Team Size**: 5

## Functional Requirements

### Input
- Input

### Output
- Output

### Key Features
1. Feature

### Nice-to-Have Features
- Nice

## Technical Constraints

### Must Use
- Python

### Cannot Use
- Nothing

### Deployment Target
- [x] Cloud

## Quality Requirements

### Performance
- **Speed**: Fast

### Security
- **Auth**: Yes

### Scalability
- **Scale**: High

## Team & Resources

### Team Composition
- [x] Senior
- [ ] Junior

### Existing Knowledge
- Python

### Infrastructure Access
- [x] AWS
"""
        brief_path.write_text(brief_content, encoding="utf-8")

        result = parse_project_brief(brief_path)

        assert "CLI Tool" in result.project_type
        assert "Library" in result.project_type
        assert "API" in result.project_type

    def test_parse_error_contains_stage_context(self, tmp_path: Path) -> None:
        """Test that parsing errors include context about which stage failed."""
        brief_path = tmp_path / "brief.md"
        brief_content = """# Project Brief

## Basic Information

- **Project Name**: Test
- **Project Type**: [x] CLI
- **Primary Goal**:
- **Target Users**: Users
- **Timeline**: 1 week
"""
        brief_path.write_text(brief_content, encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            parse_project_brief(brief_path)

        error_message = str(exc_info.value).lower()
        # Error should mention the stage that failed
        assert (
            "convert" in error_message
            or "extraction" in error_message
            or "primary_goal" in error_message
        )

    def test_parse_with_all_sections_present(self, tmp_path: Path) -> None:
        """Test parsing with comprehensive content in all sections."""
        brief_path = tmp_path / "brief.md"
        brief_content = """# Project Brief: Comprehensive Test

## Basic Information

- **Project Name**: Comprehensive Project
- **Project Type**: [x] Web App + [x] API
- **Primary Goal**: Full-featured application
- **Target Users**: Developers and end users
- **Timeline**: 4 weeks
- **Team Size**: 10 developers

## Functional Requirements

### Input
- User input forms
- API requests
- File uploads

### Output
- Web pages
- API responses
- Reports

### Key Features
1. User authentication
2. Data visualization
3. Real-time updates
4. Mobile responsive

### Nice-to-Have Features
- Dark mode
- Offline support
- Push notifications

## Technical Constraints

### Must Use
- Python 3.11+
- React
- PostgreSQL

### Cannot Use
- PHP
- MySQL
- jQuery

### Deployment Target
- [x] AWS
- [x] Docker containers

### Budget Constraints
- [x] Free/open-source only

## Quality Requirements

### Performance
- **Response Time**: <200ms
- **Throughput**: 1000 req/s
- **Page Load**: <2s

### Security
- **Authentication**: OAuth2
- **Encryption**: TLS 1.3
- **Data Sensitivity**: [x] Confidential

### Scalability
- **Users**: 100,000+
- **Storage**: 1TB+
- **Geographic**: Multi-region

### Availability
- **Uptime**: 99.9%
- **Backup**: Daily

## Team & Resources

### Team Composition
- [x] Senior developers
- [x] Mid-level developers
- [ ] Junior developers

### Existing Knowledge
- Python
- JavaScript
- Docker
- AWS

### Infrastructure Access
- [x] GitHub Actions
- [x] AWS account
- [x] Monitoring tools
"""
        brief_path.write_text(brief_content, encoding="utf-8")

        result = parse_project_brief(brief_path)

        assert isinstance(result, ProjectBrief)
        assert result.project_name == "Comprehensive Project"
        assert "Web App" in result.project_type
        assert "API" in result.project_type
        assert len(result.key_features) == 4
        assert len(result.nice_to_have_features) == 3
        assert len(result.must_use_tech) == 3
        assert len(result.cannot_use_tech) == 3
        assert result.performance_requirements["Response Time"] == "<200ms"
        assert result.security_requirements["Authentication"] == "OAuth2"
        assert result.scalability_requirements["Users"] == "100,000+"
        assert len(result.existing_knowledge) == 4
