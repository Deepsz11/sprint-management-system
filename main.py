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
    api_key="sk_VRAEahMSRg4AGp_hCqRBG6tSjFt9lGNP49G7AoxjejE",
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
    You are a senior React + TypeScript architect.

Generate the COMPLETE frontend foundation for a production-grade SaaS called Sprint Business Outcome Tracker.

Tech Stack
- React 18
- Vite
- TypeScript
- React Router v6
- TailwindCSS
- shadcn/ui
- Axios
- React Hook Form
- Zod

Generate ONLY the frontend foundation.

Include:

Project structure

Routing

Authentication

Axios API client

Token storage

Theme provider

Sidebar

Topbar

App layout

ProtectedRoute

PublicRoute

Dashboard page

Login page

404 page

ModulePlaceholder page

Common UI components

Configuration

Do NOT generate CRUD pages.

Do NOT generate feature modules.

Routes that don't exist yet must point to ModulePlaceholder.

Rules

- Use named exports consistently.
- Use ROUTES (uppercase) everywhere.
- Never use default exports except App.tsx.
- Do not generate duplicate layouts.
- Do not generate duplicate routers.
- Generate complete working files only.
- Every import must reference an existing file.
- Do not invent components.

Return all frontend files.
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