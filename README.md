# Nuxt-style README skill

An Agent Skill that writes and refines repository READMEs in a concise, Nuxt-inspired documentation style.

> [!NOTE]
> This is an opinionated style. It adds no badges and no hero artwork, and it leaves out any section your repository gives it no evidence for. If you want a README that fills in every heading a template offers, this is the wrong skill.

## Features

- 🧭 **Earned sections:** Includes an optional section only when the repository gives it real content.
- 🔍 **Evidence before prose:** Reads commands, versions, and license claims out of the repository instead of assuming them.
- 🎯 **Scannable features:** Formats each feature as one emoji, a bold label, and one concise sentence.
- 📐 **Settled headings:** Keeps `## Features` bare and gives every other H2 exactly one unrepeated emoji.
- 🧩 **Domain sections:** Finds the one to three sections that only your project would have.
- 🚦 **Sparing alerts:** Holds alerts to GitHub's recommended one or two, with severity chosen by consequence.
- 🪶 **Cheap to keep loaded:** Keeps `SKILL.md` well inside its budget and loads references only when needed.
- ✅ **Built-in evals:** Verifies the skill with 96 output assertions plus 20 trigger queries.

## 🚀 Quick Start

Install the skill with the [skills CLI](https://skills.sh):

```bash
npx skills add JonathanXDR/nuxt-style-readme-skill
```

The CLI clones with your existing git credentials, finds [`nuxt-style-readme/`](./nuxt-style-readme), and installs it for the agents you pick. Add `-g` for a user-wide install instead of the current project, and `-y` to skip the prompts.

Installing by hand still works: copy [`nuxt-style-readme/`](./nuxt-style-readme) into wherever your agent looks for skills, such as `~/.claude/skills/` or a project's `.agents/skills/`. Keep the directory name, because the specification requires a skill's `name` field to match the directory containing `SKILL.md`.

Nothing here is tied to a particular agent. The skill uses only the fields in the [Agent Skills specification](https://agentskills.io/specification) and no vendor extensions, and the [client showcase](https://agentskills.io/clients) links setup instructions for each compatible client.

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
