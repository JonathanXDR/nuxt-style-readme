# Nuxt-style README skill

An Agent Skill that writes and refines repository READMEs in a concise, Nuxt-inspired documentation style.

> [!NOTE]
> This is an opinionated style. It adds no badges and no hero artwork, and it leaves out any section your repository gives it no evidence for. If you want a README that fills in every heading a template offers, this is the wrong skill.

## Features

- 🧭 **Sections are earned:** Each optional section has an inclusion test checked against the repository, so a small CLI gets four sections and a framework gets nine.
- 🔍 **Evidence before prose:** Commands, exports, versions, and license claims are read out of the manifest, the source, and the LICENSE file rather than assumed.
- 🎯 **Scannable feature bullets:** One emoji, a bold name, one sentence of concrete capability, in a format that stays consistent across every repository you apply it to.
- 📐 **Settled heading conventions:** `## Features`, `## Why?`, and `## Background` carry no emoji, every other H2 carries exactly one, and no emoji repeats across H2 headings.
- 🧩 **Domain sections, not filler:** The skill actively looks for the one or two sections that only your project would have, which is what stops the output reading like a template.
- 🚦 **Alerts used sparingly:** Held to GitHub's own limit of one or two per document, with severity chosen by consequence and re-checked against the live documentation.
- 🪶 **Cheap to keep loaded:** `SKILL.md` is 143 lines, well inside the recommended 500 line and 5,000 token budget, with the style guide, section rules, and template loaded only at the step that needs them.
- ✅ **Ships with its own evals:** Ninety-six assertions across thirteen output cases over eight fixture repositories, plus twenty trigger queries, with every measured run and its caveats written down rather than summarized.

## 🚀 Install

The skill is the `nuxt-style-readme/` directory. Copy it into wherever your agent looks for skills.

```bash
git clone https://github.com/JonathanXDR/nuxt-style-readme-skill.git
mkdir -p ~/.agents/skills
cp -r nuxt-style-readme-skill/nuxt-style-readme ~/.agents/skills/
```

Keep the directory named `nuxt-style-readme`. The specification requires a skill's `name` field to match the name of the directory containing `SKILL.md`, so renaming the folder invalidates the skill.

Common locations are `~/.agents/skills/` and `~/.claude/skills/` for user-wide install, or `.agents/skills/` inside a project. These are conventions rather than part of the specification, which does not mandate where skills live, so check what your own client expects. The [Agent Skills client showcase](https://agentskills.io/clients) links the setup instructions for each one.

Nothing here is tied to a particular agent. The skill uses only the fields in the [Agent Skills specification](https://agentskills.io/specification) and no vendor extensions.

## 🧪 Usage

Ask for a README. The skill activates on requests to write, rewrite, restructure, tighten, or update one, including requests that never use the word README.

```text
Write a README for this repo.
The front page doesn't explain what this does. Fix it.
I dropped Node 18 support, the docs are stale now.
Make this project's docs read like my other repositories.
```

It then reads the repository, decides which sections the evidence supports, drafts, and verifies every command and claim before finishing. It asks a question only when a decision genuinely changes the README and the repository cannot settle it, such as two competing primary audiences or an unclear licensing situation.

It stays out of everything else. Source, dependencies, tests, and unrelated documentation are not touched.

## 🔧 How It Works

The design decision behind the skill is that a README is a set of judgments about one repository, not a form. So the skill encodes decision rules rather than a fixed outline, and every rule is phrased as something checkable in the repository.

Content is split so that only what a step needs gets loaded:

| File | Loaded |
| ---- | ------ |
| `SKILL.md` | On activation. The workflow, the hard rules, and the gotchas. |
| `references/section-rules.md` | Before choosing an outline. Inclusion test and canonical heading per section. |
| `references/style-guide.md` | Before writing prose. Voice, headings, emoji, tables, alerts, license wording. |
| `assets/readme-template.md` | Only when building from nothing or restructuring heavily. |

The style guide separates conventions by how far they bend: strong defaults that hold unless the repository objects, conditional patterns tied to a checkable condition, decisions left to the repository, and a list of things that never apply.

The conventions come from a set of existing READMEs that already use this style, with the wider Nuxt ecosystem as the source of the skeleton. Nuxt contributes the shape, which is the short introduction, the feature-first presentation, the fast path to first success, and the closing `⛰️ Next Steps` and `⚖️ License`. The rest is the divergence: no badges, no banner, feature bullets promoted from plain text to highlighted entries, and far more of the page spent on tables, verified commands, and honest limitations.

## 🛠️ Development

Validate against the reference library from the [Agent Skills specification repository](https://github.com/agentskills/agentskills/tree/main/skills-ref). The published package names its executable `agentskills`:

```bash
uvx --from skills-ref agentskills validate ./nuxt-style-readme
```

Installing from the repository source instead keeps the `skills-ref` name that the specification uses:

```bash
uvx --from git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref \
  skills-ref validate ./nuxt-style-readme
```

Both check frontmatter validity and naming conventions. Neither checks the 500 line and 5,000 token body budgets. The [`validate.yml`](./.github/workflows/validate.yml) workflow enforces those budgets on `main` and on pull requests, so measure locally when editing `SKILL.md`.

See [`nuxt-style-readme/evals/README.md`](./nuxt-style-readme/evals/README.md) for how to run the two eval suites and what each one is meant to catch.

## ⛰️ Next Steps

1. 📖 Read [`section-rules.md`](./nuxt-style-readme/references/section-rules.md) to see which sections a repository has to earn.
2. 🎨 Read [`style-guide.md`](./nuxt-style-readme/references/style-guide.md) if you want to fork the conventions and swap in your own.
3. 📊 Run the [eval suites](./nuxt-style-readme/evals/README.md) against your own agent before trusting the skill on a repository that matters.
4. 🐛 Hit a bug or have an idea? [Open an issue](https://github.com/JonathanXDR/nuxt-style-readme-skill/issues).

## ⚖️ License

Licensed under the [MIT license](./LICENSE) © Jonathan Russ.
