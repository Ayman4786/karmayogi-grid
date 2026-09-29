"""
Grounded RAG pipeline.

Retrieves relevant documents and builds a grounded context
for downstream LLM generation.

The pipeline does not invent source content.
"""

from ai.retrieval.hybrid_search import hybrid_search


def build_rag_context(
    query: str,
    documents: list[dict],
    top_k: int = 3,
) -> dict:
    """
    Retrieve relevant documents and build grounded context.
    """

    results = hybrid_search(
        query=query,
        documents=documents,
        top_k=top_k,
    )

    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"[SOURCE {index}]\n"
            f"ID: {result.get('id', 'UNKNOWN')}\n"
            f"CONTENT: {result.get('text', '')}\n"
        )

    context = "\n".join(context_parts)

    return {
        "query": query,
        "sources": results,
        "context": context,
        "grounded": len(results) > 0,
    }