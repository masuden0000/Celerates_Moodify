"""
Debugging utils untuk integrasi dengan Streamlit UI
"""

from typing import Optional

import streamlit as st

from src.core.ai_agent import run_agent_with_debug, toggle_debug_mode
from src.core.debug_logger import LogEntry, LogLevel, LogType, debug_logger


class StreamlitDebugPanel:
    """Debug panel untuk Streamlit"""

    def __init__(self):
        self.enabled = False

    def render_debug_controls(self):
        """Render debug controls in sidebar"""
        with st.sidebar:
            st.subheader("🔧 Debug Controls")

            # Toggle debug mode
            if st.button("Toggle Debug Mode"):
                result = toggle_debug_mode()
                st.success(result)

            # Show current status
            status = "ENABLED" if debug_logger.enable_terminal_output else "DISABLED"
            st.write(f"Status: **{status}**")

            # Clear logs button
            if st.button("Clear Debug Logs"):
                debug_logger.clear_logs()
                st.success("🧹 Debug logs cleared")

            # Show log count
            st.write(f"Total Logs: **{len(debug_logger.logs)}**")

    def render_debug_panel(self):
        """Render main debug panel"""
        if not debug_logger.logs:
            st.info("No debug logs yet. Start chatting to see logs!")
            return

        st.subheader("🔍 Debug Logs")

        # Filter controls
        col1, col2 = st.columns(2)

        with col1:
            log_types = st.multiselect(
                "Filter by Type",
                options=[lt.value for lt in LogType],
                default=[lt.value for lt in LogType],
            )

        with col2:
            log_levels = st.multiselect(
                "Filter by Level",
                options=[ll.value for ll in LogLevel],
                default=[ll.value for ll in LogLevel],
            )

        # Filter logs
        filtered_logs = [
            log
            for log in debug_logger.logs
            if log.log_type.value in log_types and log.level.value in log_levels
        ]

        if not filtered_logs:
            st.warning("No logs match the current filters")
            return

        # Display logs
        for i, log in enumerate(reversed(filtered_logs[-20:])):  # Show last 20 logs
            self._render_log_entry(log, i)

    def _render_log_entry(self, log: LogEntry, index: int):
        """Render individual log entry"""
        # Determine colors based on type and level
        type_colors = {
            LogType.USER_INPUT: "🙋",
            LogType.LLM_PROCESSING: "🧠",
            LogType.TOOL_CALL: "🔧",
            LogType.TOOL_RESPONSE: "⚡",
            LogType.AGENT_THINKING: "💭",
            LogType.FINAL_OUTPUT: "✅",
            LogType.ERROR: "❌",
            LogType.SYSTEM: "⚙️",
        }

        level_colors = {
            LogLevel.DEBUG: "blue",
            LogLevel.INFO: "green",
            LogLevel.WARNING: "orange",
            LogLevel.ERROR: "red",
            LogLevel.CRITICAL: "red",
        }

        icon = type_colors.get(log.log_type, "📋")
        color = level_colors.get(log.level, "gray")

        with st.expander(
            f"{icon} [{log.timestamp}] {log.log_type.value} - {log.message}"
        ):
            # Basic info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Level:** {log.level.value}")
            with col2:
                st.write(f"**Type:** {log.log_type.value}")
            with col3:
                if log.duration:
                    duration_str = (
                        f"{log.duration*1000:.1f}ms"
                        if log.duration < 1
                        else f"{log.duration:.2f}s"
                    )
                    st.write(f"**Duration:** {duration_str}")

            # Tool info
            if log.tool_name:
                st.write(f"**Tool:** {log.tool_name}")

            # Data
            if log.data:
                st.write("**Data:**")
                for key, value in log.data.items():
                    if isinstance(value, str) and len(value) > 200:
                        with st.expander(f"{key} (truncated)"):
                            st.code(value)
                    else:
                        st.write(f"- **{key}:** {value}")

            # Error
            if log.error:
                st.error("**Error Details:**")
                st.code(log.error)

    def render_summary(self):
        """Render debug summary"""
        if not debug_logger.logs:
            st.info("No logs to summarize")
            return

        st.subheader("📊 Debug Summary")

        # Count by type
        type_counts = {}
        tool_counts = {}
        total_duration = 0
        error_count = 0

        for log in debug_logger.logs:
            # Count by type
            type_counts[log.log_type] = type_counts.get(log.log_type, 0) + 1

            # Count tools
            if log.tool_name:
                tool_counts[log.tool_name] = tool_counts.get(log.tool_name, 0) + 1

            # Sum durations
            if log.duration:
                total_duration += log.duration

            # Count errors
            if log.level == LogLevel.ERROR:
                error_count += 1

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Logs", len(debug_logger.logs))

        with col2:
            st.metric("Total Duration", f"{total_duration:.2f}s")

        with col3:
            st.metric("Tool Calls", sum(tool_counts.values()))

        with col4:
            st.metric("Errors", error_count)

        # Charts
        if type_counts:
            st.subheader("Log Distribution")
            type_data = {t.value: count for t, count in type_counts.items()}
            st.bar_chart(type_data)

        if tool_counts:
            st.subheader("Tool Usage")
            st.bar_chart(tool_counts)


def create_streamlit_debug_panel() -> StreamlitDebugPanel:
    """Factory function untuk membuat debug panel"""
    return StreamlitDebugPanel()


def run_chat_with_debug(agent, user_input: str, enable_debug: bool = True) -> str:
    """
    Run chat dengan debug logging untuk Streamlit

    Args:
        agent: LangChain agent
        user_input: User input
        enable_debug: Enable debug mode

    Returns:
        Agent response
    """
    return run_agent_with_debug(agent, user_input, enable_debug)


# Streamlit component untuk debug panel
def debug_sidebar():
    """Render debug controls in sidebar"""
    panel = create_streamlit_debug_panel()
    panel.render_debug_controls()
    return panel


def debug_main_panel():
    """Render main debug panel"""
    panel = create_streamlit_debug_panel()

    tab1, tab2 = st.tabs(["📋 Debug Logs", "📊 Summary"])

    with tab1:
        panel.render_debug_panel()

    with tab2:
        panel.render_summary()

    return panel
