"""Regression checks for layout proof and delivery; no editorial quality scores."""
import contextlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
_style_tmp = tempfile.TemporaryDirectory(prefix='cm-test-charte-')
_style_root = Path(_style_tmp.name)
_profile = _style_root / 'profile.json'
_profile.write_text(json.dumps({'profile_id':'test-composition','identity':{'name':'Camille Test','role':'Conseiller immobilier'},'brand':{'signature_role':['Conseiller immobilier']}}))
_style = _style_root / 'charte.json'
subprocess.run([sys.executable,str(Path(__file__).with_name('configurer_charte.py')),'--profile',str(_profile),'--output',str(_style)],check=True,capture_output=True)
_previous_style = os.environ.get('CM_CHARTE')
os.environ['CM_CHARTE'] = str(_style)
import composer_visuel as composer
if _previous_style is None:
    os.environ.pop('CM_CHARTE', None)
else:
    os.environ['CM_CHARTE'] = _previous_style
import verifier_livraison as delivery


def tearDownModule():
    _style_tmp.cleanup()


class CompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.photo = cls.root / 'photo.png'
        Image.new('RGB', (1080, 1350), '#102330').save(cls.photo)
        cls.title = cls.root / 'titre.json'
        cls.title.write_text(json.dumps([
            [{'text': 'Votre image d’expert'}],
            [{'text': 'vous empêche-t-elle'}],
            [{'text': 'de '}, {'text': 'progresser ?', 'accent': True}]
        ]))
        cls.output = cls.root / 'final.png'
        result = composer.compose(cls.photo, cls.title, cls.output)
        cls.proof = Path(result['composition'])
        cls.original_proof = cls.proof.read_bytes()
        cls.original_output = cls.output.read_bytes()
        cls.reviewed = cls.root / 'texte-relu.txt'
        cls.reviewed.write_text('Un texte relu.\n\nUne idée développée.')
        cls.response = cls.root / 'reponse.md'

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def tearDown(self):
        self.output.write_bytes(self.original_output)
        self.proof.write_bytes(self.original_proof)

    def run_delivery(self, text=None, link=None, extra=(), composition=True):
        self.response.write_text(
            ':::writing{variant="social_post" id="12345"}\n'
            + (text if text is not None else self.reviewed.read_text())
            + '\n:::\n\n[final.png](' + (link or 'sandbox:' + str(self.output)) + ')\n')
        argv = ['verify', '--response', str(self.response), '--require-post-block',
                '--reviewed-text', str(self.reviewed), '--image', str(self.output)]
        if composition:
            argv += ['--composition', str(self.proof)]
        argv += list(extra)
        with patch('sys.argv', argv), contextlib.redirect_stdout(io.StringIO()) as output:
            result = delivery.main()
        return result, output.getvalue()

    def test_valid_assembly_and_exact_text_delivery(self):
        self.assertTrue(composer.verify(self.proof, self.output)['composition_verified'])
        self.assertEqual(self.run_delivery()[0], 0)

    def test_photo_without_overlay_rejected_even_with_updated_hash(self):
        self.output.write_bytes(self.photo.read_bytes())
        data = json.loads(self.proof.read_text())
        data['output']['sha256'] = composer.digest(self.output)
        self.proof.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'calque appliqué'):
            composer.verify(self.proof, self.output)

    def test_altered_output_rejected(self):
        with Image.open(self.output) as im:
            changed = im.copy()
        changed.putpixel((500, 600), (255, 0, 0))
        changed.save(self.output)
        self.assertEqual(self.run_delivery()[0], 1)

    def test_proof_cannot_point_to_another_image(self):
        other = self.root / 'autre.png'
        other.write_bytes(self.original_output)
        with self.assertRaisesRegex(ValueError, 'fichier livré'):
            composer.verify(self.proof, other)

    def test_missing_calque_is_not_proof(self):
        data = json.loads(self.proof.read_text())
        data['overlay_png']['path'] = str(self.root / 'absent.png')
        self.proof.write_text(json.dumps(data))
        self.assertEqual(self.run_delivery()[0], 1)

    def test_title_change_requires_recomposition(self):
        new_title = self.root / 'autre-titre.json'
        new_title.write_text(json.dumps([[{'text': 'Un autre titre'}]]))
        data = json.loads(self.proof.read_text())
        data['headline'] = composer.record(new_title)
        self.proof.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'texte et à la charte'):
            composer.verify(self.proof, self.output)

    def test_noncanonical_style_rejected(self):
        other = self.root / 'autre-charte.json'
        other.write_text('{}')
        data = json.loads(self.proof.read_text())
        data['style'] = composer.record(other)
        self.proof.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'charte et à la police courantes'):
            composer.verify(self.proof, self.output)

    def test_text_changed_after_review_rejected(self):
        result, output = self.run_delivery(text='Un texte différent.')
        self.assertEqual(result, 1)
        self.assertIn('diffère du texte relu', output)

    def test_raw_block_content_cannot_escape_review_comparison(self):
        for added in ['\n\n    Une phrase ajoutée.', '\n\n```\nUne phrase ajoutée.\n```']:
            with self.subTest(added=added):
                self.assertEqual(self.run_delivery(text=self.reviewed.read_text() + added)[0], 1)

    def test_series_matches_each_reviewed_text_in_order(self):
        second = self.root / 'second-texte.txt'
        second.write_text('Un second post relu.')
        self.response.write_text(':::writing{variant="social_post" id="12345"}\n'
                                 + self.reviewed.read_text() + '\n:::\n\n'
                                 + ':::writing{variant="social_post" id="12346"}\n'
                                 + second.read_text() + '\n:::\n')
        argv = ['verify', '--response', str(self.response), '--require-post-block',
                '--reviewed-text', str(self.reviewed), '--reviewed-text', str(second)]
        with patch('sys.argv', argv), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(delivery.main(), 0)

    def test_rgb_transparency_rejected_even_with_updated_hash(self):
        with Image.open(self.output) as im:
            changed = im.convert('RGB')
        changed.save(self.output, transparency=(16, 35, 48))
        data = json.loads(self.proof.read_text())
        data['output']['sha256'] = composer.digest(self.output)
        self.proof.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'transparence'):
            composer.verify(self.proof, self.output)

    def test_native_link_uses_actual_save_result(self):
        native = self.root / 'save-result.json'
        # Fictional fixture for the parser, never used as a real Library ID.
        native.write_text(json.dumps({'structuredContent': {
            'operation': 'create_library_file', 'status': 'succeeded',
            'library_file_id': 'libfile_TESTONLY', 'file_name': self.output.name,
            'file_size_bytes': self.output.stat().st_size}}))
        link = 'https://chatgpt.com/library?file_id=libfile_TESTONLY&account_id=personal'
        self.assertEqual(self.run_delivery(link=link, extra=['--library-result', str(native)])[0], 0)
        self.assertEqual(self.run_delivery(link=link.replace('libfile_TESTONLY', 'libfile_WRONG'), extra=['--library-result', str(native)])[0], 1)

    def test_new_image_needs_proof_historical_repair_is_explicit(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_delivery(composition=False)
        result, output = self.run_delivery(composition=False, extra=['--existing-image'])
        self.assertEqual(result, 0)
        self.assertFalse(json.loads(output)['composition_verified'])

    def test_other_formats_and_no_silent_crop(self):
        for format_name, height in [('1:1', 1080), ('9:16', 1920)]:
            with self.subTest(format=format_name):
                photo = self.root / f'photo-{height}.png'
                Image.new('RGB', (1080, height), '#102330').save(photo)
                output = self.root / f'final-{height}.png'
                result = composer.compose(photo, self.title, output, format_name=format_name)
                self.assertTrue(composer.verify(result['composition'], output)['composition_verified'])
                with self.assertRaisesRegex(ValueError, 'format 4:5'):
                    composer.compose(photo, self.title, self.root / 'mauvais-format.png')

    def test_invalid_headline_data_fails_cleanly(self):
        for lines in [None, ['texte'], [[3]], [[{'text': '   '}]], [[{'text': 'Titre', 'accent': 'false'}]]]:
            with self.subTest(lines=lines), self.assertRaises(ValueError):
                composer.typo.render_overlay(lines)


if __name__ == '__main__':
    unittest.main()
