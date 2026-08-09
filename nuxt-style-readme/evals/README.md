# Evals

Two suites, matching the two ways this skill can fail.

| File | Question it answers |
| ---- | ------------------- |
| `eval_queries.json` | Does the skill activate on the right requests and stay quiet on the wrong ones? |
| `evals.json` | When it does activate, is the README correct? |

`files/` holds eleven small fixture repositories. Each is deliberately minimal and exists to make one decision checkable. `pomo-cli` has a one-line README and no configuration. `quickmath` has no LICENSE. `glyphkit` wraps licensed third party artwork. `sortmerge` already has a good README and should come back nearly untouched. `glowline` provides a banner asset, a docs homepage, a playground, and a publish workflow, so it is the positive path for the conditional opening chrome. `hoverkit` already carries a fully earned chrome opening that a refinement must preserve, and `pixelfont` carries unearned chrome, badges without a publish path and a banner without an asset, that a refinement must remove and disclose.

## Output quality

`evals.json` follows the schema from [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills): `skill_name` plus an `evals` array of `id`, `prompt`, `expected_output`, `files`, and `assertions`.

Run each case twice, once with the skill and once without, each in a fresh context so nothing leaks between runs. Point both at a copy of the fixture, since a run will write a README into it. Then grade every assertion PASS or FAIL with evidence quoted from the output, and compare the two configurations.

The baseline matters more than the absolute score. An assertion that passes without the skill is not measuring the skill. Most assertions were chosen to fail without it: emoji conventions, section omission, license accuracy, and refusal to invent content are exactly what an unguided model gets wrong. The later additions recorded in iteration 3 are regression guards rather than discriminators.

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

Each of those five, plus case 13, has since gained assertions resting on a fixture fact an unguided run can get wrong. Case 2 also had an assertion corrected, since `chroma-parse` exports three symbols rather than the two it named. The totals above predate those changes.

## Iteration 3

The seven cases whose assertions changed were re-run in both arms to test whether the additions measure anything. They mostly do not.

| Scope | With skill | Without skill |
| ----- | ---------- | ------------- |
| The eleven added assertions plus the one corrected | 12 of 12 | 9 of 12 |
| All assertions on those seven cases | 58 of 59 | 45 of 59 |

Only cases 9 and 13 discriminate on the new assertions. Eight of the eleven added assertions passed in both arms, which means they are regression guards rather than evidence the skill helps. The three that earned their place are the two `## Features` assertions on case 9, where the baseline wrote no Features section at all, and the Project Structure ban on case 13, where the baseline produced an ASCII file tree for a five file repository. Adding an assertion because a rule is untested is not the same as adding one that separates the arms, and most of these did not.

The run also caught a genuine miss. On case 6 the with-skill README omitted `## Features` for `quickmath`, which contradicts the Features inclusion test, since three named exports are capabilities a user can name. That case passed in iteration 2, so this is run to run variance in a borderline judgment rather than a fixed defect. It is recorded here rather than patched, because one observation is not enough to justify changing a rule.

## Iteration 4

The skill was revised after a fresh research and review pass: the alert cap became a default with an earned exception, `## 📦 Project Structure` replaced `🗂️` as the canonical heading to match the house repositories, the refinement path now removes badges explicitly and says so to the user, feature bullets ask for a dense line rather than a sentence, and the template's Examples separator became a colon. All thirteen cases were then re-run with the skill, one run each, graded independently per case. The baseline arm was not re-run, since none of the changes alter what an unguided model does, so iteration 2 remains the baseline of record.

The revised skill passed 90 of 96. Two failures trace to fixture incoherence and the other four to three judgment misses against the skill's own rules.

The fixture failures first. On case 12 the runner deleted the Streaming API and Self-cleaning bullets from sortmerge's README because `src/index.ts` was an empty stub that could not evidence them, which is exactly what evidence-or-omission demands. On case 7 the runner documented that the conversion pipeline is not implemented, which was true, since `cli.py` was a `return 0` stub. Both fixtures were made coherent instead of weakening the assertions: sortmerge gained a streaming implementation whose defaults match its Configuration table, and har2pdf gained an argparse entry point and a `convert` module.

Case 6 omitted `## Features` for quickmath again, the same miss iteration 3 recorded and declined to patch. Two observations is a pattern, so the omit clause now reads "a single capability" and states that two or more nameable capabilities earn the section even when the description names them all.

