"""
Generates the art-deco / occult-noir SVGs used by the profile README.

    python scripts/gen.py                # placeholder stats (no network)
    GH_TOKEN=xxx python scripts/gen.py   # live stats from the GitHub GraphQL API

Edit CONFIG below to change text and links.
"""
import datetime as dt
import json
import math
import os
import pathlib
import urllib.request
from xml.sax.saxutils import escape

# ----------------------------------------------------------------- CONFIG
CONFIG = {
    "user": "Kishore-suthersingh",
    "name": "KISHORE N",
    "role": "COMPUTER VISION  ·  MACHINE LEARNING",
    "motto": "“I teach machines to see what others miss.”",
    "origin": "CHENNAI",
    "class": "VISIONARY",
    "buttons": ["PORTFOLIO", "LINKEDIN", "EMAIL", "RESUME"],
    "abilities": [
        ("I", "TRUE SIGHT", "Object detection &", "segmentation", "YOLOv8 · OpenCV", "eye"),
        ("II", "DREAMWEAVER", "Conjures images from", "noise & prompts", "SDXL · LoRA · ControlNet", "spiral"),
        ("III", "NEURAL LINK", "Reads intent straight", "from brainwaves", "EEG · CNN · RNN", "wave"),
        ("ULT", "SUMMONING", "Ships any model as", "a live API", "FastAPI · React", "gate"),
    ],
    "cases": [
        {
            "slug": "image-gen",
            "no": "001",
            "title": ["DOMAIN IMAGE", "GENERATION PIPELINE"],
            "desc": ["Stable Diffusion + ControlNet with LoRA", "fine-tuning, CLIP quality gate, FastAPI."],
            "tags": ["SDXL", "LoRA", "CLIP"],
        },
        {
            "slug": "synthetic-data",
            "no": "002",
            "title": ["MULTI-MODAL", "SYNTHETIC DATA"],
            "desc": ["Tabular, signal & image data generated", "from plain-language prompts."],
            "tags": ["CTGAN", "React", "FastAPI"],
        },
        {
            "slug": "eeg-bci",
            "no": "003",
            "title": ["EEG BRAIN-COMPUTER", "INTERFACE"],
            "desc": ["CNN/RNN brainwave classifier driving", "real-time motor control."],
            "tags": ["PyTorch", "EEG", "CNN"],
        },
        {
            "slug": "commendations",
            "no": "★",
            "title": ["COMMENDATIONS"],
            "desc": ["1st — Cognisence Coding Competition", "5th — Coders of the BlackPearl", "Smart India Hackathon — Pre-Final"],
            "tags": [],
        },
    ],
}

# Black, brass & oxblood
INK, PANEL, PANEL2 = "#0e0c0a", "#17130f", "#1f1a14"
BRASS, BRASS_HI, BRASS_LO = "#c9a45c", "#f0d79a", "#6e5830"
PARCH, DIM, BLOOD, TEAL = "#e9dcc0", "#8c7d63", "#9b2f2f", "#3f7a73"
SERIF = "Georgia,'Times New Roman',serif"

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


# ---------------------------------------------------------------- HELPERS
def t(s, x, y, size, fill=PARCH, anchor="start", spacing=0, weight="normal", style="normal", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" letter-spacing="{spacing}" font-weight="{weight}" font-style="{style}"{extra}>'
        f"{escape(s)}</text>"
    )


def deco_frame(w, h, inset=10, step=14, stroke=BRASS, fill=PANEL):
    """Double-lined frame with stepped (art-deco) corners."""
    def stepped(i, s):
        x0, y0, x1, y1 = i, i, w - i, h - i
        return (
            f"M{x0 + s} {y0}H{x1 - s}V{y0 + s / 2}H{x1 - s / 2}V{y0 + s}H{x1}"
            f"V{y1 - s}H{x1 - s / 2}V{y1 - s / 2}H{x1 - s}V{y1}"
            f"H{x0 + s}V{y1 - s / 2}H{x0 + s / 2}V{y1 - s}H{x0}"
            f"V{y0 + s}H{x0 + s / 2}V{y0 + s / 2}H{x0 + s}Z"
        )
    return (
        f'<rect width="{w}" height="{h}" fill="{INK}"/>'
        f'<path d="{stepped(inset, step)}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        f'<path d="{stepped(inset + 7, step)}" fill="none" stroke="{BRASS_LO}" stroke-width="1"/>'
    )


