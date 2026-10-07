# Contributing

Thanks for helping make this guide useful to working developers. Prefer a small, well-supported improvement over a long list of links.

This is currently a private review draft. The owner must select a repository license before public release or accepting outside contributions; see [attribution](docs/attribution.md).

## What belongs here

- A clearer explanation, concrete exercise, or important failure mode
- A primary source that teaches something the existing resources miss
- A correction to an API, protocol revision, compatibility claim, or cost assumption
- An offline test for an example's failure or authorization boundary
- A maintained translation that preserves source attribution and concept IDs

Read the [resource quality policy](docs/resource-policy.md). Disclose affiliation with any resource you suggest. Do not add affiliate links, paid-placement rankings, unverifiable benchmark claims, or promotional listicles.

## Edit the source of truth

1. Choose core topics for practical value, not a target count. Edit core-topics.json to add, merge, reorder, or remove README topics. Each topic lists its chapter IDs and a curated subset of HTTPS resource URLs from those chapters.
2. Edit the concept's note in concepts/ and its metadata in concepts.json when needed. Keep existing chapter IDs and paths stable so deep links continue to work; new IDs need only be unique positive integers. Chapters outside the core list appear automatically under Further reading.
3. Include why it matters, a build exercise, a caution, and at least two relevant primary sources.
4. Open the sources and confirm that the linked section still teaches the stated topic. Update the review date only after review.
5. Regenerate the README's marked indexes:

```sh
python3 scripts/render_readme.py
```

Do not manually edit content between the generated markers in README.md. The introduction, labs, and contribution sections are ordinary editable Markdown.

## Validate the change

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_content.py
python3 scripts/check_links.py
python3 scripts/render_readme.py --check
python3 examples/bounded_agent.py --eval
python3 -m compileall -q examples scripts tests
```

An optional external check makes public HTTP requests:

```sh
python3 scripts/check_links.py --external --json
```

Blocked, rate-limited, or timed-out URLs require review; do not silently mark them healthy. HTTP success does not prove source relevance. The checker supports the simple inline links used in this repository, not every Markdown extension.

## Example changes

- Keep the default run offline, deterministic, and credential-free.
- Require an explicit live flag for inference. State billing, data destinations, model requirements, and teardown.
- Add failure tests. Do not use production customer data or paste secrets into fixtures, logs, issue reports, or screenshots.
- Do not claim a live integration passed when only its fake client was tested.
- Keep dependencies minimal. If a dependency is added, explain the version policy and how it is updated.

## Pull request checklist

- [ ] The change has a concrete learning benefit
- [ ] Sources are primary, relevant, and reviewed with a date
- [ ] Existing concept IDs and local links remain valid
- [ ] Generated README sections are current
- [ ] Offline tests pass and any live-test limitations are disclosed
- [ ] No credentials, private account IDs, personal records, or copied unlicensed prose are included
- [ ] Affiliation and attribution are clear
