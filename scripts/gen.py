"""
Generates the pixel-art SVGs used by the profile README.

    python scripts/gen.py            # placeholder stats (no network)
    GH_TOKEN=xxx python scripts/gen.py   # live stats from the GitHub GraphQL API

Everything is drawn from a hand-made 5x7 pixel font, so no external
services or fonts are needed. Edit CONFIG below to change text/links.
"""
import datetime as dt
import json
import os
import pathlib
import urllib.request

# ----------------------------------------------------------------- CONFIG
CONFIG = {
    "user": "Kishore-suthersingh",
    "name": "KISHORE N",
    "role": "COMPUTER VISION + ML ENGINEER",
    "tagline": "CHENNAI, INDIA  -  AMRITA CCE '27",
    "class": "CV / ML ENGINEER",
    "buttons": ["PORTFOLIO", "LINKEDIN", "EMAIL", "RESUME"],
    "projects": [
        {
            "slug": "image-gen",
            "title": "DOMAIN IMAGE GEN PIPELINE",
            "desc": ["SD + CONTROLNET + LORA FINE-TUNING", "WITH A CLIP QUALITY GATE, FASTAPI"],
            "tags": ["SDXL", "LORA", "CLIP"],
        },
        {
            "slug": "synthetic-data",
            "title": "MULTI-MODAL SYNTHETIC DATA",
            "desc": ["TABULAR, SIGNAL + IMAGE DATA FROM", "NATURAL-LANGUAGE PROMPTS"],
            "tags": ["CTGAN", "REACT", "FASTAPI"],
        },
        {
            "slug": "eeg-bci",
            "title": "EEG BRAIN-COMPUTER INTERFACE",
            "desc": ["CNN/RNN BRAINWAVE CLASSIFIER FOR", "REAL-TIME MOTOR CONTROL"],
            "tags": ["PYTORCH", "EEG", "CNN"],
        },
        {
            "slug": "achievements",
            "title": "HALL OF FAME",
            "desc": ["1ST  - COGNISENCE CODING COMP", "5TH  - CODERS OF THE BLACKPEARL", "SIH - PRE-FINAL QUALIFIER"],
            "tags": [],
        },
    ],
}

# Sakura-at-night palette
BG, PANEL, BORDER = "#1b1325", "#261a33", "#ff8fb1"
PINK, LIGHT, TEAL, GOLD, DIM = "#ff8fb1", "#ffe1ec", "#7fe0d0", "#ffd86b", "#8f7fa3"

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ------------------------------------------------------------- PIXEL FONT
_F = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
    "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".###.|#...#|#....|#....|#....|#...#|.###.",
    "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####",
    "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".###.|#...#|#....|#.###|#...#|#...#|.####",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": ".###.|..#..|..#..|..#..|..#..|..#..|.###.",
    "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
    "N": "#...#|#...#|##..#|#.#.#|#..##|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
    "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.",
    "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|#.#.#|.#.#.",
    "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
    "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
    "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####",
    "3": "#####|...#.|..#..|...#.|....#|#...#|.###.",
    "4": "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.",
    "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": "..##.|.#...|#....|####.|#...#|#...#|.###.",
    "7": "#####|....#|...#.|..#..|.#...|.#...|.#...",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
    "9": ".###.|#...#|#...#|.####|....#|...#.|.##..",
    " ": ".....|.....|.....|.....|.....|.....|.....",
    "-": ".....|.....|.....|.###.|.....|.....|.....",
    "/": "....#|....#|...#.|..#..|.#...|#....|#....",
    ".": ".....|.....|.....|.....|.....|.##..|.##..",
    ",": ".....|.....|.....|.....|.##..|..#..|.#...",
    ":": ".....|.##..|.##..|.....|.##..|.##..|.....",
    "!": "..#..|..#..|..#..|..#..|..#..|.....|..#..",
    "'": "..#..|..#..|.#...|.....|.....|.....|.....",
    "+": ".....|..#..|..#..|#####|..#..|..#..|.....",
    "%": "##...|##..#|...#.|..#..|.#...|#..##|...##",
    ">": ".#...|..#..|...#.|....#|...#.|..#..|.#...",
    "<": "...#.|..#..|.#...|#....|.#...|..#..|...#.",
    "(": "...#.|..#..|.#...|.#...|.#...|..#..|...#.",
    ")": ".#...|..#..|...#.|...#.|...#.|..#..|.#...",
    "#": ".#.#.|.#.#.|#####|.#.#.|#####|.#.#.|.#.#.",
    "*": ".....|#.#.#|.###.|#####|.###.|#.#.#|.....",
}
FONT = {k: v.split("|") for k, v in _F.items()}


def text_width(s, scale):
    return max(0, len(s) * 6 * scale - scale)


def bitmap_path(rows, x0, y0, scale):
    """Turn a bitmap (list of strings) into a compact path, merging runs."""
    d = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == "#":
                start = c
                while c < len(row) and row[c] == "#":
                    c += 1
                w = (c - start) * scale
                d.append(f"M{x0 + start * scale} {y0 + r * scale}h{w}v{scale}h-{w}z")
            else:
                c += 1
    return "".join(d)


