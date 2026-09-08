# Manga / Manhua / Manhwa AI Video Production Pipeline

Production-grade automated pipeline converting comic series into AI-generated short-form vertical dramas (TikTok, YouTube Shorts, Reels) and cinematic video sequences:
1. **Source Discovery & Scraper**: MangaDex API + fallback webtoon reader scrapers
2. **Canonical Sequential Vision Analysis**: Single-reader chronological analysis via Google Antigravity CLI (`agy --effort medium`)
3. **SERYE Drama Storyboards**: 10-second dramatic blocks with 6 timestamped beats and locked freeze frames
4. **Visual Character References**: Multi-view model sheets with consistent faces & wardrobe anchors via Nano Banana Pro
5. **Flow Automator Max Production CSV**: V3 CSV schema with `@CharacterName` auto-binding, 11-part Masterclass cinematography prompts, and embedded voiceover emotion cues

---

## 🎬 Architecture & Workflow

```
[User Input: Manga Link or Title]
               │
               ▼
[Stage 1: Source Discovery & Chapter Scraper]
  ├─ MangaDex API Search & Title Resolution
  └─ Webtoon Reader Fallback (for titles without MangaDex scanlations)
  └─ Downloads panels into: output/<slug>/ch<num>/images/
               │
               ▼
[Stage 2: Canonical Sequential Image Analysis]
  └─ Single sequential reader via Google Antigravity CLI (agy --effort medium)
  └─ Preserves character names, chronology, exact dialogue, and story flow
  └─ Exports: output/<slug>/ch<num>/chapter_analysis.json
               │
               ▼
[Stage 3: Downstream Specialization]
  ├─ Subagent 1 & 2: Scene-Level Prompts & Dialogue -> video_prompts.csv
  ├─ Subagent 3: 10-Second SERYE Drama Storyboard Blocks -> storyboard_9_16.html & .md
  ├─ Character Reference Sheets: 9:16 Model Sheets -> character_refs/*_ref.png
  └─ Flow Automator Max Package: e01.csv & block*_queue.csv with @mention auto-binding
               │
               ▼
[Stage 4: Google Flow / Kling / Runway Video Generation]
  ├─ In Flow Automator Max Chrome Extension: Click 'CSV' -> Load e01.csv
  └─ Slate chip pills auto-bind character assets from the asset library
```

---

## 🛠️ Script Overview

| Script | Purpose | Key Inputs / Outputs |
| :--- | :--- | :--- |
| `manga_pipeline.py` | **Master Orchestrator**: runs the entire flow end-to-end or by stage | `--title`, `--chapters`, `--stage`, `--existing-dir` |
| `manga_source_scraper.py` | **Discovery & Scraper**: MangaDex API + Madara reader fallback | Downloads images + creates `metadata.json` |
| `sequential_chapter_analysis.py` | **Canonical Vision Reader**: sequential chronological analysis | Reads `images/` -> writes `chapter_analysis.json` |
| `script_and_prompt_engine.py` | **Scene Prompt Engine**: detailed prompts + dialogue extraction | Produces `video_prompts.csv` & `pipeline_data.json` |
| `build_serye_storyboard.py` | **10s SERYE Storyboard Blocks**: groups into 10s dramatic cuts | Generates `storyboard_9_16.html`, `.md`, `.json` |
| `generate_nano_storyboards.py` | **Character Model Sheets**: 9:16 multi-view anchors via `agy` | Outputs `character_refs/*_ref.png` |
| `build_flow_automator_csv.py` | **Flow Automator V3 CSV**: 6-block queue with `@mentions` | Generates `flow_queue/e01.csv` & per-block files |

---

## 🚀 Usage Guide

### 1. Interactive End-to-End Run
```bash
source ~/.venv_manga/bin/activate
python3 manga_pipeline.py
```

### 2. CLI Single Command
Search by manga title:
```bash
python3 manga_pipeline.py --title "The Investor Who Sees The Future" --chapters 1
```

