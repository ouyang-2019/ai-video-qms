#!/usr/bin/env node
'use strict';
const path = require('node:path');
const fs = require('node:fs');
const qms = require('./index');
function main() {
  const [command, ...args] = process.argv.slice(2);
  if (!['doctor', 'index', 'select', 'bundle', 'record'].includes(command)) throw new Error('Usage: qms doctor|index|select|bundle|record [--root PATH] [query flags]');
  /** @type {Record<string, string>} */ const flags = {};
  const allowed = ['root', 'stage', 'model', 'version', 'platform', 'mode', 'style', 'target', 'facets', 'max-chars', 'out'];
  for (let i = 0; i < args.length; i += 2) {
    const name = args[i].slice(2); const value = args[i + 1];
    if (!args[i].startsWith('--') || !allowed.includes(name) || !value || value.startsWith('--') || Object.hasOwn(flags, name)) throw new Error(`Invalid flag: ${args[i]}`);
    flags[name] = value;
  }
  const root = flags.root || process.env.AI_VIDEO_QMS_ROOT || path.resolve(__dirname, '../../standards');
  if (!path.isAbsolute(root) || !fs.existsSync(root)) throw new Error('Root must be an existing absolute path');
  /** @type {Record<string, any>} */ const query = {};
  for (const key of ['stage', 'model', 'version', 'platform', 'mode', 'style', 'target']) if (flags[key]) query[key] = flags[key];
  if (flags.facets) query.facets = flags.facets.split(',').map(facet => facet.trim());
  if (flags['max-chars'] && (!/^\d+$/.test(flags['max-chars']) || Number(flags['max-chars']) < 1)) throw new Error('Invalid --max-chars');
  let result;
  if (command === 'doctor') { result = qms.doctor(root); if (!result.ok) process.exitCode = 1; }
  else if (command === 'index') {
    const report = qms.doctor(root); if (!report.ok) throw new Error(report.errors.join('; '));
    const { registry } = qms.loadRegistry(root);
    process.stdout.write('# AI视频质量体系文件索引\n\n' + registry.documents.map(d => `- L${d.level} [${d.id} ${d.title}](${d.file}) — ${d.status} / ${d.version}`).join('\n') + '\n'); return;
  } else if (command === 'select') result = qms.selectDocuments(root, query);
  else if (command === 'bundle') { process.stdout.write(qms.buildBundle(root, query, flags['max-chars'] ? { maxChars: Number(flags['max-chars']) } : {}).text + '\n'); return; }
  else { if (!flags.out) throw new Error('record requires --out'); result = qms.writeRecord(root, query, flags.out); }
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}
try { main(); } catch (e) { process.stderr.write(`QMS: ${e instanceof Error ? e.message : String(e)}\n`); process.exitCode = 1; }
