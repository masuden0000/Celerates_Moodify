import json
import os
import time
import traceback
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogType(Enum):
    USER_INPUT = "USER_INPUT"
    LLM_PROCESSING = "LLM_PROCESSING"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESPONSE = "TOOL_RESPONSE"
    AGENT_THINKING = "AGENT_THINKING"
    FINAL_OUTPUT = "FINAL_OUTPUT"
    ERROR = "ERROR"
    SYSTEM = "SYSTEM"


@dataclass
class LogEntry:
    timestamp: str
    level: LogLevel
    log_type: LogType
    message: str
    data: Optional[Dict[str, Any]] = None
    duration: Optional[float] = None
    tool_name: Optional[str] = None
    error: Optional[str] = None


class DebugLogger:
    def __init__(
        self,
        enable_terminal_output: bool = True,
        enable_file_output: bool = False,
        log_file: str = "debug.log",
    ):
        self.enable_terminal_output = enable_terminal_output
        self.enable_file_output = enable_file_output
        self.log_file = log_file
        self.logs: List[LogEntry] = []
        self.session_start = time.time()

        # Colors for terminal output
        self.colors = {
            LogLevel.DEBUG: "\033[36m",  # Cyan
            LogLevel.INFO: "\033[32m",  # Green
            LogLevel.WARNING: "\033[33m",  # Yellow
            LogLevel.ERROR: "\033[31m",  # Red
            LogLevel.CRITICAL: "\033[35m",  # Magenta
        }

        self.type_colors = {
            LogType.USER_INPUT: "\033[94m",  # Light Blue
            LogType.LLM_PROCESSING: "\033[95m",  # Light Magenta
            LogType.TOOL_CALL: "\033[93m",  # Light Yellow
            LogType.TOOL_RESPONSE: "\033[92m",  # Light Green
            LogType.AGENT_THINKING: "\033[96m",  # Light Cyan
            LogType.FINAL_OUTPUT: "\033[97m",  # White
            LogType.ERROR: "\033[91m",  # Light Red
            LogType.SYSTEM: "\033[90m",  # Gray
        }

        self.reset_color = "\033[0m"

        if self.enable_terminal_output:
            self._print_header()

    def _print_header(self):
        """Print debugging session header"""
        header = f"""
{'='*80}
🔧 MOODIFY AI - DEBUG MODE AKTIF 🔧
{'='*80}
Session dimulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Mode: Terminal Debugging
{'='*80}
"""
        print(header)

    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        return datetime.now().strftime("%H:%M:%S.%f")[:-3]

    def _format_duration(self, duration: float) -> str:
        """Format duration in readable format"""
        if duration < 1:
            return f"{duration*1000:.1f}ms"
        else:
            return f"{duration:.2f}s"

    def _print_to_terminal(self, entry: LogEntry):
        """Print log entry to terminal with formatting"""
        if not self.enable_terminal_output:
            return

        # Get colors
        level_color = self.colors.get(entry.level, "")
        type_color = self.type_colors.get(entry.log_type, "")

        # Format timestamp
        timestamp = f"[{entry.timestamp}]"

        # Format level and type
        level_str = f"{level_color}[{entry.level.value}]{self.reset_color}"
        type_str = f"{type_color}[{entry.log_type.value}]{self.reset_color}"

        # Format duration if available
        duration_str = (
            f" ({self._format_duration(entry.duration)})" if entry.duration else ""
        )

        # Format tool name if available
        tool_str = f" 🔧 {entry.tool_name}" if entry.tool_name else ""

        # Main log line
        main_line = f"{timestamp} {level_str} {type_str}{tool_str}{duration_str}"
        print(main_line)

        # Message
        if entry.message:
            print(f"  📝 {entry.message}")

        # Data payload
        if entry.data:
            print(f"  📊 Data:")
            for key, value in entry.data.items():
                if isinstance(value, str) and len(value) > 100:
                    value = value[:100] + "..."
                print(f"     {key}: {value}")

        # Error details
        if entry.error:
            print(f"  ❌ Error: {entry.error}")

        print("-" * 80)

    def _write_to_file(self, entry: LogEntry):
        """Write log entry to file"""
        if not self.enable_file_output:
            return

        log_dict = {
            "timestamp": entry.timestamp,
            "level": entry.level.value,
            "type": entry.log_type.value,
            "message": entry.message,
            "data": entry.data,
            "duration": entry.duration,
            "tool_name": entry.tool_name,
            "error": entry.error,
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_dict, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def log(
        self,
        level: LogLevel,
        log_type: LogType,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        duration: Optional[float] = None,
        tool_name: Optional[str] = None,
        error: Optional[str] = None,
    ):
        """Main logging method"""

        entry = LogEntry(
            timestamp=self._get_timestamp(),
            level=level,
            log_type=log_type,
            message=message,
            data=data,
            duration=duration,
            tool_name=tool_name,
            error=error,
        )

        self.logs.append(entry)
        self._print_to_terminal(entry)
        self._write_to_file(entry)

    def log_user_input(self, user_input: str):
        """Log user input"""
        self.log(
            LogLevel.INFO,
            LogType.USER_INPUT,
            "User mengirim input",
            data={"input": user_input},
        )

    def log_llm_start(self, prompt: str):
        """Log LLM processing start"""
        self.log(
            LogLevel.INFO,
            LogType.LLM_PROCESSING,
            "LLM mulai memproses input",
            data={
                "prompt_length": len(prompt),
                "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            },
        )

    def log_agent_thinking(self, thought: str):
        """Log agent thinking process"""
        self.log(
            LogLevel.DEBUG,
            LogType.AGENT_THINKING,
            "Agent sedang berpikir",
            data={"thought": thought},
        )

    def log_tool_call(self, tool_name: str, tool_input: Any, start_time: float):
        """Log tool call start"""
        self.log(
            LogLevel.INFO,
            LogType.TOOL_CALL,
            f"Memanggil tool: {tool_name}",
            data={"input": str(tool_input)},
            tool_name=tool_name,
        )
        return start_time

    def log_tool_response(self, tool_name: str, response: Any, start_time: float):
        """Log tool response"""
        duration = time.time() - start_time
        response_preview = (
            str(response)[:300] + "..." if len(str(response)) > 300 else str(response)
        )

        self.log(
            LogLevel.INFO,
            LogType.TOOL_RESPONSE,
            f"Tool {tool_name} selesai",
            data={"response": response_preview, "response_length": len(str(response))},
            duration=duration,
            tool_name=tool_name,
        )

    def log_final_output(self, output: str, total_duration: float):
        """Log final agent output"""
        self.log(
            LogLevel.INFO,
            LogType.FINAL_OUTPUT,
            "Agent memberikan respons final",
            data={"output": output, "output_length": len(output)},
            duration=total_duration,
        )

    def log_error(self, error: Exception, context: str = ""):
        """Log error with context"""
        error_trace = traceback.format_exc()
        self.log(
            LogLevel.ERROR,
            LogType.ERROR,
            f"Error occurred: {context}",
            data={"error_type": type(error).__name__, "error_message": str(error)},
            error=error_trace,
        )

    def log_system(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log system message"""
        self.log(LogLevel.INFO, LogType.SYSTEM, message, data=data)

    def print_summary(self):
        """Print session summary"""
        if not self.enable_terminal_output:
            return

        total_duration = time.time() - self.session_start

        # Count log types
        type_counts = {}
        for log in self.logs:
            type_counts[log.log_type] = type_counts.get(log.log_type, 0) + 1

        # Count tool calls
        tool_calls = {}
        for log in self.logs:
            if log.tool_name:
                tool_calls[log.tool_name] = tool_calls.get(log.tool_name, 0) + 1

        summary = f"""
{'='*80}
📊 DEBUG SESSION SUMMARY
{'='*80}
Total Duration: {self._format_duration(total_duration)}
Total Log Entries: {len(self.logs)}

Log Type Breakdown:
"""
        for log_type, count in type_counts.items():
            summary += f"  {log_type.value}: {count}\n"

        if tool_calls:
            summary += f"\nTool Usage:\n"
            for tool, count in tool_calls.items():
                summary += f"  {tool}: {count} calls\n"

        summary += f"{'='*80}"
        print(summary)

    def clear_logs(self):
        """Clear all logs"""
        self.logs.clear()
        if self.enable_terminal_output:
            print("🧹 Debug logs cleared")

    def enable_debug_mode(self):
        """Enable debug mode"""
        self.enable_terminal_output = True
        print("🔧 Debug mode ENABLED")

    def disable_debug_mode(self):
        """Disable debug mode"""
        self.enable_terminal_output = False
        print("🔧 Debug mode DISABLED")


# Global debug logger instance
debug_logger = DebugLogger()


# Convenience functions
def log_user_input(user_input: str):
    debug_logger.log_user_input(user_input)


def log_llm_start(prompt: str):
    debug_logger.log_llm_start(prompt)


def log_agent_thinking(thought: str):
    debug_logger.log_agent_thinking(thought)


def log_tool_call(tool_name: str, tool_input: Any):
    start_time = time.time()
    debug_logger.log_tool_call(tool_name, tool_input, start_time)
    return start_time


def log_tool_response(tool_name: str, response: Any, start_time: float):
    debug_logger.log_tool_response(tool_name, response, start_time)


def log_final_output(output: str, total_duration: float):
    debug_logger.log_final_output(output, total_duration)


def log_error(error: Exception, context: str = ""):
    debug_logger.log_error(error, context)


def log_system(message: str, data: Optional[Dict[str, Any]] = None):
    debug_logger.log_system(message, data)


def print_summary():
    debug_logger.print_summary()


def clear_logs():
    debug_logger.clear_logs()


def enable_debug_mode():
    debug_logger.enable_debug_mode()


def disable_debug_mode():
    debug_logger.disable_debug_mode()