Or pass a direct MangaDex / Reader URL:
```bash
python3 manga_pipeline.py --url "https://theinvestorwhoseesthefuture.com/manga/the-investor-who-sees-the-future-chapter-1/" --chapters 1
```

### 3. Run on an Already Downloaded Chapter
```bash
python3 manga_pipeline.py --existing-dir ./output/the-investor-who-sees-the-future/ch1
```

### 4. Running Specific Stages
```bash
# Only run canonical vision analysis
python3 manga_pipeline.py --existing-dir ./output/ch1 --stage analyze

# Only rebuild SERYE 10s storyboards
python3 manga_pipeline.py --existing-dir ./output/ch1 --stage storyboard

# Only generate Flow Automator Max CSV
python3 manga_pipeline.py --existing-dir ./output/ch1 --stage flow
```

---

## ⚡ Google Flow Automator Max Integration

The generated queue file follows the **Flow Automator Max V3 CSV schema**:
```csv
prompt,description,hashtags,videoModel,videoMode,videoDurationSeconds,flowQuantity,videoVoiceReference,flowAspectRatio
```

### How to Batch Generate in Chrome:
1. Open the **Flow Automator Max** extension sidebar in Chrome.
2. Under the **Prompt Queue** card, click the **CSV** button.
3. Select `output/<series>/ch1/flow_queue/e01.csv`.
4. The extension automatically:
   - Parses the `@CharacterName` tokens (e.g. `@Kang Jin-Hoo`, `@Oh Taek-Gyu`).
   - Scans the Google Flow React Fiber tree and binds matching character asset chips.
   - Arms all 10-second blocks in the queue.
5. Click **Add to Queue** and start batch video generation.

---

## 📁 Output Artifacts Directory Structure

```
output/the-investor-who-sees-the-future/ch1/
├── images/                         # Downloaded original panels (page_001.webp ...)
├── metadata.json                   # Chapter metadata & page list
├── chapter_analysis.json           # Canonical single-reader story analysis
├── video_prompts.csv               # Complete scene-level video prompts & script table
├── storyboard_9_16.html            # Dark-mode visual 10s storyboard viewer
├── storyboard_9_16.md              # Director's Markdown specification
├── storyboard_9_16.json            # Machine-readable storyboard beats
├── gallery.html                    # Visual master gallery (characters + storyboards)
├── character_refs/                 # 9:16 character model sheets (4 views each)
│   ├── kang_jin_hoo_ref.png
│   ├── oh_taek_gyu_ref.png
│   ├── street_reporter_ref.png
│   ├── shin_yuri_ref.png
│   ├── female_interviewer_ref.png
│   └── spirit_shaman_ref.png
├── nano_storyboards/               # Full 10s visual storyboard strips (Block 1 to 6)
└── flow_queue/                     # Flow Automator Max ready-to-import files
    ├── e01.csv                     # Full 6-block Episode 1 CSV
    ├── block1_queue.csv .. block6  # Per-block CSVs
    ├── block1_video_prompt.txt ..  # Raw prompt text files
    └── char_refs_investor.csv      # Character reference image queue
```

---

## 🎨 Best Practices & Production Guidelines

- **Sequential Analysis Over Parallel**: Always use one sequential vision reader for an entire chapter. Sequential context prevents character name drift, maintains chronological consistency, and keeps emotional tone coherent.
- **Embedded VO Emotion Tags**: Always place voice acting directions in parentheses before dialogue: `"(flat, tired) E-rank hunter ako..."` for clean text-to-speech rendering.
- **Freeze-Frame Rule**: Every 10-second dramatic block ends with an explicit `END ON A COMPLETE FREEZE FRAME` directive to prevent visual jitter and provide clean cut points for video stitching.
- **Shallow Depth-of-Field for Screens**: When characters hold phones or read trading charts, prompts use anamorphic bokeh and shallow depth-of-field to naturally blur text into realistic lens artifacts.
