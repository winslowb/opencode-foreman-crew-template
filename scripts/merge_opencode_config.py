#!/usr/bin/env python3
import argparse, copy, datetime, json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'opencode.foreman-crew.json'
TARGET = Path.home() / '.config' / 'opencode' / 'opencode.json'
AGENT_SRC = ROOT / 'agent'
AGENT_DST = Path.home() / '.config' / 'opencode' / 'agent'

parser = argparse.ArgumentParser(description='Merge OpenCode Foreman Crew into ~/.config/opencode safely')
parser.add_argument('--apply', action='store_true', help='write merged config and copy agent prompts')
parser.add_argument('--dry-run', action='store_true', help='show what would change')
args = parser.parse_args()
if not args.apply and not args.dry_run:
    args.dry_run = True

tpl = json.loads(TEMPLATE.read_text())
cur = json.loads(TARGET.read_text()) if TARGET.exists() else {'$schema': 'https://opencode.ai/config.json'}
merged = copy.deepcopy(cur)
merged.setdefault('agent', {})
conflicts = sorted(set(merged['agent']).intersection(tpl['agent']))
if conflicts:
    raise SystemExit(f'Agent name conflicts in live config: {conflicts}. Rename first; refusing to overwrite.')
merged['agent'].update(tpl['agent'])
# Keep user's existing provider/mcp/permission settings. Do not copy notes/default_agent unless absent.
merged.setdefault('$schema', tpl.get('$schema', 'https://opencode.ai/config.json'))
merged.setdefault('default_agent', cur.get('default_agent') or tpl.get('default_agent', 'foreman'))

print(f'Target config: {TARGET}')
print(f'Agents to add: {", ".join(tpl["agent"].keys())}')
print(f'Prompt source: {AGENT_SRC}')
print(f'Prompt dest:   {AGENT_DST}')
print(f'Mode: {"APPLY" if args.apply else "DRY RUN"}')

if args.dry_run:
    print('\nNo files changed. Re-run with --apply to install.')
    raise SystemExit(0)

ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup = TARGET.with_suffix(TARGET.suffix + f'.backup.foreman-crew-{ts}')
TARGET.parent.mkdir(parents=True, exist_ok=True)
if TARGET.exists():
    backup.write_text(TARGET.read_text())
    print(f'Backup written: {backup}')
TARGET.write_text(json.dumps(merged, indent=2) + '\n')

# Copy prompts without deleting existing files.
for src in AGENT_SRC.rglob('*.md'):
    rel = src.relative_to(AGENT_SRC)
    dst = AGENT_DST / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise SystemExit(f'Prompt conflict: {dst} exists. Refusing to overwrite.')
    dst.write_text(src.read_text())
    print(f'Copied {dst}')
print('Done.')