def diamond(cx, cy, r, fill=BRASS):
    return f'<path d="M{cx} {cy - r}L{cx + r} {cy}L{cx} {cy + r}L{cx - r} {cy}Z" fill="{fill}"/>'


def rule(cx, y, half, gap=14):
    """Horizontal ornament: line ◆ line."""
    return (
        f'<path d="M{cx - half} {y}H{cx - gap}M{cx + gap} {y}H{cx + half}" stroke="{BRASS}" stroke-width="1.5"/>'
        + diamond(cx, y, 6) + diamond(cx - half, y, 3) + diamond(cx + half, y, 3)
    )


def sunburst(cx, cy, r, rays=36, color=BRASS, opacity=0.07):
    out = []
    for i in range(rays):
        if i % 2:
            continue
        a0 = math.pi * i / rays
        a1 = math.pi * (i + 1) / rays
        p0 = (cx + r * math.cos(a0 + math.pi), cy + r * math.sin(a0 + math.pi))
        p1 = (cx + r * math.cos(a1 + math.pi), cy + r * math.sin(a1 + math.pi))
        out.append(f"M{cx} {cy}L{p0[0]:.1f} {p0[1]:.1f}L{p1[0]:.1f} {p1[1]:.1f}Z")
    return f'<path d="{"".join(out)}" fill="{color}" opacity="{opacity}"/>'


def gold_gradient(gid, animate=False):
    anim = (
        '<animate attributeName="x1" values="-1;1" dur="6s" repeatCount="indefinite"/>'
        '<animate attributeName="x2" values="0;2" dur="6s" repeatCount="indefinite"/>'
        if animate else ""
    )
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{anim}'
        f'<stop offset="0" stop-color="{BRASS}"/><stop offset=".45" stop-color="{BRASS}"/>'
        f'<stop offset=".5" stop-color="{BRASS_HI}"/><stop offset=".55" stop-color="{BRASS}"/>'
        f'<stop offset="1" stop-color="{BRASS}"/></linearGradient>'
    )


def svg(w, h, body, title, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
        f"<defs>{defs}</defs>{body}</svg>\n"
    )


def write(name, content):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def roman(n):
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


