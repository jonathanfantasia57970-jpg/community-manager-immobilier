#!/usr/bin/env python3
"""Tests synthétiques des garanties de lot, sans service externe."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

import traiter_lot_rapide as batch
from corriger_luminosite import sha256
from inventorier_photos import inventory


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "sources"
        self.source.mkdir()
        self.output = self.root / "sorties"
        self.manifest = self.root / "inventaire.json"

    def tearDown(self):
        self.temp.cleanup()

    def picture(self, name, value=80, mode="RGB"):
        path = self.source / name
        color = (value, value, value, 155) if mode == "RGBA" else (value, value, value)
        Image.new(mode, (96, 64), color).save(path)
        return path

    def update_manifest(self):
        manifest = inventory(self.source)
        for row in manifest["photos"]:
            row["source_id"] = "test:" + row["relative_path"]
        self.manifest.write_text(json.dumps(manifest))

    def run_batch(self, niveau="un_peu_plus_lumineux", **kwargs):
        return batch.run_batch(self.manifest, self.output, niveau, **kwargs)

    def state(self):
        return json.loads((self.output / batch.REGISTRY_NAME).read_text())

    def test_numbering_resume_addition_source_preserved(self):
        paths = [self.picture("IMG_10.jpg"), self.picture("IMG_2.jpg")]
        hashes = [sha256(path) for path in paths]
        self.update_manifest()
        result = self.run_batch()
        self.assertEqual(result["produites_ou_reutilisees"], 2)
        photos = self.state()["photos"]
        self.assertEqual([(p["relative_path"], p["numero"]) for p in photos], [("IMG_2.jpg", 1), ("IMG_10.jpg", 2)])
        modified = (self.output / "01.jpg").stat().st_mtime_ns
        self.assertEqual(self.run_batch()["executions"], 0)
        self.assertEqual((self.output / "01.jpg").stat().st_mtime_ns, modified)
        self.picture("IMG_1.jpg")
        self.update_manifest()
        self.assertEqual(self.run_batch()["executions"], 1)
        self.assertEqual(self.state()["photos"][-1]["numero"], 3)
        self.assertEqual([sha256(path) for path in paths], hashes)
        for photo in self.state()["photos"]:
            version = photo["versions"][-1]
            self.assertEqual(version["dimensions"], [96, 64])
            self.assertFalse(version["enregistre"])
            self.assertEqual(version["controle_visuel"], "non_effectue")
            self.assertIsNone(version["niveau_atteint"])

    def test_levels_versions_and_changed_source(self):
        source = self.picture("a.jpg", value=90)
        self.update_manifest()
        means = []
        for level in batch.LEVELS:
            self.run_batch(level)
            version = self.state()["photos"][0]["versions"][-1]
            with Image.open(self.output / version["output_name"]) as image:
                means.append(float(np.asarray(image).mean()))
        self.assertLess(means[0], means[1])
        self.assertLess(means[1], means[2])
        old_hash = sha256(self.output / "01.jpg")
        self.picture(source.name, value=60)
        self.update_manifest()
        self.run_batch(batch.LEVELS[-1])
        self.assertEqual(self.state()["photos"][0]["versions"][-1]["version"], 4)
        self.assertEqual(sha256(self.output / "01.jpg"), old_hash)
        self.assertTrue((self.output / "01_v4.jpg").exists())

    def test_unknown_name_and_missing_result_preserved(self):
        self.picture("a.jpg")
        self.update_manifest()
        self.output.mkdir()
        (self.output / "01.jpg").write_bytes(b"fichier inconnu")
        self.run_batch()
        self.assertEqual((self.output / "01.jpg").read_bytes(), b"fichier inconnu")
        result = self.output / "01_v2.jpg"
        self.assertTrue(result.exists())
        result.write_bytes(b"fichier modifie")
        summary = self.run_batch()
        self.assertEqual(summary["executions"], 0)
        self.assertEqual(summary["erreurs_ou_a_reconcilier"], 1)
        self.assertEqual(result.read_bytes(), b"fichier modifie")
        self.run_batch(retry_errors=True)
        self.assertTrue((self.output / "01_v3.jpg").exists())
        self.assertEqual(result.read_bytes(), b"fichier modifie")

    def test_return_to_previous_level_reuses_intact_version(self):
        self.picture("a.jpg", value=90)
        self.update_manifest()
        self.run_batch("normal")
        original = self.output / "01.jpg"
        original_mtime = original.stat().st_mtime_ns
        original_hash = sha256(original)
        self.run_batch("beaucoup_plus_lumineux")
        summary = self.run_batch("normal")
        self.assertEqual(summary["executions"], 0)
        self.assertEqual(summary["produites_ou_reutilisees"], 1)
        photo = self.state()["photos"][0]
        self.assertEqual(len(photo["versions"]), 2)
        self.assertEqual(batch.current_version(photo)["output_name"], "01.jpg")
        self.assertEqual(original.stat().st_mtime_ns, original_mtime)
        self.assertEqual(sha256(original), original_hash)
        original.write_bytes(b"modification apres retour au niveau normal")
        summary = self.run_batch("normal")
        self.assertEqual(summary["executions"], 0)
        self.assertEqual(summary["erreurs_ou_a_reconcilier"], 1)
        photo = self.state()["photos"][0]
        self.assertEqual(len(photo["versions"]), 2)
        self.assertEqual(batch.current_version(photo)["status"], "resultat_local_manquant_ou_modifie")
        self.assertEqual(original.read_bytes(), b"modification apres retour au niveau normal")

    def test_partial_error_no_automatic_retry(self):
        self.picture("a.jpg")
        (self.source / "b.jpg").write_bytes(b"not an image")
        self.update_manifest()
        first = self.run_batch()
        self.assertEqual(first["produites_ou_reutilisees"], 1)
        self.assertEqual(first["erreurs_ou_a_reconcilier"], 1)
        second = self.run_batch()
        self.assertEqual(second["executions"], 0)
        self.assertEqual(len(self.state()["photos"][1]["versions"]), 1)
        self.run_batch(retry_errors=True)
        self.assertEqual(len(self.state()["photos"][1]["versions"]), 2)

    def test_exact_copy_and_transparency(self):
        source = self.picture("a.jpg", value=160)
        self.picture("b.png", mode="RGBA")
        self.update_manifest()
        self.run_batch("normal")
        photos = self.state()["photos"]
        self.assertEqual(photos[0]["versions"][0]["status"], "copiee_a_controler")
        self.assertEqual(sha256(source), sha256(self.output / "01.jpg"))
        with Image.open(self.output / "02.png") as image:
            self.assertEqual(image.size, (96, 64))
            self.assertEqual(image.mode, "RGBA")
            self.assertTrue(np.all(np.asarray(image)[..., 3] == 155))

    def test_parallel_workers_and_interrupted_state(self):
        for number in range(6):
            self.picture(f"{number}.jpg")
        self.update_manifest()
        lock = threading.Lock()
        active = maximum = 0
        original = batch.process_photo

        def measured(*args):
            nonlocal active, maximum
            with lock:
                active += 1
                maximum = max(maximum, active)
            time.sleep(.03)
            try:
                return original(*args)
            finally:
                with lock:
                    active -= 1

        with patch.object(batch, "process_photo", measured):
            self.run_batch(workers=3)
        self.assertGreaterEqual(maximum, 2)
        self.assertLessEqual(maximum, 3)
        state = self.state()
        state["photos"][0]["versions"][-1]["status"] = "en_cours"
        (self.output / batch.REGISTRY_NAME).write_text(json.dumps(state))
        summary = self.run_batch()
        self.assertEqual(summary["executions"], 0)
        self.assertEqual(summary["erreurs_ou_a_reconcilier"], 1)
        self.assertEqual(self.state()["photos"][0]["versions"][-1]["status"], "interrompu_a_reconcilier")

    def test_duplicate_identity_and_worker_bound(self):
        self.picture("a.jpg")
        self.update_manifest()
        with self.assertRaises(ValueError):
            self.run_batch(workers=6)
        data = json.loads(self.manifest.read_text())
        data["photos"].append(dict(data["photos"][0]))
        self.manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            self.run_batch()

    def test_dark_scene_gets_exposed_then_distinct_levels(self):
        self.picture("dark.jpg", value=90)
        self.update_manifest()
        medians = []
        for level in batch.LEVELS:
            self.run_batch(level)
            version = batch.current_version(self.state()["photos"][0])
            with Image.open(self.output / version["output_name"]) as image:
                medians.append(float(np.median(np.asarray(image))))
        self.assertGreaterEqual(medians[0], 157)
        self.assertGreaterEqual(medians[1], 177)
        self.assertGreaterEqual(medians[2], 195)
        self.assertGreaterEqual(medians[1] - medians[0], 15)
        self.assertGreaterEqual(medians[2] - medians[1], 14)

    def test_bright_window_does_not_leave_room_dark(self):
        pixels = np.full((100, 100, 3), 100, dtype=np.uint8)
        pixels[:30] = 55
        pixels[80:] = 242
        source = self.source / "window.png"
        Image.fromarray(pixels).save(source)
        self.update_manifest()
        self.run_batch()
        version = batch.current_version(self.state()["photos"][0])
        with Image.open(self.output / version["output_name"]) as image:
            actual = np.asarray(image)
        self.assertGreaterEqual(float(np.median(actual[35:75])), 175)
        self.assertGreaterEqual(float(np.median(actual[5:25])), 90)
        self.assertLess(float(np.median(actual[85:95])), 255)

    def test_recalibration_is_explicit_and_idempotent(self):
        self.picture("a.jpg")
        self.update_manifest()
        self.run_batch()
        state = self.state()
        state["photos"][0]["versions"][0].pop("calibration_version")
        (self.output / batch.REGISTRY_NAME).write_text(json.dumps(state))
        previous_hash = sha256(self.output / "01.jpg")
        self.assertEqual(self.run_batch()["executions"], 0)
        self.assertEqual(self.run_batch(recalibrate=True)["executions"], 1)
        self.assertEqual(sha256(self.output / "01.jpg"), previous_hash)
        self.assertEqual(batch.current_version(self.state()["photos"][0])["output_name"], "01_v2.jpg")
        self.assertEqual(self.run_batch(recalibrate=True)["executions"], 0)

    def test_large_white_window_is_excluded_from_calibration(self):
        pixels = np.full((100, 100, 3), 242, dtype=np.uint8)
        pixels[:20] = 100
        pixels[20:30] = 55
        source = self.source / "large_window.png"
        Image.fromarray(pixels).save(source)
        self.update_manifest()
        self.run_batch()
        version = batch.current_version(self.state()["photos"][0])
        with Image.open(self.output / version["output_name"]) as image:
            actual = np.asarray(image)
        self.assertGreaterEqual(float(np.median(actual[5:15])), 175)
        self.assertGreaterEqual(float(np.median(actual[22:28])), 90)
        self.assertLessEqual(float(np.max(np.abs(actual[40:90].astype(int) - 242))), 1)
        self.assertAlmostEqual(version["statistiques_apercu"]["fraction_pixels_proteges"], .7, places=2)
        self.assertEqual(version["status"], "produite_a_controler")
        self.assertEqual(version["controle_visuel"], "non_effectue")
        self.assertFalse(version["enregistre"])

    def test_already_bright_source_is_preserved_at_all_levels(self):
        originals = {f"bright_{value}.png": self.picture(f"bright_{value}.png", value=value)
                     for value in (205, 235, 255)}
        original_hashes = {name: sha256(source) for name, source in originals.items()}
        self.update_manifest()
        for level in batch.LEVELS:
            self.run_batch(level)
            for photo in self.state()["photos"]:
                version = batch.current_version(photo)
                self.assertEqual(version["status"], "copiee_a_controler")
                self.assertEqual(version["tentatives"], 0)
                self.assertFalse(version["statistiques_apercu"]["limite_correction_atteinte"])
                self.assertEqual(sha256(self.output / version["output_name"]),
                                 original_hashes[photo["relative_path"]])

    def test_unsupported_storage_fails_before_processing(self):
        self.picture("a.jpg")
        self.update_manifest()
        with patch.object(batch.os, "link", side_effect=OSError(95, "unsupported")):
            with self.assertRaisesRegex(ValueError, "disque natif"):
                self.run_batch()
        self.assertFalse((self.output / batch.REGISTRY_NAME).exists())
        self.assertEqual(list(self.output.glob("*.jpg")), [])

    def test_image_settings_signature_and_targeted_reprise(self):
        self.picture("a.png", value=100)
        self.picture("b.png", value=100)
        self.update_manifest()
        self.run_batch()
        old_hash = sha256(self.output / "01.jpg")
        other_mtime = (self.output / "02.jpg").stat().st_mtime_ns
        manifest = json.loads(self.manifest.read_text())
        manifest["photos"][0]["reglages_image"] = {"temperature": .12, "contrast": 1.05}
        self.manifest.write_text(json.dumps(manifest))
        self.assertEqual(self.run_batch()["executions"], 1)
        state = self.state()
        changed = batch.current_version(state["photos"][0])
        self.assertEqual(changed["output_name"], "01_v2.jpg")
        self.assertEqual(changed["reglages_image"], {"temperature": .12, "tint": 0., "contrast": 1.05, "saturation": 1.})
        self.assertEqual(changed["settings"]["temperature"], .12)
        self.assertEqual(changed["settings"]["contrast"], 1.05)
        with Image.open(self.output / changed["output_name"]) as image:
            rgb = np.asarray(image)
            luma = rgb[..., 0] * .2126 + rgb[..., 1] * .7152 + rgb[..., 2] * .0722
            self.assertGreaterEqual(float(np.median(luma)), 177)
        self.assertEqual((self.output / "02.jpg").stat().st_mtime_ns, other_mtime)
        self.assertEqual(sha256(self.output / "01.jpg"), old_hash)
        self.assertEqual(self.run_batch()["executions"], 0)
        manifest["photos"][0]["reglages_image"].update(tint=0, saturation=1)
        self.manifest.write_text(json.dumps(manifest))
        self.assertEqual(self.run_batch()["executions"], 0)
        manifest["photos"][0].pop("reglages_image")
        self.manifest.write_text(json.dumps(manifest))
        self.assertEqual(self.run_batch()["executions"], 0)
        self.assertEqual(batch.current_version(self.state()["photos"][0])["output_name"], "01.jpg")

    def test_thumbnail_cannot_cancel_explicit_colour_adjustment(self):
        # Le damier est coloré au format natif, mais son aperçu devient gris.
        pattern = np.array([[[240, 250, 240], [250, 240, 250]],
                            [[250, 240, 250], [240, 250, 240]]], dtype=np.uint8)
        pixels = np.tile(pattern, (960, 960, 1))
        source = self.source / "fine_pattern.png"
        rgba = Image.fromarray(pixels).convert("RGBA")
        rgba.save(source)
        before = sha256(source)
        preview = Image.fromarray(pixels)
        preview.thumbnail((192, 192))
        preview_rgb = np.asarray(preview)
        np.testing.assert_array_equal(batch.correct_rgb(preview_rgb, 0, 0, 0, saturation=.85), preview_rgb)
        self.update_manifest()
        manifest = json.loads(self.manifest.read_text())
        manifest["photos"][0]["reglages_image"] = {"saturation": .85}
        self.manifest.write_text(json.dumps(manifest))
        summary = self.run_batch("normal")
        self.assertEqual(summary["copies_sans_retouche"], 0)
        version = batch.current_version(self.state()["photos"][0])
        self.assertEqual(version["status"], "produite_a_controler")
        self.assertEqual(version["settings"]["saturation"], .85)
        self.assertEqual(version["tentatives"], 1)
        with Image.open(self.output / version["output_name"]) as image:
            actual = np.asarray(image.convert("RGB"))
            self.assertEqual(image.getchannel("A").getextrema(), (255, 255))
        self.assertTrue(np.all(np.any(actual != pixels, axis=-1)))
        self.assertEqual(sha256(source), before)
        self.assertEqual(self.run_batch("normal")["executions"], 0)

    def test_invalid_image_settings_refused_before_calculation(self):
        self.picture("a.png")
        self.update_manifest()
        manifest = json.loads(self.manifest.read_text())
        for settings in ({"temperature": .3}, {"unknown": 1}, {"saturation": "1.1"}, {"tint": float("nan")}):
            manifest["photos"][0]["reglages_image"] = settings
            self.manifest.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                self.run_batch()
            self.assertFalse(self.output.exists())

    def test_black_pixels_are_not_counted_as_successful_brightening(self):
        source = self.picture("black.png", value=0)
        self.update_manifest()
        for level in batch.LEVELS:
            summary = self.run_batch(level)
            version = batch.current_version(self.state()["photos"][0])
            self.assertEqual(version["status"], "copiee_a_controler")
            self.assertEqual(version["tentatives"], 0)
            self.assertEqual(sha256(source), sha256(self.output / version["output_name"]))
            self.assertEqual(summary["copies_sans_retouche"], 1)
            self.assertEqual(summary["limites_luminosite"], 1)


if __name__ == "__main__":
    unittest.main()
