# Changelog

## v3 (2026-10-19): merge original + field notes + community tutorials

One coherent version built from three inputs: free-dam-man's original v2 Skill (structure kept), our v2 field notes, and the most useful, verified parts of well-known community tutorials. Every borrowed step cites its source. Placeholders only.

Added
- `docs/tutorial-zh.md` rewritten as a 17-section beginner guide: how it works, prerequisites, route choice (Pages+CNAME vs Workers+custom domain), free-domain comparison (DNSHE tested; DigitalPlat / eu.org community-reported), web and wrangler deploys, variable table, domain binding, every ADD.txt line type, CF port families, CloudflareSpeedTest on Win10, region advice for AI, proxyip explained, Shadowrocket / Clash Verge / v2rayN import, TLS fragment for blocked domains, swap loop, maintenance and upgrades, security, FAQ table, VPS alternative.
- `SKILL.md` 3.5: PROXYIP and Cloudflare-hosted destinations (CF doc: Workers cannot `connect()` to CF IP ranges; code L44-49 auto per-colo default with fallback; `whatismyip` vs `ip.sb` check from yonggekkk).
- `SKILL.md` 7A: ADD.txt line types (IPv4/IPv6/domain, `https://` list, `sub://`, pass-through `vless://` nodes, chain-proxy labels, `*` wildcard), code-verified line refs; CF port families.
- `SKILL.md` 7B: operator-side CloudflareSpeedTest recipe (XIU2 README v2.3.5): proxy off, `-httping -cfcolo`, `-dd`, modest `-n`, IPv6 option.
- `SKILL.md` 9: troubleshooting rows for proxyip failures, AI region refusal, blocked custom domain (new subdomain or client TLS fragment, L353), UDP limits, CFST anomalies.
- `SKILL.md` 10: v2rayN as the no-converter Windows option; TLS fragment option semantics.
- `SKILL.md` 12: CF ToS note quoted from XIU2, public-generator warning from WorkerVless2sub, never set `URL` to someone else's site.
- `SKILL.md` 14 maintenance/upgrade procedure (re-pin on upgrade), 15 VPS alternative (sing-box-yg / 233boy, Reality first, merge VPS node via ADD.txt), 16 merge index.
- Final Delivery Checklist: CF-hosted-site / proxyip check and maintenance note.

Changed
- `SKILL.md` 1: pin re-checked against upstream `main` HEAD a8ab111 (2026-10-09), still byte-identical; community sources listed.
- `SKILL.md` 3.2 + `templates/env.example` + wrangler templates: `URL` (leave unset) and the other optional env switches documented.
- `templates/ADD.txt.example`: other accepted line types.
- `README.md` rewritten: overview, what's new in v3 with sources, credits.
- `docs/x-thread-zh.md` refreshed (speed test, proxyip, repo link).

Unchanged on purpose
- Gate (Section 0), W1-W7 wizard with 第X/6步 numbering, heads-up card, Branch D, region loop 0B, pin + SHA-256, token formula, two-stage ADD.txt rule, QR delivery.

## v2-field-notes (2026-10-19)

Folds in a second, independent production build (Route B, mainland-China operator, Shadowrocket + Clash Verge). All values de-identified; placeholders only.

Added
- `SKILL.md` Section 13: field-notes index for the second build.
- Section 6: "Pages direct upload of the pinned file" recipe (wrangler 4.x / Node 22) that keeps the Section 2 SHA-256 pin, plus wrangler environment fixes (`WRANGLER_SEND_METRICS=false`, project-local `WRANGLER_CACHE_DIR`, empty `node_modules/`).
- Branch D2 field notes: DNSHE rejects some disposable/bot mailbox domains (mainstream mailbox worked), TOTP 2FA must be bound before claiming, 1-year `us.ci` term with free renewal from 180 days before expiry.
- Section 4 privacy notes (code-verified): panel UI is loaded from `edt-pages.github.io`; Clash/sing-box conversion goes through the `SUBAPI` backend, which sees domain/entry IPs but not the UUID.
- Section 7 relay notes: non-443 relay ports, transparent-SNI-proxy false positives on 443, xray end-to-end exit check (`loc` + exit-IP geo over `colo`), Globalping is only a hint, ship backups and swap timed-out nodes after the phone test.
- Region advice: avoid HK for AI services; TW/JP/SG + US fallback; TW relays scarce.
- Section 10: Clash Verge (Windows) import steps.
- Section 9: troubleshooting rows (phone timeouts after server-side pass, 443 SNI-proxy artefacts, wrangler EACCES `/node_modules`, DNSHE email/TOTP, flagged project name).
- Section 12: only original-author repos (malicious forks exist); personal use only, sharing/reselling is the main ban trigger.
- `templates/wrangler.pages.toml.example`, `templates/sub_token.py` (token cross-check), `templates/probe_e2e.py` (TLS + xray end-to-end exit check).
- `docs/tutorial-zh.md` (beginner tutorial, Chinese) and `docs/x-thread-zh.md` (short thread version).

Changed
- W3 and gate item 2: suggest a neutral project name (`notes-blog`), avoid proxy-sounding words (field anecdote: a proxy-sounding name got flagged, a neutral rebuild passed).
- `templates/ADD.txt.example`: non-443 examples, verified-exit labels, backup guidance.
- Section 2: pin re-checked against upstream `main` on 2026-10-19 (still byte-identical).
- README: v2 summary, credits/attribution, updated file list.

## v2 (2026-10-17, original author)

See the README "v2 修订" paragraph and the upstream history of free-dam-man/cf-global-edge-node-skill.
