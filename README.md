# Nuxt-style README skill

An Agent Skill that writes and refines repository READMEs in a concise, Nuxt-inspired documentation style.

> [!NOTE]
> This is an opinionated style. It adds no badges and no hero artwork, and it leaves out any section your repository gives it no evidence for. If you want a README that fills in every heading a template offers, this is the wrong skill.

## Features

- 🧭 **Sections are earned:** Each optional section has an inclusion test checked against the repository, so most READMEs land at six to nine sections and a single-purpose CLI can be complete at four.
- 🔍 **Evidence before prose:** Commands, exports, versions, and license claims are read out of the manifest, the source, and the LICENSE file rather than assumed.
- 🎯 **Scannable feature bullets:** One emoji, a bold name, one sentence of concrete capability, in a format that stays consistent across every repository you apply it to.
- 📐 **Settled heading conventions:** `## Features`, `## Why?`, and `## Background` carry no emoji, every other H2 carries exactly one, and no emoji repeats across H2 headings.
- 🧩 **Domain sections, not filler:** The skill actively looks for the one to three sections that only your project would have, which is what stops the output reading like a template.
- 🚦 **Alerts used sparingly:** Defaulting to GitHub's own recommendation of one or two per document, with severity chosen by consequence and re-checked against the live documentation.
- 🪶 **Cheap to keep loaded:** `SKILL.md` stays well inside the recommended 500 line and 5,000 token budget, with the style guide, section rules, and template loaded only at the step that needs them.
- ✅ **Ships with its own evals:** 96 assertions across 13 output cases over 8 fixture repositories, plus 20 trigger queries, with the output cases run with and without the skill so the difference is measured rather than asserted.

## 🚀 Install

The skill is the [`nuxt-style-readme/`](./nuxt-style-readme) directory. Copy it into wherever your agent looks for skills.

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

It stays out of everything else. Source, dependencies, tests, and unrelated documentation are not touched, and it declines documentation that is not a README, such as changelogs, release notes, and API reference.

## 🔧 How It Works

The design decision behind the skill is that a README is a set of judgments about one repository, not a form. So the skill encodes decision rules rather than a fixed outline, and every rule is phrased as something checkable in the repository.

Content is split so that only what a step needs gets loaded:

| File | Loaded | Carries |
| ---- | ------ | ------- |
| [`SKILL.md`](./nuxt-style-readme/SKILL.md) | On activation | The workflow, the non-negotiables, the gotchas |
| [`section-rules.md`](./nuxt-style-readme/references/section-rules.md) | Before choosing an outline | An inclusion test and canonical heading per section |
| [`style-guide.md`](./nuxt-style-readme/references/style-guide.md) | Before writing prose | Voice, headings, emoji, tables, alerts, license wording |
| [`readme-template.md`](./nuxt-style-readme/assets/readme-template.md) | Only when building from nothing or restructuring heavily | A skeleton of the optional parts |

The style guide separates conventions by how far they bend: strong defaults that hold unless the repository objects, conditional patterns tied to a checkable condition, decisions left to the repository, and a list of things that never apply.

The conventions come from a set of existing READMEs that already use this style, with the wider Nuxt ecosystem as the source of the skeleton. Nuxt contributes the principles, which are the short introduction, the feature-first presentation, the fast path to first success, and minimal ceremony. The rest is the divergence: no badges, no banner, feature bullets promoted from plain text to highlighted entries, and far more of the page spent on tables, verified commands, and stated limitations.

This page is the skill's own output, so it doubles as the worked example.

## ⚠️ Limitations

- Every output eval is a single run against a single model, so the recorded scores carry no variance estimate. One borderline call, whether an install section may mention the runtime its install command already implies, has already been seen going both ways between runs.
- The eight fixture repositories are deliberately minimal stubs. They check structure, licensing, and command grounding, not whether documented behavior matches real behavior.
- Of the assertions added in iteration 3, eight of eleven passed with and without the skill, so they guard against regressions rather than measure what the skill contributes.

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

Both check frontmatter validity and naming conventions. Neither checks the body size budgets, which the [`validate.yml`](./.github/workflows/validate.yml) workflow enforces on `main` and on pull requests. Measure the same two numbers locally when editing `SKILL.md`:

```bash
wc -l < nuxt-style-readme/SKILL.md                                  # lines, budget 500
awk '/^---$/{c++; next} c>=2' nuxt-style-readme/SKILL.md | wc -c    # body chars, budget 20,000
```

The workflow divides that character count by four for its token estimate.

Bump `metadata.version` in `SKILL.md` whenever the rules change materially, so an installed copy can be traced to a revision.

See [`nuxt-style-readme/evals/README.md`](./nuxt-style-readme/evals/README.md) for how to run the two eval suites and what each one is meant to catch.

## ⛰️ Next Steps

1. 📖 Read [`section-rules.md`](./nuxt-style-readme/references/section-rules.md) to see which sections a repository has to earn.
2. 🎨 Read [`style-guide.md`](./nuxt-style-readme/references/style-guide.md) if you want to fork the conventions and swap in your own.
3. 🧱 Add a fixture under [`evals/files/`](./nuxt-style-readme/evals/files) when you hit a case the suites do not cover yet.
4. 🐛 Hit a bug or have an idea? [Open an issue](https://github.com/JonathanXDR/nuxt-style-readme-skill/issues).

## ⚖️ License

Licensed under the [MIT license](./LICENSE) © Jonathan Russ.
