#!/usr/bin/env python3
"""Open one local authenticated evidence capsule. Python 3 + cryptography.

Usage: python open_capsule.py capsules/A.json --key <64 lowercase hex>
The desk returns the key for each sealed packet when your answer checks out.
Files are authenticated before extraction; existing files are never replaced.
"""
import argparse
import base64
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

FORMAT = 'XTRACT-V8'
ALGORITHM = 'AES-256-GCM'


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('Duplicate JSON object key')
        result[key] = value
    return result


def read_json(blob):
    def unsupported(value):
        raise ValueError('JSON floating-point values are unsupported; use exact contract strings')
    return json.loads(blob, object_pairs_hook=_pairs, parse_float=unsupported, parse_constant=unsupported)


def canonical_json(value):
    def check(obj):
        if obj is None or type(obj) in (str, int, bool):
            return
        if isinstance(obj, list):
            for child in obj: check(child)
            return
        if isinstance(obj, dict) and all(type(k) is str for k in obj):
            for child in obj.values(): check(child)
            return
        raise ValueError('Unsupported canonical JSON value')
    check(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def associated_data(capsule_id):
    if not isinstance(capsule_id, str) or not re.fullmatch('[A-Z][A-Z0-9_-]*', capsule_id):
        raise ValueError('Invalid capsule identifier')
    return canonical_json({'format': FORMAT, 'id': capsule_id, 'algorithm': ALGORITHM})


def parse_key(text):
    key = text.strip()
    if not re.fullmatch(r'[0-9a-f]{64}', key):
        raise ValueError('A capsule key is 64 lowercase hexadecimal characters')
    return bytes.fromhex(key)


def decrypt_capsule(blob, key):
    envelope = read_json(blob)
    if not isinstance(envelope, dict) or set(envelope) != {'format', 'id', 'algorithm', 'nonce', 'ciphertext'}:
        raise ValueError('Invalid capsule envelope')
    if envelope['format'] != FORMAT or envelope['algorithm'] != ALGORITHM:
        raise ValueError('Unsupported capsule format')
    if isinstance(key, str):
        key = parse_key(key)
    nonce = base64.b64decode(envelope['nonce'], validate=True)
    ciphertext = base64.b64decode(envelope['ciphertext'], validate=True)
    if len(nonce) != 12:
        raise ValueError('AES-GCM requires the specified 12-byte nonce')
    try:
        plain = AESGCM(key).decrypt(nonce, ciphertext, associated_data(envelope['id']))
    except InvalidTag as error:
        raise ValueError('Capsule authentication failed') from error
    return envelope['id'], plain


def _destination(root, name):
    current = root
    for component in PurePosixPath(name).parts:
        if current.exists():
            if not current.is_dir(): raise ValueError('Extraction parent is not a directory')
            if any(p.name.casefold() == component.casefold() and p.name != component for p in current.iterdir()):
                raise ValueError('Destination name aliases an existing path')
        current = current / component
        if current.is_symlink(): raise ValueError('Symlink destinations are unsupported')
    if not current.resolve().is_relative_to(root.resolve()):
        raise ValueError('Extraction path leaves the output directory')
    if current.exists(): raise ValueError('Refusing to replace an existing file: ' + name)
    return current


def extract_payload(plain, output):
    root = Path(output).absolute()
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise ValueError('Output must be a directory without a symlink at its root')
    files, names = {}, set()
    with zipfile.ZipFile(io.BytesIO(plain)) as archive:
        for member in archive.infolist():
            name = member.filename
            components = name.split('/')
            if not name or any(not re.fullmatch('[A-Za-z0-9_.-]+', part) or part in ('.', '..') for part in components):
                raise ValueError('Unsafe or unsupported ZIP member path')
            if member.is_dir() or stat.S_IFMT(member.external_attr >> 16) not in (0, stat.S_IFREG):
                raise ValueError('Only ordinary ZIP files are supported')
            folded = name.casefold()
            if folded in names: raise ValueError('Duplicate or aliased ZIP member')
            names.add(folded)
            files[name] = archive.read(member)
    if not files: raise ValueError('Capsule ZIP is empty')
    for name in files:
        if any('/'.join(name.split('/')[:i]).casefold() in names for i in range(1, len(name.split('/')))):
            raise ValueError('ZIP file/directory conflict')
    destinations = {name: _destination(root, name) for name in files}
    root.mkdir(parents=True, exist_ok=True)
    for name, blob in files.items():
        path = destinations[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream: stream.write(blob)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capsule', type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--key', help='64 lowercase hexadecimal characters issued by the desk')
    group.add_argument('--key-file', type=Path, help='Text file containing the issued key')
    parser.add_argument('--output', type=Path, default=Path('.'))
    args = parser.parse_args()
    try:
        key = parse_key(args.key) if args.key is not None else parse_key(args.key_file.read_text())
        capsule_id, plain = decrypt_capsule(args.capsule.read_bytes(), key)
        files = extract_payload(plain, args.output)
    except (ValueError, TypeError, KeyError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, 'Cannot open capsule: ' + str(error) + '\n')
    print(json.dumps({'opened': capsule_id, 'files_written': files}, indent=2))


if __name__ == '__main__':
    main()