Cases 4 and 7 shared a shape: content that passes two inclusion tests landing in the wrong home. Case 4 put the bootstrap context in a `## 🔐 The Bootstrap Response` domain section instead of `Background`, and case 7 filed the rotating nonce under Troubleshooting as a symptom instead of under Limitations as a constraint. Two precedence sentences were added to the section rules: a domain section never absorbs content that passes a generic inclusion test, and a workaround does not demote a constraint.

The four failed cases were re-run after these changes and scored 29 of 30. Cases 4, 6, and 7 passed in full. The remaining miss is on case 12, where the run added "sortmerge requires Node.js 20 or newer" to the Install section and the grader read the Prerequisites assertion's rationale as banning the sentence, not just the section. It is recorded rather than patched. The assertion's letter was satisfied, the sentence is evidenced by the `engines` field, and one observation of a borderline judgment does not justify a rule. Case 6's first grader died on an API error mid-response, so its verdict comes from an independent re-grade.

## Iteration 5

The feature bullet rule changed shape by explicit direction: descriptions are now one full present-tense sentence leading with an active verb and ending with a period, labels are one to four words in sentence case, and clauses were added for specific verbs, for reserving "Supports" for compatibility, and for separating automatic behavior from opt-in configuration. This was a directed style decision rather than a fix, so only a spot check ran: cases 1 and 9, one run each, graded with an added shape audit. Both passed every assertion, 15 of 15, and every produced bullet satisfied all three shape properties. The primary READMEs themselves still carry fragment bullets, so the next refresh of those repositories will rewrite their feature lists.

A follow-up tightened length: descriptions stay as short as accuracy allows, aiming for the whole bullet to render on one line, which usually means eight to fifteen words. Case 3 spot-checked the change at 8 of 8, with a maximum of 93 visible characters and 12 words per description across its four bullets.

## Iteration 6

The opening chrome rules changed by explicit direction, modeled on nuxt/scripts and nuxt/image: a linked banner, a reference-style badge block, and Documentation and Playground bullets now open the README when, and only when, the repository provides them. A banner needs the committed asset, badges need a published package with a release path, and each bullet needs a real target. The glowline fixture and case 14 cover the positive path.

The first verification pass ran cases 14, 13, and 9 at 25 of 26. Case 14 passed in full, so found chrome is assembled correctly, and case 9 confirmed nothing leaks into a plain library. The one failure was case 13, where the runner gave pomo-cli a standalone license badge, since the first wording made a LICENSE file alone count as badge evidence. Both Nuxt references derive their license badge from npm, so the rule was tightened: the badge block belongs to published packages, and a LICENSE file alone earns no badge. Case 13 re-ran at 10 of 10.

The frontmatter description also changed in this revision, from "no badges and no hero artwork" to the conditional phrasing. The 20 of 20 trigger measurement predates that edit and was not re-run: the changed clause describes the output style rather than the activation conditions, and every trigger-bearing phrase is untouched. Treat the trigger score as measured against the previous description until the protocol runs again.

## Iteration 7

A final consistency review with three independent reviewers closed out the chrome revision. Its main finding was a blocker: the refinement rule still ordered unconditional badge and artwork removal from the pre-chrome era, which on a published package with an earned banner and badge block would have stripped exactly what the style now requires. The rule now follows the inclusion tests in both directions. The review also caught a template instruction that would have deleted the required `<!-- Badges -->` marker, a drifted duplicate of the chrome inclusion tests in the style guide, and stale counts and cross references, all fixed.

Case 12 re-ran after its fixture heading moved to `🚀 Quick Start` and passed 9 of 9. The run also added the install-implied runtime sentence again, the same borderline iteration 4 recorded, so with two observations the Prerequisites rule now says not to restate that runtime as prose either.

Trigger pass 3 ran the full corrected-harness protocol against the description as revised in iteration 6: twenty queries, three runs each. All twenty passed, every should-trigger at a rate above one half and every should-not below it, so the iteration 6 caveat is resolved.

## Iteration 8