def text(s, x, y, scale, color, anchor="start", extra=""):
    s = s.upper()
    if anchor == "middle":
        x -= text_width(s, scale) // 2
    elif anchor == "end":
        x -= text_width(s, scale)
    d = []
    for i, ch in enumerate(s):
        glyph = FONT.get(ch, FONT["*"])
        d.append(bitmap_path(glyph, x + i * 6 * scale, y, scale))
    return f'<path fill="{color}" d="{"".join(d)}"{extra}/>'


def shadow_text(s, x, y, scale, color, shadow, anchor="start"):
    return text(s, x + scale, y + scale, scale, shadow, anchor) + text(s, x, y, scale, color, anchor)


PETAL = [".##..", "####.", "#####", ".####", "..##."]


def petal(x, y, scale, color, fall=None):
    p = f'<path fill="{color}" d="{bitmap_path(PETAL, 0, 0, scale)}"/>'
    if not fall:
        return f'<g transform="translate({x} {y})">{p}</g>'
    dur, dist, delay = fall
    return (
        f'<g transform="translate({x} {y})"><g>{p}'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{dist // 3} {dist}" '
        f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        f"</g></g>"
    )


def frame(w, h, px=4, fill=PANEL, border=BORDER):
    """Pixel-style panel with notched corners."""
    return (
        f'<rect x="{px}" y="0" width="{w - 2 * px}" height="{h}" fill="{border}"/>'
        f'<rect x="0" y="{px}" width="{w}" height="{h - 2 * px}" fill="{border}"/>'
        f'<rect x="{px}" y="{px}" width="{w - 2 * px}" height="{h - 2 * px}" fill="{fill}"/>'
    )


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'
    )


def write(name, content):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


