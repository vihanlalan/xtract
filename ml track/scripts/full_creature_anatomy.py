"""
Full manual cross-reference of every creature's description.
We print every creature with its full description + all limb-related
phrases highlighted, so nothing is missed by regex.
"""
import csv, re

with open(r'creatures_table_final.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
rows = [r for r in rows if r['creature_name'].strip()]

# All number words we care about
num_words = ['one','two','three','four','five','six','seven','eight','nine','ten',
             'eleven','twelve','thirteen','fourteen','fifteen','sixteen','twenty',
             'fifty','dozens','many','numerous','hundreds','thousands']

# limb-related words
limb_kws = ['arm','tentacle','limb','leg','appendage','fin','cirri','feeler',
            'vine','thread','filament','sucker','whisker','claw','head','wing']

def highlight(desc):
    """Find all sentences/phrases mentioning limbs or counts near limbs."""
    hits = []
    words = desc.lower().split()
    for i, w in enumerate(words):
        clean = re.sub(r'[^a-z]', '', w)
        if clean in num_words or re.match(r'^\d+$', clean):
            # grab context window
            window = words[max(0,i-2):i+4]
            hits.append(' '.join(window))
        for lk in limb_kws:
            if lk in clean:
                window = words[max(0,i-3):i+3]
                hits.append(' '.join(window))
    # deduplicate
    seen = set()
    out = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out

print("=" * 120)
print("COMPLETE CREATURE ANATOMY CROSS-REFERENCE")
print("=" * 120)

for i, r in enumerate(rows, 1):
    name  = r['creature_name'].strip()
    desc  = r['creature_description'].strip()
    audio = r['audio_file'].strip()
    hits  = highlight(desc)
    
    print(f"\n#{i:02d}  [{name}]  ({audio})")
    print(f"     DESC: {desc}")
    if hits:
        print(f"     KEY PHRASES: {' | '.join(hits)}")
    else:
        print(f"     KEY PHRASES: (none matched)")

print()
print("=" * 120)
print("EXPLICIT LIMB COUNT TABLE (manual annotation)")
print("=" * 120)

# Manual table after reading all descriptions carefully
manual = [
    # (name, limb_count, limb_type, note)
    ("Kraken",                   8,  "arms",         "bulbous mantle + eight muscular arms"),
    ("Common Octopus",           8,  "arms",         "eight flexible arms"),
    ("Dumbo Octopus",            8,  "arms",         "eight short arms"),
    ("Argonaut",                 8,  "arms",         "eight sucker-bearing arms"),
    ("Blue-Ringed Octopus",      8,  "arms",         "eight sucker-lined arms"),
    ("Mimic Octopus",            8,  "arms",         "long-armed (implied 8, octopus)"),
    ("Giant Pacific Octopus",    8,  "arms",         "eight thick sucker-covered arms"),
    ("Coconut Octopus",          8,  "arms",         "eight sucker-lined arms"),
    ("Glass Octopus",            8,  "arms",         "eight delicate arms"),
    ("Blanket Octopus",          8,  "arms",         "eight arms"),
    ("Giant Squid",             10,  "limbs",        "eight arms + two long feeding tentacles"),
    ("Colossal Squid",          10,  "limbs",        "eight arms + two feeding tentacles"),
    ("Cuttlefish",              10,  "limbs",        "eight arms + two retractable feeding tentacles"),
    ("Bobtail Squid",           10,  "limbs",        "eight arms + two longer tentacles"),
    ("Vampire Squid",            8,  "arms",         "eight webbed arms (no feeding tentacles)"),
    ("theara",                   0,  "cirri",        "dozens of slender cirri instead of eight arms — NOT 8"),
    ("Ram's Horn Squid",        10,  "limbs",        "ten limbs (explicit)"),
    ("Chambered Squid",         10,  "limbs",        "ten limbs (explicit, fictional)"),
    ("Lion's Mane Jellyfish",   -1,  "tentacles",    "hundreds or thousands — indeterminate"),
    ("Moon Jellyfish",          -1,  "tentacles",    "many fine marginal tentacles — indeterminate"),
    ("Box Jellyfish",           -1,  "tentacles",    "clusters from four corners — indeterminate"),
    ("Sea Anemone",             -1,  "tentacles",    "many short stinging tentacles"),
    ("Hydra",                   -1,  "tentacles",    "ring of stinging tentacles — indeterminate"),
    ("Portuguese Man o War",    -1,  "threads",      "very long stinging fishing threads — indeterminate"),
    ("Sea Cucumber",            -1,  "tentacles",    "branching feeding tentacles — indeterminate"),
    ("Sun Star",                -1,  "arms",         "numerous arms (20+) — indeterminate"),
    ("Feather Star",            -1,  "arms",         "many feathery arms — indeterminate"),
    ("Brittle Star",             5,  "arms",         "five long thin arms (explicit)"),
    ("Nudibranch",              -1,  "gills",        "external gills/projections — no limb count"),
    ("Sea Hare",                -1,  "flaps",        "ear-like sensory flaps — no limb count"),
    ("Octo-Jelly",               8,  "limbs",        "eight smooth octopus-like trailing limbs (explicit, fictional)"),
    ("Spider-Squid",             8,  "limbs",        "eight thin limbs (explicit, fictional)"),
    ("Tentacle-Ball",           50,  "appendages",   "fifty short sucker-bearing appendages (explicit, fictional)"),
    ("Eight-Leg Eel",            8,  "limbs",        "eight short smooth limbs near its head (explicit, fictional)"),
    ("Ghost Cephalopod",         6,  "arms",         "six arms covered in pale suction cups (explicit, fictional)"),
    ("Sucker-Plant",            12,  "vines",        "twelve thick vines (explicit, fictional)"),
    ("Neon Squid",              10,  "limbs",        "eight arms + two tentacles (explicit, fictional)"),
    ("Deep-Sea Horror",          9,  "limbs",        "nine uneven limbs (explicit, fictional)"),
    ("False Kraken",             8,  "arms",         "eight-armed (name says it all, explicit, fictional)"),
    ("Abyssal Medusa",          12,  "tentacles",    "twelve ribbon-like tentacles (explicit, fictional)"),
    ("Coral Wraith",            -1,  "arms",         "many branch-like arms — indeterminate"),
    ("Leviathan Eel",            4,  "feelers",      "four whisker-like feelers (explicit)"),
    ("Merrow",                  -1,  "hands",        "webbed hands, no count given"),
    ("Kelpie",                  -1,  "",             "horse — no appendage count"),
    ("Hippocampus",             -1,  "",             "horse forebody + fish tail — no count"),
    ("Scylla",                  -1,  "limbs",        "multiple writhing lower limbs — indeterminate"),
    ("Charybdis",               -1,  "",             "whirlpool — no appendages"),
    ("Siren",                   -1,  "",             "singer — no appendage count"),
    ("Nereid",                  -1,  "",             "nymph — no appendage count"),
    ("Megalodon",               -1,  "",             "shark — fins, no count"),
    ("Sea Serpent",             -1,  "",             "serpent body + finned crest — no count"),
    ("Cthulhu",                 -1,  "tendrils",     "facial tendrils + wings — indeterminate"),
    ("Akkorokamui",             -1,  "tentacles",    "enormous tentacles — indeterminate"),
    ("Umibozu",                 -1,  "",             "humanoid — no appendage count"),
    ("Mizuchi",                 -1,  "",             "dragon/serpent — no count"),
    ("Tiamat",                  -1,  "",             "dragon-like — no count"),
    ("Jormungandr",             -1,  "",             "world serpent — no appendages"),
]

print(f"\n{'#':<3} {'Creature':<26} {'Count':>6} {'Type':<12} {'Notes'}")
print("-" * 110)
special = []
for i, (name, cnt, kind, note) in enumerate(manual, 1):
    cnt_str = str(cnt) if cnt >= 0 else "?"
    sq_str  = str(cnt**2) if cnt > 0 else "-"
    marker  = "  <-- UNIQUE" if cnt > 0 and cnt not in (8, 10) else ""
    print(f"{i:<3} {name:<26} {cnt_str:>6} {kind:<12} {note}{marker}")
    if cnt > 0:
        special.append((name, cnt, kind))

print()
print("=" * 110)
print("ALL CREATURES WITH POSITIVE LIMB COUNTS + SQUARED VALUES")
print("=" * 110)
for name, cnt, kind in special:
    sq = cnt ** 2
    flag = "  *** NON-STANDARD (not 8 or 10) ***" if cnt not in (8, 10) else ""
    print(f"  {name:<28}  limbs={cnt:>3}  squared={sq:>5}  ({kind}){flag}")
