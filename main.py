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
    api_key="sk__s-4ZUpPMgxicto4jR8HL0ipVwU6HlIcp7dbvIxg-4I",
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

The application already has:

- Authentication
- Dashboard
- Projects module
- Sprints module

These modules are COMPLETE and WORKING.

====================================================
IMPORTANT RULES (READ CAREFULLY)
====================================================

DO NOT modify, overwrite, regenerate, delete or reformat ANY existing files.

Especially DO NOT touch:

src/router/*
src/components/layout/*
src/providers/*
src/config/*
src/features/auth/*
src/App.tsx
src/main.tsx

If any shared file requires changes,
DO NOT regenerate it.

Instead output a section named:

MANUAL ROUTER PATCH

showing only the exact code that must be manually replaced.

Never rewrite existing files.

Return ONLY newly created files.

====================================================
TASK
====================================================

Generate a complete Work Items module.

Create ONLY these files:

src/features/work-items/
    types.ts
    workItemsApi.ts
    workItemSchemas.ts
    useWorkItems.ts
    useSprintOptions.ts
    useAssigneeOptions.ts

src/features/work-items/components/
    WorkItemsTable.tsx
    WorkItemFilters.tsx
    WorkItemStatusBadge.tsx
    Pagination.tsx
    Modal.tsx
    CreateWorkItemDialog.tsx
    EditWorkItemDialog.tsx
    DeleteWorkItemDialog.tsx
    WorkItemsLoadingState.tsx
    WorkItemsErrorState.tsx

src/features/work-items/index.ts

src/pages/work-items/WorkItemsPage.tsx

====================================================
WORK ITEM MODEL
====================================================

Each work item should support:

- id
- title
- description
- sprintId
- assigneeId
- priority
- status
- estimate
- storyPoints
- dueDate
- createdAt
- updatedAt

Priority:

- Low
- Medium
- High
- Critical

Status:

- Backlog
- Todo
- In Progress
- In Review
- Done
- Blocked

====================================================
PAGE FEATURES
====================================================

Implement:

✔ Search
✔ Filters
✔ Pagination
✔ Loading state
✔ Empty state
✔ Error state
✔ Create Work Item dialog
✔ Edit Work Item dialog
✔ Delete confirmation dialog

====================================================
TABLE
====================================================

Columns:

- Title
- Sprint
- Assignee
- Priority
- Status
- Story Points
- Due Date
- Actions

Actions:

- Edit
- Delete

====================================================
API
====================================================

Use the same API patterns already used by Projects and Sprints.

Do not invent a different architecture.

====================================================
OUTPUT FORMAT
====================================================

Return ONLY new files.

Do NOT regenerate existing files.

If routing changes are required, output ONLY:

MANUAL ROUTER PATCH

with the exact replacement needed inside AppRouter.tsx.

No other shared files should be modified.
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