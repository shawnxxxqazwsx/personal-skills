#!/usr/bin/env python3
"""Build/validate complete Stereo or 9.1.6-to-9.0.6 IR Banks; stdlib only.

All source WAVs remain read-only. build publishes a fresh directory atomically,
catalog publishes a fresh JSON file, and neither command replaces a destination.
"""
from __future__ import annotations

import argparse
import ctypes
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import sys
import tempfile
import uuid

RATE = 48000
MAX_FRAMES = 1_440_000
MAX_LANES = 128
MAX_BUDGET = 120_000_000
MAX_GROUPS = 8
ROLES = {i + 1: role for i, role in enumerate(
    ['L', 'R', 'C', 'LFE', 'LW', 'RW', 'LS', 'RS', 'LB', 'RB',
     'FTL', 'FTR', 'MTL', 'MTR', 'RTL', 'RTR'])}
OUTPUT_SLOTS = [i for i in range(1, 17) if i != 4]
PROFILES = {'stereo': [1, 2], '916': OUTPUT_SLOTS}
NAMES = {'stereo': '01_立体声输入_9.0.6输出.irmatrix.json',
         '916': '02_9.1.6输入_9.0.6输出.irmatrix.json'}
FLOAT_GUID = bytes.fromhex('0300000000001000800000aa00389b71')


class BankError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise BankError(message)


def integer(value, low, high, label):
    need(type(value) is int and low <= value <= high, f'{label}: expected integer {low}..{high}')
    return value


def text(value, label):
    need(isinstance(value, str) and bool(value.strip()), f'{label}: expected nonempty string')
    return value


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def file_identity(status):
    return (status.st_dev, status.st_ino, status.st_size, status.st_mtime_ns, status.st_ctime_ns)


def load_json_snapshot(path, limit=16 * 1024 * 1024):
    need(path.is_file() and path.stat().st_size <= limit, f'invalid/oversize JSON file: {path}')
    with path.open('rb') as stream:
        before = file_identity(os.fstat(stream.fileno()))
        raw = stream.read(limit + 1)
        need(len(raw) <= limit and file_identity(os.fstat(stream.fileno())) == before,
             f'JSON changed/grew during read: {path}')
    need(file_identity(path.stat()) == before, f'JSON path changed during read: {path}')
    def invalid_constant(value):
        raise BankError(f'non-finite JSON number: {value}')
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=object_pairs, parse_constant=invalid_constant)
    return value, hashlib.sha256(raw).hexdigest()


def load_json(path, limit=16 * 1024 * 1024):
    return load_json_snapshot(path, limit)[0]


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def confined(path, root):
    need(path == root or root in path.parents, f'canonical path escapes package root: {path}')


@dataclass(frozen=True)
class WavInfo:
    frames: int
    data_offset: int
    data_bytes: int
    sha256: str
    peak: float
    l1: float
    identity: tuple


