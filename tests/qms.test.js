'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');
const qms = require('../tools/qms');
/** @param {Record<string, any>} overrides */
function doc(overrides) { return { id: 'SOP-COMMON', title: 'Common', level: 3, kind: 'sop', version: '1.0.0', file: 'documents/common.md', stages: ['script'], models: ['common'], model_versions: ['*'], platforms: ['*'], modes: ['*'], styles: [], status: 'released', verification: 'structural', source_ids: ['S'], requires: [], privacy: 'ai_allowed', ...overrides }; }
/** @param {import('node:test').TestContext} t @param {Record<string, any>[]} [documents] */
function fixture(t, documents = [doc({})]) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'qms-test-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const registry = { schema_version: 1, documents, profiles: ['h3', 'seedance'].map(model => ({ model, version: '1', platform: 'official', modes: ['text'], status: 'released', source_ids: ['S'] })) };
  const sources = { schema_version: 1, sources: [{ source_id: 'S', source_kind: 'internal', captured_at: '2026-09-08', license_status: 'internal', verification: 'structural', revision: 'rev1' }] };
  const save = () => { fs.writeFileSync(path.join(root, 'registry.json'), JSON.stringify(registry)); fs.writeFileSync(path.join(root, 'sources.json'), JSON.stringify(sources)); };
  for (const d of documents) { fs.mkdirSync(path.dirname(path.join(root, d.file)), { recursive: true }); fs.writeFileSync(path.join(root, d.file), `# ${d.id}\nMeaningful controlled procedure.\n`); }
  save(); return { root, registry, sources, save };
}
const video = { stage: 'video', model: 'h3', version: '1', platform: 'official', mode: 'text' };

test('image profiles cannot be routed as video and video cannot be routed as image assets', t => {
  const f = fixture(t,[doc({stages:['assets','video'],models:['gpt-image']})]);
  f.registry.profiles.push({model:'gpt-image',version:'2',platform:'images-api',modes:['T2I'],artifact:'image',status:'released',source_ids:['S']}); f.save();
  const query={stage:'assets',model:'gpt-image',version:'2',platform:'images-api',mode:'T2I'};
  assert.equal(qms.selectDocuments(f.root,query).documents.length,1);
  assert.throws(()=>qms.selectDocuments(f.root,{...query,stage:'video'}),/artifact/);
  assert.throws(()=>qms.selectDocuments(f.root,{...video,stage:'assets'}),/artifact/);
  f.registry.profiles[2].artifact='unknown';f.save();assert.equal(qms.doctor(f.root).ok,false);
});

