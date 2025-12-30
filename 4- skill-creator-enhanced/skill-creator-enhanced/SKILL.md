---
name: skill-creator-enhanced
description: Production-grade guide for creating excellent skills. Use when users want to create a new skill (or update an existing skill) that extends Claude's capabilities. Covers structure, content quality, user interaction patterns, documentation, domain standards enforcement, and technical robustness. Creates skills that score 90+ on skill-validator.
---

# Skill Creator Enhanced

Create production-grade skills that extend Claude's capabilities.

## What This Skill Does

- Guides creation of new skills from scratch
- Helps improve existing skills to production quality
- Provides patterns for all skill types (Builder, Guide, Automation)
- Ensures skills meet validation criteria

## What This Skill Does NOT Do

- Create the actual domain content (user provides that)
- Test skills in production environments
- Deploy or distribute skills
- Handle skill versioning/updates after creation

---

## Required Clarifications

Before creating a skill, ask:

### 1. Skill Type
"What type of skill are you creating?"
- **Builder** → Creates artifacts (widgets, code, documents)
- **Guide** → Provides instructions (how-to, tutorials)
- **Automation** → Executes workflows (file processing, deployments)

### 2. Domain
"What domain or technology does this skill cover?"
- Example: "ChatGPT widgets", "PDF processing", "BigQuery analytics"

### 3. Concrete Examples
"Can you give 2-3 examples of how this skill would be used?"
- Example prompts users would give
- Expected outputs for each

### 4. Existing Resources
"Do you have any existing scripts, templates, or documentation to include?"
- Scripts for `scripts/`
- Templates for `assets/`
- Reference docs for `references/`

### Optional Clarifications

5. **Official Docs**: "Are there official documentation URLs for this domain?"
6. **Standards**: "Are there industry standards to enforce?" (WCAG, OWASP, etc.)

---

## Core Principles

### Concise is Key

Context window is a public good. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Appropriate Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** | Multiple approaches valid | "Choose your preferred style" |
| **Medium** | Preferred pattern exists | Pseudocode with parameters |
| **Low** | Operations are fragile | Exact scripts, few parameters |

### Progressive Disclosure

Three-level loading system:

1. **Metadata** (~100 words) - Always in context
2. **SKILL.md body** (<500 lines) - When skill triggers
3. **References** (unlimited) - As needed by Claude

---

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Templates, images, fonts
```

### SKILL.md Requirements

| Component | Requirement |
|-----------|-------------|
| Line count | <500 lines (extract to references/) |
| Frontmatter | `name` + `description` with triggers |
| Form | Imperative ("Do X" not "You should X") |
| Scope | What it does AND does not do |

### What NOT to Include

- README.md (SKILL.md IS the readme)
- CHANGELOG.md
- LICENSE (inherited from repo)
- Duplicate information

---

## Skill Creation Process

### Step 1: Understand with Examples

Ask clarifying questions (see Required Clarifications above).

Conclude when you have:
- Clear skill type (Builder/Guide/Automation)
- 2-3 concrete usage examples
- Known resources to include

### Step 2: Plan Resources

For each example, identify:

| Resource Type | When to Create |
|---------------|----------------|
| `scripts/` | Same code rewritten repeatedly, deterministic reliability needed |
| `references/` | Documentation Claude should reference while working |
| `assets/` | Templates, images, boilerplate for output |

### Step 3: Initialize

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates template with proper structure.

### Step 4: Implement

1. **Start with resources** - Create scripts/, references/, assets/ files
2. **Test scripts** - Run to verify they work
3. **Write SKILL.md** - Follow patterns below

#### SKILL.md Patterns

**Frontmatter**:
```yaml
---
name: skill-name
description: What it does + when to use + triggers. Use when users ask to...
---
```

**Body structure**:
1. What this skill does / does not do
2. Required clarifications (for Builder skills)
3. Core workflow steps
4. Reference files table
5. Output checklist

See `references/skill-patterns.md` for complete patterns.

### Step 5: Add Quality Elements

For production-grade skills, include:

| Element | Where | Purpose |
|---------|-------|---------|
| Clarification questions | SKILL.md | Prevent wrong assumptions |
| Official doc links | references/ | Enable latest patterns |
| Enforcement checklists | SKILL.md or references/ | Ensure compliance |
| Output checklist | SKILL.md | Quality gate before delivery |
| Error handling | references/ | Graceful failures |

See `references/quality-patterns.md` for implementation details.

### Step 6: Package

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Validates and creates `.skill` file.

### Step 7: Iterate

Use skill on real tasks → Notice issues → Update and retest.

---

## Output Checklist

Before delivering a skill, verify:

### Structure
- [ ] SKILL.md exists and <500 lines
- [ ] Frontmatter has name + description with triggers
- [ ] No README.md, CHANGELOG.md in skill directory
- [ ] Progressive disclosure (details in references/)

### Content
- [ ] Imperative form throughout
- [ ] Scope clarity (does / does not do)
- [ ] Clear workflow steps
- [ ] No verbose explanations

### User Interaction (Builder skills)
- [ ] Required clarifications section
- [ ] Optional clarifications separated
- [ ] Context awareness guidance

### Documentation
- [ ] Official doc links (if applicable)
- [ ] Reference files for complex details
- [ ] "When to read" table for references

### Domain Standards (if applicable)
- [ ] Must Follow checklist
- [ ] Must Avoid list
- [ ] Output quality gate

### Technical (if applicable)
- [ ] Error handling guidance
- [ ] Dependencies documented
- [ ] Scripts tested

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/skill-patterns.md` | SKILL.md structure and examples |
| `references/quality-patterns.md` | Clarifications, enforcement, checklists |
| `references/technical-patterns.md` | Error handling, security, dependencies |
| `references/workflows.md` | Sequential and conditional workflows |
| `references/output-patterns.md` | Template and example patterns |

---

## Quick Reference

### Must Follow
- [ ] SKILL.md <500 lines
- [ ] Frontmatter with triggers
- [ ] Imperative form
- [ ] No extraneous files
- [ ] Progressive disclosure

### Must Avoid
- Verbose explanations
- "You should" language
- Duplicate information
- Deep reference nesting
- README.md files
