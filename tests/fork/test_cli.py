# SPDX-License-Identifier: Apache-2.0
"""Verify the fork's opt-in policy and upstream command compatibility."""

from inspect import unwrap

import click
import pytest
from click.testing import CliRunner
from typer.main import get_command

from skillsentry_foss.cli import build_command
from skillspector.cli import app


@pytest.mark.parametrize("name", ["scan", "baseline"])
@pytest.mark.parametrize(
    "options, expected", [([], True), (["--no-llm"], True), (["--llm"], False)]
)
def test_llm_opt_in(name, options, expected):
    command = build_command().commands[name]
    command.callback = lambda **kwargs: click.echo(str(kwargs["no_llm"]))
    result = CliRunner().invoke(command, ["SKILL.md", *options])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == str(expected)


def test_upstream_app_still_defaults_to_llm():
    build_command()
    upstream = get_command(app)
    for name in ("scan", "baseline"):
        parameter = next(p for p in upstream.commands[name].params if p.name == "no_llm")
        assert parameter.default is False
        assert "--llm" not in parameter.secondary_opts


def test_every_upstream_command_and_option_is_retained():
    upstream, fork = get_command(app), build_command()
    assert upstream.commands.keys() == fork.commands.keys()
    for name in upstream.commands:
        original = upstream.commands[name]
        derived = fork.commands[name]
        assert unwrap(original.callback) is unwrap(derived.callback)
        assert [(p.name, p.opts) for p in original.params] == [
            (p.name, p.opts) for p in derived.params
        ]


def test_fork_version_and_help():
    for option, expected in [("--version", "SkillSentry FOSS"), ("--help", "OSV")]:
        result = CliRunner().invoke(build_command(), [option])
        assert result.exit_code == 0, result.output
        assert expected in result.output


def test_explicit_mode_order_matches_click():
    command = build_command().commands["scan"]
    command.callback = lambda **kwargs: click.echo(str(kwargs["no_llm"]))
    result = CliRunner().invoke(command, ["SKILL.md", "--llm", "--no-llm"])
    assert result.exit_code == 0
    assert result.output.strip() == "True"
