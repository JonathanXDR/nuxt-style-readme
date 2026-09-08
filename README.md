# nuxt-style-readme

An [Agent Skill](https://agentskills.io) that writes and refines repository READMEs in a concise, Nuxt-inspired documentation style.

> [!NOTE]
> This is an opinionated style, and it omits more than it adds. If you want a README that fills in every heading a template offers, this is the wrong skill.

## Features

- 🧭 **Earned sections:** Includes an optional section only when the repository gives it real content.
- 🔍 **Evidence before prose:** Reads commands, versions, and license claims out of the repository instead of assuming them.
- 🖼️ **Banners and badges:** Adds a banner, badge, or docs link only when the repository proves it exists.
- 🌍 **Any ecosystem:** Applies to repositories in any language or framework, not only Nuxt or JavaScript.
- 🎯 **Scannable features:** Formats each feature as one emoji, a bold label, and one concise sentence.
- 🧩 **Domain sections:** Names a section after the part of the repository that no generic heading fits.
- 🚦 **Sparing alerts:** Defaults to GitHub's recommended one or two alerts, and picks severity by consequence.
- ✍️ **Punctuation rules:** Keeps em dashes, en dashes, and semicolons out of the prose it writes.
- 🪶 **Cheap to keep loaded:** Loads `SKILL.md` on activation and each reference only when a step needs it.
- ✅ **[Built-in evals](./nuxt-style-readme/evals):** Verifies the skill with 100+ output assertions plus 20 trigger queries.

## Background

The skeleton comes from the Nuxt ecosystem: a short introduction, feature-first presentation, a fast path to first success, the banner and badges opening, and minimal ceremony. Most conventions come from the author's other repositories, and the rest extend the same logic where those repositories offered no precedent. Where Nuxt opens with a banner and badges by default, this style includes them only when it finds them in the repository.

## 🚀 Quick Start

Install the skill with the [skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add JonathanXDR/nuxt-style-readme
```

The CLI asks whether to install into the current project or globally for your user. Pass `-g` to skip the prompt and choose global.

Nothing here is tied to a particular agent. The skill uses only the fields in the [Agent Skills specification](https://agentskills.io/specification), with no vendor extensions. The [client showcase](https://agentskills.io/clients) links to setup instructions for each compatible client.

## 🧪 Usage

Ask for a README. The skill activates on requests to write, rewrite, restructure, tighten, or update one, including requests that never use the word README. Any of these reaches it:

```text
Write a README for this repo.
The front page doesn't explain what this does. Fix it.
I dropped Node 18 support, the docs are stale now.
Make this project's docs read like my other repositories.
```

It then reads the repository and decides which sections the evidence supports. It drafts the README, then verifies every command and claim against a file before finishing. It asks a question only when the repository cannot settle a decision that changes the README, such as which of two competing audiences is primary, or what an unclear license grants.

It does not touch source, dependencies, tests, or unrelated documentation. It also declines requests for anything that is not a README, such as changelogs, release notes, and API reference.

## 🔧 How It Works

A README is a set of judgments about one repository, not a form to fill in. So the skill encodes decision rules rather than a fixed outline, and it phrases every section rule as something you can check in the repository.

The skill splits its content so that each step loads only what it needs:

| File                                                                  | Loaded                                                   | Carries                                                 |
| --------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| [`SKILL.md`](./nuxt-style-readme/SKILL.md)                            | On activation                                            | The workflow, the non-negotiables, the gotchas          |
| [`section-rules.md`](./nuxt-style-readme/references/section-rules.md) | Before choosing an outline                               | An inclusion test and canonical heading per section     |
| [`style-guide.md`](./nuxt-style-readme/references/style-guide.md)     | Before writing prose                                     | Voice, headings, emoji, tables, alerts, license wording |
| [`readme-template.md`](./nuxt-style-readme/assets/readme-template.md) | Only when building from nothing or restructuring heavily | A skeleton of the optional parts                        |

The skill sits in a `nuxt-style-readme/` subdirectory because the specification requires the directory name to match the skill name.

The style guide grades its conventions by how far they bend: strong defaults that hold unless the repository objects, conditional patterns that depend on a condition you can check, repository-specific calls left to the evidence, and an avoid list of what never belongs in a README.

This page is the skill's own output, so it doubles as the worked example.

## 🔬 Measurement

Both suites live in `nuxt-style-readme/evals/`. CI does not run them, so rerun the cases a rule change touches yourself. Every output case runs in a fresh context against a copy of its fixture, once with the skill and once without. The without-skill figure is a single sweep of all sixteen cases, while the with-skill figure is each case's most recent run.

| Suite          | Scale                                             | Result                                       |
| -------------- | ------------------------------------------------- | -------------------------------------------- |
| Output quality | 124 assertions, 16 cases, 11 fixture repositories | 124 of 124 with the skill, 88 of 124 without |
| Triggering     | 20 queries, three runs each                       | 20 of 20                                     |

The baseline is the number that matters, because an assertion that passes without the skill measures nothing. The 36 baseline failures are what the skill contributes. The largest cluster is convention drift, such as an emoji on the `## Features` heading and missing or wrong H2 emoji across nine cases. A smaller chrome cluster comes from a fixture that earns a banner, badges, and a Playground bullet, where the unguided run produced a bare banner and none of the rest.

The third cluster is the serious one. The unguided run invented an MIT license for an unlicensed fixture, added badges and an Examples section to a trivial CLI that evidences neither, missed another fixture's legal alert, and kept an impossible npm install line for a private package. On a fixture whose README was already correct, it rewrote enough to fail four preservation assertions.

## ⚠️ Limitations

- Both output quality figures come from one run per configuration, so neither carries a variance estimate. One borderline call went both ways between runs before a rule change settled it: whether a library with three named exports earns a Features section.
- The fixture repositories are small and purpose-built, each shaped to make one decision checkable. Assertions do check documented claims against fixture source, but nothing runs the fixtures, so a correct README for broken code would still pass.
- The trigger score depends on a corrected harness. The stock one runs each query in an empty project root and scores 11 of 20, because it measures the missing repository rather than the skill's description.

## 🛠️ Development

Three checks run in CI on `main` and on every pull request. Run them locally in the same order.

Validate the skill's frontmatter and naming against the reference library from the [Agent Skills specification repository](https://github.com/agentskills/agentskills/tree/main/skills-ref):

```bash
uvx --from 'skills-ref==0.1.1' agentskills validate ./nuxt-style-readme
```

The published package is named `skills-ref` while the executable inside it is named `agentskills`, so the command names both. The release and the specification repository have never agreed on that name, which is why the version is pinned.

Check prose punctuation across every Markdown file in the repository:

```bash
python3 scripts/check_prose.py
```

It fails on em dashes, en dashes, spaced hyphens standing in for other punctuation, and semicolons in prose. Fenced blocks, inline code, inline link targets, and lowercase named entities are exempt, because the characters there are content.

Measure `SKILL.md` against its two size budgets:

```bash
wc -l < nuxt-style-readme/SKILL.md                                  # lines, budget 500
awk '/^---$/{c++; next} c>=2' nuxt-style-readme/SKILL.md | wc -c    # body chars, budget 20,000
```

The validator never looks at the body, so [`validate.yml`](./.github/workflows/validate.yml) is what enforces both budgets. It divides the character count by four and tests that estimate against a 5,000 token ceiling.

Bump `metadata.version` in `SKILL.md` whenever the rules change materially, so an installed copy traces back to a revision.

The trigger suite runs one query per invocation through [`scripts/trigger_run.py`](./scripts/trigger_run.py). See [`evals/README.md`](./nuxt-style-readme/evals/README.md) for both protocols and the harness traps worth knowing before you reproduce the numbers.

## ⛰️ Next Steps

1. 📖 Read [`section-rules.md`](./nuxt-style-readme/references/section-rules.md) to see which sections a repository has to earn.
2. 🎨 Read [`style-guide.md`](./nuxt-style-readme/references/style-guide.md) if you want to fork the conventions and swap in your own.
3. 🧱 Add a fixture under [`evals/files/`](./nuxt-style-readme/evals/files) when you hit a case the suites do not cover yet.
4. 🐛 Hit a bug or have an idea? [Open an issue](https://github.com/JonathanXDR/nuxt-style-readme/issues).

## ⚖️ License

Licensed under the [MIT license](./LICENSE) © Jonathan Russ.
