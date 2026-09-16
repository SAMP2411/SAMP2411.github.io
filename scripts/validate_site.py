#!/usr/bin/env python3
"""Validate published/reachable pages and their local dependencies; stdlib only."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.duplicates, self.refs, self.issues = set(), [], [], []
        self.headings = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:
                self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        if tag == 'h1':
            self.headings += 1
        if tag == 'img' and 'alt' not in a:
            self.issues.append('image is missing alt attribute')
        for key in ('href', 'src', 'poster'):
            if a.get(key):
                # Canonicals/social URLs are metadata, not loadable dependencies.
                if tag == 'link' and a.get('rel') == 'canonical':
                    continue
                self.refs.append(a[key])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors, documents, seen_assets = [], {}, set()
    pending = [root / 'index.html']
    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        try:
            for node in ET.parse(sitemap).iter():
                if node.tag.endswith('loc') and node.text:
                    pending.append(root / unquote(urlsplit(node.text).path).lstrip('/'))
        except ET.ParseError as exc:
            errors.append(f'sitemap.xml: {exc}')

    def resolve(source, ref):
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc:
            return None, ''
        raw = unquote(parsed.path)
        target = (root / raw.lstrip('/') if raw.startswith('/') else source.parent / raw) if raw else source
        target = target.resolve()
        if not target.is_relative_to(root):
            errors.append(f'{source.relative_to(root)}: reference escapes site root: {ref}')
            return None, ''
        if target.is_dir():
            target /= 'index.html'
        return target, unquote(parsed.fragment)

    while pending:
        path = pending.pop()
        if path.is_dir():
            path /= 'index.html'
        if path in documents:
            continue
        if not path.is_file():
            errors.append(f'missing page: {path.relative_to(root)}')
            continue
        doc = Document(path.read_text(encoding='utf-8'))
        documents[path] = doc
        errors.extend(f'{path.relative_to(root)}: {issue}' for issue in doc.issues)
        errors.extend(f'{path.relative_to(root)}: duplicate id {ident}' for ident in doc.duplicates)
        if doc.headings != 1:
            errors.append(f'{path.relative_to(root)}: expected one h1, found {doc.headings}')
        for ref in doc.refs:
            target, _ = resolve(path, ref)
            if target and target.suffix.lower() == '.html' and target not in documents:
                pending.append(target)

    def check_asset(path):
        if path in seen_assets or not path.is_file():
            return
        seen_assets.add(path)
        if path.suffix.lower() == '.css':
            for ref in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)', path.read_text(encoding='utf-8')):
                target, _ = resolve(path, ref.strip())
                if target and not target.is_file():
                    errors.append(f'{path.relative_to(root)}: missing CSS asset {ref}')
                elif target:
                    check_asset(target)

    for path, doc in documents.items():
        for ref in doc.refs:
            target, fragment = resolve(path, ref)
            if not target:
                continue
            if not target.is_file():
                errors.append(f'{path.relative_to(root)}: missing target {ref}')
            elif fragment and target in documents and fragment not in documents[target].ids:
                errors.append(f'{path.relative_to(root)}: missing anchor {ref}')
            else:
                check_asset(target)
    result = {'pages': len(documents), 'referenced_assets': len(seen_assets), 'errors': sorted(set(errors))}
    print(json.dumps(result, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