def inspect_wav(path):
    """Strict RIFF/WAVE float32 mono reader; streams PCM without dependencies."""
    need(path.is_file() and path.suffix.lower() == '.wav', f'WAV missing/wrong extension: {path}')
    length = path.stat().st_size
    with path.open('rb') as stream:
        before = file_identity(os.fstat(stream.fileno()))
        need(before[2] == length, f'WAV changed during open: {path}')
        head = stream.read(12)
        need(len(head) == 12 and head[:4] == b'RIFF' and head[8:] == b'WAVE',
             f'expected little-endian RIFF/WAVE: {path}')
        end = struct.unpack('<I', head[4:8])[0] + 8
        need(end == length, f'RIFF size/trailing bytes mismatch: {path}')
        fmt = data = None
        position = 12
        while position < end:
            need(position + 8 <= end, f'truncated WAV chunk: {path}')
            stream.seek(position)
            kind, size = struct.unpack('<4sI', stream.read(8))
            start = position + 8
            need(start + size + (size & 1) <= end, f'WAV chunk exceeds RIFF: {path}')
            if kind == b'fmt ':
                need(fmt is None and 16 <= size <= 65536, f'duplicate/invalid fmt chunk: {path}')
                fmt = stream.read(size)
            elif kind == b'data':
                need(fmt is not None, f'WAV data must follow fmt for native JUCE compatibility: {path}')
                need(data is None, f'duplicate WAV data chunk: {path}')
                data = (start, size)
            position = start + size + (size & 1)
        need(fmt is not None and data is not None, f'missing WAV fmt/data: {path}')
        tag, channels, rate, byte_rate, align, bits = struct.unpack('<HHIIHH', fmt[:16])
        need(channels == 1 and rate == RATE and byte_rate == RATE * 4 and align == 4 and bits == 32,
             f'WAV must be mono 48000 Hz float32: {path}')
        if tag == 0xFFFE:
            need(len(fmt) >= 40, f'truncated extensible WAV: {path}')
            cb, valid, mask = struct.unpack('<HHI', fmt[16:24])
            need(cb >= 22 and 18 + cb <= len(fmt) and valid == 32 and fmt[24:40] == FLOAT_GUID
                 and (mask == 0 or mask.bit_count() == 1), f'not extensible IEEE float32 mono: {path}')
        else:
            need(tag == 3, f'WAV is not IEEE float32: {path}')
            if len(fmt) != 16:
                need(len(fmt) >= 18 and 18 + struct.unpack('<H', fmt[16:18])[0] <= len(fmt),
                     f'invalid IEEE float fmt extension: {path}')
        start, size = data
        need(size % 4 == 0, f'WAV PCM byte count is not aligned: {path}')
        frames = integer(size // 4, 1, MAX_FRAMES, 'WAV frames')
        stream.seek(start)
        peak = l1 = 0.0
        remaining = size
        while remaining:
            chunk = stream.read(min(32768, remaining))
            need(chunk and len(chunk) % 4 == 0, f'truncated WAV PCM: {path}')
            remaining -= len(chunk)
            for (sample,) in struct.iter_unpack('<f', chunk):
                need(math.isfinite(sample), f'WAV contains NaN/Inf: {path}')
                magnitude = abs(sample)
                peak = max(peak, magnitude)
                l1 += magnitude
                need(peak <= 1e6 and l1 <= 1e9, f'WAV exceeds peak/L1 arithmetic budget: {path}')
        stream.seek(0)
        checksum = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(chunk)
        need(file_identity(os.fstat(stream.fileno())) == before, f'WAV changed during inspection: {path}')
    need(file_identity(path.stat()) == before, f'WAV path changed during inspection: {path}')
    return WavInfo(frames, start, size, checksum.hexdigest(), peak, l1, before)


def rows(value, slots, identity, label, default_role=False, unique_ids=False):
    need(isinstance(value, list) and len(value) == len(slots), f'{label}: wrong row count')
    result = []
    seen = set()
    identities = set()
    for row in value:
        need(isinstance(row, dict), f'{label}: expected object row')
        slot = integer(row.get('slot'), 1, 16, f'{label}.slot')
        need(slot in slots and slot not in seen, f'{label}: duplicate/inactive/LFE slot {slot}')
        name = text(row.get(identity), f'{label}.{identity}')
        need(not unique_ids or name not in identities, f'{label}: recipe requires unique {identity}')
        role = text(row.get('role', ROLES[slot] if default_role else None), f'{label}.role')
        result.append(dict(row, slot=slot, **{identity: name, 'role': role}))
        seen.add(slot)
        identities.add(name)
    need(seen == set(slots), f'{label}: incomplete active slots')
    return result


def source_order(inputs):
    return list(dict.fromkeys(row['physical_source_id'] for row in inputs))


def pack_lanes(lanes):
    """Greedy source/output ordered groups, preserving frame boundaries."""
    groups, current = [], []
    budget = 0
    for lane in lanes:
        frames = integer(lane.get('frames'), 1, MAX_FRAMES, 'lane.frames')
        cost = 4 * frames
        need(cost <= MAX_BUDGET, 'one lane exceeds group sample budget')
        if current and (len(current) == MAX_LANES or budget + cost > MAX_BUDGET
                        or frames != current[0]['frames']):
            groups.append({'id': len(groups) + 1, 'lanes': current})
            current, budget = [], 0
        current.append(dict(lane, lane=len(current) + 1))
        budget += cost
    if current:
        groups.append({'id': len(groups) + 1, 'lanes': current})
    need(1 <= len(groups) <= MAX_GROUPS, 'complete Bank requires more than 8 internal groups (or has no lanes)')
    return groups


def validate_bank(path, profile=None, wav_cache=None):
    path = Path(path).resolve(strict=True)
    value, manifest_sha = load_json_snapshot(path)
    need(isinstance(value, dict), 'manifest must be an object')
    need(value.get('format') == 'clara://ir-router-matrix/v1', 'unsupported manifest format')
    integer(value.get('version'), 1, 1, 'version')
    for key in ('input_bus_channels', 'output_bus_channels'):
        integer(value.get(key), 16, 16, key)
    integer(value.get('max_sample_rate'), 192000, 192000, 'max_sample_rate')
    text(value.get('entry_uuid'), 'entry_uuid')
    text(value.get('label'), 'label')
    root_text = text(value.get('package_root'), 'package_root')
    need(not Path(root_text).is_absolute(), 'package_root must be relative')
    root = (path.parent / root_text).resolve(strict=True)
    need(root.is_dir(), 'package_root must be a directory')
    confined(path, root)
    raw_inputs = value.get('inputs')
    need(isinstance(raw_inputs, list), 'inputs must be an array')
    actual_slots = [r.get('slot') if isinstance(r, dict) else None for r in raw_inputs]
    for slot in actual_slots:
        integer(slot, 1, 16, 'input slot')
    inferred = next((name for name, slots in PROFILES.items() if set(actual_slots) == set(slots)
                     and len(actual_slots) == len(slots)), None)
    need(inferred is not None and (profile is None or inferred == profile), 'Bank input slots do not match requested stereo/916 profile')
    inputs = rows(raw_inputs, PROFILES[inferred], 'physical_source_id', 'inputs')
    outputs = rows(value.get('outputs'), OUTPUT_SLOTS, 'receiver_id', 'outputs')
    for key, occupied in (('silent_input_slots', PROFILES[inferred]), ('silent_output_slots', OUTPUT_SLOTS)):
        silent = value.get(key)
        need(isinstance(silent, list), f'{key} must be an array')
        for slot in silent:
            integer(slot, 1, 16, key)
        need(len(silent) == len(set(silent)) and set(silent) == set(range(1, 17)) - set(occupied),
             f'{key}: incomplete/duplicate active-silent coverage')
    source_slots = {}
    for row in inputs:
        source_slots.setdefault(row['physical_source_id'], set()).add(row['slot'])
    receivers = {row['slot']: row['receiver_id'] for row in outputs}
    order = {source: i for i, source in enumerate(source_order(inputs))}
    banks = value.get('banks')
    need(isinstance(banks, list) and 1 <= len(banks) <= MAX_GROUPS, 'Bank requires 1..8 internal groups')
    cells, physical, previous = set(), set(), (-1, -1)
    cache = {} if wav_cache is None else wav_cache
    group_receipts = []
    used_wavs = set()
    for bi, bank in enumerate(banks, 1):
        need(isinstance(bank, dict), 'group must be an object')
        integer(bank.get('id'), bi, bi, 'group.id')
        lanes = bank.get('lanes')
        need(isinstance(lanes, list) and 1 <= len(lanes) <= MAX_LANES, 'group requires 1..128 lanes')
        common_frames, budget = None, 0
        for li, lane in enumerate(lanes, 1):
            need(isinstance(lane, dict), 'lane must be an object')
            integer(lane.get('lane'), li, li, 'lane.lane')
            output = integer(lane.get('output_slot'), 1, 16, 'lane.output_slot')
            source = text(lane.get('physical_source_id'), 'lane.physical_source_id')
            need(source in order and output in receivers and lane.get('receiver_id') == receivers[output], 'lane source/receiver identity mismatch')
            position = (order[source], output)
            need(position > previous and (source, output) not in physical, 'lane order/physical transfer duplicated; require source-major/output-slot ascending')
            previous = position
            physical.add((source, output))
            slots = lane.get('input_slots')
            need(isinstance(slots, list) and slots, 'lane requires explicit input_slots')
            for slot in slots:
                integer(slot, 1, 16, 'lane.input_slots')
            need(len(slots) == len(set(slots)) and set(slots) == source_slots[source], 'incomplete/duplicate/reinterpreted physical source folding')
            for slot in slots:
                need((slot, output) not in cells, 'duplicate logical cell')
                cells.add((slot, output))
            integer(lane.get('sample_rate'), RATE, RATE, 'lane.sample_rate')
            frames = integer(lane.get('frames'), 1, MAX_FRAMES, 'lane.frames')
            need(common_frames is None or common_frames == frames, 'one group requires common WAV frames')
            common_frames = frames
            budget += 4 * frames
            need(budget <= MAX_BUDGET, 'group exceeds 120000000 preparation samples')
            sha = lane.get('sha256')
            need(isinstance(sha, str) and re.fullmatch('[0-9a-f]{64}', sha), 'invalid lowercase full-file SHA256')
            relative = text(lane.get('mono_wav'), 'lane.mono_wav')
            need(not Path(relative).is_absolute(), 'mono_wav must be relative')
            wav = (path.parent / relative).resolve(strict=True)
            confined(wav, root)
            used_wavs.add(wav)
            if wav not in cache or cache[wav].identity != file_identity(wav.stat()):
                cache[wav] = inspect_wav(wav)
            info = cache[wav]
            need(info.sha256 == sha and info.frames == frames, f'WAV SHA256/frame binding mismatch: {wav}')
        group_receipts.append({'id': bi, 'physical_lanes': len(lanes), 'frames': common_frames,
                               'preparation_samples_192k': budget})
    expected = {(i, o) for i in PROFILES[inferred] for o in OUTPUT_SLOTS}
    need(cells == expected, 'complete Bank omits logical input/output cells')
    need(len(physical) == len(source_slots) * 15, 'physical transfer coverage mismatch')
    need(digest(path) == manifest_sha, 'manifest changed during validation')
    for wav in used_wavs:
        need(file_identity(wav.stat()) == cache[wav].identity, f'WAV changed during Bank validation: {wav}')
    return {'ok': True, 'manifest': str(path), 'sha256': manifest_sha, 'profile': inferred,
            'label': value['label'], 'room': value.get('room'), 'active_inputs': len(inputs),
            'logical_cells': len(cells), 'physical_lanes': len(physical),
            'unique_physical_sources': len(source_slots), 'groups': group_receipts}


def copy_asset(source, info, target, frames):
    if frames == info.frames:
        shutil.copyfile(source, target)
        need(digest(target) == info.sha256, f'source WAV changed while copying: {source}')
        return
    # Explicit padding: preserve every original float sample, append zeros only;
    # emit a canonical fresh IEEE float WAV, with no normalization or time shift.
    with source.open('rb') as stream, target.open('xb') as out:
        payload = frames * 4
        out.write(struct.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 36 + payload, b'WAVE', b'fmt ', 16,
                              3, 1, RATE, RATE * 4, 4, 32, b'data', payload))
        stream.seek(info.data_offset)
        remaining = info.data_bytes
        while remaining:
            chunk = stream.read(min(1024 * 1024, remaining))
            need(chunk, f'source WAV changed while padding: {source}')
            out.write(chunk)
            remaining -= len(chunk)
        remaining = (frames - info.frames) * 4
        zeros = bytes(32768)
        while remaining:
            n = min(remaining, len(zeros)); out.write(zeros[:n]); remaining -= n
    need(digest(source) == info.sha256, f'source WAV changed while padding: {source}')


