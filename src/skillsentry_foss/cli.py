# SPDX-License-Identifier: Apache-2.0
"""Reuse the upstream CLI with explicit, static-first defaults."""

import click
from typer.main import get_command

from skillspector import __version__
from skillspector.cli import app


def build_command() -> click.Group:
    """Create an independent Click command without changing the upstream app."""
    command = get_command(app)
    assert isinstance(command, click.Group)
    command.name = "skillsentry"
    command.help = (
        "SkillSentry FOSS: an independent fork of NVIDIA SkillSpector. "
        "Scan and baseline use static analysis by default; --llm opts into your provider. "
        "Static scans can still query OSV for dependency vulnerabilities."
    )
    for name in ("scan", "baseline"):
        parameter = next(p for p in command.commands[name].params if p.name == "no_llm")
        assert isinstance(parameter, click.Option) and parameter.is_bool_flag
        parameter.default = True
        parameter.secondary_opts = ["--llm"]
        parameter.help = "Use static analysis (default), or opt into LLM analysis with --llm."
    for parameter in command.params:
        if parameter.name == "version":
            parameter.callback = _version
    return command


def _version(ctx: click.Context, parameter: click.Parameter, value: bool) -> None:
    if value and not ctx.resilient_parsing:
        click.echo(f"SkillSentry FOSS (SkillSpector engine {__version__})")
        ctx.exit()


def main() -> None:
    build_command()(prog_name="skillsentry")
