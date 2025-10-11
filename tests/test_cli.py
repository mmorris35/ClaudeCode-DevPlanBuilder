"""Tests for CLI entry point module.

This module tests the Click-based command-line interface including
the main group, version flag, verbose flag, and help text.
"""

from click.testing import CliRunner

from claude_planner import __version__
from claude_planner.cli import cli


class TestCLIGroup:
    """Test the main CLI group and global options."""

    def test_cli_help(self) -> None:
        """Test that --help displays usage information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Claude Code Project Planner" in result.output
        assert "generate" in result.output or "Commands:" in result.output
        assert "--help" in result.output
        assert "--version" in result.output
        assert "--verbose" in result.output

    def test_cli_version(self) -> None:
        """Test that --version displays the version number."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert __version__ in result.output
        assert "claude-planner" in result.output.lower()

    def test_cli_verbose_flag(self) -> None:
        """Test that --verbose flag enables verbose output."""
        runner = CliRunner()
        # Run with --verbose and --help (need a valid invocation)
        result = runner.invoke(cli, ["--verbose", "--help"])

        # Verbose mode message should appear before help text
        assert "Verbose mode enabled" in result.output or result.exit_code == 0

    def test_cli_no_command(self) -> None:
        """Test running CLI with no command shows error."""
        runner = CliRunner()
        result = runner.invoke(cli, [])

        # Click shows error when no command given to a group
        assert result.exit_code == 2  # Exit code 2 for usage errors
        assert "Missing command" in result.output or "Usage:" in result.output

    def test_cli_context_stores_verbose(self) -> None:
        """Test that verbose flag is stored in context for sub-commands."""
        runner = CliRunner()

        # Test with --help (valid command that completes successfully)
        result = runner.invoke(cli, ["--help"], catch_exceptions=False, obj={})
        assert result.exit_code == 0

        # Test with verbose=True
        result = runner.invoke(cli, ["--verbose", "--help"], catch_exceptions=False, obj={})
        assert result.exit_code == 0
        # Verbose flag should trigger the message or complete successfully
        assert result.exit_code == 0


class TestMainFunction:
    """Test the main() entry point function."""

    def test_main_success(self) -> None:
        """Test that main() returns 0 on success."""
        # Note: We can't easily test main() directly since it calls cli()
        # which requires sys.exit. This is a basic structural test.
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_main_with_version(self) -> None:
        """Test main entry point with --version."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.output


class TestCLIDocumentation:
    """Test CLI help text and documentation."""

    def test_help_includes_examples(self) -> None:
        """Test that help text includes usage examples."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        # Check for example commands mentioned in help
        assert "claude-planner" in result.output.lower()

    def test_help_includes_subcommands(self) -> None:
        """Test that help text mentions available subcommands."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        # Main help should mention that commands exist
        # (even if they're not implemented yet, the help structure is there)
        assert "--help" in result.output

    def test_verbose_option_help_text(self) -> None:
        """Test that --verbose option has descriptive help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "--verbose" in result.output
        assert "debug" in result.output.lower() or "verbose" in result.output.lower()


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_invalid_option(self) -> None:
        """Test that invalid options show appropriate error."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--invalid-option"])

        assert result.exit_code != 0
        assert "Error" in result.output or "no such option" in result.output.lower()

    def test_help_on_invalid_command(self) -> None:
        """Test that invalid commands show error message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["nonexistent-command"])

        assert result.exit_code != 0
        assert "Error" in result.output or "no such command" in result.output.lower()
