"""
Custom callback handler untuk debugging LangChain agent
"""

import time
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import AgentAction, AgentFinish, LLMResult

    from src.core.debug_logger import (
        LogLevel,
        LogType,
        debug_logger,
        log_agent_thinking,
        log_error,
        log_final_output,
        log_llm_start,
        log_system,
        log_tool_call,
        log_tool_response,
    )

    class MoodifyDebugCallbackHandler(BaseCallbackHandler):
        """Custom callback handler untuk debugging proses agent"""

        def __init__(self):
            super().__init__()
            self.tool_start_times = {}
            self.llm_start_time = None
            self.agent_start_time = None
            self.current_run_id = None

        def on_agent_action(
            self, action: AgentAction, *, run_id: UUID, **kwargs: Any
        ) -> Any:
            """Called when agent decides to take an action"""
            tool_name = action.tool
            tool_input = action.tool_input

            debug_logger.log(
                LogLevel.INFO,
                LogType.AGENT_THINKING,
                f"Agent memutuskan untuk menggunakan tool: {tool_name}",
                data={
                    "tool": tool_name,
                    "input": str(tool_input),
                    "reasoning": action.log,
                },
            )

            # Store start time for this tool call
            self.tool_start_times[str(run_id)] = time.time()

        def on_agent_finish(
            self, finish: AgentFinish, *, run_id: UUID, **kwargs: Any
        ) -> Any:
            """Called when agent finishes"""
            total_duration = (
                time.time() - self.agent_start_time if self.agent_start_time else 0
            )

            debug_logger.log(
                LogLevel.INFO,
                LogType.FINAL_OUTPUT,
                "Agent selesai memproses dan memberikan jawaban final",
                data={
                    "output": finish.return_values.get("output", ""),
                    "log": finish.log,
                },
                duration=total_duration,
            )

        def on_llm_start(
            self,
            serialized: Dict[str, Any],
            prompts: List[str],
            *,
            run_id: UUID,
            **kwargs: Any,
        ) -> Any:
            """Called when LLM starts"""
            self.llm_start_time = time.time()

            if not self.agent_start_time:
                self.agent_start_time = time.time()

            # Log the full prompt being sent to LLM
            full_prompt = prompts[0] if prompts else ""

            debug_logger.log(
                LogLevel.INFO,
                LogType.LLM_PROCESSING,
                "LLM mulai memproses prompt",
                data={
                    "model": serialized.get("name", "unknown"),
                    "prompt_length": len(full_prompt),
                    "prompt_preview": (
                        full_prompt[:500] + "..."
                        if len(full_prompt) > 500
                        else full_prompt
                    ),
                },
            )

        def on_llm_end(
            self, response: LLMResult, *, run_id: UUID, **kwargs: Any
        ) -> Any:
            """Called when LLM ends"""
            duration = time.time() - self.llm_start_time if self.llm_start_time else 0

            # Get the response text
            response_text = ""
            if response.generations and response.generations[0]:
                response_text = response.generations[0][0].text

            debug_logger.log(
                LogLevel.INFO,
                LogType.LLM_PROCESSING,
                "LLM selesai memproses",
                data={
                    "response_length": len(response_text),
                    "response_preview": (
                        response_text[:300] + "..."
                        if len(response_text) > 300
                        else response_text
                    ),
                    "token_usage": (
                        response.llm_output.get("token_usage", {})
                        if response.llm_output
                        else {}
                    ),
                },
                duration=duration,
            )

        def on_tool_start(
            self,
            serialized: Dict[str, Any],
            input_str: str,
            *,
            run_id: UUID,
            **kwargs: Any,
        ) -> Any:
            """Called when tool starts"""
            tool_name = serialized.get("name", "unknown_tool")

            debug_logger.log(
                LogLevel.INFO,
                LogType.TOOL_CALL,
                f"Mulai eksekusi tool: {tool_name}",
                data={"input": input_str},
                tool_name=tool_name,
            )

            self.tool_start_times[str(run_id)] = time.time()

        def on_tool_end(self, output: str, *, run_id: UUID, **kwargs: Any) -> Any:
            """Called when tool ends"""
            duration = time.time() - self.tool_start_times.get(str(run_id), time.time())

            debug_logger.log(
                LogLevel.INFO,
                LogType.TOOL_RESPONSE,
                "Tool selesai dieksekusi",
                data={
                    "output_length": len(output),
                    "output_preview": (
                        output[:300] + "..." if len(output) > 300 else output
                    ),
                },
                duration=duration,
            )

            # Clean up
            if str(run_id) in self.tool_start_times:
                del self.tool_start_times[str(run_id)]

        def on_tool_error(
            self,
            error: Union[Exception, KeyboardInterrupt],
            *,
            run_id: UUID,
            **kwargs: Any,
        ) -> Any:
            """Called when tool encounters an error"""
            debug_logger.log(
                LogLevel.ERROR,
                LogType.ERROR,
                f"Tool error occurred",
                data={"error_type": type(error).__name__, "error_message": str(error)},
                error=str(error),
            )

        def on_llm_error(
            self,
            error: Union[Exception, KeyboardInterrupt],
            *,
            run_id: UUID,
            **kwargs: Any,
        ) -> Any:
            """Called when LLM encounters an error"""
            debug_logger.log(
                LogLevel.ERROR,
                LogType.ERROR,
                f"LLM error occurred",
                data={"error_type": type(error).__name__, "error_message": str(error)},
                error=str(error),
            )

        def on_chain_start(
            self,
            serialized: Dict[str, Any],
            inputs: Dict[str, Any],
            *,
            run_id: UUID,
            **kwargs: Any,
        ) -> Any:
            """Called when chain starts"""
            chain_name = serialized.get("name", "unknown_chain")

            if chain_name == "AgentExecutor":
                self.agent_start_time = time.time()

                debug_logger.log(
                    LogLevel.INFO,
                    LogType.SYSTEM,
                    "Agent executor dimulai",
                    data={"inputs": inputs},
                )

        def on_chain_end(
            self, outputs: Dict[str, Any], *, run_id: UUID, **kwargs: Any
        ) -> Any:
            """Called when chain ends"""
            duration = (
                time.time() - self.agent_start_time if self.agent_start_time else 0
            )

            debug_logger.log(
                LogLevel.INFO,
                LogType.SYSTEM,
                "Agent executor selesai",
                data={"outputs": outputs},
                duration=duration,
            )

        def on_chain_error(
            self,
            error: Union[Exception, KeyboardInterrupt],
            *,
            run_id: UUID,
            **kwargs: Any,
        ) -> Any:
            """Called when chain encounters an error"""
            debug_logger.log(
                LogLevel.ERROR,
                LogType.ERROR,
                f"Chain error occurred",
                data={"error_type": type(error).__name__, "error_message": str(error)},
                error=str(error),
            )

        def on_text(self, text: str, *, run_id: UUID, **kwargs: Any) -> Any:
            """Called when agent produces intermediate text"""
            if text.strip():
                debug_logger.log(
                    LogLevel.DEBUG,
                    LogType.AGENT_THINKING,
                    "Agent intermediate text",
                    data={"text": text.strip()},
                )

except ImportError as e:
    # Fallback jika LangChain tidak tersedia
    class MoodifyDebugCallbackHandler:
        def __init__(self):
            print("⚠️ LangChain tidak tersedia, debug callback tidak aktif")
            log_error(e, "LangChain import failed")

    def create_debug_callback():
        return None


def create_debug_callback():
    """Factory function untuk membuat debug callback"""
    try:
        return MoodifyDebugCallbackHandler()
    except Exception as e:
        log_error(e, "Failed to create debug callback")
        return None
