# Module Summary: LLM Assisted Coding for a Factorial Function

## Overview
This module demonstrates a highly efficient, practical workflow for collaborating with a Large Language Model (LLM) (`gpt-5-mini` via the `litellm` library) to automate both core algorithm development and robust quality assurance validation.

## Key Takeaways
*   **Prompt Architecture:** Splitting context into structural roles (`SYSTEM_PROMPT`) and execution requirements (`USER_PROMPT`) guarantees clean, deterministic code outputs without unnecessary prose.
*   **Self-Checking & Validation:** Initial implementation validation via manual unit targets should be immediately escalated to automated unit test frameworks.
*   **Target Edge Cases:** Production-ready LLM-assisted code must explicitly account for typical engineering boundary conditions (e.g., zero value states, improper data types, and negative integer inputs).

## Execution Workflow
1.  **Environment Setup:** Configuration of API endpoints and checking for specialized base URLs (e.g., Vocareum detection).
2.  **Code Generation:** Prompting the LLM for a clean recursive factorial implementation with typing protection.
3.  **Smoke Testing:** Immediate sanity check against expected outcomes ($5! = 120$).
4.  **Test Automation:** Prompting the LLM to write a `unittest.TestCase` suite covering positive, zero, and exception-raising scenarios.
5.  **Validation Execution:** Programmatically triggering `unittest.main()` to finalize verification.