# ------------------------------------------------------------------ STATS
def fetch_stats(user, token):
    today = dt.date.today()
    query = """
    query($login:String!,$from:DateTime!,$to:DateTime!,$yfrom:DateTime!){
      user(login:$login){
        repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){
          totalCount
          nodes{ stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}} }
        }
        year: contributionsCollection(from:$yfrom,to:$to){ contributionCalendar{ totalContributions } }
        cal: contributionsCollection(from:$from,to:$to){
          contributionCalendar{ weeks{ contributionDays{ contributionCount } } }
        }
      }
    }"""
    variables = {
        "login": user,
        "from": (today - dt.timedelta(days=364)).isoformat() + "T00:00:00Z",
        "to": today.isoformat() + "T23:59:59Z",
        "yfrom": f"{today.year}-01-01T00:00:00Z",
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

    counts = [d["contributionCount"] for w in u["cal"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today not started yet
        i -= 1
    current = 0
    while i >= 0 and counts[i] > 0:
        current += 1
        i -= 1
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)

    langs, stars = {}, 0
    for repo in u["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    return {
        "year": u["year"]["contributionCalendar"]["totalContributions"],
        "current": current,
        "longest": longest,
        "repos": u["repositories"]["totalCount"],
        "stars": stars,
        "langs": [(n, s / total) for n, s in sorted(langs.items(), key=lambda kv: -kv[1])[:5]],
    }


PLACEHOLDER = {
    "year": 0, "current": 0, "longest": 0, "repos": 0, "stars": 0,
    "langs": [("Python", 0.62), ("JavaScript", 0.18), ("Jupyter Notebook", 0.12), ("C++", 0.05), ("CSS", 0.03)],
}


# ---------------------------------------------------------------- DRAWING
def draw_header():
    w, h = 1000, 340
    defs = gold_gradient("gold", animate=True) + (
        f'<radialGradient id="glow" cx=".5" cy="1" r=".8"><stop offset="0" stop-color="{BLOOD}" stop-opacity=".35"/>'
        f'<stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>'
    )
    b = [deco_frame(w, h, fill=PANEL)]
    b.append(f'<rect x="18" y="18" width="{w - 36}" height="{h - 36}" fill="url(#glow)"/>')
    b.append(sunburst(w / 2, h - 18, 620, opacity=0.06))
    # slow pulse on the rays
    b.append(f'<g opacity=".5">{sunburst(w / 2, h - 18, 620, rays=72, opacity=0.05)}'
             '<animate attributeName="opacity" values=".2;.7;.2" dur="7s" repeatCount="indefinite"/></g>')
    # top crest
    b.append(f'<path d="M{w / 2 - 60} 18L{w / 2} 58L{w / 2 + 60} 18" fill="none" stroke="{BRASS}" stroke-width="1.5"/>')
    b.append(diamond(w / 2, 40, 8))
    # side pillars
    for x in (60, w - 60):
        for k in range(4):
            b.append(f'<rect x="{x - 2 - k * 7}" y="{90 + k * 10}" width="{4 + k * 14}" height="2" fill="{BRASS_LO}"/>')
        b.append(f'<rect x="{x - 1}" y="70" width="2" height="200" fill="{BRASS_LO}"/>')
    b.append(t("—  DOSSIER OF  —", w / 2, 100, 15, DIM, "middle", 8))
    b.append(t(CONFIG["name"], w / 2 + 2, 182, 78, "#000", "middle", 18, "bold", extra=' opacity=".6"'))
    b.append(t(CONFIG["name"], w / 2, 180, 78, "url(#gold)", "middle", 18, "bold"))
    b.append(rule(w / 2, 212, 260))
    b.append(t(CONFIG["role"], w / 2, 250, 20, PARCH, "middle", 6))
    b.append(t(CONFIG["motto"], w / 2, 288, 17, DIM, "middle", 1, style="italic"))
    write("header.svg", svg(w, h, "".join(b), f"{CONFIG['name']} — {CONFIG['role']}", defs))


def draw_buttons():
    w, h = 230, 62
    for label in CONFIG["buttons"]:
        c = 12
        plate = f"M{c} 2H{w - c}L{w - 2} {h / 2}L{w - c} {h - 2}H{c}L2 {h / 2}Z"
        b = (
            f'<path d="{plate}" fill="{PANEL}" stroke="{BRASS}" stroke-width="2"/>'
            f'<path d="M{c + 6} 8H{w - c - 6}M{c + 6} {h - 8}H{w - c - 6}" stroke="{BRASS_LO}" stroke-width="1"/>'
            + diamond(22, h / 2, 4) + diamond(w - 22, h / 2, 4)
            + t(label, w / 2, h / 2 + 6, 17, BRASS_HI, "middle", 5)
        )
        write(f"btn-{label.lower()}.svg", svg(w, h, b, label))


def draw_card(stats, live):
    w, h = 1000, 360
    defs = gold_gradient("gold2")
    b = [deco_frame(w, h)]
    year = dt.date.today().year

    # --- emblem
    cx, cy = 150, 150
    b.append(sunburst(cx, cy + 60, 150, rays=28, opacity=0.08))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="72" fill="{INK}" stroke="{BRASS}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{BRASS_LO}" stroke-width="1" stroke-dasharray="2 5"/>')
    b.append(f'<g transform="rotate(45 {cx} {cy})"><rect x="{cx - 42}" y="{cy - 42}" width="84" height="84" fill="none" stroke="{BRASS_LO}"/></g>')
    b.append(t(CONFIG["name"][0], cx, cy + 22, 64, "url(#gold2)", "middle", 0, "bold"))
    b.append(t(CONFIG["name"], cx, 262, 22, PARCH, "middle", 6, "bold"))
    b.append(t(f"CLASS · {CONFIG['class']}", cx, 288, 12, BRASS, "middle", 4))
    b.append(t(f"ORIGIN · {CONFIG['origin']}", cx, 308, 12, DIM, "middle", 4))

    # --- attributes
    x0 = 320
    b.append(f'<path d="M{x0 - 25} 40V{h - 40}" stroke="{BRASS_LO}"/>')
    b.append(t("ATTRIBUTES", x0, 58, 14, BRASS, spacing=5))
    rows = [
        (f"DEEDS OF {roman(year)}", stats["year"], 1000),
        ("CURRENT STREAK", stats["current"], 30),
        ("LONGEST STREAK", stats["longest"], 100),
        ("ARCHIVES", stats["repos"], 50),
        ("RENOWN", stats["stars"], 100),
    ]
    for i, (k, v, cap) in enumerate(rows):
        y = 92 + i * 50
        b.append(t(k, x0, y, 12, DIM, spacing=3))
        b.append(t(str(v) if live else "—", x0 + 300, y, 18, PARCH, "end"))
        b.append(f'<rect x="{x0}" y="{y + 10}" width="300" height="6" fill="{INK}" stroke="{BRASS_LO}" stroke-width=".5"/>')
        frac = min(1, v / cap) if live else 0
        b.append(f'<rect x="{x0}" y="{y + 10}" width="{max(2, 300 * frac):.0f}" height="6" fill="{BLOOD}"/>')
        for k2 in range(1, 10):
            b.append(f'<rect x="{x0 + k2 * 30}" y="{y + 10}" width="1" height="6" fill="{INK}"/>')

    # --- arsenal (languages)
    x1 = 690
    b.append(f'<path d="M{x1 - 25} 40V{h - 40}" stroke="{BRASS_LO}"/>')
    b.append(t("ARSENAL", x1, 58, 14, BRASS, spacing=5))
    for i, (name, frac) in enumerate(stats["langs"]):
        y = 92 + i * 50
        b.append(diamond(x1 + 5, y - 5, 5, BRASS if i == 0 else BRASS_LO))
        b.append(t(name, x1 + 20, y, 15, PARCH))
        b.append(t(f"{round(frac * 100)}%", x1 + 270, y, 13, DIM, "end"))
        b.append(f'<rect x="{x1 + 20}" y="{y + 10}" width="250" height="3" fill="{INK}"/>')
        b.append(f'<rect x="{x1 + 20}" y="{y + 10}" width="{max(2, 250 * frac):.0f}" height="3" fill="{TEAL if i else BRASS}"/>')

    stamp = f"LAST SIGHTED {dt.date.today():%d %b %Y}".upper() if live else "RUN THE WORKFLOW TO REVEAL"
    b.append(t(stamp, w - 40, h - 26, 10, BRASS_LO, "end", 4))
    title = f"Dossier: {stats['year']} contributions in {year}, {stats['current']}-day streak, top languages"
    write("card.svg", svg(w, h, "".join(b), title, defs))


def icon(kind, cx, cy):
    s = f'stroke="{BRASS_HI}" stroke-width="2.5" fill="none" stroke-linecap="round"'
    if kind == "eye":
        return (f'<path d="M{cx - 24} {cy}Q{cx} {cy - 22} {cx + 24} {cy}Q{cx} {cy + 22} {cx - 24} {cy}Z" {s}/>'
                f'<circle cx="{cx}" cy="{cy}" r="7" fill="{BRASS_HI}"/>')
    if kind == "spiral":
        pts = []
        for i in range(60):
            a = i * 0.32
            r = 2 + i * 0.4
            pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
        return f'<polyline points="{" ".join(pts)}" {s}/>'
    if kind == "wave":
        return (f'<path d="M{cx - 26} {cy}H{cx - 14}L{cx - 8} {cy - 16}L{cx - 1} {cy + 18}L{cx + 6} {cy - 10}'
                f'L{cx + 11} {cy}H{cx + 26}" {s}/>')
    # gate
    return (f'<path d="M{cx - 20} {cy + 20}V{cy - 6}Q{cx - 20} {cy - 22} {cx} {cy - 22}Q{cx + 20} {cy - 22} {cx + 20} {cy - 6}V{cy + 20}" {s}/>'
            f'<path d="M{cx - 9} {cy + 20}V{cy - 2}Q{cx} {cy - 12} {cx + 9} {cy - 2}V{cy + 20}" {s} opacity=".6"/>')


def draw_abilities():
    w, h = 1000, 250
    b = [deco_frame(w, h)]
    slot = (w - 80) / 4
    for i, (key, name, l1, l2, tech, kind) in enumerate(CONFIG["abilities"]):
        cx = 40 + slot * i + slot / 2
        ult = key == "ULT"
        r = 44
        hexagon = " ".join(f"{cx + r * math.cos(math.pi / 3 * k + math.pi / 6):.1f},{78 + r * math.sin(math.pi / 3 * k + math.pi / 6):.1f}" for k in range(6))
        b.append(f'<polygon points="{hexagon}" fill="{INK}" stroke="{BLOOD if ult else BRASS}" stroke-width="{3 if ult else 2}"/>')
        if ult:
            b.append(f'<polygon points="{hexagon}" fill="none" stroke="{BLOOD}" stroke-width="2" opacity=".6">'
                     f'<animate attributeName="opacity" values=".1;.8;.1" dur="2.5s" repeatCount="indefinite"/></polygon>')
        b.append(icon(kind, cx, 78))
        b.append(f'<rect x="{cx - 18}" y="114" width="36" height="18" fill="{BLOOD if ult else BRASS}"/>')
        b.append(t(key, cx, 128, 12, INK, "middle", 1, "bold"))
        b.append(t(name, cx, 160, 16, PARCH, "middle", 4, "bold"))
        b.append(t(l1, cx, 182, 13, DIM, "middle"))
        b.append(t(l2, cx, 198, 13, DIM, "middle"))
        b.append(t(tech, cx, 222, 11, BRASS, "middle", 2))
        if i:
            b.append(f'<path d="M{40 + slot * i} 40V{h - 40}" stroke="{BRASS_LO}" stroke-dasharray="2 6"/>')
    write("abilities.svg", svg(w, h, "".join(b), "Abilities: " + ", ".join(a[1] for a in CONFIG["abilities"])))


def draw_cases():
    w, h = 490, 250
    for c in CONFIG["cases"]:
        b = [deco_frame(w, h, step=12)]
        b.append(t(f"CASE FILE № {c['no']}", 36, 50, 11, BRASS, spacing=5))
        b.append(f'<path d="M36 62H{w - 36}" stroke="{BRASS_LO}"/>')
        y = 96
        for ln in c["title"]:
            b.append(t(ln, 36, y, 22, PARCH, spacing=3, weight="bold"))
            y += 28
        y += 6
        for ln in c["desc"]:
            b.append(t(ln, 36, y, 14, DIM, style="italic"))
            y += 20
        x = 36
        for tag in c["tags"]:
            tw = len(tag) * 9 + 24
            b.append(f'<rect x="{x}" y="{h - 62}" width="{tw}" height="24" fill="none" stroke="{BLOOD}" stroke-width="1.5"/>')
            b.append(t(tag.upper(), x + tw / 2, h - 45, 11, "#d0645a", "middle", 2, "bold"))
            x += tw + 10
        # wax-seal stamp
        sx, sy = w - 66, 62
        b.append(f'<g transform="rotate(-14 {sx} {sy})"><circle cx="{sx}" cy="{sy}" r="30" fill="none" stroke="{BLOOD}" stroke-width="2" opacity=".75"/>'
                 f'<circle cx="{sx}" cy="{sy}" r="25" fill="none" stroke="{BLOOD}" stroke-width="1" opacity=".75"/>'
                 + t("SEALED" if c["tags"] else "HONOR", sx, sy + 3, 8, BLOOD, "middle", 0, "bold", extra=' opacity=".9"') + "</g>")
        write(f"cases/{c['slug']}.svg", svg(w, h, "".join(b), " ".join(c["title"])))


def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    stats, live = PLACEHOLDER, False
    if token:
        try:
            stats, live = fetch_stats(CONFIG["user"], token), True
        except Exception as e:  # keep building with placeholders rather than failing
            print("stats fetch failed, using placeholders:", e)
    draw_header()
    draw_buttons()
    draw_card(stats, live)
    draw_abilities()
    draw_cases()


if __name__ == "__main__":
    main()
