"""Building an AI agent from first principles.

Kept deliberately free of imports: `config`, `tools`, and `agent` import each
other, and pulling them in here would create a circular import. Import from
the submodules directly:

    from ai_agent_learning.agent import build_agent
    from ai_agent_learning.tools import build_tools
"""

__version__ = "0.1.0"
