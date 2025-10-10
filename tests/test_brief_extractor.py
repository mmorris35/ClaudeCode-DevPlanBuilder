"""Unit tests for PROJECT_BRIEF.md field extraction module."""

from claude_planner.generator.brief_extractor import (
    extract_basic_info,
    extract_quality_requirements,
    extract_requirements,
    extract_team_info,
    extract_tech_constraints,
)


class TestExtractBasicInfo:
    """Test cases for extract_basic_info function."""

    def test_extract_all_fields(self) -> None:
        """Test extracting all basic info fields."""
        sections = {
            "Basic Information": """- **Project Name**: My Awesome Project
- **Project Type**: [x] CLI Tool + [x] Library
- **Primary Goal**: Build something great
- **Target Users**: Developers
- **Timeline**: 2 weeks
- **Team Size**: 5 developers"""
        }

        result = extract_basic_info(sections)

        assert result["project_name"] == "My Awesome Project"
        assert result["project_type"] == ["CLI Tool", "Library"]
        assert result["primary_goal"] == "Build something great"
        assert result["target_users"] == "Developers"
        assert result["timeline"] == "2 weeks"
        assert result["team_size"] == "5 developers"

    def test_extract_single_project_type(self) -> None:
        """Test extracting single checked project type."""
        sections = {
            "Basic Information": """- **Project Name**: Simple Project
- **Project Type**: [x] API + [ ] CLI Tool"""
        }

        result = extract_basic_info(sections)

        assert result["project_type"] == ["API"]

    def test_extract_with_missing_fields(self) -> None:
        """Test extracting when some fields are missing."""
        sections = {
            "Basic Information": """- **Project Name**: Minimal Project
- **Timeline**: 1 week"""
        }

        result = extract_basic_info(sections)

        assert result["project_name"] == "Minimal Project"
        assert result["project_type"] == []  # No checkboxes found
        assert result["primary_goal"] == ""
        assert result["target_users"] == ""
        assert result["timeline"] == "1 week"
        assert result["team_size"] == ""

    def test_extract_from_empty_section(self) -> None:
        """Test extracting from empty sections."""
        sections: dict[str, str] = {}

        result = extract_basic_info(sections)

        assert result["project_name"] == ""
        assert result["project_type"] == []
        assert result["primary_goal"] == ""
        assert result["target_users"] == ""
        assert result["timeline"] == ""
        assert result["team_size"] == ""


class TestExtractRequirements:
    """Test cases for extract_requirements function."""

    def test_extract_all_requirements(self) -> None:
        """Test extracting all functional requirements."""
        sections = {
            "Input": """- File 1
- File 2
- Config file""",
            "Output": """- Generated code
- Documentation
- Test suite""",
            "Key Features": """1. Feature A
2. Feature B
3. Feature C""",
            "Nice-to-Have Features": """- Web UI
- API integration""",
        }

        result = extract_requirements(sections)

        assert len(result["input"]) == 3
        assert "File 1" in result["input"]
        assert "File 2" in result["input"]
        assert "Config file" in result["input"]

        assert len(result["output"]) == 3
        assert "Generated code" in result["output"]

        assert len(result["key_features"]) == 3
        assert "Feature A" in result["key_features"]

        assert len(result["nice_to_have"]) == 2
        assert "Web UI" in result["nice_to_have"]

    def test_extract_with_missing_sections(self) -> None:
        """Test extracting when some sections are missing."""
        sections: dict[str, str] = {
            "Input": """- Input file""",
            "Key Features": """- Must have feature""",
        }

        result = extract_requirements(sections)

        assert result["input"] == ["Input file"]
        assert result["output"] == []
        assert result["key_features"] == ["Must have feature"]
        assert result["nice_to_have"] == []

    def test_extract_from_empty_sections(self) -> None:
        """Test extracting from empty sections."""
        sections: dict[str, str] = {}

        result = extract_requirements(sections)

        assert result["input"] == []
        assert result["output"] == []
        assert result["key_features"] == []
        assert result["nice_to_have"] == []

    def test_extract_mixed_list_formats(self) -> None:
        """Test extracting from different list formats."""
        sections = {
            "Input": """- Unordered item 1
- Unordered item 2""",
            "Output": """1. Ordered item 1
2. Ordered item 2""",
        }

        result = extract_requirements(sections)

        assert len(result["input"]) == 2
        assert len(result["output"]) == 2


class TestExtractTechConstraints:
    """Test cases for extract_tech_constraints function."""

    def test_extract_all_constraints(self) -> None:
        """Test extracting all technical constraints."""
        sections = {
            "Must Use": """- Python 3.11+
- Click framework
- Jinja2""",
            "Cannot Use": """- GUI frameworks
- External APIs
- Databases""",
            "Deployment Target": """- [x] Local only
- Must support: Linux, macOS, Windows 10+""",
        }

        result = extract_tech_constraints(sections)

        assert len(result["must_use"]) == 3
        assert "Python 3.11+" in result["must_use"]
        assert "Click framework" in result["must_use"]

        assert len(result["cannot_use"]) == 3
        assert "GUI frameworks" in result["cannot_use"]

        assert len(result["deployment_target"]) == 2

    def test_extract_with_missing_sections(self) -> None:
        """Test extracting when some sections are missing."""
        sections = {
            "Must Use": """- Python""",
        }

        result = extract_tech_constraints(sections)

        assert result["must_use"] == ["Python"]
        assert result["cannot_use"] == []
        assert result["deployment_target"] == []

    def test_extract_from_empty_sections(self) -> None:
        """Test extracting from empty sections."""
        sections: dict[str, str] = {}

        result = extract_tech_constraints(sections)

        assert result["must_use"] == []
        assert result["cannot_use"] == []
        assert result["deployment_target"] == []


