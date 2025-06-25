"""
Debug wrapper untuk tools agar bisa dimonitor prosesnya
"""

import time
from functools import wraps
from typing import Any, Callable

from src.core.debug_logger import log_error, log_tool_call, log_tool_response


def debug_tool(tool_name: str):
    """Decorator untuk membuat tool bisa di-debug"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Log tool call start
            start_time = log_tool_call(tool_name, {"args": args, "kwargs": kwargs})

            try:
                # Execute tool
                result = func(*args, **kwargs)

                # Log successful response
                log_tool_response(tool_name, result, start_time)

                return result

            except Exception as e:
                # Log error
                log_error(e, f"Error in tool: {tool_name}")

                # Re-raise the exception
                raise e

        return wrapper

    return decorator


class ToolDebugger:
    """Class untuk debug tool calls secara manual"""

    @staticmethod
    def wrap_function(func: Callable, tool_name: str) -> Callable:
        """Wrap function dengan debugging"""
        return debug_tool(tool_name)(func)

    @staticmethod
    def call_with_debug(func: Callable, tool_name: str, *args, **kwargs) -> Any:
        """Call function dengan debugging manual"""
        start_time = log_tool_call(tool_name, {"args": args, "kwargs": kwargs})

        try:
            result = func(*args, **kwargs)
            log_tool_response(tool_name, result, start_time)
            return result
        except Exception as e:
            log_error(e, f"Error in tool: {tool_name}")
            raise e