test('supplementary relation and method snapshots are hash sealed', t => {
  const f=fixture(t);fs.writeFileSync(path.join(f.root,'relations.json'),'[]');
  const digest=crypto.createHash('sha256').update('[]').digest('hex');
  fs.writeFileSync(path.join(f.root,'supplement-content.json'),JSON.stringify({files:[{file:'relations.json',sha256:digest}]}));
  assert(qms.doctor(f.root).ok);
  fs.writeFileSync(path.join(f.root,'relations.json'),'[{}]');
  assert(!qms.doctor(f.root).ok);
});
test('new registered model families work without code changes', t => {
  const f = fixture(t, [doc({ models: ['future-video'], stages: ['video'] })]);
  f.registry.profiles.push({ model: 'future-video', version: 'v1', platform: 'lab', modes: ['T2V'], status: 'released', source_ids: ['S'] }); f.save();
  assert.equal(qms.selectDocuments(f.root, { stage: 'video', model: 'future-video', version: 'v1', platform: 'lab', mode: 'T2V' }).documents.length, 1);
});
test('source privacy cannot be downgraded by a document', t => {
  const f = fixture(t);
  f.sources.sources[0].privacy = 'local'; f.save();
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'script' }), /SOP/);
  assert.equal(qms.selectDocuments(f.root, { stage: 'script', target: 'local' }).documents.length, 1);
  f.sources.sources[0].privacy = 'no_ai'; f.save();
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'script', target: 'local' }), /SOP/);
});
test('production release requires its manifest and seals routing metadata', t => {
  const f = fixture(t); f.registry.release_required = true; f.save();
  assert.equal(qms.doctor(f.root).ok, false);
  const digest = name => crypto.createHash('sha256').update(fs.readFileSync(path.join(f.root, name))).digest('hex');
  const d = f.registry.documents[0];
  fs.writeFileSync(path.join(f.root, 'release-content.json'), JSON.stringify({ schema_version: 1, registry_sha256: digest('registry.json'), sources_sha256: digest('sources.json'), documents: [{ id: d.id, file: d.file, version: d.version, sha256: digest(d.file) }] }));
  assert.equal(qms.doctor(f.root).ok, true);
  f.registry.documents[0].styles = ['altered']; f.save();
  assert.equal(qms.doctor(f.root).ok, false);
});
test('common selection and exact model isolation', t => {
  const f = fixture(t, [doc({}), ...['h3', 'seedance'].map(model => doc({ id: `SOP-${model}`, file: `documents/${model}.md`, stages: ['video'], models: [model] }))]);
  assert.equal(qms.doctor(f.root).ok, true);
  assert.deepEqual(qms.selectDocuments(f.root, { stage: 'script' }).documents.map(d => d.id), ['SOP-COMMON']);
  assert.deepEqual(qms.selectDocuments(f.root, video).documents.map(d => d.id), ['SOP-h3']);
  for (const query of [{ ...video, version: '2' }, { ...video, platform: 'unknown' }, { ...video, mode: undefined }, { stage: 'script', model: 'h3' }]) assert.throws(() => qms.selectDocuments(f.root, query));
});
test('styles, status and examples are scoped', t => {
  const f = fixture(t, [doc({}), doc({ id: 'STYLE', file: 'documents/style.md', styles: ['comedy'] }), ...['draft', 'obsolete'].map(status => doc({ id: status, file: `documents/${status}.md`, status })), ...['example', 'record'].map(kind => doc({ id: kind, file: `documents/${kind}.md`, kind, level: 4 }))]);
  assert.equal(qms.selectDocuments(f.root, { stage: 'script' }).documents.length, 1);
  assert.equal(qms.selectDocuments(f.root, { stage: 'script', style: 'comedy' }).documents.length, 2);
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'script', style: 'unknown' }), /style/);
});
test('dependency closure rejects missing, cycles, status and privacy', t => {
  const f = fixture(t, [doc({ requires: ['BASE'] }), doc({ id: 'BASE', file: 'documents/base.md', kind: 'manual', level: 1, stages: ['governance'] })]);
  assert.equal(qms.selectDocuments(f.root, { stage: 'script' }).documents.length, 2);
  f.registry.documents[1].privacy = 'local'; f.save();
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'script' }), /Incompatible/);
  assert.equal(qms.selectDocuments(f.root, { stage: 'script', target: 'local' }).documents.length, 2);
  f.registry.documents[1].privacy = 'no_ai'; f.save(); assert.throws(() => qms.selectDocuments(f.root, { stage: 'script', target: 'local' }), /Incompatible/);
  f.registry.documents[1].privacy = 'ai_allowed'; f.registry.documents[1].requires = ['SOP-COMMON']; f.save(); assert.equal(qms.doctor(f.root).ok, false);
  f.registry.documents[1].requires = []; f.registry.documents[1].status = 'draft'; f.save(); assert.equal(qms.doctor(f.root).ok, false);
  f.registry.documents.pop(); f.save(); assert.equal(qms.doctor(f.root).ok, false);
});
test('path traversal and source references fail validation', t => {
  const f = fixture(t); f.registry.documents[0].file = '../escape.md'; f.save(); assert.equal(qms.doctor(f.root).ok, false);
  f.registry.documents[0].file = 'documents/common.md'; f.registry.documents[0].source_ids = ['missing']; f.save(); assert.equal(qms.doctor(f.root).ok, false);
});
test('symlink escape is rejected', t => {
  const f = fixture(t); const outside = fs.mkdtempSync(path.join(os.tmpdir(), 'qms-outside-')); t.after(() => fs.rmSync(outside, { recursive: true, force: true }));
  fs.writeFileSync(path.join(outside, 'external.md'), '# external');
  try { fs.symlinkSync(outside, path.join(f.root, 'linked'), 'junction'); } catch (e) { t.skip(`Symlink unavailable: ${e.message}`); return; }
  f.registry.documents[0].file = 'linked/external.md'; f.save(); assert.equal(qms.doctor(f.root).ok, false);
});
test('bundle is deterministic, includes complete content and respects total budget', t => {
  const f = fixture(t); const a = qms.buildBundle(f.root, { stage: 'script' });
  assert.equal(a.sha256, qms.buildBundle(f.root, { stage: 'script' }).sha256);
  assert.ok(a.text.includes('Meaningful controlled procedure.'));
  assert.throws(() => qms.buildBundle(f.root, { stage: 'script' }, { maxChars: a.text.length - 1 }), /budget/);
  assert.equal(qms.buildBundle(f.root, { stage: 'script' }, { maxChars: a.text.length }).text, a.text);
});
test('record is immutable, snapshots source revision and rejects documents output', t => {
  const f = fixture(t); const out = path.join(f.root, 'record');
  const record = qms.writeRecord(f.root, { stage: 'script' }, out);
  assert.equal(record.generation_executed, false); assert.equal(record.sources[0].revision, 'rev1');
  assert.equal(fs.existsSync(path.join(out, 'bundle.md')), true);
  assert.throws(() => qms.writeRecord(f.root, { stage: 'script' }, out), /exists/);
  assert.throws(() => qms.writeRecord(f.root, { stage: 'script' }, path.join(f.root, 'documents', 'record')), /inside documents/);
});
test('release manifest checks content, duplicate, missing and unknown ids', t => {
  const f = fixture(t); const d = f.registry.documents[0];
  const row = { id: d.id, version: d.version, file: d.file, sha256: crypto.createHash('sha256').update(fs.readFileSync(path.join(f.root, d.file))).digest('hex') };
  const release = rows => fs.writeFileSync(path.join(f.root, 'release-content.json'), JSON.stringify({ schema_version: 1, documents: rows }));
  release([row]); assert.equal(qms.doctor(f.root).ok, true);
  release([row, row]); assert.equal(qms.doctor(f.root).ok, false);
  release([]); assert.equal(qms.doctor(f.root).ok, false);
  release([row, { ...row, id: 'UNKNOWN' }]); assert.equal(qms.doctor(f.root).ok, false);
  release([row]); fs.appendFileSync(path.join(f.root, d.file), 'changed'); assert.equal(qms.doctor(f.root).ok, false);
});
test('CLI errors are clean and nonzero', t => {
  const f = fixture(t); const cli = path.resolve(__dirname, '../tools/qms/cli.js');
  const result = spawnSync(process.execPath, [cli, 'select', '--root', f.root, '--unknown', 'x'], { encoding: 'utf8' });
  assert.equal(result.status, 1); assert.match(result.stderr, /Invalid flag/);
});

