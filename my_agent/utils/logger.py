"""
Logging and Observability for MAPIS
"""
import structlog
import logging
import time
from functools import wraps
from typing import Callable, Any, Dict

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


def log_agent_execution(agent_name: str):
    """Decorator to log agent execution with timing"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Agent {agent_name} started", agent=agent_name)
            try:
                result = await func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(
                    f"Agent {agent_name} completed",
                    agent=agent_name,
                    duration_seconds=elapsed,
                    status="success"
                )
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"Agent {agent_name} failed",
                    agent=agent_name,
                    duration_seconds=elapsed,
                    status="error",
                    error=str(e)
                )
                raise
        return wrapper
    return decorator


def log_tool_usage(tool_name: str, params: Dict[str, Any] = None):
    """Log tool usage"""
    logger.info(f"Tool {tool_name} used", tool=tool_name, params=params or {})

