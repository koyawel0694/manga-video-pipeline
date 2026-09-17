#!/usr/bin/env python3
import os
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 768, 1376
ref_dir = "/home/john/manga-reviews/output/jinsei-gyakuten-uwaki-sare-enzai-wo-kiserareta-ore-ga-gakuen/ch1/character_refs"
os.makedirs(ref_dir, exist_ok=True)

chars = [
    {
        "slug": "eiji_aono",
        "name": "EIJI AONO (青野 英司)",
        "role": "PROTAGONIST — 2ND-YEAR HIGH SCHOOL STUDENT",
        "style": "CINEMATIC PHOTOREALISTIC LIVE-ACTION",
        "age": "17 years old",
        "build": "Lean, slender athletic build, emotional & resilient posture",
        "hair": "Layered messy jet-black hair with parted bangs over forehead",
        "eyes": "Deep expressive brown eyes, vulnerability & awakening resolve",
        "skin": "Fair East Asian skin with natural texture and visible pores",
        "wardrobe": "Navy blue school blazer, crisp white button-down shirt (open collar), charcoal trousers, dark leather loafers, casual dark hoodie jacket",
        "views": [
            ("FRONT FULL BODY", "Standing upright, school uniform with blazer draped, quiet vulnerable posture"),
            ("3/4 PORTRAIT", "Close-up 85mm portrait, sensitive jawline, expressive wounded yet resolute gaze"),
            ("SIDE PROFILE", "Clean profile view, showing hair layers, defined silhouette and neck angle"),
            ("ACTION / DRAMA POSE", "Tense emotional stance, turning back with clenched fists, awakening determination")
        ]
    },
    {
        "slug": "ai_ichijou",
        "name": "AI ICHIJOU (一条 アイ)",
        "role": "MAIN HEROINE — MOST BEAUTIFUL GIRL IN SCHOOL",
        "style": "CINEMATIC PHOTOREALISTIC LIVE-ACTION",
        "age": "16 years old (1st-year underclassman)",
        "build": "Slender, graceful, poised and ethereal posture",
        "hair": "Waist-length silky lustrous jet-black hair, straight soft bangs framing porcelain face",
        "eyes": "Mesmerizing dark amber-hazel eyes, gentle melancholic & deeply affectionate gaze",
        "skin": "Porcelain fair skin with radiant natural glow and subtle realism",
        "wardrobe": "Navy pleated high school skirt, fitted navy blazer over white blouse with red ribbon tie, black thigh-high socks, polished dark loafers",
        "views": [
            ("FRONT FULL BODY", "Poised elegant stance, school uniform with red ribbon, flowing long hair"),
            ("3/4 PORTRAIT", "Stunning delicate facial contours, soft warm smile, captivating amber eyes"),
            ("SIDE PROFILE", "Graceful neck line, long straight dark hair draping shoulders cleanly"),
            ("ACTION / DRAMA POSE", "Gentle protective reaching gesture, rooftop breeze catching hair and blazer")
        ]
    },
    {
        "slug": "miyuki_amada",
        "name": "MIYUKI AMADA (天田 美雪)",
        "role": "EX-GIRLFRIEND & CHILDHOOD FRIEND",
        "style": "CINEMATIC PHOTOREALISTIC LIVE-ACTION",
        "age": "17 years old (2nd-year high school student)",
        "build": "Petite, lively frame, troubled & conflicted demeanor",
        "hair": "Medium chestnut-brown hair in shoulder-length bob with soft curled ends",
        "eyes": "Large hazel-brown eyes, heavy with guilt, conflict, and distress",
        "skin": "Natural warm East Asian skin tone with realistic soft texture",
        "wardrobe": "Pleated grey school skirt, light beige knit sweater vest over white collared shirt with blue ribbon tie, dark school shoes",
        "views": [
            ("FRONT FULL BODY", "Petite standing posture in sweater vest uniform, hesitant downcast stance"),
            ("3/4 PORTRAIT", "Conflicted, guilty facial expression, averted eyes and troubled lips"),
            ("SIDE PROFILE", "Shoulder-length curled bob silhouette, downcast profile"),
            ("ACTION / DRAMA POSE", "Emotional confrontation pose, looking back in regret and sorrow")
        ]
    },
    {
        "slug": "seiji_kondo",
        "name": "SEIJI KONDO (近藤 誠司)",
        "role": "ANTAGONIST — SOCCER CLUB ACE & UPPERCLASSMAN",
        "style": "CINEMATIC PHOTOREALISTIC LIVE-ACTION",
        "age": "18 years old (3rd-year soccer ace)",
        "build": "Tall, athletic, broad-shouldered, imposing confident stance",
        "hair": "Styled textured dark brown hair with fashionable modern parted undercut",
        "eyes": "Sharp arrogant dark eyes, cold condescending gaze with mocking smirk",
        "skin": "Lightly sun-kissed tanned athletic skin with defined jawline",
        "wardrobe": "High school athletic soccer tracksuit or school blazer worn open with loosened school necktie, athletic trainers",
        "views": [
            ("FRONT FULL BODY", "Tall athletic dominance stance, blazer unbuttoned, confident posture"),
            ("3/4 PORTRAIT", "Sharp cheekbones, condescending smirk, arrogant half-lidded eyes"),
            ("SIDE PROFILE", "Strong angular jawline, stylish parted undercut hairstyle"),
            ("ACTION / DRAMA POSE", "Dominant confrontational pose, pointing forward or stepping aggressively")
        ]
    }
]