function craftDoc(id, facets, overrides = {}) {
  return doc({ id, file: `documents/${id}.md`, stages: ['craft'], facets, ...overrides });
}
test('craft facets load only requested controls and their procedure dependencies', t => {
  const f = fixture(t, [
    craftDoc('EXPRESSION', ['expression'], { requires: ['PERFORMANCE'] }),
    craftDoc('MICRO', ['microexpression']),
    craftDoc('CAMERA', ['camera']),
    craftDoc('EXPRESSION-FORM', ['expression'], { kind: 'template', level: 4, requires: ['EXPRESSION'] }),
    doc({ id: 'PERFORMANCE', file: 'documents/performance.md', kind: 'procedure', level: 2, stages: ['governance'] })
  ]);
  assert.equal(qms.doctor(f.root).ok, true);
  const result = qms.selectDocuments(f.root, { stage: 'craft', facets: ['expression'] });
  assert.deepEqual(result.documents.map(d => d.id), ['PERFORMANCE', 'EXPRESSION', 'EXPRESSION-FORM']);
  assert.match(result.documents.find(d => d.id === 'PERFORMANCE').reason, /required by/);
  assert.match(result.documents.find(d => d.id === 'EXPRESSION').reason, /facets expression/);
});
test('video keeps its v1 baseline and adds facets without loading the entire craft library', t => {
  const f = fixture(t, [doc({ stages: ['video'] }), craftDoc('CAMERA', ['camera'], { stages: ['video', 'craft'] }), craftDoc('BLOCKING', ['blocking'])]);
  assert.deepEqual(qms.selectDocuments(f.root, video).documents.map(d => d.id), ['SOP-COMMON']);
  assert.deepEqual(qms.selectDocuments(f.root, { ...video, facets: ['camera'] }).documents.map(d => d.id), ['CAMERA', 'SOP-COMMON']);
  const first = qms.buildBundle(f.root, { ...video, facets: ['blocking', 'camera', 'blocking'] });
  const second = qms.buildBundle(f.root, { ...video, facets: ['camera', 'blocking'] });
  assert.equal(first.sha256, second.sha256);
  assert.throws(() => qms.buildBundle(f.root, { ...video, facets: ['camera'] }, { maxChars: 10 }), /budget/);
});
test('facet queries reject unknown, missing and malformed controls explicitly', t => {
  const f = fixture(t, [craftDoc('CAMERA', ['camera']), craftDoc('TEMPLATE-ONLY', ['tone'], { kind: 'template', level: 4 }), craftDoc('DRAFT', ['expression'], { status: 'draft' })]);
  for (const facets of [undefined, []]) assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets }), /requires at least one facet/);
  for (const facets of ['camera', [null], [''], [' camera']]) assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets }), /facets must/);
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['unknown'] }), /Unknown facet: unknown/);
  for (const facet of ['tone', 'expression']) assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: [facet] }), new RegExp(`No applicable released SOP for facet: ${facet}`));
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['camera', 'expression'] }), /facet: expression/);
});
test('craft controls preserve exact model, platform and tuple isolation', t => {
  const f = fixture(t, [craftDoc('H3-CAMERA', ['camera'], { models: ['h3'], model_versions: ['1'], platforms: ['official'], modes: ['text'] }), craftDoc('SEED-CAMERA', ['camera'], { models: ['seedance'] })]);
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['camera'] }), /No applicable/);
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['camera'], model: 'h3' }), /Full model/);
  assert.deepEqual(qms.selectDocuments(f.root, { ...video, stage: 'craft', facets: ['camera'] }).documents.map(d => d.id), ['H3-CAMERA']);
  assert.throws(() => qms.selectDocuments(f.root, { ...video, stage: 'craft', facets: ['camera'], platform: 'other' }), /exact released model profile/);
});
test('examples, private sources and restricted dependencies cannot enter facet bundles', t => {
  const f = fixture(t, [craftDoc('CAMERA', ['camera']), craftDoc('EXAMPLE', ['camera'], { kind: 'example', level: 4 }), craftDoc('RECORD', ['camera'], { kind: 'record', level: 4 }), craftDoc('PRIVATE', ['blocking'], { privacy: 'local' })]);
  assert.deepEqual(qms.selectDocuments(f.root, { stage: 'craft', facets: ['camera'] }).documents.map(d => d.id), ['CAMERA']);
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['blocking'] }), /No applicable/);
  assert.deepEqual(qms.selectDocuments(f.root, { stage: 'craft', facets: ['blocking'], target: 'local' }).documents.map(d => d.id), ['PRIVATE']);
  f.registry.documents[0].requires = ['PRIVATE']; f.save();
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['camera'] }), /Incompatible dependency: PRIVATE/);
  f.sources.sources[0].privacy = 'no_ai'; f.save();
  assert.throws(() => qms.selectDocuments(f.root, { stage: 'craft', facets: ['camera'], target: 'local' }), /No applicable/);
});
test('doctor checks optional facet metadata and release seals include facets', t => {
  const f = fixture(t, [craftDoc('CAMERA', ['camera'])]);
  for (const facets of ['camera', [null], [''], [' camera'], ['camera', 'camera']]) {
    f.registry.documents[0].facets = facets; f.save(); assert.equal(qms.doctor(f.root).ok, false);
  }
  f.registry.documents[0].facets = ['camera']; f.save();
  const digest = name => crypto.createHash('sha256').update(fs.readFileSync(path.join(f.root, name))).digest('hex');
  const d = f.registry.documents[0];
  fs.writeFileSync(path.join(f.root, 'release-content.json'), JSON.stringify({ schema_version: 1, registry_sha256: digest('registry.json'), documents: [{ id: d.id, file: d.file, version: d.version, sha256: digest(d.file) }] }));
  assert.equal(qms.doctor(f.root).ok, true);
  d.facets = ['blocking']; f.save(); assert.equal(qms.doctor(f.root).ok, false);
});
test('CLI parses comma-separated facets and rejects empty items', t => {
  const f = fixture(t, [craftDoc('CAMERA', ['camera']), craftDoc('BLOCKING', ['blocking'])]);
  const cli = path.resolve(__dirname, '../tools/qms/cli.js');
  const run = facets => spawnSync(process.execPath, [cli, 'select', '--root', f.root, '--stage', 'craft', '--facets', facets], { encoding: 'utf8' });
  const result = run('camera, blocking');
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout).documents.map(d => d.id), ['BLOCKING', 'CAMERA']);
  const invalid = run('camera,'); assert.equal(invalid.status, 1); assert.match(invalid.stderr, /facets must/);
});


