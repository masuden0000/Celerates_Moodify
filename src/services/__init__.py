# Services package - External services and utilities

from .debug_logger import (
    debug_logger,
    disable_debug_mode,
    enable_debug_mode,
    log_error,
    log_final_output,
    log_llm_start,
    log_system,
    log_user_input,
)
from .lyrics_service import (
    extract_song_from_query,
    is_lyrics_query,
    search_lyrics_with_gemini,
)

__all__ = [
    "search_lyrics_with_gemini",
    "extract_song_from_query",
    "is_lyrics_query",
    "debug_logger",
    "enable_debug_mode",
    "disable_debug_mode",
    "log_error",
    "log_final_output",
    "log_llm_start",
    "log_system",
    "log_user_input",
]
