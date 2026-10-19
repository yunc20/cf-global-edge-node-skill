# Changelog

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
