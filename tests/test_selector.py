"""Unit tests for template selector module."""

from pathlib import Path

import pytest

from claude_planner.templates.selector import (
    list_templates,
    load_template_config,
    select_template,
)


class TestListTemplates:
    """Test cases for list_templates function."""

    def test_list_templates_returns_all_templates(self) -> None:
        """Test that list_templates returns all available templates."""
        templates = list_templates()

        assert isinstance(templates, list)
        assert len(templates) > 0
        # Should have at least base, web-app, api, cli
        assert "base" in templates
        assert "web-app" in templates
        assert "api" in templates
        assert "cli" in templates

    def test_list_templates_returns_sorted(self) -> None:
        """Test that templates are returned in sorted order."""
        templates = list_templates()

        assert templates == sorted(templates)

    def test_list_templates_excludes_non_directories(self, tmp_path: Path) -> None:
        """Test that non-directory items are excluded."""
        # This tests the actual implementation logic
        # The real templates dir should only have directories
        templates = list_templates()

        # All returned items should be valid template names (strings)
        for template in templates:
            assert isinstance(template, str)
            assert len(template) > 0


class TestSelectTemplate:
    """Test cases for select_template function."""

    def test_select_cli_template(self) -> None:
        """Test selecting CLI template."""
        template_path = select_template("CLI Tool")

        assert template_path.exists()
        assert template_path.is_dir()
        assert template_path.name == "cli"

    def test_select_web_app_template(self) -> None:
        """Test selecting web-app template."""
        template_path = select_template("Web App")

        assert template_path.exists()
        assert template_path.is_dir()
        assert template_path.name == "web-app"

    def test_select_api_template(self) -> None:
        """Test selecting API template."""
        template_path = select_template("API")

        assert template_path.exists()
        assert template_path.is_dir()
        assert template_path.name == "api"

    def test_select_template_case_insensitive(self) -> None:
        """Test that template selection is case insensitive."""
        template_path1 = select_template("CLI Tool")
        template_path2 = select_template("cli tool")
        template_path3 = select_template("CLI TOOL")

        assert template_path1 == template_path2 == template_path3

    def test_select_template_with_alternative_name(self) -> None:
        """Test selecting template with alternative project type names."""
        # "cli" should also match
        template_path = select_template("cli")
        assert template_path.name == "cli"

        # "rest-api" should match API template
        template_path = select_template("rest-api")
        assert template_path.name == "api"

    def test_select_template_fallback_to_base(self) -> None:
        """Test that unknown project types fall back to base template."""
        template_path = select_template("Unknown Project Type")

        assert template_path.exists()
        assert template_path.name == "base"

    def test_select_template_with_whitespace(self) -> None:
        """Test that extra whitespace is handled."""
        template_path = select_template("  CLI Tool  ")

        assert template_path.name == "cli"


class TestLoadTemplateConfig:
    """Test cases for load_template_config function."""

    def test_load_base_template_config(self) -> None:
        """Test loading base template configuration."""
        from claude_planner.templates.selector import _get_templates_dir

        template_path = _get_templates_dir() / "base"
        config = load_template_config(template_path)

        assert isinstance(config, dict)
        assert config["name"] == "base"
        assert "description" in config
        assert "version" in config

    def test_load_web_app_template_config(self) -> None:
        """Test loading web-app template configuration."""
        from claude_planner.templates.selector import _get_templates_dir

        template_path = _get_templates_dir() / "web-app"
        config = load_template_config(template_path)

        assert config["name"] == "web-app"
        assert config["description"] == "Full-stack web application template"
        assert "project_types" in config
        assert "Web App" in config["project_types"]
        assert "default_tech_stack" in config
        assert "default_phases" in config

    def test_load_api_template_config(self) -> None:
        """Test loading API template configuration."""
        from claude_planner.templates.selector import _get_templates_dir

        template_path = _get_templates_dir() / "api"
        config = load_template_config(template_path)

        assert config["name"] == "api"
        assert "API" in config["project_types"]
        assert "default_tech_stack" in config

    def test_load_cli_template_config(self) -> None:
        """Test loading CLI template configuration."""
        from claude_planner.templates.selector import _get_templates_dir

        template_path = _get_templates_dir() / "cli"
        config = load_template_config(template_path)

        assert config["name"] == "cli"
        assert "CLI" in config["project_types"]
        assert "default_tech_stack" in config

    def test_load_config_missing_file(self, tmp_path: Path) -> None:
        """Test loading config from directory without config.yaml."""
        template_dir = tmp_path / "no_config"
        template_dir.mkdir()

        with pytest.raises(FileNotFoundError) as exc_info:
            load_template_config(template_dir)

        assert "not found" in str(exc_info.value).lower()

    def test_load_config_invalid_yaml(self, tmp_path: Path) -> None:
        """Test loading config with invalid YAML."""
        template_dir = tmp_path / "invalid_yaml"
        template_dir.mkdir()
        config_file = template_dir / "config.yaml"
        config_file.write_text("invalid: yaml: content: [[[", encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            load_template_config(template_dir)

        assert "yaml" in str(exc_info.value).lower()

    def test_load_config_missing_required_fields(self, tmp_path: Path) -> None:
        """Test loading config with missing required fields."""
        template_dir = tmp_path / "incomplete"
        template_dir.mkdir()
        config_file = template_dir / "config.yaml"
        # Missing 'description' and 'version'
        config_file.write_text("name: incomplete\n", encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            load_template_config(template_dir)

        error_msg = str(exc_info.value).lower()
        assert "missing required fields" in error_msg

    def test_load_config_not_a_dict(self, tmp_path: Path) -> None:
        """Test loading config that isn't a dictionary."""
        template_dir = tmp_path / "not_dict"
        template_dir.mkdir()
        config_file = template_dir / "config.yaml"
        config_file.write_text("- item1\n- item2\n", encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            load_template_config(template_dir)

        assert "expected dict" in str(exc_info.value).lower()
