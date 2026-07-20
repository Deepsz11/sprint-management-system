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
    api_key="sk_PVtpuSIenPkvjzqXt1s8QcZnbCmy2UpHdszgN56vuyo",
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

The application already has fully working modules:

- Authentication
- Dashboard
- Organizations
- Teams
- Projects
- Sprints
- Work Items
- Business Outcomes
- KPIs

====================================================
STRICT RULES
====================================================

Never modify, overwrite, regenerate, delete or reformat any existing shared files.

DO NOT touch:

src/router/*
src/components/layout/*
src/providers/*
src/config/*
src/features/auth/*
src/App.tsx
src/main.tsx

If routing needs to change:

DO NOT modify AppRouter.tsx.

Instead output:

=========================
MANUAL ROUTER PATCH
=========================

showing ONLY the exact replacement.

Return ONLY newly created files.

====================================================
TASK
====================================================

Generate a complete Users module.

Create ONLY these files:

src/features/users/
    types.ts
    usersApi.ts
    userSchemas.ts
    useUsers.ts
    useOrganizationOptions.ts
    useTeamOptions.ts
    useRoleOptions.ts

src/features/users/components/
    UsersTable.tsx
    UserFilters.tsx
    UserStatusBadge.tsx
    RoleBadge.tsx
    Pagination.tsx
    Modal.tsx
    InviteUserDialog.tsx
    EditUserDialog.tsx
    DeactivateUserDialog.tsx
    UsersLoadingState.tsx
    UsersErrorState.tsx

src/features/users/index.ts

src/pages/users/UsersPage.tsx

====================================================
USER MODEL
====================================================

Each user contains:

- id
- firstName
- lastName
- email
- avatarUrl
- organizationId
- teamId
- role
- jobTitle
- phone
- status
- lastLogin
- createdAt
- updatedAt

Roles:

- Org Admin
- Project Manager
- Team Lead
- Member
- Viewer

Status:

- Active
- Invited
- Suspended
- Disabled

====================================================
PAGE FEATURES
====================================================

Implement:

✔ Search
✔ Organization filter
✔ Team filter
✔ Role filter
✔ Status filter
✔ Pagination
✔ Loading state
✔ Empty state
✔ Error state

Dialogs:

✔ Invite User
✔ Edit User
✔ Deactivate User

====================================================
TABLE
====================================================

Columns:

- Avatar
- Name
- Email
- Organization
- Team
- Role
- Status
- Last Login
- Actions

Actions:

- Edit
- Deactivate

====================================================
API
====================================================

Follow exactly the same architecture used by:

- Organizations
- Teams
- Projects
- Sprints
- Work Items
- Business Outcomes
- KPIs

Do NOT invent a different architecture.

====================================================
OUTPUT FORMAT
====================================================

Return ONLY newly created files.

Never regenerate existing files.

If AppRouter.tsx requires modification, output ONLY:

MANUAL ROUTER PATCH

Do not modify any shared files.
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