# Resource quality and maintenance

## Selection

Prefer official documentation, specifications, maintained project documentation, and original research. First-party engineering articles are useful when labeled as experience from that implementation. Provider material can teach general patterns, but provider-specific guarantees must stay labeled.

Each concept should have a small reading path: enough resources to understand and build the idea, without turning the page into an unranked search result. Add videos only when the exact content has been reviewed; a recognizable channel alone is not evidence of quality.

A resource must:

1. Address the concept directly and teach an identifiable skill or decision.
2. Have clear authorship and a stable, accessible URL.
3. Distinguish evidence, examples, and marketing claims.
4. State relevant version or compatibility limits when those affect the example.
5. Add value beyond links already present.

Do not copy third-party prose or code without checking its license and attribution requirements. No affiliate links, sponsored ranking, invented endorsements, or unsupported “best model” claims.

## Dates mean specific things

A chapter's Resource review date is when its primary resources were opened and checked for topic and current interface guidance. It is not the article's publication date, proof of every claim, or a live integration test date.

An HTTP link-check result reports whether the URL responded at that moment. It does not prove the right content is still at the address, validate an external fragment, or test an API. Keep these two checks distinct.

## Maintenance cadence

Recommended maintainer practice, not an installed automation:

- Review broken-link reports and consequential API changes when reported.
- Recheck provider setup labs, protocol versions, model-access behavior, and security guidance before a release.
- Periodically sample every concept's resources for relevance and update the date only after review.
- Prefer canonical destinations after redirects, but keep durable legacy links where an official redirect is the supported entry point.
- Avoid hard-coded pricing and universal model IDs. Point readers to current catalogs and require explicit configuration.

## Link tooling

Run python3 scripts/check_links.py for local file and Markdown anchor checks. Run it with --external for bounded public HTTP checks. The latter uses a reviewed HTTPS-host allowlist, rejects URL credentials and unapproved ports/hosts, and never follows redirects. It uses HEAD, falls back to GET when HEAD is rejected, and reports redirects, blocked/rate-limited pages, and network failures as needing review. It does not authenticate to sites or bypass access restrictions. Review any proposed additions to REVIEWED_HOSTS in the script. The allowlist is not a network sandbox; use trusted DNS and appropriate egress controls, and never run arbitrary contributed code with secrets.

The parser intentionally handles this repository's inline Markdown links and simple headings. It ignores fenced code. If you introduce reference-style links, HTML anchors, or other Markdown extensions, extend the parser and its tests rather than relying on an unverified green result.

## Framework neutrality

The control-flow examples use plain Python so the essential contracts stay visible. Frameworks can be useful for durability, integration, and tracing, but they are optional implementations of the concepts. Evaluate the abstraction before adopting it; do not add a framework merely to complete the reading list.
