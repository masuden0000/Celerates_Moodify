import re


def clean_agent_response(response: str) -> str:
    """
    Membersihkan response dari semua debugging output
    """
    # Hapus semua pattern debugging LangChain
    patterns_to_remove = [
        r"Thought:.*?(?=\n|$)",
        r"Do I need to use a tool\?.*?(?=\n|$)",
        r"Action:.*?(?=\n|$)",
        r"Action Input:.*?(?=\n|$)",
        r"Observation:.*?(?=\n|$)",
        r"Final Answer:.*?(?=\n|$)",
        r"I need to.*?(?=\n|$)",
        r"Let me.*?(?=\n|$)",
        r"I should.*?(?=\n|$)",
    ]

    cleaned = response

    # Remove all debugging patterns
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)

    # Clean up whitespace
    cleaned = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned)  # Max 2 newlines
    cleaned = re.sub(r"^\s+|\s+$", "", cleaned)  # Trim start/end

    # Jika response masih kosong atau hanya debugging, return fallback
    if not cleaned or len(cleaned.strip()) < 10:
        return "Maaf, ada masalah dengan response. Coba input lagi ya! 😅"

    return cleaned


def extract_final_answer(response: str) -> str:
    """
    Extract only the final answer part from agent response
    """
    # Cari pattern "Final Answer:" dan ambil setelahnya
    final_answer_match = re.search(
        r"Final Answer:\s*(.*)", response, re.DOTALL | re.IGNORECASE
    )

    if final_answer_match:
        return final_answer_match.group(1).strip()

    # Jika tidak ada Final Answer, clean response biasa
    return clean_agent_response(response)
