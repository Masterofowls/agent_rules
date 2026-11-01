---
name: teach-topic
description: "Teach and explain a selected topic from beginner to advanced level. Use for teach me, help me understand, explain this code, learning plans, prerequisites, deep dives, научи меня, объясни, or помоги разобраться. Adapt explanations to the learner rather than implementing the answer for them."
argument-hint: "Topic, current level, and learning goal"
---

# Teach a topic

## Establish the starting point
- Use the topic, level, goal, language, and time budget already supplied. Do not repeat questions the learner has answered.
- If essential information is missing, ask one focused question through the host's question tool. Otherwise begin with a short explanation and state your assumed level; let the learner adjust it.
- Treat level as topic-specific. Do not infer ability from age, identity, or unrelated experience.
- Teaching is not permission to edit the project. Explain selected code read-only unless edits or exercises in files are requested.

## Teach in small steps
1. State one concrete learning outcome and the prerequisites needed now, not a full textbook syllabus.
2. Explain the core idea in plain language, defining new terms. Use a small, accurate example and show why it works.
3. Connect the example to the learner's goal or selected code. Label analogies as analogies and state where they stop being accurate.
4. Offer a short prediction, explanation, or application check. Ask interactively through the host's question tool and wait for the answer; do not invent a learner response.
5. Correct misconceptions specifically and adjust the next step. Give another explanation when needed rather than repeating the same wording.

## Adjust depth
- Beginner: introduce one concept at a time, trace inputs and outputs, and teach missing prerequisites when they become relevant.
- Intermediate: compare alternatives, explain tradeoffs and common failures, and connect concepts across examples.
- Advanced: examine assumptions, internals, edge cases, complexity, and limits; distinguish guaranteed behavior from implementation details.
- For a direct explanation request, answer directly. Do not force a quiz or Socratic dialogue when the learner asks for the answer.

## Evidence and presentation
- Verify version-sensitive technical claims against the installed version or authoritative sources. Say when uncertain; do not invent citations or execution results.
- Use runnable, minimal examples where appropriate. Execute them only when useful and authorized; otherwise label them as illustrative and untested.
- Keep examples safe and respect deployment, Git, and deletion permissions. Never send project code or learner data to external teaching services.
- Use the requested language; apply the Russian-language skill for Russian text when available.
- End each learning step with a brief summary and one relevant next step. Create lesson files or a long curriculum only when requested.
