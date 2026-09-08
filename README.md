# Manga/Manhua/Manhwa Video Pipeline

Automated pipeline for transforming manga, manhua, and manhwa chapters into production-ready video assets:
1. Source discovery and chapter scraping
2. Vision-based dialogue, chat bubble, and scene action extraction
3. Structured generative AI video animation prompts
4. 9:16 vertical storyboards with complete "ingredients" via Google Antigravity CLI (`agy`)
5. CSV synthesis for manual video generation (Google Flow, Kling, Runway Gen-3, Luma)

## Architecture & Workflow

```
[User Input: Manga Link or Title]
               │
               ▼
[Hermes Source Discovery: MangaDex API / Web]
               │
               ▼
[Interactive Chapter Selection ("How many chapters to scrape?")]
               │
               ▼
[Manga Chapter Scraper: Download Panels & Metadata]
               │
               ├──► Subagent 1: Extract chat bubbles, analyze story flow,
               │                accurate character dialogue with VO emotion tags,
               │                detailed scene action descriptions
               │
               ├──► Subagent 2: Structured generative video animation prompts
               │                (camera kinematics, character dynamics, lighting, anime style)
               │
               └──► Subagent 3: 9:16 Vertical Storyboard & Ingredients Guide
                                (TikTok/Shorts safe zones, character visual anchors,
                                 camera cues, SFX/BGM audio cues via Google Antigravity CLI)
               │
               ▼
[Deliverables Generated]
 ├── video_prompts.csv   (Complete structured video prompts + character scripts)
 ├── storyboard_9_16.md  (Director-level 9:16 vertical production storyboard)
 ├── storyboard_9_16.html(Interactive dark-mode visual viewer with phone frames)
 └── pipeline_data.json  (Machine-readable structured dataset)
               │
               ▼
[Manual Video Generation by User]
 (Upload panel, paste prompt into Kling / Flow / Runway, generate TTS voiceover)
```

## Setup & Dependencies

```bash
# Activate python environment
source ~/.venv_manga/bin/activate

# Required tools
# - Google Antigravity CLI (agy) at ~/.local/bin/agy
# - Vision proxy on http://localhost:8765/v1
```

## Usage

### 1. End-to-End Orchestrator

Run interactively:
```bash
python3 manga_pipeline.py
```

Run with search query:
```bash
python3 manga_pipeline.py --title "From Goblin to Goblin God" --chapters 1
```

Run with MangaDex URL:
```bash
python3 manga_pipeline.py --url "https://mangadex.org/title/a958abd8-745d-4f47-9c4d-89abae30f5df" --chapters 1
```

Process an already downloaded chapter:
```bash
python3 manga_pipeline.py --existing-dir ./output/ch2
```

### 2. Standalone Modules

- **Source Discovery & Scraper:**
  ```bash
  python3 manga_source_scraper.py --query "Solo Leveling" --chapters 1
  ```

- **Subagents 1 & 2 (Dialogue, Video Prompts & CSV):**
  ```bash
  python3 script_and_prompt_engine.py --chapter-dir ./output/ch2 --output-csv ./output/ch2/video_prompts.csv
  ```

- **Subagent 3 (9:16 Storyboard via Antigravity):**
  ```bash
  python3 storyboard_agy.py --chapter-dir ./output/ch2
  ```

## Output Deliverables

- `video_prompts.csv`: Complete production table with `Scene_Number`, `Character_Speaker`, `Dialogue_Script` (including emotion cue), `Action_Description`, `Video_Animation_Prompt`, `Camera_Movement`, `Visual_Style_FX`, `Estimated_Duration_Sec`.
- `storyboard_9_16.html`: Responsive visual HTML viewer with mobile frames, safe zones, image thumbnails, and copyable ingredients.
- `storyboard_9_16.md`: Director's breakdown of every cut and audio/visual asset requirements.
