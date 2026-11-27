Question: Determine if llm prefers specific or general purpose tools

Make 5 or so arithmetic functions 
Tools are python functions:

Def arithmeticN(a, b, string: op) 
With
Op = (“add”, “sub”, etc.) 

Arithmetic1 does only addition 
Arithmetic2 addition, subtraction 
ArithmeticN can do all N operands 

Make function name unspecific on purpose. This is to ensure it chooses based on the content not based on the name. 

Hypothesis:
Work step by step and add more if needed.
H1: The LLM prefers using specific tools.
H2: The previous tool usage influences the next tool choice. 
((H3 (maybe adjust research question): Name of tool influences choice.))

Metrik:
ratio between specific and general tool choice. 


Experiments:
Setup: LLM is given all N tools at its disposal. Keep the tool description similar. in system prompt say to only use the tool for arithmetic problems. 
1k (or smth) prompts of form “what is a + b?”, 
→ evaluate percentage of usage per tool including no-tool (N+1 cases)

Compare to prompts of form “what is a+b/c”, 
→ does use of general tool (for “/c”) influence tool choice (for “a+b”)
((What about “a/b+c”?,
→ Does order matter? ))

((Change specific-tool function name to “addition” - does usage increase?)) 
