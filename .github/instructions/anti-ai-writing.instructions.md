---
description: "Use when writing any user-facing text, copy, documentation, README, commit messages, code comments, or replies. Avoids typical AI-sounding phrases, filler, and boilerplate so the project reads as human-written."
applyTo: "**"
---
# Anti-AI writing

## Avoid AI-sounding phrases

- No openers like "Certainly!", "Sure!", "Great question", "I'd be happy to", "Here's a...", "Let's dive in", "In today's fast-paced world".
- No closers like "I hope this helps", "Feel free to reach out", "Let me know if you have any questions", "In conclusion", "Overall,".
- No marketing filler: "seamless", "robust", "powerful", "cutting-edge", "game-changing", "revolutionize", "unlock", "elevate", "leverage", "empower", "delve", "tapestry", "landscape", "realm", "journey", "testament", "navigate the complexities".
- No empty hedging or praise: "It's important to note that", "It's worth mentioning", "Ultimately", "Remember that".
- No "not just X, but Y" or "more than just..." constructions, and no rule-of-three lists used for rhythm only.
- Avoid overuse of em dashes, emoji, bold, and bullet lists where plain sentences work.

## Write like a person

- Be specific and concrete; state facts, numbers, and names instead of vague claims.
- Use short, direct sentences; vary length; use plain words ("use", not "utilize").
- Say what the product does, not how amazing it is; no self-praise.
- Match the project's voice and the audience; do not sound like a template.
- Use real content, never lorem ipsum, "John Doe", or "Acme Inc." placeholders in final output.

## Code, comments, and commits

- Comment only the non-obvious why; never narrate what the code does ("// Initialize the state", "// Loop through items").
- No leftover AI artifacts: "Here is the updated code", "TODO: implement", "as an AI", or explanatory notes inside files.
- Commit messages: short imperative subject saying what changed ("Fix cart total rounding"), no fluff, no emoji, no long summaries.
- Name things plainly; avoid generic names such as `helper`, `utils2`, `handleData`, `myFunction`.
- Error and log messages state the problem and the cause, not apologies ("Oops! Something went wrong").

## UI copy

- Buttons and labels: short verbs ("Save", "Sign in"), no "Get started today!" style slogans.
- Empty states and errors: say what happened and what to do next, in one or two plain sentences.
- Headlines: one concrete claim; no generic taglines such as "Your all-in-one solution".

## Replies to the user

- Lead with the result; keep it short; no preamble, no recap of the question, no offers for more help.
- Report what changed and what was verified; do not claim success without evidence.
- Use the `no-ai-design-slop` and `audit-ai-design-slop` skills for visual slop; this file covers text.
- For Russian text, also follow the Russian instructions: no calques or machine-translation phrasing ("Давайте погрузимся", "В современном мире", "Безусловно!", "Надеюсь, это поможет").