def publish_directory(stage, output):
    """Atomic no-replace rename, including a concurrently created empty target."""
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == 'darwin':
        function = getattr(libc, 'renamex_np', None)
        need(function is not None, 'atomic no-replace rename unavailable')
        function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        result = function(os.fsencode(stage), os.fsencode(output), 0x4)  # SDK RENAME_EXCL
    elif sys.platform.startswith('linux'):
        function = getattr(libc, 'renameat2', None)
        need(function is not None, 'atomic no-replace rename unavailable')
        function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        result = function(-100, os.fsencode(stage), -100, os.fsencode(output), 1)  # RENAME_NOREPLACE
    elif os.name == 'nt':
        os.rename(stage, output)  # Windows rename fails if destination exists.
        return
    else:
        raise BankError('atomic no-replace directory publication unsupported on this platform')
    if result:
        raise OSError(ctypes.get_errno(), 'atomic no-replace Bank publication failed', str(output))


def build_recipe(recipe_path, output):
    recipe_path = Path(recipe_path).resolve(strict=True)
    output = Path(output)
    need(output.is_absolute(), '--output must be a new absolute directory')
    need(not os.path.lexists(output), f'output already exists: {output}')
    need(output.parent.is_dir(), 'output parent directory must exist')
    value = load_json(recipe_path)
    need(isinstance(value, dict) and value.get('schema') == 'chlora-ir-bank-recipe/v1', 'unsupported recipe schema')
    label = text(value.get('label'), 'recipe.label')
    metadata = value.get('metadata', {})
    need(isinstance(metadata, dict), 'recipe.metadata must be an object')
    metadata = dict(metadata, base_label=label)
    room = value.get('room')
    if room is not None:
        text(room, 'recipe.room')
    profiles = value.get('profiles')
    need(isinstance(profiles, dict) and profiles and set(profiles) <= set(PROFILES), 'profiles must contain stereo and/or 916')
    inputs = {name: sorted(rows(profiles[name], PROFILES[name], 'physical_source_id', f'profiles.{name}', default_role=True), key=lambda r: r['slot'])
              for name in PROFILES if name in profiles}
    outputs = sorted(rows(value.get('outputs'), OUTPUT_SLOTS, 'receiver_id', 'outputs', unique_ids=True), key=lambda r: r['slot'])
    sources = set(row['physical_source_id'] for rows_ in inputs.values() for row in rows_)
    expected = {(source, row['receiver_id']) for source in sources for row in outputs}
    transfers = value.get('transfers')
    need(isinstance(transfers, list), 'transfers must be an array')
    bindings = {}
    for transfer in transfers:
        need(isinstance(transfer, dict), 'transfer must be an object')
        pair = (text(transfer.get('physical_source_id'), 'transfer.physical_source_id'), text(transfer.get('receiver_id'), 'transfer.receiver_id'))
        need(pair not in bindings, f'duplicate transfer: {pair}')
        file = Path(text(transfer.get('file'), 'transfer.file'))
        bindings[pair] = file.resolve(strict=True) if file.is_absolute() else (recipe_path.parent / file).resolve(strict=True)
    need(set(bindings) == expected, f'missing/extra physical transfers: missing={sorted(expected - set(bindings))}, extra={sorted(set(bindings) - expected)}')
    padding = value.get('pad_to_common_frames', False)
    need(type(padding) is bool, 'pad_to_common_frames must be boolean')
    info_by_file = {path: inspect_wav(path) for path in set(bindings.values())}
    lengths = {info.frames for info in info_by_file.values()}
    need(len(lengths) == 1 or padding, 'WAV frame counts differ; explicitly set pad_to_common_frames:true for trailing-zero-only copies')
    common = max(lengths)
    # Admission before any output: no partially built bundle for oversized groups.
    for name, profile_inputs in inputs.items():
        pack_lanes([{'frames': common} for _ in range(15 * len(source_order(profile_inputs)))])
    stage = Path(tempfile.mkdtemp(prefix='.' + output.name + '.ir-bank-', dir=output.parent))
    try:
        assets = stage / 'assets'; assets.mkdir()
        asset_for_pair = {}
        by_input_hash = {}
        for pair, source in bindings.items():
            info = info_by_file[source]
            if info.sha256 not in by_input_hash:
                temporary = assets / ('copy-' + uuid.uuid4().hex + '.wav')
                copy_asset(source, info, temporary, common)
                final_hash = digest(temporary)
                target = assets / (final_hash + '.wav')
                if target.exists():
                    temporary.unlink()
                else:
                    temporary.rename(target)
                by_input_hash[info.sha256] = target.relative_to(stage).as_posix()
            asset_for_pair[pair] = by_input_hash[info.sha256]
        for name, profile_inputs in inputs.items():
            lanes = []
            for source in source_order(profile_inputs):
                slots = [row['slot'] for row in profile_inputs if row['physical_source_id'] == source]
                for receiver in outputs:
                    asset = asset_for_pair[(source, receiver['receiver_id'])]
                    lanes.append({'input_slots': slots, 'output_slot': receiver['slot'], 'physical_source_id': source,
                                  'receiver_id': receiver['receiver_id'], 'mono_wav': asset,
                                  'sha256': Path(asset).stem, 'sample_rate': RATE, 'frames': common})
            manifest = {'format': 'clara://ir-router-matrix/v1', 'version': 1,
                        'entry_uuid': str(uuid.uuid4()), 'label': label + (' · 立体声 → 9.0.6' if name == 'stereo' else ' · 9.1.6 → 9.0.6'), 'package_root': '.',
                        'input_bus_channels': 16, 'output_bus_channels': 16, 'max_sample_rate': 192000,
                        'inputs': profile_inputs, 'outputs': outputs,
                        'silent_input_slots': [i for i in range(1, 17) if i not in PROFILES[name]],
                        'silent_output_slots': [4], 'banks': pack_lanes(lanes)}
            if room is not None:
                manifest['room'] = room
            manifest['metadata'] = metadata
            (stage / NAMES[name]).write_bytes(json_bytes(manifest))
        cache = {}
        receipts = [validate_bank(stage / NAMES[name], name, cache) for name in inputs]
        # Recheck original bindings, including originals deduplicated by bytes.
        for source, info in info_by_file.items():
            need(digest(source) == info.sha256, f'source asset changed during build: {source}')
        publish_directory(stage, output)
        for receipt in receipts:
            receipt['manifest'] = str(output / Path(receipt['manifest']).name)
        return {'ok': True, 'command': 'build', 'output': str(output), 'source_files_unchanged': True,
                'padded_to_frames': common if len(lengths) > 1 else None,
                'unique_asset_files': len(list((output / 'assets').glob('*.wav'))), 'banks': receipts}
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def catalog(root, output=None):
    root = Path(root).resolve(strict=True)
    need(root.is_dir(), 'catalog root must be a directory')
    output = Path(output) if output is not None else root / 'bank-catalog.json'
    need(output.parent.is_dir() and not os.path.lexists(output), 'catalog destination must be new and its parent must exist')
    records, cache = [], {}
    for candidate in sorted(root.rglob('*.irmatrix.json')):
        path = candidate.resolve(strict=True); confined(path, root)
        receipt = validate_bank(path, wav_cache=cache)
        room = receipt['room']
        if not isinstance(room, str) or not room.strip():
            relative_parent = candidate.parent.relative_to(root)
            room = relative_parent.parts[0] if relative_parent.parts else root.name
        records.append({'room': room, 'label': receipt['label'], 'path': candidate.relative_to(root).as_posix(),
                        'sha256': receipt['sha256'], 'active_inputs': receipt['active_inputs']})
        need(len(records) <= 4096, 'catalog exceeds 4096 entries')
    need(records, 'catalog root contains no Bank manifests')
    payload = json_bytes({'schema': 'clara://ir-bank-catalog/v1', 'banks': records})
    need(len(payload) <= 1024 * 1024, 'catalog exceeds 1 MiB native parser limit')
    fd, temporary = tempfile.mkstemp(prefix='.' + output.name + '.', dir=output.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload); stream.flush(); os.fsync(stream.fileno())
        os.link(temporary, output)  # Atomic creation; an existing destination is never replaced.
    finally:
        os.unlink(temporary)
    return {'ok': True, 'command': 'catalog', 'output': str(output), 'entries': len(records), 'sha256': digest(output)}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise BankError(message)


def main(argv=None):
    parser = Parser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    build = commands.add_parser('build', help='create new Bank bundle from a recipe (never replace)')
    build.add_argument('recipe', type=Path); build.add_argument('--output', required=True, type=Path)
    validate = commands.add_parser('validate', help='fully validate one complete Bank and all referenced WAVs')
    validate.add_argument('bank', type=Path); validate.add_argument('--profile', choices=list(PROFILES))
    cat = commands.add_parser('catalog', help='create new native catalog; default ROOT/bank-catalog.json')
    cat.add_argument('root', type=Path); cat.add_argument('--output', type=Path)
    try:
        args = parser.parse_args(argv)
        if args.command == 'build':
            result = build_recipe(args.recipe, args.output)
        elif args.command == 'validate':
            result = validate_bank(args.bank, args.profile)
        else:
            result = catalog(args.root, args.output)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except (BankError, OSError, ValueError, TypeError, KeyError, struct.error) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