class TestExtractQualityRequirements:
    """Test cases for extract_quality_requirements function."""

    def test_extract_performance_requirements(self) -> None:
        """Test extracting performance requirements."""
        sections = {
            "Performance": """- **Generation Time**: <5 seconds
- **Memory Usage**: <200 MB
- **Startup Time**: <1 second"""
        }

        result = extract_quality_requirements(sections)

        assert "Generation Time" in result["performance"]
        assert result["performance"]["Generation Time"] == "<5 seconds"
        assert result["performance"]["Memory Usage"] == "<200 MB"
        assert result["performance"]["Startup Time"] == "<1 second"

    def test_extract_security_requirements(self) -> None:
        """Test extracting security requirements."""
        sections = {
            "Security": """- **Authentication**: N/A (local tool)
- **Data Sensitivity**: [x] Internal
- **Encryption**: N/A"""
        }

        result = extract_quality_requirements(sections)

        assert "Authentication" in result["security"]
        assert result["security"]["Authentication"] == "N/A (local tool)"
        assert "Data Sensitivity" in result["security"]

    def test_extract_scalability_requirements(self) -> None:
        """Test extracting scalability requirements."""
        sections = {
            "Scalability": """- **Plan Size**: Handle 200+ subtasks
- **Template Count**: Support 50+ templates"""
        }

        result = extract_quality_requirements(sections)

        assert "Plan Size" in result["scalability"]
        assert result["scalability"]["Plan Size"] == "Handle 200+ subtasks"

    def test_extract_all_quality_sections(self) -> None:
        """Test extracting from all quality sections."""
        sections = {
            "Performance": """- **Speed**: Fast""",
            "Security": """- **Auth**: Required""",
            "Scalability": """- **Scale**: High""",
        }

        result = extract_quality_requirements(sections)

        assert "Speed" in result["performance"]
        assert "Auth" in result["security"]
        assert "Scale" in result["scalability"]

    def test_extract_with_missing_sections(self) -> None:
        """Test extracting when some sections are missing."""
        sections = {
            "Performance": """- **Metric**: Value""",
        }

        result = extract_quality_requirements(sections)

        assert len(result["performance"]) == 1
        assert result["security"] == {}
        assert result["scalability"] == {}

    def test_extract_from_empty_sections(self) -> None:
        """Test extracting from empty sections."""
        sections: dict[str, str] = {}

        result = extract_quality_requirements(sections)

        assert result["performance"] == {}
        assert result["security"] == {}
        assert result["scalability"] == {}

    def test_extract_ignores_lines_without_bold_or_colon(self) -> None:
        """Test that lines without ** or : are ignored."""
        sections = {
            "Performance": """Some introductory text
- **Valid Field**: Value
Just a comment
- **Another Field**: Another Value"""
        }

        result = extract_quality_requirements(sections)

        assert len(result["performance"]) == 2
        assert "Valid Field" in result["performance"]
        assert "Another Field" in result["performance"]


class TestExtractTeamInfo:
    """Test cases for extract_team_info function."""

    def test_extract_all_team_info(self) -> None:
        """Test extracting all team information."""
        sections = {
            "Team Composition": """- [x] Senior
- [ ] Junior
- [x] Full-stack""",
            "Existing Knowledge": """- Python
- JavaScript
- Docker""",
            "Infrastructure Access": """- [x] GitHub Actions
- [x] AWS""",
        }

        result = extract_team_info(sections)

        # Type assertion for mypy - team_composition is dict[str, bool]
        team_comp = result["team_composition"]
        assert isinstance(team_comp, dict)
        assert team_comp["Senior"] is True
        assert team_comp["Junior"] is False
        assert team_comp["Full-stack"] is True

        # existing_knowledge is list[str]
        existing_knowledge = result["existing_knowledge"]
        assert isinstance(existing_knowledge, list)
        assert len(existing_knowledge) == 3
        assert "Python" in existing_knowledge
        assert "Docker" in existing_knowledge

        # Infrastructure has checkboxes but we extract list items
        infrastructure = result["infrastructure"]
        assert isinstance(infrastructure, list)
        assert len(infrastructure) == 2

    def test_extract_with_missing_sections(self) -> None:
        """Test extracting when some sections are missing."""
        sections = {
            "Team Composition": """- [x] Senior""",
        }

        result = extract_team_info(sections)

        team_comp = result["team_composition"]
        assert isinstance(team_comp, dict)
        assert team_comp["Senior"] is True
        assert result["existing_knowledge"] == []
        assert result["infrastructure"] == []

    def test_extract_from_empty_sections(self) -> None:
        """Test extracting from empty sections."""
        sections: dict[str, str] = {}

        result = extract_team_info(sections)

        assert result["team_composition"] == {}
        assert result["existing_knowledge"] == []
        assert result["infrastructure"] == []

    def test_extract_team_composition_only_checked(self) -> None:
        """Test extracting only checked team composition items."""
        sections = {
            "Team Composition": """- [x] Expert
- [ ] Intermediate
- [ ] Beginner"""
        }

        result = extract_team_info(sections)

        team_comp = result["team_composition"]
        assert isinstance(team_comp, dict)
        assert team_comp["Expert"] is True
        assert team_comp["Intermediate"] is False
        assert team_comp["Beginner"] is False
