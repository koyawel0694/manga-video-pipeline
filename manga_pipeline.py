#!/usr/bin/env python3
"""
manga_pipeline.py — Master Orchestrator for Manga/Manhua/Manhwa Video Pipeline.

Implements the complete Excalidraw whiteboard flow:
  [Node 1] User inputs manga/manhua/manhwa link or title
      ↓
  [Node 2] Hermes discovers source materials (MangaDex / web)
      ↓
  [Node 3] Interactive chapter selection ("You will ask me if how many chapters i want to scrape")
      ↓
  [Node 4] Scrapes chapters into structured workspace
      ↓
  [Node 5] Runs processing:
      ├─ Subagent 1: Extract chat bubbles, analyze flow, accurate script & scene action descriptions
      ├─ Subagent 2: Create detailed structured generative video prompts to animate panels
      └─ Subagent 3: Create 9:16 vertical storyboard using Google Antigravity CLI (agy) for ingredients guide
      ↓
  [Node 6] Synthesize final deliverables:
      ├─ Complete CSV with video structured prompts, scripts & dialogues
      └─ 9:16 vertical visual storyboard guide (Markdown + HTML viewer)
      ↓
  [Node 7] Ready for user manual video generation (Flow / Kling / Runway / Luma)

Usage:
  Interactive:
    python3 manga_pipeline.py
  CLI Direct:
    python3 manga_pipeline.py --title "Solo Leveling" --chapters 1 --max-pages 5
    python3 manga_pipeline.py --url "https://mangadex.org/title/..." --chapters 1
    python3 manga_pipeline.py --existing-dir /home/john/manga-reviews/output/ch2
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Add script directory to sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from manga_source_scraper import run_pipeline_source_flow
from script_and_prompt_engine import process_chapter
from storyboard_agy import generate_storyboard_agy


def print_banner(text: str):
    line = "=" * 64
    print(f"\n{line}")
    print(f"  {text}")
    print(f"{line}\n")


def orchestrate_manga_pipeline(
    title_or_url: str = None,
    num_chapters: int = None,
    max_pages_per_ch: int = None,
    existing_dir: str = None,
    output_base: str = "/home/john/manga-reviews/output",
) -> list[dict]:
    """Execute the full end-to-end manga video pipeline."""
    base_out = Path(output_base).resolve()
    base_out.mkdir(parents=True, exist_ok=True)

    target_chapter_dirs = []

    # If existing directory was specified directly (e.g. testing with scraped chapter)
    if existing_dir:
        ed = Path(existing_dir).resolve()
        if not ed.exists():
            raise FileNotFoundError(f"Existing directory not found: {ed}")
        target_chapter_dirs.append(ed)
        print_banner(f"USING EXISTING CHAPTER DIRECTORY: {ed.name}")
    else:
        # Step 1-4: Source discovery & Chapter scraping
        print_banner("STEP 1: SOURCE DISCOVERY & CHAPTER SCRAPING")
        scraped_metas = run_pipeline_source_flow(
            input_target=title_or_url,
            num_chapters=num_chapters,
            output_base=base_out,
            max_pages_per_ch=max_pages_per_ch,
        )

        if not scraped_metas:
            print("[ABORT] No chapters were downloaded or selected.")
            return []

        for meta in scraped_metas:
            ch_num = meta["chapter"]["chapter"]
            # Find chapter directory
            # Title slug directory was used
            manga_dir = base_out / Path(meta["images"][0]).parent.parent.name
            ch_dir = manga_dir if manga_dir.name.startswith("ch") else (manga_dir / f"ch{ch_num}")
            if not ch_dir.exists():
                ch_dir = Path(meta["images"][0]).parent.parent
            target_chapter_dirs.append(ch_dir)

    all_results = []

    # Process each chapter through Subagents 1, 2, and 3
    for ch_dir in target_chapter_dirs:
        print_banner(f"PROCESSING CHAPTER: {ch_dir.name}")

        # Subagent 1 & 2: Script, Dialogue, Action Descriptions & Animation Video Prompts -> CSV
        print("[ORCHESTRATOR] Spawning Subagent 1 (Script & Dialogue) + Subagent 2 (Video Prompts)...")
        csv_path = ch_dir / "video_prompts.csv"
        scenes, final_csv = process_chapter(
            chapter_dir=ch_dir,
            output_csv=csv_path,
            max_pages=max_pages_per_ch,
        )

        # Subagent 3: 9:16 Vertical Storyboard & Ingredients Guide via agy
        print("\n[ORCHESTRATOR] Spawning Subagent 3 (9:16 Storyboard via Google Antigravity agy)...")
        beats, md_path, html_path = generate_storyboard_agy(
            chapter_dir=ch_dir,
            output_dir=ch_dir,
            max_scenes=len(scenes),
        )

        chapter_summary = {
            "chapter_dir": str(ch_dir),
            "csv_prompts": str(final_csv),
            "storyboard_markdown": str(md_path),
            "storyboard_html": str(html_path),
            "total_scenes": len(scenes),
            "total_beats": len(beats),
        }
        all_results.append(chapter_summary)

        # Print final chapter handoff summary
        print("\n" + "#" * 64)
        print("  CHAPTER PROCESSING DELIVERABLES READY")
        print("#" * 64)
        print(f"Directory:           {ch_dir}")
        print(f"1. Video Prompts CSV: {final_csv}")
        print(f"2. 9:16 Storyboard MD: {md_path}")
        print(f"3. Visual HTML View:   {html_path}")
        print(f"Total Video Scenes:  {len(scenes)}")
        print("#" * 64 + "\n")

    print_banner("PIPELINE EXECUTION COMPLETE — READY FOR MANUAL VIDEO GENERATION")
    print("How to generate videos:")
    print("1. Open the CSV or HTML viewer to inspect scene prompts & ingredients.")
    print("2. In Google Flow / Kling / Runway / Luma:")
    print("   - Select 9:16 Vertical aspect ratio.")
    print("   - Upload the referenced panel from images/.")
    print("   - Paste the Video_Animation_Prompt.")
    print("3. Use the Dialogue_Script with parenthesized emotion cues for TTS voiceover.")
    print("-" * 64)

    return all_results


def main():
    parser = argparse.ArgumentParser(description="Master Manga Video Pipeline Orchestrator")
    parser.add_argument("--title", "-t", default=None, help="Manga title to search")
    parser.add_argument("--url", "-u", default=None, help="Manga URL to scrape")
    parser.add_argument("--chapters", "-c", type=int, default=None, help="How many chapters to scrape")
    parser.add_argument("--max-pages", "-m", type=int, default=None, help="Max pages per chapter (for quick runs)")
    parser.add_argument("--existing-dir", "-e", default=None, help="Process an already scraped chapter directory")
    parser.add_argument("--output-base", "-o", default="/home/john/manga-reviews/output", help="Output base directory")
    args = parser.parse_args()

    input_target = args.url or args.title
    orchestrate_manga_pipeline(
        title_or_url=input_target,
        num_chapters=args.chapters,
        max_pages_per_ch=args.max_pages,
        existing_dir=args.existing_dir,
        output_base=args.output_base,
    )


if __name__ == "__main__":
    main()