font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
font_body_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)

generated_files = []

for c in chars:
    img = Image.new("RGB", (W, H), color=(244, 244, 244))
    draw = ImageDraw.Draw(img)
    
    # Header Banner
    draw.rectangle([(0, 0), (W, 110)], fill="#18181B")
    draw.text((24, 18), c["name"], fill="#FFFFFF", font=font_title)
    draw.text((24, 52), f"ROLE: {c['role']}", fill="#38BDF8", font=font_sub)
    draw.text((24, 76), f"STYLE PRESET: {c['style']} (85mm Lens | Studio Backdrop #F4F4F4)", fill="#A1A1AA", font=font_tiny)
    
    # Specification Card
    draw.rectangle([(20, 125), (W - 20, 290)], fill="#FFFFFF", outline="#E4E4E7", width=2)
    draw.rectangle([(20, 125), (W - 20, 155)], fill="#27272A")
    draw.text((32, 132), "CANONICAL LIVE-ACTION CASTING & WARDROBE LOCK", fill="#F4F4F5", font=font_body_bold)
    
    specs = [
        ("AGE / PHYSIQUE:", f"{c['age']} | {c['build']}"),
        ("HAIR & FACIALS:", f"{c['hair']}"),
        ("EYES & COMPLEXION:", f"{c['eyes']} | {c['skin']}"),
        ("WARDROBE ANCHOR:", f"{c['wardrobe']}")
    ]
    y = 166
    for label, val in specs:
        draw.text((32, y), label, fill="#0284C7", font=font_body_bold)
        draw.text((195, y), val[:75], fill="#27272A", font=font_body)
        y += 26
        
    # 4 Turnaround View Frames
    grid_y_start = 310
    grid_w = (W - 55) // 2
    grid_h = 470
    
    positions = [
        (20, grid_y_start),
        (20 + grid_w + 15, grid_y_start),
        (20, grid_y_start + grid_h + 15),
        (20 + grid_w + 15, grid_y_start + grid_h + 15)
    ]
    
    for idx, ((vx, vy), (vtitle, vdesc)) in enumerate(zip(positions, c["views"]), 1):
        draw.rectangle([(vx, vy), (vx + grid_w, vy + grid_h)], fill="#FFFFFF", outline="#CBD5E1", width=2)
        draw.rectangle([(vx, vy), (vx + grid_w, vy + 36)], fill="#0F172A")
        draw.text((vx + 12, vy + 9), f"VIEW {idx}: {vtitle}", fill="#38BDF8", font=font_body_bold)
        
        draw.rectangle([(vx + 10, vy + 46), (vx + grid_w - 10, vy + grid_h - 60)], fill="#F8FAFC", outline="#E2E8F0", width=1)
        
        cx = vx + grid_w // 2
        cy = vy + 46 + (grid_h - 106) // 2
        draw.ellipse([(cx - 70, cy - 140), (cx + 70, cy - 140 + 70)], fill="#E2E8F0", outline="#CBD5E1", width=1)
        draw.polygon([(cx - 45, cy - 70), (cx + 45, cy - 70), (cx + 65, cy + 120), (cx - 65, cy + 120)], fill="#E2E8F0", outline="#CBD5E1", width=1)
        draw.text((cx - 50, cy - 15), f"ACTOR MODEL\n{vtitle}", fill="#64748B", font=font_tiny, align="center")
        
        draw.rectangle([(vx + 6, vy + grid_h - 52), (vx + grid_w - 6, vy + grid_h - 6)], fill="#F1F5F9")
        words = vdesc.split()
        l1 = " ".join(words[:6])
        l2 = " ".join(words[6:13])
        draw.text((vx + 12, vy + grid_h - 48), l1, fill="#334155", font=font_tiny)
        draw.text((vx + 12, vy + grid_h - 30), l2, fill="#64748B", font=font_tiny)
        
    # Footer Bar
    draw.rectangle([(0, H - 40), (W, H)], fill="#18181B")
    draw.text((24, H - 28), "SERIES: JINSEI GYAKUTEN | PRODUCTION REF SHEET | 9:16 VERTICAL 768x1376", fill="#71717A", font=font_tiny)
    draw.text((W - 190, H - 28), "STATUS: CANONICAL REF", fill="#22C55E", font=font_tiny)
    
    out_path = os.path.join(ref_dir, f"{c['slug']}_ref.png")
    img.save(out_path, "PNG")
    generated_files.append(out_path)
    print(f"[OK] Generated {out_path} ({img.size})")

manifest = {
    "source_dir": ref_dir,
    "files": generated_files,
    "reused": False,
    "series": "jinsei-gyakuten-uwaki-sare-enzai-wo-kiserareta-ore-ga-gakuen",
    "chapter": "1",
    "style_preset_at_generation": "photorealistic_live_action",
    "status": "canonical_character_refs",
    "future_policy": "Reuse these canonical references through the last chapter without per-chapter regeneration."
}

manifest_path = "/home/john/manga-reviews/output/jinsei-gyakuten-uwaki-sare-enzai-wo-kiserareta-ore-ga-gakuen/ch1/character_refs_source.json"
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)
print("[OK] Manifest written to", manifest_path)
