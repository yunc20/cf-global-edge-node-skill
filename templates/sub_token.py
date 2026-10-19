#!/usr/bin/env python3
"""Cross-check the edgetunnel subscription token: TOKEN = MD5MD5(host + uuid).

MD5MD5(x) = md5( md5hex(x)[7:27] )  (pinned _worker.js L5403-5415)

Usage (values come from env so they never land in shell history or files):
  HOST="<HOST>" UUID="<UUID>" python3 sub_token.py            # prints the subscription URL
  HOST=... UUID=... python3 sub_token.py --token-only
Compare with TOKEN in /admin/config.json; if they differ you used the wrong host or UUID.
The printed URL is a credential: do not paste it into public places.
"""
import hashlib, os, sys

def md5hex(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def md5md5(s: str) -> str:
    return md5hex(md5hex(s)[7:27])

def main() -> None:
    host = os.environ.get("HOST", "").strip().lower()
    uuid = os.environ.get("UUID", "").strip().lower()
    if not host or not uuid:
        sys.exit("Set HOST and UUID environment variables")
    token = md5md5(host + uuid)
    print(token if "--token-only" in sys.argv else f"https://{host}/sub?token={token}")

if __name__ == "__main__":
    main()
