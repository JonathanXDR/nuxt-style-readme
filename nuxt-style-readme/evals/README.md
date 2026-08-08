# Evals

Two suites, matching the two ways this skill can fail.

| File | Question it answers |
| ---- | ------------------- |
| `eval_queries.json` | Does the skill activate on the right requests and stay quiet on the wrong ones? |
| `evals.json` | When it does activate, is the README correct? |

`files/` holds eight small fixture repositories. Each is deliberately minimal and exists to make one decision checkable. `pomo-cli` has a one-line README and no configuration. `quickmath` has no LICENSE. `glyphkit` wraps licensed third party artwork. `sortmerge` already has a good README and should come back nearly untouched.

## Output quality

`evals.json` follows the schema from [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills): `skill_name` plus an `evals` array of `id`, `prompt`, `expected_output`, `files`, and `assertions`.

Run each case twice, once with the skill and once without, each in a fresh context so nothing leaks between runs. Point both at a copy of the fixture, since a run will write a README into it. Then grade every assertion PASS or FAIL with evidence quoted from the output, and compare the two configurations.

The baseline matters more than the absolute score. An assertion that passes without the skill is not measuring the skill. Assertions here were chosen to fail without it: emoji conventions, section omission, license accuracy, and refusal to invent content are exactly what an unguided model gets wrong.

Case 13 is the one to watch. It asks for a "comprehensive, professional" README for a trivial CLI, which is the request most likely to produce badges, invented features, and sections with nothing in them.

## Triggering

`eval_queries.json` follows [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions): twenty realistic queries, ten that should trigger and ten that should not. Each carries a `split` of `train` or `validation`, roughly 60/40 with a proportional mix in each, so the documented two-file workflow can be reproduced by filtering rather than by keeping two copies in sync.

Run each query three times and compute a trigger rate. A should-trigger query passes above 0.5, a should-not-trigger query passes below it. Tune the description against the train set only, then check generalization against the validation set.

The negative cases are near misses on purpose. Release notes, API reference, a contributing guide, a docs site page, a changelog, and an ADR are all documentation work that is not a README. Reading a README is not writing one.

Two queries guard the skill's name specifically. "Help me figure out why my Nuxt app is throwing a hydration mismatch" must not trigger, because the word Nuxt in the skill name describes the output style rather than the target project. "This is a Rust crate, the README is three lines long" must trigger, for the same reason in reverse.

When a query fails, fix the category rather than the wording. Adding the exact phrase from a failed query is how a description overfits.

## Iteration 1

The first pass was a smoke test: cases 10, 12, and 13, one run each, with and without the skill. Its clearest result was case 13, where the baseline produced a 352 line README with a hand-written table of contents, an `## Examples` section for a repository containing no examples, and no `## Features` section, while the skill stayed at 86 lines. Grading also exposed gaps in the assertions themselves, which were revised afterward. The revised assertion set is what ships in `evals.json` and what iteration 2 graded. The pass totals recorded from this run predate those revisions and no longer reconcile with the shipped set, so they are not repeated here.

## Iteration 2

All thirteen cases ran with and without the skill, one run per configuration, each in a fresh context against a copy of its fixture, on claude-fable-5. An independent grader per case checked every assertion against the actual files.

| Configuration | Assertions passed |
| ------------- | ----------------- |
| With skill | 85 of 85 |
| Without skill | 69 of 85 |

The baseline's sixteen failures fall into two clusters. Convention drift covers most of them: a missing `## Features` section, plain `## Usage` and `## Requirements` headings, `## Why not just rsync?` in place of `## Why?`, a Background section renamed and given an emoji, and a Limitations heading without `⚠️`. The integrity cluster is smaller and more serious. On case 10 the baseline wrote an MIT license section for a repository that has no license, and on case 13 it answered the request for a "comprehensive, professional" README with shields.io badges, an Examples section for a repository containing none, nine H2 sections, and a notification claim that `main.go` does not support.

Cases 6, 8, 9, 11, and 12 passed identically in both arms. Their assertions still guard against regressions, but on this model they did not discriminate, so read with-versus-baseline deltas there as noise.

## Trigger measurement

The documented three-runs-per-query protocol was executed twice against the twenty queries, because the first pass exposed a harness artifact rather than a description problem.

The stock harness runs each query in an empty project root and counts a run as triggered only when the first tool call consults the skill. Under those conditions every should-not-trigger query passed at a rate of 0.00, and nine of ten should-trigger queries failed, most at 0.00. A controlled diagnostic that placed a real small repository in the project root flipped the outcome: the very first tool call became the skill invocation. The failures measured the missing repository, not the description.

The second pass therefore used a corrected harness: each run received its own isolated copy of a small real repository as its project root, and detection accepted a skill consult at any point in the session within a 120 second budget.

| Pass | Harness | Result |
| ---- | ------- | ------ |
| 1 | Stock, empty project root, first tool call only | 11 of 20. Every negative correct, nine of ten positives failed. |
| 2 | Corrected, real repository root, any-point detection | 20 of 20. Every positive at 3 of 3, every negative at 0 of 3. |

Both passes ran on claude-fable-5 with three runs per query. The description was not changed between them, so pass 2 measures the description exactly as shipped, with nothing tuned against either split.
