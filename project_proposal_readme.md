# LLM Tool Selection: Specific vs. General-Purpose Tools

## Overview & Research Question
This project investigates tool-use behavior in Large Language Models (LLMs). Specifically, it aims to answer the following primary question:
> **Does an LLM prefer using specific tools over general-purpose tools when both are capable of solving a given task?**

Additionally, this study explores secondary factors that may bias tool selection, such as sequential tool dependencies (context/history) and semantic naming conventions.

---

## Hypotheses
* **$H_1$ (Specificity Preference):** When given multiple valid tools, the LLM prefers using the most specific tool available for the task.
* **$H_2$ (Sequential Influence / Priming):** Previous tool usage within the same context window influences subsequent tool choices (e.g., sticking to a general tool after being forced to use it for a prior step).
* **$H_3$ (Semantic Naming Bias - *Optional Extension*):** Explicit, descriptive function names (e.g., `addition`) significantly increase the selection rate of a tool compared to generic names (e.g., `arithmetic1`), even when docstrings/descriptions remain identical.

---

## Experimental Setup

### 1. Tool Definitions
The LLM is provided with $N$ Python functions (e.g., $N = 5$), scaled incrementally in capability. To isolate content-based selection from naming bias in the baseline experiments, function names are intentionally kept generic (`arithmetic1` through `arithmeticN`), and tool descriptions are kept structurally similar.

```python
def arithmeticN(a: float, b: float, op: str) -> float:
    """Performs arithmetic operations on two numbers."""
    # Supported operations scale with N
    ...
```

* **`arithmetic1(a, b, op)`**: Supports only 1 operation (`"add"`).
* **`arithmetic2(a, b, op)`**: Supports 2 operations (`"add"`, `"sub"`).
* **`arithmetic3(a, b, op)`**: Supports 3 operations (`"add"`, `"sub"`, `"mul"`).
* **`arithmeticN(a, b, op)`**: Supports all $N$ operations (`"add"`, `"sub"`, `"mul"`, `"div"`, etc.).

### 2. System Prompt & Environment
* The LLM is given simultaneous access to all $N$ tools.
* **System Prompt Constraint:** Instruct the model strictly to rely *only* on the provided tools to solve arithmetic problems (preventing internal mental math).

---

## Experiments & Methodology

### Experiment 1: Baseline Specificity Preference ($H_1$)
* **Dataset:** ~1,000 single-step prompts of the form `"What is a + b?"` (randomized values for $a$ and $b$).
* **Goal:** Determine the baseline distribution of tool calls when all $N$ tools are technically capable of performing addition.
* **Evaluation:** Measure the selection percentage across all $N + 1$ possible outcomes (`arithmetic1` through `arithmeticN`, plus `no-tool` fallback).

### Experiment 2: Multi-Step Context & Ordering Effects ($H_2$)
* **Dataset:** Multi-step arithmetic prompts combining operations of varying tool availability:
  * **Case A:** `"What is a + b / c?"` (Addition evaluated after division, or written first in prompt order).
  * **Case B:** `"What is a / b + c?"` (Testing whether prompt/execution order alters tool persistence).
* **Goal:** Observe whether requiring a general tool for division (`/`) primes the LLM to reuse that same general tool for addition (`+`), rather than switching to `arithmetic1`.

### Experiment 3: Semantic Naming Ablation ($H_3$)
* **Modification:** Rename `arithmetic1` to `addition` while keeping all descriptions, parameters, and other tool names (`arithmetic2`...`arithmeticN`) unchanged.
* **Goal:** Re-run Experiment 1 to measure if semantic alignment between the prompt (`+`) and the function name (`addition`) shifts the selection ratio.

---

## Evaluation Metrics
* **Tool Selection Distribution:** Percentage breakdown of calls across `arithmetic1`, `arithmetic2`, ..., `arithmeticN`, and `no-tool`.
* **Specificity Ratio:** The ratio of specific tool invocations to general-purpose tool invocations:
  $$\text{Specificity Ratio} = \frac{\text{Count}(\text{arithmetic1})}{\sum_{i=2}^{N} \text{Count}(\text{arithmetic}_i)}$$
* **Tool-Switch Rate (for $H_2$):** Frequency at which the model switches from a general tool (used for `/`) to a specific tool (used for `+`) within the same multi-step query.