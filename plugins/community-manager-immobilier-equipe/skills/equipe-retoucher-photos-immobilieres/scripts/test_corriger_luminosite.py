"""Tests synthétiques de fidélité et de protection des fichiers, sans réseau."""
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, PngImagePlugin

from corriger_luminosite import correct_file, correct_rgb, sha256, linear_luminance


class TonalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def make_source(self, mode="RGB", name="source.png", **options):
        path = self.root / name
        color = (55, 75, 95, 128) if mode == "RGBA" else (55, 75, 95)
        Image.new(mode, (30, 20), color).save(path, **options)
        return path

    def test_source_dimensions_and_candidate_status(self):
        source = self.make_source()
        original_hash = sha256(source)
        out = self.root / "out.png"
        report = correct_file(source, out, 0.25, 0.7)
        self.assertEqual(sha256(source), original_hash)
        self.assertEqual(report["dimensions"], [30, 20])
        self.assertEqual(report["status"], "candidate_requires_visual_review")
        self.assertFalse(report["enregistre"])
        with Image.open(out) as result:
            self.assertGreater(result.getpixel((10, 10))[0], 55)
            self.assertTrue(result.info.get("icc_profile"))

    def test_overwrite_and_noop_refused(self):
        source = self.make_source()
        for dest in (source, self.make_source(name="existing.png")):
            before = dest.read_bytes()
            with self.assertRaises(ValueError):
                correct_file(source, dest, 0.2)
            self.assertEqual(dest.read_bytes(), before)
        with self.assertRaises(ValueError):
            correct_file(source, self.root / "noop.png")
        self.assertFalse((self.root / "noop.png").exists())

    def test_curve_preserves_endpoints_and_order(self):
        ramp = np.repeat(np.arange(256, dtype=np.uint8)[None, :, None], 3, axis=2)
        for ev, shadows, highlights in [(0.25, 0.7, 0), (3.0, 2, 0.8), (-1.5, 0, 0.8)]:
            corrected = correct_rgb(ramp, ev, shadows, highlights)
            self.assertTrue(np.all(corrected[0, 0] == 0))
            self.assertTrue(np.all(corrected[0, -1] == 255))
            self.assertTrue(np.all(np.diff(corrected[0, :, 0].astype(int)) >= 0))
            self.assertTrue(np.all(corrected[..., 0] == corrected[..., 1]))

    def test_alpha_and_no_geometry_change(self):
        source = self.make_source(mode="RGBA")
        report = correct_file(source, self.root / "alpha.png", 0.2)
        self.assertEqual(report["dimensions"], [30, 20])
        with Image.open(self.root / "alpha.png") as out:
            self.assertEqual(out.getchannel("A").getextrema(), (128, 128))
        with self.assertRaises(ValueError):
            correct_file(source, self.root / "alpha.jpg", 0.2)

    def test_selective_curve_monotone_and_highlights_protected(self):
        ramp = np.repeat(np.arange(256, dtype=np.uint8)[None, :, None], 3, axis=2)
        for ev in (-1.5, -.5, 0, .05, .5, 1.5, 3):
            for shadows in (0, .05, .5, 1.5, 2):
                for highlights in (0, .2, .8):
                    with self.subTest(ev=ev, shadows=shadows, highlights=highlights):
                        result = correct_rgb(ramp, ev, shadows, highlights)
                        self.assertTrue(np.all(np.diff(result[0, :, 0].astype(int)) >= 0))
                        self.assertEqual(int(result[0, 0, 0]), 0)
                        self.assertEqual(int(result[0, 255, 0]), 255)
                        if ev >= 0 and highlights == 0:
                            np.testing.assert_array_equal(result[:, 220:], ramp[:, 220:])
        lifted = correct_rgb(ramp, 2, 1, 0)
        self.assertGreater(int(lifted[0, 70, 0]), 70)
        self.assertGreater(int(lifted[0, 130, 0]), 130)
        self.assertLess(int(lifted[0, 219, 0]), 221)

    def test_png_preserves_bright_regions_and_band_boundaries(self):
        # Plusieurs bandes de calcul et frontières artificielles franchies par
        # les mêmes tons : la sortie doit dépendre des pixels, pas de la bande.
        pixels = np.full((193, 256, 3), 242, dtype=np.uint8)
        pixels[:, :64] = 60
        pixels[:, 64:128] = np.arange(64, dtype=np.uint8)[None, :, None] + 90
        pixels[:, 128:164] = np.arange(220, 256, dtype=np.uint8)[None, :, None]
        source = self.root / "window.png"
        Image.fromarray(pixels).save(source)
        original_hash = sha256(source)
        output = self.root / "selective.png"
        report = correct_file(source, output, 2.5, 1.2)
        with Image.open(output) as image:
            result = np.asarray(image)
        self.assertEqual(sha256(source), original_hash)
        np.testing.assert_array_equal(result[:, 128:], pixels[:, 128:])
        self.assertGreater(float(np.median(result[:, :64])), 100)
        for row in (63, 64, 127, 128, 191, 192):
            np.testing.assert_array_equal(result[row], result[0])
        stats = report["sample_statistics_before_encoding"]
        self.assertGreater(stats["protected_sample_pixels"], 0)
        self.assertEqual(stats["protected_sample_pixels_changed"], 0)
        self.assertEqual(stats["new_clipped_sample_channels"], 0)

    def test_coloured_pixels_do_not_gain_clipped_channels(self):
        pixels = np.random.default_rng(17).integers(0, 256, (96, 96, 3), dtype=np.uint8)
        result = correct_rgb(pixels, 3, 2, 0)
        self.assertFalse(np.any((pixels < 255) & (result == 255)))
        self.assertTrue(np.all(result >= pixels))

    def test_colour_controls_direction_and_luminance(self):
        gray = np.full((10, 10, 3), 128, dtype=np.uint8)
        warm = correct_rgb(gray, 0, 0, 0, temperature=.25)
        cool = correct_rgb(gray, 0, 0, 0, temperature=-.25)
        magenta = correct_rgb(gray, 0, 0, 0, tint=.20)
        green = correct_rgb(gray, 0, 0, 0, tint=-.20)
        self.assertGreater(int(warm[0, 0, 0]), int(warm[0, 0, 2]))
        self.assertLess(int(cool[0, 0, 0]), int(cool[0, 0, 2]))
        self.assertLess(int(magenta[0, 0, 1]), int(magenta[0, 0, 0]))
        self.assertGreater(int(green[0, 0, 1]), int(green[0, 0, 0]))
        for image in (warm, cool, magenta, green):
            np.testing.assert_allclose(linear_luminance(image), linear_luminance(gray), atol=.003)
        np.testing.assert_array_equal(correct_rgb(gray, 0, 0, 0), gray)
        pixels = np.array([[[160, 110, 70], [255, 255, 255], [0, 0, 0]]], dtype=np.uint8)
        more = correct_rgb(pixels, 0, 0, 0, saturation=1.15)
        less = correct_rgb(pixels, 0, 0, 0, saturation=.85)
        self.assertGreater(np.ptp(more[0, 0]), np.ptp(less[0, 0]))
        for image in (more, less):
            np.testing.assert_array_equal(image[:, 1:], pixels[:, 1:])
            np.testing.assert_allclose(linear_luminance(image), linear_luminance(pixels), atol=.003)

    def test_contrast_monotone_and_bright_regions_preserved(self):
        ramp = np.repeat(np.arange(256, dtype=np.uint8)[None, :, None], 3, axis=2)
        for contrast in (.85, .95, 1, 1.05, 1.15):
            for ev, shadows, highlights in [(0, 0, 0), (3, 2, 0), (-1.5, 0, .8)]:
                result = correct_rgb(ramp, ev, shadows, highlights, contrast=contrast)
                self.assertTrue(np.all(np.diff(result[0, :, 0].astype(int)) >= 0))
                self.assertEqual(int(result[0, 0, 0]), 0)
                self.assertEqual(int(result[0, 255, 0]), 255)
                if ev >= 0 and highlights == 0:
                    np.testing.assert_array_equal(result[:, 220:], ramp[:, 220:])
        stronger = correct_rgb(ramp, 0, 0, 0, contrast=1.15)
        self.assertLess(int(stronger[0, 100, 0]), 100)
        self.assertGreater(int(stronger[0, 180, 0]), 180)

    def test_colour_gamut_has_no_new_clipped_channels(self):
        pixels = np.random.default_rng(32).integers(0, 256, (128, 128, 3), dtype=np.uint8)
        for temperature, tint, saturation in [(.25, .20, 1.15), (-.25, -.20, 1.15), (.25, -.20, .85)]:
            colour_only = correct_rgb(pixels, 0, 0, 0, temperature=temperature,
                                      tint=tint, saturation=saturation)
            self.assertFalse(np.any((pixels < 255) & (colour_only == 255)))
            np.testing.assert_allclose(linear_luminance(colour_only), linear_luminance(pixels), atol=.005)
            combined = correct_rgb(pixels, 3, 2, 0, temperature=temperature,
                                   tint=tint, contrast=1.15, saturation=saturation)
            self.assertFalse(np.any((pixels < 255) & (combined == 255)))

    def test_colour_only_png_source_alpha_and_invalid_values(self):
        source = self.make_source(mode="RGBA")
        before = sha256(source)
        output = self.root / "colour.png"
        report = correct_file(source, output, temperature=.12, tint=-.05, contrast=1.04, saturation=1.05)
        self.assertEqual(sha256(source), before)
        self.assertEqual(report["dimensions"], [30, 20])
        self.assertEqual(report["settings"]["temperature"], .12)
        self.assertFalse(report["enregistre"])
        with Image.open(output) as image:
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.getchannel("A").getextrema(), (128, 128))
        for settings in ({"temperature": .26}, {"tint": -.21}, {"contrast": 1.16},
                         {"saturation": .84}, {"contrast": float("nan")}, {"temperature": True}):
            with self.assertRaises(ValueError):
                correct_file(source, self.root / "invalid.png", **settings)
        self.assertFalse((self.root / "invalid.png").exists())

    def test_exif_orientation_and_nested_dimensions(self):
        exif = Image.Exif()
        exif[274] = 6
        exif[34665] = {40961: 1, 40962: 30, 40963: 20}
        source = self.make_source(name="rotated.jpg", exif=exif)
        out = self.root / "oriented.jpg"
        correct_file(source, out, 0.2)
        with Image.open(out) as image:
            self.assertEqual(image.size, (20, 30))
            self.assertIsNone(image.getexif().get(274))
            detail = image.getexif().get_ifd(34665)
            self.assertEqual((detail[40962], detail[40963]), (20, 30))
            self.assertEqual(detail[40961], 1)
            self.assertNotIn(40961, image.getexif())

    def test_uncalibrated_exif_without_profile_refused(self):
        exif = Image.Exif()
        exif[34665] = {40961: 65535}
        source = self.make_source(name="uncalibrated.jpg", exif=exif)
        with self.assertRaisesRegex(ValueError, "non sRGB"):
            correct_file(source, self.root / "out.png", 0.2)

    def test_non_srgb_gamma_refused(self):
        info = PngImagePlugin.PngInfo()
        info.add(b"gAMA", struct.pack(">I", 100000))
        source = self.make_source(pnginfo=info)
        with self.assertRaisesRegex(ValueError, "gamma"):
            correct_file(source, self.root / "out.png", 0.2)

    def test_rgb_16_bit_png_refused(self):
        def chunk(kind, payload):
            return (struct.pack(">I", len(payload)) + kind + payload
                    + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff))
        header = struct.pack(">IIBBBBB", 2, 1, 16, 2, 0, 0, 0)
        pixels = b"\x00" + struct.pack(">6H", *([25700] * 3 + [25701] * 3))
        source = self.root / "high-depth.png"
        source.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                           + chunk(b"IDAT", zlib.compress(pixels)) + chunk(b"IEND", b""))
        with self.assertRaisesRegex(ValueError, "haute profondeur"):
            correct_file(source, self.root / "out.png", 0.2)

    def test_invalid_settings_and_corrupt_image_refused(self):
        source = self.make_source()
        for value in (float("nan"), float("inf"), 3.1):
            with self.assertRaises(ValueError):
                correct_file(source, self.root / "out.png", value)
        source.write_bytes(b"not an image")
        with self.assertRaises(OSError):
            correct_file(source, self.root / "out.png", 0.2)
        self.assertFalse((self.root / "out.png").exists())


if __name__ == "__main__":
    unittest.main()
