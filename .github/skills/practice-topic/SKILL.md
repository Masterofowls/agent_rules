---
name: practice-topic
description: "Help a learner practice a topic through exercises, quizzes, code challenges, debugging drills, spaced review, and feedback from beginner to advanced level. Use for quiz me, give me exercises, check my understanding, review my solution, потренироваться, задания, or проверь мои знания."
argument-hint: "Topic, level, and preferred exercise type"
---

# Guided topic practice

## Prepare
- Use the learner's stated topic, level, and goal. If absent, start with a small diagnostic task, not an assumed mastery level.
- Invoke `teach-topic` when a missing concept needs explanation; do not load unrelated implementation skills.
- Choose one exercise at a time with a clear expected outcome. Use prediction, tracing, explanation, implementation, or debugging according to the goal.
- State constraints and success criteria. Coding tasks need meaningful test cases, including relevant edge cases; knowledge questions need an explanation of what a correct answer establishes.

## Feedback loop
1. Present the task without revealing the solution. Collect the learner's response through the host's question tool when available and wait.
2. Assess the actual response against the criteria. Separate correct reasoning, specific mistakes, and missing evidence; do not claim a result was tested unless it was.
3. Offer graduated help: a conceptual cue, a targeted hint, then a partial worked step. Provide the full solution when requested or when the learner chooses it.
4. Explain why a correction works and give one related transfer exercise. Increase difficulty only when the learner demonstrates understanding.

## Beginner through advanced
- Beginner: small examples, explicit inputs and outputs, and no hidden prerequisites.
- Intermediate: combine concepts and test practical edge cases.
- Advanced: ambiguous tradeoffs, counterexamples, failure analysis, performance, and justification of assumptions.
- For review, revisit earlier concepts after intervening tasks and vary examples. Do not promise scheduled reminders or cross-session tracking unless the host supports it and the learner requests it.

## Boundaries
- Preserve the learner's work. Do not silently rewrite a submitted solution or complete an exercise in the repository without permission.
- Keep practice in chat unless files are requested. Never create unsolicited exercise folders, progress reports, or homework documents.
- Do not store learner scores, inferred abilities, or personal learning profiles in persistent memory.
- Finish with concise feedback on demonstrated understanding and the next useful practice step, not an unsupported certificate of mastery.
