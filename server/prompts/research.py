def healthcare_research_brief(
    research_question: str,
) -> str:
    """
    Create a structured prompt for synthesizing
    healthcare research evidence.
    """

    return f"""
You are assisting with healthcare research.

Research question:
{research_question}

Use only the research evidence provided by the
connected healthcare research tools.

Produce a structured research brief containing:

1. Research question
2. Key findings
3. Relevant PubMed evidence
4. Relevant clinical trial evidence
5. Areas of agreement
6. Areas of uncertainty or conflicting evidence
7. Limitations
8. Sources requiring further review

Important rules:

- Do not invent research findings.
- Do not claim that evidence proves causation unless
  the retrieved evidence supports that conclusion.
- Clearly distinguish retrieved evidence from
  interpretation.
- Identify when information is unavailable.
- Do not provide individualized medical advice.
- Include identifiers such as PMID and NCT ID whenever
  they are available.
""".strip()
