"""
Prompt construction for grounded generation.
"""


def build_grounded_prompt(
    question_task: str,
    context: str,
) -> str:
    """
    Build a prompt that requires generation to stay grounded
    in the supplied source context.
    """

    return f"""
You are generating content for a competency assessment system.

Use ONLY the supplied source context.

Do not invent facts, sources, citations, or answers that are
not supported by the context.

SOURCE CONTEXT:
{context}

TASK:
{question_task}

Return a concise, evidence-grounded response.
""".strip()