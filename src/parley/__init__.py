"""parley — Dual AI Agent Conversation via MCP Servers (EX06, uoh-sqak).

Two autonomous LLM agents — a Cop and a Thief — play a turn-based chase on a
partially-observable grid, each on its own FastMCP server, conversing in free
natural language, from init through six sub-games to an automated email report.
"""

from parley.shared.version import __version__

__all__ = ["__version__"]
