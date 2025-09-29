#!/usr/bin/env python3
import hashlib
import sys

# Put the target hashes here (lowercase hex)
targets = {
    "db9a2da27f2ed3e04823fd17160e7c94": "MD5",
    "482b2d5c05d5b8cb9ae886cf8642fd5f": "MD5",
    "ef2b06c668f2259f3977c0f74cfd76d8a9da12ae342ffd030616414ac4ab506b852908413d7fde1367bb6e4ffa3d6d5": "SHA3-384",
    "b9e3c87ae6e63e306f6a6c1367bcff35c017083539d6fe5e0384ff412758dab2637d6812de0feac05486ca05d48ca13": "SHA3-384",
}

found = {}

def md5_newline(s: bytes) -> str:
    return hashlib.md5(s + b"\n").hexdigest()

def sha3_384_newline(s: bytes) -> str:
    return hashlib.sha3_384(s + b"\n").hexdigest()

if len(sys.argv) < 2:
    print("Usage: python3 find_newline_hashes.py wordlist.txt")
    sys.exit(1)

wordlist = sys.argv[1]
with open(wordlist, "rb") as f:
    for raw in f:
        w = raw.rstrip(b"\r\n")
        if not w:
            continue
        # Try lowercase/uppercase variants if you want:
        candidates = {w, w.lower(), w.capitalize(), w.upper()}
        for cand in candidates:
            h1 = md5_newline(cand)
            if h1 in targets and h1 not in found:
                found[h1] = cand.decode("utf-8", errors="replace")
                print("FOUND MD5:", h1, "->", found[h1])
            h2 = sha3_384_newline(cand)
            if h2 in targets and h2 not in found:
                found[h2] = cand.decode("utf-8", errors="replace")
                print("FOUND SHA3-384:", h2, "->", found[h2])
        # quick exit if we found all
        if len(found) == len(targets):
            break

print("Done. Found", len(found), "of", len(targets))
for k, v in found.items():
    print(k, "->", v)
