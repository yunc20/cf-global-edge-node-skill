#!/usr/bin/env python3
"""TLS + end-to-end exit check for preferred-entry candidates (SKILL.md Sections 0B R3 / 7).

For each candidate: (1) TLS handshake to IP:PORT with SNI=<HOST>; (2) if OK, start a one-node
xray-core VLESS+WS+TLS client and fetch cdn-cgi/trace + an IP-geo lookup through it.
Judge the region by loc= and exit-IP geolocation; colo= is only a hint.

Usage:
  HOST="<HOST>" UUID="<UUID>" XRAY=/path/to/xray python3 probe_e2e.py candidates.json results.json
candidates.json: [{"ip": "<ENTRY_IP>", "port": 8443, "req": "JP"}, ...]

Caveats: run from a network without a transparent proxy. If the agent box intercepts 443 by SNI,
443 results are void (prefer 2053/2083/2087/8443). Passing here does not guarantee the operator's
carrier can reach the entry; keep backups and confirm with one real client test.
Never commit candidates.json/results.json together with a subscription URL.
"""
import concurrent.futures as cf, json, os, socket, ssl, subprocess, sys, tempfile, time

HOST, UUID = os.environ.get("HOST", ""), os.environ.get("UUID", "")
XRAY = os.environ.get("XRAY", "xray")
GEO = os.environ.get("GEO_URL", "https://ipinfo.io/json")

def tls(c):
    ctx = ssl.create_default_context()
    try:
        t = time.time()
        with socket.create_connection((c["ip"], c["port"]), timeout=6) as s:
            with ctx.wrap_socket(s, server_hostname=HOST) as x:
                return f"OK {x.version()} {int((time.time() - t) * 1000)}ms"
    except Exception as e:
        return f"FAIL {type(e).__name__}"

def curl(port, url):
    return subprocess.run(["curl", "-s", "-m", "15", "-x", f"socks5h://127.0.0.1:{port}", url],
                          capture_output=True, text=True).stdout

def e2e(i, c):
    port = 11000 + i
    cfg = {"log": {"loglevel": "none"},
           "inbounds": [{"port": port, "listen": "127.0.0.1", "protocol": "socks"}],
           "outbounds": [{"protocol": "vless",
                          "settings": {"vnext": [{"address": c["ip"], "port": c["port"],
                                                  "users": [{"id": UUID, "encryption": "none"}]}]},
                          "streamSettings": {"network": "ws", "security": "tls",
                                             "tlsSettings": {"serverName": HOST, "fingerprint": "chrome"},
                                             "wsSettings": {"path": "/", "headers": {"Host": HOST}}}}]}
    fd, fn = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(cfg, f)
    p = subprocess.Popen([XRAY, "run", "-c", fn], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.5)
        t = time.time()
        tr = dict(l.split("=", 1) for l in curl(port, "https://www.cloudflare.com/cdn-cgi/trace").splitlines() if "=" in l)
        ms = int((time.time() - t) * 1000)
        if not tr:
            return "E2E-FAIL"
        try:
            g = json.loads(curl(port, GEO))
            geo = f"{g.get('country')}/{g.get('city')}/{g.get('org')}"
        except Exception:
            geo = "geo-fail"
        return f"loc={tr.get('loc')} colo={tr.get('colo')} exit={tr.get('ip')} geo={geo} {ms}ms"
    finally:
        p.kill()
        os.remove(fn)

def run(ic):
    i, c = ic
    c["tls"] = tls(c)
    c["e2e"] = e2e(i, c) if c["tls"].startswith("OK") else "skip"
    c["match"] = bool(c.get("req")) and f"loc={c['req']}" in c["e2e"]
    return c

def main():
    if not HOST or not UUID or len(sys.argv) != 3:
        sys.exit(__doc__)
    cands = json.load(open(sys.argv[1]))
    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, enumerate(cands)))
    with open(sys.argv[2], "w") as f:
        json.dump(res, f, indent=1)
    os.chmod(sys.argv[2], 0o600)
    for c in res:
        print(f"{c.get('req','?'):<3} {c['ip']}:{c['port']:<6} {c['tls']:<22} {c['e2e']}  {'MATCH' if c['match'] else ''}")

if __name__ == "__main__":
    main()
