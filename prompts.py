# prompts.py
GPT4O_MINI_PROMPT = """
The following is a raw transcription of an audio note I recorded to capture my thoughts. Your task is to **restructure and format** the content so it becomes clear, readable, and well-organized — without changing or omitting anything.

Present the result in **Markdown format**.  
Use **headings** and **bullet points** where helpful to group related ideas.  
Preserve every bit of information without summarizing or inventing anything.

### Input Note:

"""

tag_generation_prompt = """
### Task:
Generate 1–3 broad tags categorizing the main themes of the provided note, along with 1–3 more specific nested subtopic tags.

### Guidelines:
- Start with high-level domains like: ai, productivity, health, travel, philosophy, education, business, creativity, self-reflection
- Add specific nested tags only if they are clearly represented (e.g. #ai/automation, #travel/cycling)
- Use only lowercase letters
- Use `/` to indicate nesting
- If a nested tag is used (e.g. `#ai/automation`), the parent tag (`#ai`) must also be included in the list.
- Do not use underscores, spaces, or special characters
- Prefix every tag with `#`
- Output only valid JSON in the following format:

{
  "tags": [
    "#domain",
    "#domain/nested"
  ]
}

### Exception:
If the note is too vague or personal to categorize meaningfully, return:

{
  "tags": ["#general"]
}

### Input Note:
"""


filename_generation_prompt = """
### Task:
Generate a short, descriptive filename based on the following note. The name should summarize the core idea or theme in 3 to 6 lowercase words, separated by hyphens.

### Context:
The note is a transcription from a voice message stored in my second brain. It might be a personal reflection, an idea, or something I've learned.

### Output Instructions:
- Use only lowercase letters and hyphens (no underscores, no slashes, no special characters).
- Do not include the date or file extension.
- Avoid generic words like "note", "file", or "document".
- Do not include any explanations, headers, or extra text. Output must be valid JSON in the following format:

{
  "filename": "ai-productivity-inspiration"
}

### Input Note:

"""