Two cases now guard the refinement path for chrome, the rule whose blocker iteration 7 fixed without coverage. Case 15 gives hoverkit, a published package whose README already carries the earned banner, badges, and bullets, a tighten-the-wording request, and every piece of chrome must survive. Case 16 gives pixelfont, a private package whose README carries badges without a publish path and a banner without an asset, a tidy-up request, and the chrome must go with the removal stated to the user. Both passed in full on their first run, 9 of 9 and 8 of 8, taking the suite to 123 assertions over 16 cases and eleven fixtures.

The prose punctuation scan that had been run by hand all along now runs in CI, and its first repository-wide pass caught real contamination: a pass 3 trigger run had written a README into the real har2pdf fixture, which sat unnoticed in one commit until the scan flagged its semicolons. The stray file is removed, the committed driver at `scripts/trigger_run.py` now verifies the source repository after every run, and the trap is recorded under Trigger measurement.

## Iteration 9

Three directed refinements landed without a measurement run, since none touches an assertion. Counts that grow with the project round down to a stable floor in feature bullets, 100+ rather than 123, while counts that are themselves the fact stay exact. A feature label may carry a link when the feature has a canonical page, adapted from the nuxt-ai-ready README, with the colon kept inside the bold. And the bullet range widened from four to nine to about four to fifteen, with room past fifteen when the project genuinely earns it. The repository README applies the first two.

## Iteration 10

A delta review of everything since the iteration 7 full review surfaced one real gap and a set of small repairs. The gap: hoverkit's README omitted the Configuration and Development sections its own scripts, options, and release workflow earn under the section rules, so a rule-following run on case 15 had to choose between compliance and the assertion pinning the section list. The fixture now carries both sections and the assertion names all six. The repairs: the counts rule gained a discriminator so small nameable sets stay exact, the bullet range gained its bottom-end escape so a two-capability project is not pressured to pad, a linked feature label now explicitly counts as the first meaningful mention, case 16 gained an assertion against the impossible public npm install for a private package, the prose checker's dash test now honors the inline-code exemption it claimed, and the trigger driver's contamination check diffs against the pre-run state instead of flagging the developer's own edits.

Cases 15 and 16 re-ran after the changes and passed 18 of 18, taking the suite to 124 assertions.

## Trigger measurement

The documented three-runs-per-query protocol was executed twice against the twenty queries, because the first pass exposed a harness artifact rather than a description problem.

The stock harness runs each query in an empty project root and counts a run as triggered only when the first tool call consults the skill. Under those conditions every should-not-trigger query passed at a rate of 0.00, and nine of ten should-trigger queries failed, most at 0.00. A controlled diagnostic that placed a real small repository in the project root flipped the outcome: the very first tool call became the skill invocation. The failures measured the missing repository, not the description.

The second pass therefore used a corrected harness: each run received its own isolated copy of a small real repository as its project root, and detection accepted a skill consult at any point in the session within a 120 second budget.

That harness has one more trap worth knowing before anyone runs it again. It sends `SIGKILL` to each `claude` process as soon as a verdict is reached, which that process cannot catch, so it never shuts down the MCP servers it started. Those servers are reparented to the init process and survive. A well behaved server exits when its stdin closes, but one that does not will sit spinning, and a hundred or so runs can leave enough of them to saturate several CPU cores. Spawn each run in its own process group with `start_new_session=True` and signal the group with `os.killpg` rather than the single process.

| Pass | Harness | Result |
| ---- | ------- | ------ |
| 1 | Stock, empty project root, first tool call only | 11 of 20. Every negative correct, nine of ten positives failed. |
| 2 | Corrected, real repository root, any-point detection | 20 of 20. Every positive at 3 of 3, every negative at 0 of 3. |
| 3 | Corrected, re-run after the iteration 6 description change | 20 of 20. Every positive above one half, every negative below it. |

All passes ran on claude-fable-5 with three runs per query, with nothing tuned against either split. The description changed in iteration 6, so pass 3 repeated the protocol against the description as it ships. The current trigger score is pass 3. The driver is committed at [`scripts/trigger_run.py`](../../scripts/trigger_run.py), one query per invocation, printing TRIGGERED or NOT_TRIGGERED.

The harness has a third trap beyond the two above. A nested session running with permissions skipped can wander outside its temporary project root: one pass 3 run, given the query that names har2pdf, located the real fixture on disk and wrote a README into it. The committed driver now checks the source repository for modifications after every run and warns loudly. Verify `git status` is clean after any harness campaign before staging eval directories wholesale.
