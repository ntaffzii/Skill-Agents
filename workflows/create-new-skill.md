# Create New Skill

## Goal

Turn a repeated task into a clean, installable skill with clear metadata and a practical workflow.

## When To Use

Use when the user asks to create, improve, classify, compare, or reorganize skills.

## Skills

- `skill-management`
- `github-skill-research`
- `grill-with-docs`
- `handoff`

## Steps

1. Define the repeated job with `grill-with-docs`.
   - What does the skill help the agent do?
   - When should it trigger?
   - What should the agent avoid?

2. Create the skill with `skill-management`.
   - Use `github-skill-research` first when the user asks to compare against real repositories, 9arm-style skills, or cross-agent workflow patterns.
   - If web-capture tools are available and the skill depends on current public web examples, capture sources through provider-neutral tools and save source URLs.
   - Choose the right bucket.
   - Write `SKILL.md` with `name` and `description`.
   - Keep the body procedural and concise.
   - If docs tools are available, inspect existing README, skill indexes, and related references before adding a new pattern.

3. Add references only when needed.
   - Use `references/` for detailed syntax, examples, or domain docs.
   - Keep `SKILL.md` as the navigation and operating guide.

4. Validate.
   - Confirm metadata is present.
   - Confirm the skill has one main job.
   - Confirm the workflow includes verification.
   - If structured-data tools are available, validate any updated skill or workflow registry JSON.

5. Hand off.
   - Explain how to use the skill and what prompt should trigger it.
   - If memory tools are available, save reusable decisions about when the skill should trigger.

## Output

End with:

- Skill created or updated
- Trigger phrase examples
- Files added
- Validation result
