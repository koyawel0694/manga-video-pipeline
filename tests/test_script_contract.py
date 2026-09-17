import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from build_block_prompts_txt import format_continuous_prompt, provider_safe_action, provider_script_cue
from build_serye_storyboard import build_storyboard
from chapter_contract import build_script_entries, script_cue


class ScriptContractTests(unittest.TestCase):
    def test_source_script_keeps_sfx_out_of_spoken_lines(self):
        scenes = [
            {
                "page_number": 1,
                "page_file": "page_001.png",
                "scene_title": "Impact",
                "dialogue_text": "轰!!",
                "speaker": "",
                "voice_emotion": "none",
            },
            {
                "page_number": 1,
                "page_file": "page_001.png",
                "scene_title": "Declaration",
                "dialogue_text": "I will win.",
                "speaker": "Hero",
                "voice_emotion": "resolute",
            },
        ]

        entries = build_script_entries(scenes)

        self.assertEqual([entry["text_type"] for entry in entries], ["sfx", "spoken"])
        self.assertEqual(entries[0]["speaker"], "Narrator")
        self.assertIn("not spoken", script_cue({**entries[0], "source_text": entries[0]["dialogue_text"]}))

    def test_continuous_prompt_contains_exact_script_cue(self):
        beat = {
            "timestamp": "0s-1.5s",
            "label": "THE OPENING",
            "source_scene_id": "p001-s01",
            "scene_title": "Declaration",
            "action": "The hero steps forward.",
            "camera": "Push in slowly.",
            "source_text": "I will win.",
            "text_type": "spoken",
            "speaker": "Hero",
            "voice_emotion": "(resolute)",
        }
        block = {"block_title": "Declaration", "beats": [beat]}
        prompt = format_continuous_prompt("Demo", block, 1, {
            "style_anchor": "test style",
            "motion_anchor": "test motion",
            "negative_anchor": "test negative",
        })

        self.assertIn(script_cue(beat), prompt)
        self.assertIn("Do not invent, paraphrase, repeat, or move source dialogue", prompt)

    def test_provider_safe_redaction_keeps_canonical_ledger_separate(self):
        sensitive = {
            "source_scene_id": "p017-s04",
            "scene_title": "Surrendering to Lust",
            "action": "A heart-shaped speech bubble with breathless moans surrounds a silhouette.",
            "camera": "Slow push-in.",
            "source_text": "Yes♡ Ah... Ahn...♡ Ngh...",
            "dialogue_text": "Yes♡ Ah... Ahn...♡ Ngh...",
            "text_type": "spoken",
            "speaker": "Miyuki",
            "voice_emotion": "(breathless, lustful)",
        }
        action = provider_safe_action(sensitive)
        cue = provider_script_cue(sensitive)

        self.assertIn("fully clothed", action)
        self.assertIn("public-place", action)
        self.assertNotIn("breathless moans", action.lower())
        self.assertNotIn("Yes♡ Ah", cue)
        self.assertIn("MANGA SCRIPT SAFETY REDACTION", cue)
        self.assertIn("p017-s04", cue)

    def test_provider_safe_rewrite_preserves_safe_dialogue_line(self):
        beat = {
            "source_scene_id": "p017-s02",
            "scene_title": "Embrace of Betrayal",
            "action": "Miyuki embraces the blonde upperclassman while wrapped in sheets.",
            "camera": "Pan across the embracing couple.",
            "source_text": "Eek Senpai! EIJI'S SERIOUSLY DISGUSTING, YOU KNOW?",
            "dialogue_text": "Eek Senpai! EIJI'S SERIOUSLY DISGUSTING, YOU KNOW?",
            "text_type": "spoken",
            "speaker": "Miyuki",
            "voice_emotion": "(flirtatious, dismissive)",
        }
        action = provider_safe_action(beat)
        cue = provider_script_cue(beat)

        self.assertIn("fully clothed", action)
        self.assertIn("Eek Senpai! EIJI'S SERIOUSLY DISGUSTING, YOU KNOW?", cue)
        self.assertIn("(cold, dismissive)", cue)
        self.assertNotIn("flirtatious", cue.lower())

    def test_storyboard_uses_unique_narrative_scene_ids_and_non_overlapping_pages(self):
        pages = []
        scenes = []
        for page_number in range(1, 19):
            page_scenes = []
            for scene_number in range(1, 4):
                scene = {
                    "page_number": page_number,
                    "page_file": f"page_{page_number:03d}.png",
                    "scene_title": f"Page {page_number} scene {scene_number}",
                    "dialogue_text": f"Line {page_number}-{scene_number}",
                    "speaker": "Hero",
                    "voice_emotion": "intense",
                    "action_description": "The hero moves.",
                    "camera_movement": "Hold.",
                    "story_flow": "Continue.",
                    "visual_style_fx": "None",
                }
                page_scenes.append(scene)
                scenes.append(scene)
            pages.append({"page_number": page_number, "page_file": f"page_{page_number:03d}.png", "scenes": page_scenes})

        story, episodes = build_storyboard({"title": "Demo", "chapter": "1", "pages": pages}, scenes)
        narrative_ids = [
            beat["source_scene_id"]
            for block in story["blocks"]
            for beat in block["beats"]
            if not beat["is_transitional"]
        ]
        ranges = [episode["page_range"] for episode in episodes]

        self.assertEqual(len(narrative_ids), len(set(narrative_ids)))
        self.assertEqual(story["script_line_count"], len(scenes))
        self.assertEqual(ranges, [[1, 18]])


if __name__ == "__main__":
    unittest.main()