# ------------------------------------------------------------------ STATS
def fetch_stats(user, token):
    today = dt.date.today()
    start = dt.date(today.year, 1, 1)
    query = """
    query($login:String!,$from:DateTime!,$to:DateTime!,$yfrom:DateTime!){
      user(login:$login){
        repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){
          totalCount
          nodes{ stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}} }
        }
        year: contributionsCollection(from:$yfrom,to:$to){ contributionCalendar{ totalContributions } }
        cal: contributionsCollection(from:$from,to:$to){
          contributionCalendar{ weeks{ contributionDays{ date contributionCount } } }
        }
      }
    }"""
    variables = {
        "login": user,
        "from": (today - dt.timedelta(days=364)).isoformat() + "T00:00:00Z",
        "to": today.isoformat() + "T23:59:59Z",
        "yfrom": start.isoformat() + "T00:00:00Z",
    }
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-readme-gen"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    u = data["data"]["user"]

    days = [d for w in u["cal"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    # current streak: if today has nothing yet, start counting from yesterday
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    current = 0
    while i >= 0 and counts[i] > 0:
        current += 1
        i -= 1
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)

    langs = {}
    stars = 0
    for repo in u["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]

    return {
        "year_contribs": u["year"]["contributionCalendar"]["totalContributions"],
        "current": current,
        "longest": longest,
        "repos": u["repositories"]["totalCount"],
        "stars": stars,
        "langs": [(n, s / total) for n, s in top],
    }


PLACEHOLDER = {
    "year_contribs": 0, "current": 0, "longest": 0, "repos": 0, "stars": 0,
    "langs": [("PYTHON", 0.62), ("JAVASCRIPT", 0.18), ("JUPYTER NOTEBOOK", 0.12), ("C++", 0.05), ("CSS", 0.03)],
}

# ---------------------------------------------------------------- DRAWING
def draw_header():
    w, h = 1000, 300
    b = [f'<rect width="{w}" height="{h}" fill="{BG}"/>']
    # stars
    for i in range(40):
        x, y = (i * 137) % w, (i * 71) % 150 + 8
        b.append(f'<rect x="{x}" y="{y}" width="3" height="3" fill="{DIM}" opacity="{0.3 + (i % 4) * 0.15}"/>')
    # pixel moon
    moon = ["..####..", ".######.", "########", "########", "########", "########", ".######.", "..####.."]
    b.append(f'<path fill="{LIGHT}" opacity=".9" d="{bitmap_path(moon, 860, 30, 8)}"/>')
    # ground + torii silhouette
    b.append(f'<rect y="270" width="{w}" height="30" fill="#140e1c"/>')
    b.append(f'<g fill="#3a2438"><rect x="40" y="200" width="150" height="10"/><rect x="50" y="215" width="130" height="8"/>'
             f'<rect x="70" y="200" width="10" height="70"/><rect x="150" y="200" width="10" height="70"/></g>')
    # falling petals
    for i in range(14):
        x = 30 + (i * 73) % 940
        b.append(petal(x, -10, 3, PINK if i % 3 else LIGHT, fall=(6 + i % 5, 280, -(i * 0.9))))
    # title
    b.append(shadow_text(CONFIG["name"], w // 2, 70, 12, PINK, "#5c2a4a", "middle"))
    b.append(text(CONFIG["role"], w // 2, 172, 4, LIGHT, "middle"))
    b.append(text(CONFIG["tagline"], w // 2, 212, 3, DIM, "middle"))
    blink = '<animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/>'
    b.append(f'<g>{text("PRESS START", w // 2, 245, 3, GOLD, "middle")}{blink}</g>')
    write("header.svg", svg(w, h, "".join(b), f"{CONFIG['name']} - {CONFIG['role']}"))


def draw_buttons():
    w, h = 230, 64
    for label in CONFIG["buttons"]:
        body = frame(w, h) + text("> " + label, w // 2, (h - 21) // 2, 3, LIGHT, "middle")
        write(f"btn-{label.lower()}.svg", svg(w, h, body, label))


def draw_card(stats, live):
    w, h = 1000, 320
    b = [frame(w, h)]
    level = stats["year_contribs"] // 50 + 1
    xp = (stats["year_contribs"] % 50) / 50
    year = dt.date.today().year

    # left column: player
    b.append(text("PLAYER 1", 40, 36, 2, DIM))
    b.append(shadow_text(CONFIG["name"], 40, 60, 5, PINK, "#5c2a4a"))
    b.append(text("CLASS: " + CONFIG["class"], 40, 116, 2, LIGHT))
    b.append(text(f"LVL {level}", 40, 150, 4, GOLD))
    b.append(f'<rect x="40" y="190" width="260" height="20" fill="#140e1c"/>')
    b.append(f'<rect x="44" y="194" width="{max(4, int(252 * xp))}" height="12" fill="{TEAL}"/>')
    b.append(text(f"XP {stats['year_contribs'] % 50}/50", 40, 222, 2, DIM))
    for i in range(min(stats["current"], 10) or 1):  # hearts = streak, capped
        b.append(petal(40 + i * 24, 256, 4, PINK if stats["current"] else DIM))

    # middle column: stats
    rows = [
        (f"COMMITS {year}", stats["year_contribs"]),
        ("CURRENT STREAK", stats["current"]),
        ("LONGEST STREAK", stats["longest"]),
        ("PUBLIC REPOS", stats["repos"]),
        ("STARS EARNED", stats["stars"]),
    ]
    b.append(f'<rect x="340" y="30" width="4" height="260" fill="#3a2a4a"/>')
    for i, (k, v) in enumerate(rows):
        y = 40 + i * 50
        b.append(text(k, 370, y, 2, DIM))
        b.append(text(str(v) if live else "--", 370, y + 18, 3, LIGHT))

    # right column: languages
    b.append(f'<rect x="620" y="30" width="4" height="260" fill="#3a2a4a"/>')
    b.append(text("INVENTORY", 650, 40, 2, DIM))
    colors = [PINK, TEAL, GOLD, LIGHT, DIM]
    for i, (name, frac) in enumerate(stats["langs"]):
        y = 70 + i * 44
        b.append(text(name[:16], 650, y, 2, LIGHT))
        b.append(text(f"{round(frac * 100)}%", 960, y, 2, DIM, "end"))
        b.append(f'<rect x="650" y="{y + 20}" width="310" height="10" fill="#140e1c"/>')
        b.append(f'<rect x="650" y="{y + 20}" width="{max(4, int(310 * frac))}" height="10" fill="{colors[i]}"/>')

    stamp = "UPDATED " + dt.date.today().isoformat() if live else "RUN THE WORKFLOW TO LOAD STATS"
    b.append(text(stamp, w - 30, h - 26, 2, "#5a4a6a", "end"))
    write("card.svg", svg(w, h, "".join(b), f"Player card: level {level}, {stats['year_contribs']} contributions in {year}, {stats['current']}-day streak"))


def draw_projects():
    w, h = 490, 230
    for p in CONFIG["projects"]:
        b = [frame(w, h)]
        b.append(petal(28, 28, 3, PINK))
        title = p["title"]
        # wrap title at ~22 chars on a word boundary
        lines, cur = [], ""
        for word in title.split():
            if len(cur) + len(word) + 1 > 22 and cur:
                lines.append(cur)
                cur = word
            else:
                cur = f"{cur} {word}".strip()
        lines.append(cur)
        y = 26
        for ln in lines:
            b.append(text(ln, 56, y, 3, LIGHT))
            y += 30
        y += 8
        for ln in p["desc"]:
            b.append(text(ln, 28, y, 2, DIM))
            y += 22
        x = 28
        for tag in p["tags"]:
            tw = text_width(tag, 2) + 20
            b.append(f'<rect x="{x}" y="{h - 52}" width="{tw}" height="30" fill="#3a2438"/>')
            b.append(text(tag, x + 10, h - 44, 2, PINK))
            x += tw + 10
        write(f"projects/{p['slug']}.svg", svg(w, h, "".join(b), p["title"]))


def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    stats, live = PLACEHOLDER, False
    if token:
        try:
            stats, live = fetch_stats(CONFIG["user"], token), True
        except Exception as e:  # keep the old look rather than failing the build
            print("stats fetch failed, using placeholders:", e)
    draw_header()
    draw_buttons()
    draw_card(stats, live)
    draw_projects()


if __name__ == "__main__":
    main()
