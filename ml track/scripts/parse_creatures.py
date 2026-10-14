import csv, re

with open(r'creatures_table_final.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
rows = [r for r in rows if r['creature_name'].strip()]

num_map = {
    'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,
    'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12,'thirteen':13,
    'fourteen':14,'fifteen':15,'sixteen':16,'twenty':20,'fifty':50,
    'dozens':24,'many':-1,'numerous':-1,'hundreds':-1,'thousands':-1
}
limb_kinds = r'arms?|tentacles?|limbs?|legs?|appendages?|fins?|cirri|feelers?|vines?|threads?|filaments?'

def parse(desc):
    desc_l = desc.lower()
    results = []
    # digit + limb-word
    for m in re.finditer(r'(\d+)\s+(?:' + limb_kinds + r')', desc_l):
        results.append((int(m.group(1)), m.group(0).strip()))
    # word-number + limb-word
    for word, val in num_map.items():
        pat = r'\b' + word + r'\s+(?:' + limb_kinds + r')\b'
        for m in re.finditer(pat, desc_l):
            results.append((val, m.group(0).strip()))
    # deduplicate preserving order
    seen = set()
    out = []
    for item in results:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

print("=" * 130)
print(f"{'#':<3} {'Creature':<26} {'Audio File':<28} {'Limb Mentions':<50} {'Note'}")
print("=" * 130)

for i, r in enumerate(rows, 1):
    name  = r['creature_name'].strip()
    audio = r['audio_file'].strip()
    desc  = r['creature_description'].strip()
    limbs = parse(desc)
    lstr  = '; '.join(f'{n} {k}' for n,k in limbs) if limbs else '-- (indeterminate/many)'
    counts = [n for n,k in limbs if n > 0]
    note = f'TOTAL={sum(counts)}' if counts else ''
    print(f"{i:<3} {name:<26} {audio:<28} {lstr:<50} {note}")

print()
print("=" * 130)
print()
print("SUMMARY: CREATURES WITH EXACT LIMB COUNTS")
print("-" * 80)
for i, r in enumerate(rows, 1):
    name  = r['creature_name'].strip()
    desc  = r['creature_description'].strip()
    limbs = parse(desc)
    counts = [n for n,k in limbs if n > 0]
    if counts:
        total = sum(counts)
        detail = '; '.join(f'{n} {k}' for n,k in limbs if n > 0)
        print(f"  {name:<28} -> {detail}  [TOTAL APPENDAGES = {total}]  [SQUARED = {total**2}]")

print()
print("SPECIAL FOCUS: creature with unique/non-standard limb count")
print("-" * 80)
for i, r in enumerate(rows, 1):
    name  = r['creature_name'].strip()
    desc  = r['creature_description'].strip()
    limbs = parse(desc)
    counts = [n for n,k in limbs if n > 0]
    if counts:
        total = sum(counts)
        if total not in (8, 10):   # flag non-standard counts
            detail = '; '.join(f'{n} {k}' for n,k in limbs if n > 0)
            print(f"  *** {name:<26} -> {detail}  [TOTAL={total}]  [SQUARED={total**2}]  ***")