test('record rejects outside and controlled paths, including linked parents', t => {
  const f = fixture(t);
  const outside = fs.mkdtempSync(path.join(os.tmpdir(), 'qms-record-outside-'));
  assert(path.resolve(outside).startsWith(path.resolve(os.tmpdir()) + path.sep));
  t.after(() => fs.rmSync(outside, { recursive: true, force: true }));
  assert.throws(() => qms.writeRecord(f.root, { stage: 'script' }, path.join(outside, 'escape')), /inside the project root/);
  assert(!fs.existsSync(path.join(outside, 'escape')));
  for (const name of ['standards', 'tools', 'skills', 'wiki', 'docs', '.git']) {
    fs.mkdirSync(path.join(f.root, name));
    assert.throws(() => qms.writeRecord(f.root, { stage: 'script' }, path.join(f.root, name, 'record')), /controlled directories/);
  }
  try { fs.symlinkSync(outside, path.join(f.root, 'linked-out'), 'junction'); }
  catch (e) { t.diagnostic(`Linked-parent assertion unavailable: ${e.message}`); return; }
  assert.throws(() => qms.writeRecord(f.root, { stage: 'script' }, path.join(f.root, 'linked-out', 'escape')), /inside the project root/);
  assert(!fs.existsSync(path.join(outside, 'escape')));
});

test('a standards subdirectory permits immutable records in its marked project', t => {
  const f = fixture(t);
  const standards = path.join(f.root, 'standards');
  fs.mkdirSync(standards);
  for (const name of ['registry.json', 'sources.json', 'documents']) fs.renameSync(path.join(f.root, name), path.join(standards, name));
  fs.writeFileSync(path.join(f.root, 'qms-project.json'), JSON.stringify({schema_version:1,name:'ai-video-qms'}));
  const out = path.join(f.root, 'record');
  assert.equal(qms.writeRecord(standards, {stage:'script'}, out).outputDir, out);
  assert(fs.existsSync(path.join(out, 'record.json')));
});
