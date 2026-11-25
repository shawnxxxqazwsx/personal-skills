#!/usr/bin/env python3
"""Bounded stdlib tests; every created asset lives in TemporaryDirectory."""
import contextlib
import copy
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ir_bank as bank


def wav(path, samples=(.25, -.125, .0625), extensible=False, tag=3, extra=False):
    payload = b''.join(struct.pack('<f', sample) for sample in samples)
    fmt = struct.pack('<HHIIHH', 0xFFFE if extensible else tag, 1, 48000, 192000, 4, 32)
    if extensible:
        fmt += struct.pack('<HHI', 22, 32, 4) + bank.FLOAT_GUID
    chunks = b'fmt ' + struct.pack('<I', len(fmt)) + fmt
    if extra:
        chunks += b'JUNK' + struct.pack('<I', 3) + b'abc\0'
    chunks += b'data' + struct.pack('<I', len(payload)) + payload
    path.write_bytes(b'RIFF' + struct.pack('<I', len(chunks) + 4) + b'WAVE' + chunks)
    return path


class BankTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='chlora-ir-bank-unit-')
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.temp.cleanup)

    def recipe(self, profiles=('stereo', '916'), physical=15, identical=False):
        definitions = {}
        for name in profiles:
            definitions[name] = [{'slot': slot, 'physical_source_id': f'S{index % physical:02}'}
                                 for index, slot in enumerate(bank.PROFILES[name])]
        sources = sorted({r['physical_source_id'] for rows in definitions.values() for r in rows})
        outputs = [{'slot': slot, 'receiver_id': f'R{slot:02}', 'role': bank.ROLES[slot]}
                   for slot in bank.OUTPUT_SLOTS]
        transfers = []
        source = self.root / 'same.wav'
        if identical:
            wav(source)
        for si, sid in enumerate(sources):
            for receiver in outputs:
                path = source if identical else wav(self.root / f'{sid}-{receiver["receiver_id"]}.wav',
                                                    ((si + 1) / 32, receiver['slot'] / 64, -.03125))
                transfers.append({'physical_source_id': sid, 'receiver_id': receiver['receiver_id'], 'file': path.name})
        value = {'schema': 'chlora-ir-bank-recipe/v1', 'label': 'Test Bank', 'room': 'Test Room',
                 'profiles': definitions, 'outputs': outputs, 'transfers': transfers}
        return value

    def save_recipe(self, value):
        path = self.root / 'recipe.json'; path.write_bytes(bank.json_bytes(value)); return path

    def build(self, value, name='built'):
        output = self.root / name
        receipt = bank.build_recipe(self.save_recipe(value), output)
        return output, receipt

    def test_full_profiles_common_assets_source_identity_and_native_order(self):
        recipe = self.recipe()
        originals = {p: p.read_bytes() for p in self.root.glob('*.wav')}
        output, receipt = self.build(recipe)
        stereo = bank.load_json(output / bank.NAMES['stereo'])
        surround = bank.load_json(output / bank.NAMES['916'])
        self.assertEqual([r['logical_cells'] for r in receipt['banks']], [30, 225])
        self.assertEqual([r['physical_lanes'] for r in receipt['banks']], [30, 225])
        self.assertEqual([len(g['lanes']) for g in surround['banks']], [128, 97])
        self.assertEqual(receipt['unique_asset_files'], 225)
        self.assertNotEqual(stereo['entry_uuid'], surround['entry_uuid'])
        self.assertEqual(stereo['banks'][0]['lanes'][0]['mono_wav'], surround['banks'][0]['lanes'][0]['mono_wav'])
        self.assertEqual(stereo['metadata']['base_label'], recipe['label'])
        self.assertEqual(stereo['label'], recipe['label'] + ' · 立体声 → 9.0.6')
        self.assertEqual(surround['label'], recipe['label'] + ' · 9.1.6 → 9.0.6')
        positions = [(lane['physical_source_id'], lane['output_slot'])
                     for group in surround['banks'] for lane in group['lanes']]
        self.assertEqual(positions, sorted(positions))
        for group in surround['banks']:
            self.assertEqual([v['lane'] for v in group['lanes']], list(range(1, len(group['lanes']) + 1)))
        for path, original in originals.items():
            self.assertEqual(path.read_bytes(), original)
        for name in ('stereo', '916'):
            self.assertTrue(bank.validate_bank(output / bank.NAMES[name], name)['ok'])

    def test_shared_source_folding_and_equal_bytes_do_not_merge_lane_identity(self):
        output, receipt = self.build(self.recipe(physical=1, identical=True))
        self.assertEqual(receipt['unique_asset_files'], 1)
        self.assertEqual([r['physical_lanes'] for r in receipt['banks']], [15, 15])
        stereo = bank.load_json(output / bank.NAMES['stereo'])
        surround = bank.load_json(output / bank.NAMES['916'])
        self.assertEqual(stereo['banks'][0]['lanes'][0]['input_slots'], [1, 2])
        self.assertEqual(surround['banks'][0]['lanes'][0]['input_slots'], bank.OUTPUT_SLOTS)
        output2, receipt2 = self.build(self.recipe(profiles=('916',), physical=3, identical=True), 'three-sources')
        self.assertEqual(receipt2['banks'][0]['physical_lanes'], 45)
        self.assertEqual(receipt2['unique_asset_files'], 1)
        self.assertEqual(len(bank.load_json(output2 / bank.NAMES['916'])['banks'][0]['lanes']), 45)

    def test_padding_is_explicit_trailing_zero_only_and_original_bytes_stay(self):
        recipe = self.recipe(profiles=('stereo',), physical=1)
        first = self.root / recipe['transfers'][0]['file']; wav(first, (.5,))
        before = first.read_bytes()
        with self.assertRaisesRegex(bank.BankError, 'pad_to_common_frames'):
            self.build(recipe)
        self.assertFalse((self.root / 'built').exists())
        recipe['pad_to_common_frames'] = True
        output, receipt = self.build(recipe)
        self.assertEqual(receipt['padded_to_frames'], 3)
        manifest = bank.load_json(output / bank.NAMES['stereo'])
        asset = output / manifest['banks'][0]['lanes'][0]['mono_wav']
        info = bank.inspect_wav(asset)
        with asset.open('rb') as stream:
            stream.seek(info.data_offset); self.assertEqual(stream.read(), struct.pack('<fff', .5, 0, 0))
        self.assertEqual(first.read_bytes(), before)
        self.assertEqual({g['frames'] for g in receipt['banks'][0]['groups']}, {3})

    def test_wav_extensible_and_exact_copy_with_extra_chunks(self):
        recipe = self.recipe(profiles=('stereo',), physical=1, identical=True)
        source = self.root / 'same.wav'; wav(source, extensible=True, extra=True)
        original = source.read_bytes(); self.assertEqual(bank.inspect_wav(source).frames, 3)
        output, receipt = self.build(recipe)
        self.assertEqual(receipt['unique_asset_files'], 1)
        self.assertEqual(next((output / 'assets').iterdir()).read_bytes(), original)

    def test_bad_wavs_and_arithmetic_limits(self):
        for index, sample in enumerate([float('nan'), float('inf'), -float('inf'), 1_000_001.]):
            path = wav(self.root / f'bad-{index}.wav', [sample])
            with self.assertRaises(bank.BankError): bank.inspect_wav(path)
        with self.assertRaises(bank.BankError): bank.inspect_wav(wav(self.root / 'pcm.wav', tag=1))
        good = wav(self.root / 'l1-boundary.wav', [1_000_000.] * 1000)
        self.assertEqual(bank.inspect_wav(good).l1, 1e9)
        with self.assertRaises(bank.BankError): bank.inspect_wav(wav(self.root / 'too-much.wav', [1_000_000.] * 1001))
        bad = wav(self.root / 'truncated.wav'); bad.write_bytes(bad.read_bytes()[:-1])
        with self.assertRaises(bank.BankError): bank.inspect_wav(bad)

    def test_validator_rejects_data_before_fmt_even_with_correct_hash(self):
        output, _ = self.build(self.recipe(profiles=('stereo',), physical=1, identical=True))
        manifest_path = output / bank.NAMES['stereo']
        manifest = bank.load_json(manifest_path)
        asset = output / manifest['banks'][0]['lanes'][0]['mono_wav']
        original = asset.read_bytes()
        self.assertEqual(original[12:16], b'fmt ')
        self.assertEqual(original[36:40], b'data')
        asset.write_bytes(original[:12] + original[36:] + original[12:36])
        for group in manifest['banks']:
            for lane in group['lanes']:
                lane['sha256'] = bank.digest(asset)
        manifest_path.write_bytes(bank.json_bytes(manifest))
        with self.assertRaisesRegex(bank.BankError, 'data must follow fmt'):
            bank.validate_bank(manifest_path, 'stereo')

    def test_greedy_budget_boundary_lane_limit_frames_and_eight_group_gate(self):
        self.assertEqual([len(g['lanes']) for g in bank.pack_lanes([{'frames': 1}] * 129)], [128, 1])
        self.assertEqual([len(g['lanes']) for g in bank.pack_lanes([{'frames': 1_000_000}] * 30)], [30])
        self.assertEqual([len(g['lanes']) for g in bank.pack_lanes([{'frames': 1_000_001}] * 30)], [29, 1])
        self.assertEqual(len(bank.pack_lanes([{'frames': 1_440_000}] * 160)), 8)
        with self.assertRaisesRegex(bank.BankError, '8 internal groups'):
            bank.pack_lanes([{'frames': 1_440_000}] * 161)
        for invalid in [True, 0, 1.0, 1_440_001]:
            with self.assertRaises(bank.BankError): bank.pack_lanes([{'frames': invalid}])
        self.assertEqual(len(bank.pack_lanes([{'frames': 2}, {'frames': 3}])), 2)

    def test_missing_extra_duplicate_recipe_transfers_and_bad_profile_reject(self):
        base = self.recipe(profiles=('stereo',), physical=1, identical=True)
        for kind in ('missing', 'extra', 'duplicate', 'input-lfe', 'output-lfe', 'boolean-slot', 'duplicate-receiver'):
            value = copy.deepcopy(base)
            if kind == 'missing': value['transfers'].pop()
            if kind == 'extra': value['transfers'].append(dict(value['transfers'][0], physical_source_id='not-used'))
            if kind == 'duplicate': value['transfers'].append(value['transfers'][0])
            if kind == 'input-lfe': value['profiles']['stereo'][0]['slot'] = 4
            if kind == 'output-lfe': value['outputs'][0]['slot'] = 4
            if kind == 'boolean-slot': value['profiles']['stereo'][0]['slot'] = True
            if kind == 'duplicate-receiver': value['outputs'][1]['receiver_id'] = value['outputs'][0]['receiver_id']
            with self.subTest(kind=kind), self.assertRaises(bank.BankError): self.build(value)
            self.assertFalse((self.root / 'built').exists())

    def test_validator_rejects_malformed_shape_hash_frames_order_folding_and_profile(self):
        output, _ = self.build(self.recipe(profiles=('stereo',), physical=1, identical=True))
        path = output / bank.NAMES['stereo']; original = bank.load_json(path)
        mutations = [lambda v: v.update(version=True), lambda v: v.update(version=1.0),
                     lambda v: v['banks'][0]['lanes'][0].update(sha256='0' * 64),
                     lambda v: v['banks'][0]['lanes'][0].update(frames=True),
                     lambda v: v['banks'][0]['lanes'][0].update(sample_rate=48000.0),
                     lambda v: v['banks'][0]['lanes'][0].update(input_slots=[1]),
                     lambda v: v['banks'][0]['lanes'][0].update(input_slots=[1, 1, 2]),
                     lambda v: v['banks'][0]['lanes'][0].update(output_slot=4),
                     lambda v: v['banks'][0]['lanes'].pop(),
                     lambda v: v.update(silent_input_slots=[4]),
                     lambda v: v['outputs'][0].update(slot=2),
                     lambda v: v['banks'][0].update(id=True),
                     lambda v: v.update(package_root='assets')]
        for index, change in enumerate(mutations):
            broken = copy.deepcopy(original); change(broken); path.write_bytes(bank.json_bytes(broken))
            with self.subTest(case=index), self.assertRaises((bank.BankError, OSError)): bank.validate_bank(path)
        broken = copy.deepcopy(original); broken['banks'][0]['lanes'][0], broken['banks'][0]['lanes'][1] = broken['banks'][0]['lanes'][1], broken['banks'][0]['lanes'][0]
        for i, lane in enumerate(broken['banks'][0]['lanes'], 1): lane['lane'] = i
        path.write_bytes(bank.json_bytes(broken))
        with self.assertRaisesRegex(bank.BankError, 'order'): bank.validate_bank(path)
        path.write_bytes(bank.json_bytes(original))
        with self.assertRaisesRegex(bank.BankError, 'profile'): bank.validate_bank(path, '916')

    def test_native_display_roles_and_repeated_receiver_ids_are_accepted_by_validator(self):
        recipe = self.recipe(profiles=('stereo',), physical=1, identical=True)
        recipe['profiles']['stereo'][0]['role'] = 'stage_source_01'
        recipe['outputs'][0]['role'] = 'Custom receiver description'
        output, _ = self.build(recipe)
        path = output / bank.NAMES['stereo']; value = bank.load_json(path)
        value['outputs'][1]['receiver_id'] = value['outputs'][0]['receiver_id']
        for lane in value['banks'][0]['lanes']:
            if lane['output_slot'] == value['outputs'][1]['slot']:
                lane['receiver_id'] = value['outputs'][0]['receiver_id']
        path.write_bytes(bank.json_bytes(value))
        self.assertTrue(bank.validate_bank(path)['ok'])

    def test_canonical_root_escape_absolute_path_and_symlink_escape(self):
        output, _ = self.build(self.recipe(profiles=('stereo',), physical=1, identical=True))
        path = output / bank.NAMES['stereo']; original = bank.load_json(path)
        outside = wav(self.root / 'outside.wav')
        for relative in [str(outside), '../outside.wav', 'assets/escape.wav']:
            if relative.endswith('escape.wav'): (output / relative).symlink_to(outside)
            value = copy.deepcopy(original); value['banks'][0]['lanes'][0]['mono_wav'] = relative
            path.write_bytes(bank.json_bytes(value))
            with self.assertRaises((bank.BankError, OSError)): bank.validate_bank(path)

    def test_destinations_never_replace_even_at_atomic_directory_publish_race(self):
        recipe = self.recipe(profiles=('stereo',), physical=1, identical=True)
        output = self.root / 'already'; output.mkdir(); (output / 'keep').write_text('unchanged')
        with self.assertRaises(bank.BankError): bank.build_recipe(self.save_recipe(recipe), output)
        self.assertEqual((output / 'keep').read_text(), 'unchanged')
        publish = bank.publish_directory
        def race(stage, destination):
            destination.mkdir(); (destination / 'keep').write_text('racing-writer'); publish(stage, destination)
        with mock.patch.object(bank, 'publish_directory', side_effect=race), self.assertRaises(OSError):
            self.build(recipe, 'raced')
        self.assertEqual((self.root / 'raced/keep').read_text(), 'racing-writer')
        self.assertEqual(list(self.root.glob('.raced.ir-bank-*')), [])

    def test_catalog_paths_hash_profiles_limits_and_no_replace(self):
        output, _ = self.build(self.recipe(physical=1, identical=True))
        receipt = bank.catalog(output); rows = bank.load_json(output / 'bank-catalog.json')['banks']
        self.assertEqual(receipt['entries'], 2)
        self.assertEqual({r['active_inputs'] for r in rows}, {2, 15})
        for row in rows:
            self.assertFalse(Path(row['path']).is_absolute()); self.assertEqual(row['sha256'], bank.digest(output / row['path']))
        original = (output / 'bank-catalog.json').read_bytes()
        with self.assertRaises(bank.BankError): bank.catalog(output)
        self.assertEqual((output / 'bank-catalog.json').read_bytes(), original)
        huge = self.root / 'huge-catalog.json'
        with mock.patch.object(bank, 'validate_bank', return_value={'room': 'R', 'label': 'x' * 1_048_576, 'sha256': '0' * 64, 'active_inputs': 2}), self.assertRaisesRegex(bank.BankError, '1 MiB'):
            bank.catalog(output, huge)
        self.assertFalse(huge.exists())
        many = self.root / 'many'; many.mkdir()
        for i in range(4097): (many / f'{i:04}.irmatrix.json').touch()
        with mock.patch.object(bank, 'validate_bank', return_value={'room': 'R', 'label': 'L', 'sha256': '0' * 64, 'active_inputs': 2}), self.assertRaisesRegex(bank.BankError, '4096'):
            bank.catalog(many)
        self.assertFalse((many / 'bank-catalog.json').exists())

    def test_cli_receipt_and_json_error_nonzero(self):
        output, _ = self.build(self.recipe(profiles=('stereo',), physical=1, identical=True))
        script = Path(bank.__file__)
        result = subprocess.run([sys.executable, '-B', str(script), 'validate', str(output / bank.NAMES['stereo']), '--profile', 'stereo'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr); self.assertTrue(json.loads(result.stdout)['ok']); self.assertEqual(result.stderr, '')
        result = subprocess.run([sys.executable, '-B', str(script), 'validate', str(output / bank.NAMES['stereo']), '--profile', 'wrong'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0); self.assertFalse(json.loads(result.stderr)['ok']); self.assertEqual(result.stdout, '')
        duplicated = self.root / 'duplicate.json'; duplicated.write_text('{"version":1,"version":1}')
        with self.assertRaisesRegex(bank.BankError, 'duplicate JSON key'): bank.load_json(duplicated)
        invalid = self.root / 'nonfinite.json'; invalid.write_text('{"bad":NaN}')
        with self.assertRaisesRegex(bank.BankError, 'non-finite'): bank.load_json(invalid)


if __name__ == '__main__':
    unittest.main(verbosity=2)
