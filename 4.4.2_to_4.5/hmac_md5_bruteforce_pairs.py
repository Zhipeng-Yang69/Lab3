import sys, hmac, hashlib, itertools, time
from multiprocessing import Pool, cpu_count

def load_list(path, maxlen=6):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and line.strip().isalpha() and len(line.strip()) <= maxlen]

def case_variants(s, allcases_maxlen=0):
    # yield lower, Title, UPPER and optionally all permutations for short strings
    yield s.lower()
    yield s.title()
    yield s.upper()
    if allcases_maxlen and len(s) <= allcases_maxlen:
        # yield all nontrivial permutations (skip the ones already yielded)
        letters = list(s)
        for mask in range(1, 1 << len(letters)):
            cand = ''.join(letters[i].upper() if ((mask >> i) & 1) else letters[i].lower() for i in range(len(letters)))
            yield cand

def check_pair(args):
    key, text, target_hex, allcases_maxlen = args
    for kv in dict.fromkeys(case_variants(key, allcases_maxlen)):
        kb = kv.encode('utf-8')
        for tv in dict.fromkeys(case_variants(text, allcases_maxlen)):
            mac = hmac.new(kb, tv.encode('utf-8'), hashlib.md5).hexdigest()
            if mac == target_hex:
                return (kv, tv, mac)
    return None
def main():
'''
    if len(sys.argv) < 4:
        print("Usage: python3 hmac_md5_bruteforce_pairs.py target_hex female_names.txt author_names.txt [allcase_maxlen]")
        sys.exit(2)
'''
    target = sys.argv[1].lower()
    female_file = sys.argv[2]
    author_file = sys.argv[3]
    allcases_maxlen = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    females = load_list(female_file)
    authors = load_list(author_file)

    print(f"Loaded {len(females)} female keys and {len(authors)} author texts. total combos = {len(females)*len(authors)}")
    if not females or not authors:
        print("Wordlists empty or contain invalid entries.")
        sys.exit(1)

    pairs = [(k,t,target,allcases_maxlen) for k in females for t in authors]

    start = time.time()
    found = None
    procs = max(1, min(cpu_count(), 8))
    with Pool(processes=procs) as pool:
        for res in pool.imap_unordered(check_pair, pairs, chunksize=32):
            if res:
                found = res
                pool.terminate()
                break
    elapsed = time.time() - start
    if found:
        print("FOUND!")
        print("Key:", found[0])
        print("Text:", found[1])
        print("HMAC:", found[2])
    else:
        print("No match found in provided lists with requested variants.")
    print(f"Elapsed: {elapsed:.2f}s")

if __name__ == "__main__":
    main()
