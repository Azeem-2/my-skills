# Skill Patterns

SKILL.md structure and examples for different skill types.

---

## SKILL.md Structure

### Complete Template

```markdown
---
name: skill-name
description: What it does + when to use + key triggers. Use when users ask to...
---

# Skill Name

Brief one-line description.

## What This Skill Does
- Capability 1
- Capability 2
- Capability 3

## What This Skill Does NOT Do
- Exclusion 1
- Exclusion 2

---

## Required Clarifications

Before proceeding, ask:

1. **Question A**: "Specific question?"
2. **Question B**: "Another question?"

### Optional Clarifications
3. **Question C**: "Nice-to-know?" (if relevant)

---

## Workflow

1. Step one
2. Step two
3. Step three

---

## [Domain-Specific Section]

Content specific to what the skill does.

---

## Output Checklist

Before delivering, verify:
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/file1.md` | When X |
| `references/file2.md` | When Y |
```

---

## By Skill Type

### Builder Skills (Create Artifacts)

**Key elements**:
- Required Clarifications section (essential)
- Output specification
- Domain standards enforcement
- Templates in assets/

**Example frontmatter**:
```yaml
---
name: widget-creator
description: Create production widgets for ChatGPT Apps. Use when users ask to build UI components, visual interfaces, or interactive elements.
---
```

**Example clarifications**:
```markdown
## Required Clarifications

1. **Data shape**: "What will `toolOutput` contain?"
   ```json
   Example: { items: [...], total: 10 }
   ```

2. **Action type**: "Display only or interactive?"
   - Display → No callTool needed
   - Interactive → Need tool name

3. **Display mode**: "Inline, fullscreen, or pip?"
```

### Guide Skills (Provide Instructions)

**Key elements**:
- Clear step-by-step workflow
- Good/bad examples
- Progressive disclosure to references
- Official documentation links

**Example frontmatter**:
```yaml
---
name: api-integration-guide
description: Guide for integrating external APIs. Use when users need to connect to third-party services, handle authentication, or manage API responses.
---
```

**Example workflow**:
```markdown
## Integration Workflow

1. **Identify API** - Determine endpoint and auth method
2. **Configure Auth** - Set up credentials (see references/auth-patterns.md)
3. **Implement Calls** - Follow patterns below
4. **Handle Errors** - Use retry with backoff
5. **Test** - Verify all endpoints work
```

### Automation Skills (Execute Workflows)

**Key elements**:
- Tested scripts in scripts/
- Error handling guidance
- Dependencies documented
- Sequential workflow steps

**Example frontmatter**:
```yaml
---
name: pdf-processor
description: Process PDF files with extraction, rotation, and form filling. Use when users need to manipulate PDF documents programmatically.
---
```

**Example scripts section**:
```markdown
## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/extract_text.py` | Extract text from PDF | `python extract_text.py input.pdf` |
| `scripts/rotate_pages.py` | Rotate pages | `python rotate_pages.py input.pdf 90` |
| `scripts/fill_form.py` | Fill form fields | `python fill_form.py template.pdf data.json` |

All scripts tested with Python 3.10+.
```

---

## Frontmatter Best Practices

### Good Description (triggers well)

```yaml
description: Create production widgets for ChatGPT Apps using OpenAI Apps SDK. Use when users ask to build UI components, visual interfaces, progress trackers, quiz interfaces, or interactive elements. Supports inline, fullscreen, and pip display modes.
```

**Why it works**:
- States what it does
- Lists specific triggers
- Mentions key capabilities

### Bad Description (triggers poorly)

```yaml
description: Widget stuff
```

**Why it fails**:
- Too vague
- No triggers
- No capabilities listed

---

## Scope Clarity Examples

### Good Scope

```markdown
## What This Skill Does
- Creates ChatGPT widgets with window.openai integration
- Supports all display modes (inline, fullscreen, pip)
- Implements theme support (light/dark)
- Follows OpenAI UX/UI guidelines

## What This Skill Does NOT Do
- Create native mobile apps
- Handle backend server logic
- Manage user authentication
- Deploy widgets to production
```

### Bad Scope (missing exclusions)

```markdown
## What This Skill Does
- Creates widgets
```

---

## Reference Organization

### By Domain (for multi-domain skills)

```
references/
├── aws.md        # AWS-specific patterns
├── gcp.md        # GCP-specific patterns
└── azure.md      # Azure-specific patterns
```

### By Complexity (for single-domain skills)

```
references/
├── quick-start.md     # Basic usage
├── advanced.md        # Complex scenarios
└── troubleshooting.md # Common issues
```

### By Feature (for feature-rich skills)

```
references/
├── authentication.md  # Auth patterns
├── state-management.md # State handling
└── error-handling.md   # Error patterns
```
