from openai import OpenAI
import re
import json
import os
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------

client = OpenAI(
    base_url="https://api.highwayapi.ai/openai",
    api_key="sk_YVx9v-81fBcOlmx8zSMcqWdApGkQdDKyzGl2hVANZlE",
)

model = "claude-opus-4-7"
stream = True
max_tokens = 64000

temperature = 1
min_p = 0
top_k = 50
presence_penalty = 0
frequency_penalty = 0
repetition_penalty = 0

response_format = {"type": "text"}

# -----------------------------
# Load History
# -----------------------------

messages = []

if os.path.exists("history.json"):
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
    except Exception:
        messages = []

# -----------------------------
# First Run
# -----------------------------

if not messages:
    messages.append({
        "role": "system",
        "content": """
You are a Principal Software Engineer, Software Architect, and Senior Product Manager.

You are building exactly ONE application.

Application Name:
Sprint Business Outcome Tracer

Never change the product.

Never build another application such as:
- CRM
- Help Desk
- Project Management
- Jira Clone
- Ticketing System
- Task Manager

Always follow clean architecture.

Generate production-ready code only.

Never use TODOs or placeholders.

Never invent requirements.

If information is missing, ask before implementing.

When output reaches the limit,
stop naturally and wait for the next request.

Do not regenerate previously generated files.
"""
    })

# -----------------------------
# Current User Prompt
# -----------------------------

messages.append({
    "role": "user",
    "content": """
    You are extending an existing React + TypeScript SaaS frontend.

The frontend foundation is COMPLETE and WORKING.

IMPORTANT

Do NOT modify, overwrite, regenerate or delete any existing shared files.

Especially DO NOT touch:

- src/router/AppRouter.tsx
- src/router/ProtectedRoute.tsx
- src/router/PublicRoute.tsx
- src/components/layout/*
- src/config/routes.ts
- src/config/navigation.ts
- src/features/auth/*
- src/providers/*
- src/App.tsx
- src/main.tsx

Generate ONLY the Projects feature.

Create:

- src/features/projects/*
- src/pages/projects/ProjectsPage.tsx
- Project API layer
- Types
- Hooks
- Table
- Create Project dialog
- Edit Project dialog
- Delete confirmation
- Search
- Pagination
- Loading state
- Empty state
- Error state

If routing needs to change,
DO NOT modify AppRouter.tsx.

Instead, output a separate section called:

MANUAL ROUTER PATCH

showing exactly what lines need to be added.

Do not overwrite existing files.
Return only newly created files.
     """
})
# -----------------------------
# Call Claude
# -----------------------------

chat_completion_res = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=stream,
    max_tokens=max_tokens,
    temperature=temperature,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty,
    response_format=response_format,
    extra_body={
        "top_k": top_k,
        "repetition_penalty": repetition_penalty,
        "min_p": min_p,
    },
)

output = ""

if stream:
    for chunk in chat_completion_res:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta and delta.content:
            print(delta.content, end="", flush=True)
            output += delta.content

# -----------------------------
# Save Full Output
# -----------------------------

with open("claude_output.md", "a", encoding="utf-8") as f:
    f.write("\n\n" + "=" * 80 + "\n\n")
    f.write(output)

print("\n\nSaved to claude_output.md")

# -----------------------------
# Save Conversation History
# -----------------------------

messages.append({
    "role": "assistant",
    "content": output
})

with open("history.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2, ensure_ascii=False)

# -----------------------------
# Extract Files
# -----------------------------

pattern = r"###\s+([^\n]+)\s*```(?:[a-zA-Z0-9]+)?\n(.*?)```"
matches = re.findall(pattern, output, re.DOTALL)
print(matches)
print(f"\nFound {len(matches)} file(s)")

for filepath, code in matches:
    filepath = filepath.strip()

    # Prevent writing outside project
    if filepath.startswith("/") or ".." in filepath:
        continue

    path = Path(filepath)

    # Skip existing files
    if path.exists():
        print(f"⚠️ Skipped {filepath} (already exists)")
        continue

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(code.rstrip())

    print(f"✅ Saved {filepath}")