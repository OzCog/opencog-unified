/* ============================================================================
   entities — metagraph workbench
   One typed metagraph (nodes / binary edges / hyperedges), many projections:
     transport   — force topology, protocol edges, role rings, GIS layers
     computation — layered DAG blocks with activation (utilization) bars
   Hyperedges render as convex hulls or as junction nodes (bipartite expansion).
   Native schema documented in the Help card; d9 {Pkgs,Wlds} auto-imported.
   ========================================================================== */
'use strict';

/* ---------------------------------------------------------------- palette */
const INK = '#ffffff', INK2 = '#c3c2b7', MUTED = '#898781';
const PAGE = '#0d0d0d', SURFACE = '#1a1a19', RAISED = '#232322', GRID = '#2c2c2a', AXIS = '#383835';
const SEQ_LO = '#6da7ec', SEQ_HI = '#184f95';   // sequential blue (dark ordinal band)
const CRIT = '#d03b3b';

const NODE_TYPES = {
  hw:       { label: 'hardware',  color: '#3987e5', glyph: 'square',   r: 7,   layer: 'hw' },
  net:      { label: 'network',   color: '#d95926', glyph: 'triangle', r: 9,   layer: 'net' },
  cluster:  { label: 'cluster',   color: '#199e70', glyph: 'hex',      r: 12,  layer: 'cluster' },
  workload: { label: 'workload',  color: '#c98500', glyph: 'circle',   r: 8,   layer: 'wl' },
  pkg:      { label: 'package',   color: '#d55181', glyph: 'diamond',  r: 5.5, layer: 'wl' },
  storage:  { label: 'storage',   color: '#008300', glyph: 'cyl',      r: 9,   layer: 'wl' },
  ns:       { label: 'namespace', color: '#9085e9', glyph: 'folder',   r: 7,   layer: 'ns' },
};
const EDGE_TYPES = {
  link:   { color: '#6a6a66', alpha: .50, dash: null,    rated: true },
  tunnel: { color: '#9085e9', alpha: .75, dash: [7, 5],  rated: true },
  flow:   { color: '#199e70', alpha: .65, dash: null,    rated: true },
  dep:    { color: '#d55181', alpha: .30, dash: null },
  nfs:    { color: '#008300', alpha: .45, dash: [2, 3] },
  sched:  { color: '#6a6a66', alpha: .28, dash: [1, 3] },
  nsrel:  { color: '#9085e9', alpha: .25, dash: [1, 3] },
};
const HYPER_TYPES = {
  dep:     { label: 'dep closure', color: '#d55181', layer: 'hdep',  pad: 18 },
  tenancy: { label: 'tenant',      color: '#e66767', layer: 'hten',  pad: 26 },
  mesh:    { label: 'meshwork',    color: '#3987e5', layer: 'hmesh', pad: 30 },
};
const LAYERS = [
  { id: 'hw',      group: 'substrate', name: 'Hardware' },
  { id: 'net',     group: 'substrate', name: 'Network topology' },
  { id: 'ns',      group: 'topology',  name: 'Namespaces' },
  { id: 'cluster', group: 'topology',  name: 'Compute clusters' },
  { id: 'wl',      group: 'payload',   name: 'Workloads · pkgs · storage' },
  { id: 'hdep',    group: 'overlays',  name: 'Dep closures', off: true },
  { id: 'hten',    group: 'overlays',  name: 'Tenancy', off: true },
  { id: 'hmesh',   group: 'overlays',  name: 'Meshwork' },
];
const ROLE_LIST = ['ingress', 'egress', 'hop', 'relay'];

/* ---------------------------------------------------------------- state */
const state = {
  mode: 'transport',          // 'transport' | 'computation'
  hyperRender: 'hull',        // 'hull' | 'junction'
  layers: new Set(LAYERS.filter(l => !l.off).map(l => l.id)),
  selection: null,            // {kind:'node'|'hyper'|'ns', id|path}
  hover: null,                // same shape
  isolate: false,
  q: '',
  matches: new Set(),
  t: d3.zoomIdentity,
  anim: null,                 // mode tween {t0, dur}
  dashOff: 0,
  seed: 9,
};
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

let model = null;             // {nodes, edges, hyperedges}
let idx = null;               // indexes built from model
let sim = null;

/* ---------------------------------------------------------------- utils */
const $ = s => document.querySelector(s);
function mulberry32(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const nid = x => (typeof x === 'object' ? x.id : x);
const easeC = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
function toast(msg, ms = 3800) {
  const el = $('#toast'); el.textContent = msg; el.style.display = 'block';
  clearTimeout(el._t); el._t = setTimeout(() => el.style.display = 'none', ms);
}

/* ============================================================ generator */
function generateEstate(seed) {
  const R = mulberry32(seed);
  const ri = (a, b) => a + Math.floor(R() * (b - a + 1));
  const rf = (a, b) => a + R() * (b - a);
  const pick = a => a[Math.floor(R() * a.length)];
  const nodes = [], edges = [], hyperedges = [];
  const add = n => (nodes.push(n), n);
  const E = (s, t, type, tags = {}) => edges.push({ source: s, target: t, type, tags });

  const CLOUDS = ['aurora', 'borealis', 'cumulus'];
  const PKG_FAMS = ['PSOnnxRtm.3.7', 'PSTkzShr.3.7', 'PSTkz.2.7', 'ImgCntMod.1', 'ImgSclr.1',
    'ImgSeg.1', 'ImgObjExtr.1', 'ImgObjRemv.1', 'Plx.1', 'ScrRegDtec.1', 'TxtRcog.1',
    'ImgSch.3', 'ImgTxtSch.3', 'FaceAnls.1', 'QryBlkLst.1', 'QryProc.1', 'SemTxt.1',
    'Mgr.1', 'SesMgr.1', 'Dat.CntExtr.1', 'Dat.ImgProc.1', 'Dat.ImgTrsf.1', 'Dat.ImgSch.1',
    'Dat.Anls.1', 'MshCtl.1', 'LedgKpr.1', 'AudRoll.1', 'TokBrkr.1', 'VecStr.2', 'GrphIdx.2',
    'EvtQue.1', 'SchdOpt.1', 'CfgSnap.1', 'KeyFab.1', 'ObsPipe.1', 'InfRt.1'];
  const WL_KINDS = ['anls', 'cnt-extr', 'img-proc', 'sem-txt', 'qry', 'ses', 'sync',
    'audit', 'ledger', 'mesh-ctl', 'infer', 'embed'];

  // shared package registry (zipf-ish popularity)
  const pkgs = PKG_FAMS.map((fam, i) => add({
    id: 'pkg:' + fam, type: 'pkg', name: fam, ns: 'shared/registry',
    tags: { family: fam, version: 'w.x.y.z', pop: +(1 / (1 + i * .35)).toFixed(3) },
  }));
  const wPick = (arr, w, k) => {           // weighted sample w/o replacement
    const pool = arr.map((v, i) => ({ v, w: w(v, i) })); const out = [];
    while (out.length < k && pool.length) {
      let s = pool.reduce((a, p) => a + p.w, 0), x = R() * s, j = 0;
      while ((x -= pool[j].w) > 0) j++;
      out.push(pool.splice(j, 1)[0].v);
    }
    return out;
  };

  const allWl = [];
  CLOUDS.forEach((c, ci) => {
    add({ id: 'ns:' + c, type: 'ns', name: c, ns: c, tags: { kind: 'cloud' } });
    add({ id: `ns:${c}/infra`, type: 'ns', name: 'infra', ns: `${c}/infra`, tags: { kind: 'infra' } });
    E('ns:' + c, `ns:${c}/infra`, 'nsrel');

    // network fabric
    const gwIn = add({ id: `net:${c}/gw-in`, type: 'net', name: 'gw-in', ns: `${c}/infra`, tags: { role: 'ingress', ip: `10.${ci}.0.1` } });
    const gwOut = add({ id: `net:${c}/gw-out`, type: 'net', name: 'gw-out', ns: `${c}/infra`, tags: { role: 'egress', ip: `10.${ci}.0.2` } });
    const relay = add({ id: `net:${c}/relay`, type: 'net', name: 'relay', ns: `${c}/infra`, tags: { role: 'relay', ip: `10.${ci}.0.9` } });
    const spines = [0, 1].map(s => add({ id: `net:${c}/spine${s}`, type: 'net', name: `spine${s}`, ns: `${c}/infra`, tags: { role: 'hop', ip: `10.${ci}.1.${s}` } }));
    const leaves = d3.range(ri(3, 4)).map(l => add({ id: `net:${c}/leaf${l}`, type: 'net', name: `leaf${l}`, ns: `${c}/infra`, tags: { role: 'hop', ip: `10.${ci}.2.${l}` } }));
    spines.forEach(s => { E(gwIn.id, s.id, 'link', { protocol: 'eth', rate: 40000 }); E(gwOut.id, s.id, 'link', { protocol: 'eth', rate: 40000 }); });
    E(relay.id, gwOut.id, 'link', { protocol: 'eth', rate: 10000 });
    leaves.forEach(l => spines.forEach(s => E(l.id, s.id, 'link', { protocol: 'eth', rate: 40000 })));

    // hardware
    const hosts = d3.range(ri(9, 13)).map(h => {
      const leaf = ri(0, leaves.length - 1);
      const n = add({ id: `hw:${c}/h${h}`, type: 'hw', name: `h${h}`, ns: `${c}/infra`, tags: { ip: `10.${ci}.${2 + leaf}.${10 + h}`, hwtype: pick(['blade', 'blade', 'edge', 'gpu', 'nas']) } });
      E(n.id, leaves[leaf].id, 'link', { protocol: 'eth', rate: pick([1000, 2500, 10000]) });
      return n;
    });

    // clusters & storage
    const clusters = ['k8s', 'batch'].map(k => {
      const n = add({ id: `cl:${c}/${k}`, type: 'cluster', name: k, ns: `${c}/infra`, tags: { cores: ri(64, 512), memGiB: ri(256, 4096), sched: k === 'k8s' ? 'kube' : 'slurm' } });
      wPick(hosts, () => 1, ri(4, 6)).forEach(h => E(n.id, h.id, 'sched'));
      return n;
    });
    const stores = ['obj', 'blk'].map(k => {
      const n = add({ id: `st:${c}/${k}`, type: 'storage', name: k, ns: `${c}/infra`, tags: { tb: ri(40, 400), kind: k === 'obj' ? 's3' : 'ceph-rbd' } });
      E(n.id, pick(leaves).id, 'link', { protocol: 'eth', rate: 10000 });
      return n;
    });

    // namespaces + workloads
    d3.range(ri(2, 3)).forEach(oi => {
      const org = `org-${'abc'[oi]}`;
      add({ id: `ns:${c}/${org}`, type: 'ns', name: org, ns: `${c}/${org}`, tags: { kind: 'org' } });
      E('ns:' + c, `ns:${c}/${org}`, 'nsrel');
      d3.range(ri(1, 3)).forEach(ti => {
        const team = `team-${ti + 1}`, path = `${c}/${org}/${team}`;
        add({ id: 'ns:' + path, type: 'ns', name: team, ns: path, tags: { kind: 'team' } });
        E(`ns:${c}/${org}`, 'ns:' + path, 'nsrel');
        d3.range(ri(2, 4)).forEach(() => {
          const kind = pick(WL_KINDS);
          const wl = add({
            id: `wl:${path}/${kind}-${allWl.length}`, type: 'workload', name: `${kind}-${allWl.length}`,
            ns: path, tags: { util: +rf(.15, .97).toFixed(2), replicas: ri(1, 9), site: pick(['edge', 'core', 'dmz']) },
          });
          allWl.push(wl);
          E(wl.id, pick(clusters).id, 'sched');
          if (R() < .6) E(pick(stores).id, wl.id, 'nfs', { rate: ri(50, 900), protocol: 'nfs' });
          wPick(pkgs, p => p.tags.pop, ri(3, 7)).forEach(p => E(p.id, wl.id, 'dep'));
        });
      });
    });
  });

  // cross-cloud tunnels (wg meshwork)
  for (let a = 0; a < 3; a++) for (let b = a + 1; b < 3; b++)
    E(`net:${CLOUDS[a]}/gw-out`, `net:${CLOUDS[b]}/gw-in`, 'tunnel', { protocol: 'wg', rate: ri(200, 900) });
  E(`net:${CLOUDS[0]}/relay`, `net:${CLOUDS[2]}/relay`, 'tunnel', { protocol: 'wg', rate: ri(100, 400) });

  // pipelines (acyclic by construction: forward index only)
  d3.range(ri(9, 13)).forEach(() => {
    const i = ri(0, allWl.length - 2), j = ri(i + 1, allWl.length - 1);
    if (i !== j) E(allWl[i].id, allWl[j].id, 'flow', { protocol: pick(['grpc', 'http2', 'amqp']), rate: ri(10, 400) });
  });

  // hyperedges: dep closures (a package shared by >=2 workloads IS a hyperedge)
  const consumers = new Map(pkgs.map(p => [p.id, []]));
  edges.filter(e => e.type === 'dep').forEach(e => consumers.get(e.source).push(e.target));
  consumers.forEach((wls, pid) => {
    if (wls.length >= 2) hyperedges.push({
      id: 'hx:dep:' + pid, type: 'dep', name: pid.replace('pkg:', ''),
      members: [pid, ...wls], tags: { consumers: wls.length },
    });
  });
  // tenants (identity-free: numbers only), spanning clouds
  d3.range(7).forEach(i => {
    const members = wPick(allWl, () => 1, ri(4, 11)).map(w => w.id);
    hyperedges.push({ id: 'hx:t' + i, type: 'tenancy', name: `tenant-0${i + 1}`, members, tags: { workloads: members.length } });
  });
  // the meshwork itself
  hyperedges.push({
    id: 'hx:mesh', type: 'mesh', name: 'wg-meshwork',
    members: nodes.filter(n => n.type === 'net' && ['ingress', 'egress', 'relay'].includes(n.tags.role)).map(n => n.id),
    tags: { protocol: 'wg' },
  });

  return { nodes, edges, hyperedges, clouds: CLOUDS };
}

/* ========================================================== d9 importer */
function importD9(j) {
  const nodes = [], edges = [], hyperedges = [];
  const seen = new Set();
  (j.Pkgs || []).forEach(p => {
    const id = 'pkg:' + p.FamNam;
    if (seen.has(id)) return; seen.add(id);
    nodes.push({ id, type: 'pkg', name: p.FamNam, ns: 'd9/pkgs', tags: { family: p.FamNam, version: typeof p.Version === 'string' ? p.Version : '?' } });
  });
  const seenWl = new Set();
  (j.Wlds || []).forEach(w => {
    const id = 'wl:' + w.Id;
    if (seenWl.has(id)) return;
    seenWl.add(id);
    nodes.push({ id, type: 'workload', name: w.Id.split('.').pop(), ns: 'd9/wld', tags: { wldId: w.Id, util: .5 } });
    (w.Pkgs || []).forEach(p => {
      const pid = 'pkg:' + p.FamNam;
      if (!seen.has(pid)) { seen.add(pid); nodes.push({ id: pid, type: 'pkg', name: p.FamNam, ns: 'd9/pkgs', tags: { family: p.FamNam } }); }
      edges.push({ source: pid, target: id, type: 'dep', tags: p.ManfPkg ? { manifest: true } : {} });
    });
  });
  const consumers = new Map();
  edges.forEach(e => { (consumers.get(e.source) ?? consumers.set(e.source, []).get(e.source)).push(e.target); });
  consumers.forEach((wls, pid) => {
    if (wls.length >= 2) hyperedges.push({ id: 'hx:dep:' + pid, type: 'dep', name: pid.replace('pkg:', ''), members: [pid, ...wls], tags: { consumers: wls.length } });
  });
  return { nodes, edges, hyperedges, clouds: ['d9'] };
}

/* ============================================================== indexes */
function buildAll(m) {
  // validate + normalize BEFORE committing to globals, so a malformed import
  // throws here and the previous model keeps rendering untouched
  if (!Array.isArray(m.nodes) || !m.nodes.length) throw new Error('model needs a non-empty nodes[]');
  const seenIds = new Set();
  m.nodes = m.nodes.filter(n => {
    if (!n || n.id == null || seenIds.has(n.id)) return false;
    seenIds.add(n.id);
    n.name = String(n.name ?? n.id);
    n.tags = n.tags || {};
    return true;
  });
  const nodeById = new Map(m.nodes.map(n => [n.id, n]));
  m.edges = (m.edges || []).filter(e => e && nodeById.has(nid(e.source)) && nodeById.has(nid(e.target)));
  m.hyperedges = (m.hyperedges || []).filter(h => h && Array.isArray(h.members)
    && (h.members = h.members.filter(id => nodeById.has(id))).length >= 2
    && (h.name = String(h.name ?? h.id), h.tags = h.tags || {}, true));
  model = m;

  const adj = new Map(m.nodes.map(n => [n.id, []]));
  m.edges.forEach(e => { adj.get(nid(e.source)).push(e); adj.get(nid(e.target)).push(e); });
  const hypersByNode = new Map();
  m.hyperedges.forEach(h => h.members.forEach(id =>
    (hypersByNode.get(id) ?? hypersByNode.set(id, []).get(id)).push(h)));
  const hyperById = new Map(m.hyperedges.map(h => [h.id, h]));

  // cloud assignment + anchors
  const clouds = m.clouds || [...new Set(m.nodes.map(n => (n.ns || '').split('/')[0]).filter(Boolean))];
  const anchors = new Map(clouds.map((c, i) => {
    const a = -Math.PI / 2 + i * 2 * Math.PI / Math.max(clouds.length, 1);
    const rr = clouds.length > 1 ? 520 : 0;
    return [c, { x: Math.cos(a) * rr, y: Math.sin(a) * rr }];
  }));
  m.nodes.forEach(n => {
    n.cloud = clouds.includes((n.ns || '').split('/')[0]) ? (n.ns || '').split('/')[0] : null;
    n.vis = NODE_TYPES[n.type] || { label: n.type, color: MUTED, glyph: 'circle', r: 7, layer: 'wl' };
  });
  // tunnel endpoints flag
  m.edges.forEach(e => { if (e.type === 'tunnel') { nodeById.get(nid(e.source)).tun = true; nodeById.get(nid(e.target)).tun = true; } });

  idx = { nodeById, adj, hypersByNode, hyperById, clouds, anchors };
  initPositions();
  initSim();
  buildLayersPanel();
  buildLegend();
  buildTree();
  clearSelection();
  state.q = ''; state.matches = new Set(); $('#search').value = '';
  renderInspector();
  updateStatus();
  requestDraw();
}

function initPositions() {
  const R = mulberry32(state.seed + 101);
  model.nodes.forEach(n => {
    const a = idx.anchors.get(n.cloud) || { x: 0, y: 0 };
    n.x = a.x + (R() - .5) * 300;
    n.y = a.y + (R() - .5) * 300;
  });
}

const LINK_DIST = { link: 46, tunnel: 300, flow: 130, dep: 80, nfs: 90, sched: 55, nsrel: 42 };
const LINK_STR  = { link: .55, tunnel: .04, flow: .05, dep: .12, nfs: .06, sched: .25, nsrel: .5 };
function initSim() {
  if (sim) sim.stop();
  sim = d3.forceSimulation(model.nodes)
    .force('link', d3.forceLink(model.edges).id(d => d.id)
      .distance(l => LINK_DIST[l.type] || 70).strength(l => LINK_STR[l.type] ?? .3))
    .force('charge', d3.forceManyBody().strength(-170).distanceMax(650))
    .force('collide', d3.forceCollide(d => d.vis.r + 7))
    .force('ax', d3.forceX(d => (idx.anchors.get(d.cloud) || { x: 0 }).x).strength(.07))
    .force('ay', d3.forceY(d => (idx.anchors.get(d.cloud) || { y: 0 }).y).strength(.07))
    .alpha(1).alphaDecay(.025)
    .on('tick', requestDraw);
  if (state.mode === 'computation') { sim.stop(); layoutDAG(); startTween(); }
}

/* ========================================================== visibility */
function nodeVisible(n) {
  if (state.mode === 'computation' && !['pkg', 'storage', 'workload'].includes(n.type)) return false;
  if (!state.layers.has(n.vis.layer)) return false;
  if (state.isolate && state.selection && !related(n)) return false;
  return true;
}
function edgeVisible(e) {
  if (state.mode === 'computation' && !['dep', 'nfs', 'flow'].includes(e.type)) return false;
  return nodeVisible(e.source) && nodeVisible(e.target);
}
function hyperVisible(h) {
  // selection reveals its hyperedges even when their layer is off
  const revealed = rel && rel.H.has(h.id);
  if (state.mode === 'computation' && h.type !== 'tenancy' && !revealed) return false;
  if (!revealed && !state.layers.has(HYPER_TYPES[h.type]?.layer)) return false;
  return h.members.filter(id => nodeVisible(idx.nodeById.get(id))).length >= 2;
}

/* related(): is node connected to the current selection? */
function relatedSets() {
  const s = state.selection;
  if (!s) return null;
  const N = new Set(), E = new Set(), H = new Set();
  if (s.kind === 'node') {
    N.add(s.id);
    (idx.adj.get(s.id) || []).forEach(e => { E.add(e); N.add(nid(e.source)); N.add(nid(e.target)); });
    (idx.hypersByNode.get(s.id) || []).forEach(h => { H.add(h.id); h.members.forEach(id => N.add(id)); });
  } else if (s.kind === 'hyper') {
    const h = idx.hyperById.get(s.id);
    if (h) { H.add(h.id); h.members.forEach(id => N.add(id)); }
    model.edges.forEach(e => { if (N.has(nid(e.source)) && N.has(nid(e.target))) E.add(e); });
  } else if (s.kind === 'ns') {
    model.nodes.forEach(n => { if (inNs(n.ns, s.path)) N.add(n.id); });
    model.edges.forEach(e => { if (N.has(nid(e.source)) && N.has(nid(e.target))) E.add(e); });
  }
  return { N, E, H };
}
let rel = null;
function related(n) { return !rel || rel.N.has(n.id); }

/* ======================================================== DAG layout */
function layoutDAG() {
  const parts = model.nodes.filter(n => ['pkg', 'storage', 'workload'].includes(n.type));
  const wl = parts.filter(n => n.type === 'workload');
  const flowPred = new Map(wl.map(n => [n.id, []]));
  model.edges.forEach(e => { if (e.type === 'flow') flowPred.get(nid(e.target))?.push(nid(e.source)); });
  const depth = new Map(), onstack = new Set();
  const depthOf = id => {                    // longest path; back-edges broken at 0
    if (depth.has(id)) return depth.get(id);
    if (onstack.has(id)) return 0;
    onstack.add(id);
    const preds = flowPred.get(id) || [];
    const d = preds.length ? 1 + Math.max(0, ...preds.map(depthOf)) : 1;
    onstack.delete(id);
    depth.set(id, d); return d;
  };
  wl.forEach(n => depthOf(n.id));
  parts.forEach(n => { n.dagLayer = n.type === 'workload' ? depth.get(n.id) : 0; });

  const byLayer = d3.group(parts, n => n.dagLayer);
  const maxL = d3.max(parts, n => n.dagLayer);
  // order: layer 0 by type+popularity; others by barycenter of predecessors
  const yOf = new Map();
  const order0 = (byLayer.get(0) || []).sort((a, b) =>
    a.type.localeCompare(b.type) || (b.tags?.pop || 0) - (a.tags?.pop || 0) || a.name.localeCompare(b.name));
  order0.forEach((n, i) => yOf.set(n.id, i));
  for (let L = 1; L <= maxL; L++) {
    const preds = new Map();
    (byLayer.get(L) || []).forEach(n => {
      const ps = [];
      (idx.adj.get(n.id) || []).forEach(e => {
        if (!['dep', 'nfs', 'flow'].includes(e.type)) return;
        const p = nid(e.source) === n.id ? nid(e.target) : nid(e.source);
        const pn = idx.nodeById.get(p);
        if (pn && pn.dagLayer < L && yOf.has(p)) ps.push(yOf.get(p));
      });
      preds.set(n.id, ps.length ? d3.mean(ps) : 1e9);
    });
    (byLayer.get(L) || [])
      .sort((a, b) => preds.get(a.id) - preds.get(b.id) || a.name.localeCompare(b.name))
      .forEach((n, i) => yOf.set(n.id, i));
  }
  // wrap tall layers into sub-columns; layer x-offsets are cumulative
  const WRAP = 26, SUBW = 126, GAP = 140;
  const xoff = []; let acc = 0;
  for (let L = 0; L <= maxL; L++) {
    const c = (byLayer.get(L) || []).length;
    xoff[L] = acc;
    acc += (Math.max(1, Math.ceil(c / WRAP)) - 1) * SUBW + 110 + GAP;
  }
  for (let L = 0; L <= maxL; L++) {
    const col = (byLayer.get(L) || []);
    const step = L === 0 ? 34 : 56;
    col.forEach(n => {
      const o = yOf.get(n.id);
      const sub = Math.floor(o / WRAP), row = o % WRAP;
      const rows = Math.min(WRAP, col.length - sub * WRAP);
      n.tx = xoff[L] + sub * SUBW;
      n.ty = (row - (rows - 1) / 2) * step;
    });
  }
}
function startTween() {
  model.nodes.forEach(n => { n.sx = n.x; n.sy = n.y; });
  state.anim = { t0: performance.now(), dur: reducedMotion ? 0 : 560 };
  rafLoop();
}

/* ============================================================ canvas */
const canvas = $('#graph');
const ctx = canvas.getContext('2d');
let W = 0, H = 0, DPR = 1;
function resize() {
  const r = canvas.parentElement.getBoundingClientRect();
  DPR = window.devicePixelRatio || 1;
  W = Math.max(10, r.width); H = Math.max(10, r.height);
  canvas.width = W * DPR; canvas.height = H * DPR;
  requestDraw();
}
new ResizeObserver(resize).observe($('#main'));
(function watchDPR() {   // re-render crisply when the window moves between monitors
  matchMedia(`(resolution: ${devicePixelRatio}dppx)`)
    .addEventListener('change', () => { resize(); watchDPR(); }, { once: true });
})();

let drawQueued = false;
function requestDraw() {
  if (drawQueued) return;
  drawQueued = true;
  requestAnimationFrame(() => { drawQueued = false; draw(); });
}
let rafOn = false;
function rafLoop() {
  if (rafOn) return; rafOn = true;
  const step = () => {
    const animating = !!state.anim;
    const pulsing = state.mode === 'computation' && !reducedMotion;
    if (state.anim) {
      const p = state.anim.dur === 0 ? 1 : Math.min(1, (performance.now() - state.anim.t0) / state.anim.dur);
      const e = easeC(p);
      model.nodes.forEach(n => {
        if (n.tx == null) return;
        n.x = n.sx + (n.tx - n.sx) * e;
        n.y = n.sy + (n.ty - n.sy) * e;
      });
      if (p >= 1) state.anim = null;
    }
    if (pulsing) state.dashOff -= 1.1;
    draw();
    if (animating || pulsing) requestAnimationFrame(step);
    else rafOn = false;
  };
  requestAnimationFrame(step);
}

/* ---- glyphs ---- */
function glyphPath(g, x, y, r) {
  ctx.beginPath();
  switch (g) {
    case 'circle': ctx.arc(x, y, r, 0, 2 * Math.PI); break;
    case 'square': ctx.rect(x - r * .9, y - r * .9, r * 1.8, r * 1.8); break;
    case 'diamond': ctx.moveTo(x, y - r * 1.15); ctx.lineTo(x + r * 1.15, y); ctx.lineTo(x, y + r * 1.15); ctx.lineTo(x - r * 1.15, y); ctx.closePath(); break;
    case 'triangle': ctx.moveTo(x, y - r * 1.15); ctx.lineTo(x + r, y + r * .85); ctx.lineTo(x - r, y + r * .85); ctx.closePath(); break;
    case 'hex': for (let i = 0; i < 6; i++) { const a = Math.PI / 6 + i * Math.PI / 3; ctx[i ? 'lineTo' : 'moveTo'](x + r * Math.cos(a), y + r * Math.sin(a)); } ctx.closePath(); break;
    case 'cyl': ctx.rect(x - r * .95, y - r * .8, r * 1.9, r * 1.6); break;
    case 'folder':
      ctx.moveTo(x - r, y - r * .55); ctx.lineTo(x - r * .25, y - r * .55); ctx.lineTo(x, y - r * .2);
      ctx.lineTo(x + r, y - r * .2); ctx.lineTo(x + r, y + r * .75); ctx.lineTo(x - r, y + r * .75); ctx.closePath(); break;
  }
}
function drawNodeGlyph(n, emph) {
  const { color, glyph } = n.vis;
  const r = n.vis.r;
  glyphPath(glyph, n.x, n.y, r);
  ctx.fillStyle = color; ctx.fill();
  ctx.lineWidth = 1.5 / state.t.k; ctx.strokeStyle = SURFACE; ctx.stroke(); // surface ring
  if (glyph === 'cyl') { // storage: lid line
    ctx.beginPath(); ctx.moveTo(n.x - r * .95, y0(n, r)); ctx.lineTo(n.x + r * .95, y0(n, r));
    ctx.strokeStyle = 'rgba(255,255,255,.5)'; ctx.lineWidth = 1.2 / Math.sqrt(state.t.k); ctx.stroke();
  }
  if (emph === 'sel') { glyphPath(glyph, n.x, n.y, r + 3.5); ctx.strokeStyle = INK; ctx.lineWidth = 1.4 / state.t.k; ctx.stroke(); }
  if (emph === 'match') { ctx.setLineDash([3, 2]); glyphPath('circle', n.x, n.y, r + 4.5); ctx.strokeStyle = INK2; ctx.lineWidth = 1.2 / state.t.k; ctx.stroke(); ctx.setLineDash([]); }
  // transport role rings on network nodes
  if (state.mode === 'transport' && n.type === 'net' && n.tags?.role) {
    ctx.strokeStyle = n.vis.color; ctx.lineWidth = 1.6;
    const rr = r + 4;
    const dashes = { ingress: null, egress: [5, 3], hop: [1.5, 2.6], relay: null };
    ctx.setLineDash(dashes[n.tags.role] || []);
    ctx.beginPath(); ctx.arc(n.x, n.y, rr, 0, 2 * Math.PI); ctx.stroke();
    if (n.tags.role === 'relay') { ctx.beginPath(); ctx.arc(n.x, n.y, rr + 2.6, 0, 2 * Math.PI); ctx.lineWidth = .9; ctx.stroke(); }
    ctx.setLineDash([]);
    if (n.tun) { glyphPath('diamond', n.x, n.y - rr - 5, 3.2); ctx.fillStyle = EDGE_TYPES.tunnel.color; ctx.fill(); }
  }
}
const y0 = (n, r) => n.y - r * .8 + 2.6;

/* ---- hulls ---- */
function hullGeometry(h) {
  const pts = h.members.map(id => idx.nodeById.get(id)).filter(nodeVisible).map(n => [n.x, n.y]);
  if (pts.length < 2) return null;
  const hull = pts.length === 2 ? pts : (d3.polygonHull(pts) || pts);
  return { hull, pts };
}
function drawHull(h, emph) {
  const g = hullGeometry(h); if (!g) return;
  const conf = HYPER_TYPES[h.type] || { color: MUTED, pad: 20 };
  const a = emph === 'sel' ? .34 : emph === 'dim' ? .05 : .16;
  ctx.beginPath();
  g.hull.forEach((p, i) => ctx[i ? 'lineTo' : 'moveTo'](p[0], p[1]));
  ctx.closePath();
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  ctx.lineWidth = conf.pad * 2;
  ctx.strokeStyle = hexA(conf.color, a); ctx.stroke();
  ctx.fillStyle = hexA(conf.color, a * .55); ctx.fill();
  if (emph === 'sel') {
    ctx.lineWidth = 1.4 / state.t.k; ctx.strokeStyle = conf.color; ctx.stroke();
  }
  // label at hull top
  if (state.t.k > .45 || emph === 'sel') {
    const top = g.hull.reduce((m, p) => p[1] < m[1] ? p : m);
    ctx.font = `${Math.min(40, Math.max(10, 12 / state.t.k))}px system-ui, sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    haloText(h.name, top[0], top[1] - conf.pad - 4, hexA(conf.color, emph === 'dim' ? .35 : .95));
  }
}
function drawJunction(h, emph) {
  const g = hullGeometry(h); if (!g) return;
  const conf = HYPER_TYPES[h.type] || { color: MUTED };
  const cx = d3.mean(g.pts, p => p[0]), cy = d3.mean(g.pts, p => p[1]);
  h.jx = cx; h.jy = cy;
  const a = emph === 'dim' ? .12 : .5;
  ctx.strokeStyle = hexA(conf.color, a); ctx.lineWidth = 1;
  g.pts.forEach(p => { ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(p[0], p[1]); ctx.stroke(); });
  glyphPath('diamond', cx, cy, 6);
  ctx.fillStyle = hexA(conf.color, emph === 'dim' ? .3 : 1); ctx.fill();
  ctx.strokeStyle = SURFACE; ctx.lineWidth = 1.2; ctx.stroke();
  if (emph === 'sel') { glyphPath('diamond', cx, cy, 9.5); ctx.strokeStyle = INK; ctx.lineWidth = 1.3 / state.t.k; ctx.stroke(); }
}
function hexA(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`;
}
function haloText(txt, x, y, fill) {
  ctx.lineWidth = 3 / state.t.k; ctx.strokeStyle = PAGE; ctx.strokeText(txt, x, y);
  ctx.fillStyle = fill; ctx.fillText(txt, x, y);
}

/* ---- edges ---- */
function edgeWidth(e) {
  const conf = EDGE_TYPES[e.type] || {};
  if (!conf.rated || !e.tags?.rate) return 1;
  return Math.max(.6, Math.min(3.4, .4 + Math.log10(e.tags.rate) * .62));
}
function drawEdge(e, dim) {
  const conf = EDGE_TYPES[e.type] || { color: MUTED, alpha: .4 };
  const s = e.source, t = e.target;
  ctx.strokeStyle = hexA(conf.color, dim ? conf.alpha * .18 : conf.alpha);
  ctx.lineWidth = edgeWidth(e);
  ctx.setLineDash(conf.dash || []);
  if (e.type === 'flow' && state.mode === 'computation') { ctx.setLineDash([7, 6]); ctx.lineDashOffset = state.dashOff; }
  ctx.beginPath();
  if (state.mode === 'computation') {
    const dx = (t.x - s.x) * .45;
    ctx.moveTo(s.x, s.y); ctx.bezierCurveTo(s.x + dx, s.y, t.x - dx, t.y, t.x, t.y);
  } else {
    ctx.moveTo(s.x, s.y); ctx.lineTo(t.x, t.y);
  }
  ctx.stroke();
  ctx.setLineDash([]); ctx.lineDashOffset = 0;
}

/* ---- computation blocks ---- */
const BLOCK = { workload: { w: 106, h: 34 }, pkg: { w: 94, h: 20 }, storage: { w: 98, h: 26 } };
function drawBlock(n, emph) {
  const b = BLOCK[n.type]; const x = n.x - b.w / 2, y = n.y - b.h / 2;
  ctx.beginPath(); ctx.roundRect(x, y, b.w, b.h, 5);
  ctx.fillStyle = RAISED; ctx.fill();
  ctx.strokeStyle = emph === 'sel' ? INK : hexA(n.vis.color, .8); ctx.lineWidth = emph === 'sel' ? 1.6 : 1; ctx.stroke();
  ctx.fillStyle = n.vis.color; ctx.fillRect(x, y, 3, b.h); // type accent
  ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
  ctx.font = `600 10.5px system-ui, sans-serif`;
  ctx.fillStyle = emph === 'dim' ? MUTED : INK;
  ctx.fillText(truncate(n.name, b.w - 16), x + 8, n.type === 'workload' ? y + 11 : y + b.h / 2);
  if (n.type === 'workload') {
    ctx.font = `9px ${'ui-monospace, monospace'}`; ctx.fillStyle = MUTED;
    ctx.fillText(truncate(shortNs(n.ns), b.w - 16), x + 8, y + 22);
    const u = n.tags?.util ?? 0;                    // activation bar
    const bw = b.w - 12;
    ctx.fillStyle = GRID; ctx.fillRect(x + 6, y + b.h - 5.5, bw, 3);
    ctx.fillStyle = u > .9 ? CRIT : d3.interpolateRgb(SEQ_LO, SEQ_HI)(u);
    ctx.fillRect(x + 6, y + b.h - 5.5, bw * u, 3);
  }
  if (emph === 'match') { ctx.setLineDash([3, 2]); ctx.strokeStyle = INK2; ctx.strokeRect(x - 3, y - 3, b.w + 6, b.h + 6); ctx.setLineDash([]); }
}
function truncate(s, wpx) {
  if (ctx.measureText(s).width <= wpx) return s;
  while (s.length > 2 && ctx.measureText(s + '…').width > wpx) s = s.slice(0, -1);
  return s + '…';
}
const shortNs = ns => (ns || '').split('/').slice(0, 3).join('/');

/* ---- cloud landmasses (GIS base) ---- */
function drawClouds() {
  idx.clouds.forEach(c => {
    const a = idx.anchors.get(c); if (!a) return;
    const pts = model.nodes.filter(n => n.cloud === c);
    if (!pts.length) return;
    const r = Math.max(180, d3.max(pts, n => Math.hypot(n.x - a.x, n.y - a.y)) + 70);
    ctx.beginPath(); ctx.arc(a.x, a.y, r, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgba(255,255,255,.016)'; ctx.fill();
    ctx.setLineDash([4, 7]); ctx.strokeStyle = 'rgba(255,255,255,.07)'; ctx.lineWidth = 1; ctx.stroke(); ctx.setLineDash([]);
    ctx.font = '600 24px system-ui, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillStyle = 'rgba(255,255,255,.10)';
    ctx.fillText(c.toUpperCase(), a.x, a.y - r - 20);
  });
}

/* ---- main draw ---- */
function draw() {
  rel = relatedSets();
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  ctx.fillStyle = PAGE; ctx.fillRect(0, 0, W, H);
  ctx.translate(state.t.x, state.t.y); ctx.scale(state.t.k, state.t.k);

  if (!model) return;
  if (state.mode === 'transport') drawClouds();

  const emphOf = obj => {
    if (state.selection?.kind === 'hyper' && obj.id === state.selection.id) return 'sel';
    if (rel && !rel.H?.has(obj.id)) return 'dim';
    return null;
  };
  // hulls / junctions: big → small so small ones stay pickable & visible
  const hypers = model.hyperedges.filter(hyperVisible)
    .sort((a, b) => (HYPER_TYPES[b.type]?.pad || 0) - (HYPER_TYPES[a.type]?.pad || 0));
  if (state.hyperRender === 'hull') hypers.forEach(h => drawHull(h, emphOf(h)));

  model.edges.filter(edgeVisible).forEach(e => drawEdge(e, rel && !rel.E.has(e)));
  if (state.hyperRender === 'junction') hypers.forEach(h => drawJunction(h, emphOf(h)));

  const vis = model.nodes.filter(nodeVisible);
  vis.forEach(n => {
    const dim = rel && !rel.N.has(n.id);
    const emph = state.selection?.kind === 'node' && n.id === state.selection.id ? 'sel'
      : state.matches.has(n.id) ? 'match' : dim ? 'dim' : null;
    ctx.globalAlpha = dim ? .14 : 1;
    if (state.mode === 'computation') drawBlock(n, emph);
    else drawNodeGlyph(n, emph);
    ctx.globalAlpha = 1;
  });

  if (state.mode === 'transport') drawLabels(vis);
  updateStatus();
}
function drawLabels(vis) {
  const k = state.t.k;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  vis.forEach(n => {
    const dim = rel && !rel.N.has(n.id);
    const focus = (state.selection?.kind === 'node' && n.id === state.selection.id)
      || state.hover?.id === n.id || state.matches.has(n.id);
    const thr = { workload: 1.15, ns: 1.15, cluster: .8, net: 1.5, storage: 1.5, hw: 2.3, pkg: 2.3 }[n.type] ?? 2;
    if (!focus && k < thr) return;
    if (dim && !focus) return;
    ctx.font = `${Math.max(9, 10.5 / Math.sqrt(k))}px system-ui, sans-serif`;
    haloText(n.name, n.x, n.y + n.vis.r + 3, focus ? INK : INK2);
  });
}

/* ====================================================== interaction */
function pickNode(mx, my) {
  const [x, y] = state.t.invert([mx, my]);
  let best = null, bd = Infinity;
  for (const n of model.nodes) {
    if (!nodeVisible(n)) continue;
    let d;
    if (state.mode === 'computation') {
      const b = BLOCK[n.type];
      d = Math.max(Math.abs(n.x - x) - b.w / 2, Math.abs(n.y - y) - b.h / 2);
      if (d > 0) continue; d = Math.abs(d);
    } else {
      d = Math.hypot(n.x - x, n.y - y) - n.vis.r;
      if (d > 8 / state.t.k) continue;     // constant ~8px slop in screen space
    }
    if (d < bd) { bd = d; best = n; }
  }
  return best;
}
function pickHyper(mx, my) {
  const [x, y] = state.t.invert([mx, my]);
  let best = null, bestArea = Infinity;
  for (const h of model.hyperedges.filter(hyperVisible)) {
    if (state.hyperRender === 'junction') {
      if (h.jx != null && Math.hypot(h.jx - x, h.jy - y) < 11) return h;
      continue;
    }
    const g = hullGeometry(h); if (!g) continue;
    const pad = (HYPER_TYPES[h.type]?.pad || 20);
    const poly = g.hull;
    const inside = poly.length > 2 && d3.polygonContains(poly, [x, y]);
    const near = !inside && poly.some((p, i) => segDist([x, y], p, poly[(i + 1) % poly.length]) < pad);
    if (inside || near) {
      const area = poly.length > 2 ? Math.abs(d3.polygonArea(poly)) : 1;
      if (area < bestArea) { bestArea = area; best = h; }
    }
  }
  return best;
}
function segDist(p, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const l2 = dx * dx + dy * dy;
  let t = l2 ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2 : 0;
  t = Math.max(0, Math.min(1, t));
  return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy);
}

const zoom = d3.zoom()
  .scaleExtent([.06, 14])
  .filter(ev => {
    if (ev.type === 'mousedown' || ev.type === 'touchstart') return !ev.button && !pickNode(...evXY(ev));
    return !ev.button;
  })
  .on('zoom', ev => {
    if (ev.sourceEvent) state.lastGesture = performance.now();
    state.t = ev.transform; requestDraw();
  });
const drag = d3.drag()
  .subject(ev => pickNode(...evXY(ev.sourceEvent || ev)))
  .on('start', ev => {
    if (!ev.subject) return;
    canvas.classList.add('dragging');
    if (state.mode === 'transport') { if (!ev.active) sim.alphaTarget(.25).restart(); }
  })
  .on('drag', ev => {
    if (!ev.subject) return;
    const [x, y] = state.t.invert(evXY(ev.sourceEvent));
    if (state.mode === 'computation') {   // no fx/fy here: a DAG coordinate must not pin the node in transport
      ev.subject.x = x; ev.subject.y = y; ev.subject.tx = x; ev.subject.ty = y; requestDraw();
    } else {
      ev.subject.fx = x; ev.subject.fy = y;
    }
  })
  .on('end', ev => {
    canvas.classList.remove('dragging');
    if (!ev.subject) return;
    if (state.mode === 'transport') { if (!ev.active) sim.alphaTarget(0); }
    renderInspector(); // pin state may show
  });
function evXY(ev) {
  const p = ev.touches?.[0] ?? ev.changedTouches?.[0] ?? ev;
  const r = canvas.getBoundingClientRect();
  return [p.clientX - r.left, p.clientY - r.top];
}
d3.select(canvas).call(drag).call(zoom).on('dblclick.zoom', null);

canvas.addEventListener('click', ev => {
  const [mx, my] = evXY(ev);
  const n = pickNode(mx, my);
  if (n) return select({ kind: 'node', id: n.id });
  const h = pickHyper(mx, my);
  if (h) return select({ kind: 'hyper', id: h.id });
  clearSelection();
});
canvas.addEventListener('dblclick', ev => {
  const n = pickNode(...evXY(ev));
  if (n) { n.fx = n.fy = null; if (state.mode === 'transport') sim.alpha(.2).restart(); renderInspector(); }
});
canvas.addEventListener('mousemove', ev => {
  const [mx, my] = evXY(ev);
  const n = pickNode(mx, my);
  const h = n ? null : pickHyper(mx, my);
  canvas.style.cursor = (n || h) ? 'pointer' : '';
  const tt = $('#tooltip');
  const prev = state.hover?.id;
  state.hover = n ? { kind: 'node', id: n.id } : h ? { kind: 'hyper', id: h.id } : null;
  if (state.hover?.id !== prev) requestDraw();
  if (n) {
    const tags = Object.entries(n.tags || {}).slice(0, 3).map(([k, v]) => `${k}=${v}`).join(' · ');
    tt.innerHTML = `<div class="tt-name">${esc(n.name)}</div><div class="tt-type">${esc(n.vis.label)} · ${esc(n.ns || '')}</div>${tags ? `<div class="tt-tags">${esc(tags)}</div>` : ''}`;
  } else if (h) {
    const conf = HYPER_TYPES[h.type] || {};
    tt.innerHTML = `<div class="tt-name">${esc(h.name)}</div><div class="tt-type">${esc(conf.label || h.type)} · ${h.members.length} members</div>`;
  }
  if (n || h) {
    tt.style.display = 'block';
    const mr = $('#main').getBoundingClientRect();
    tt.style.left = Math.min(mx + 16, mr.width - 270) + 'px';
    tt.style.top = (my + 14) + 'px';
  } else tt.style.display = 'none';
});
canvas.addEventListener('mouseleave', () => { $('#tooltip').style.display = 'none'; state.hover = null; requestDraw(); });

function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
const inNs = (ns, path) => ns === path || (ns || '').startsWith(path + '/');

/* ------------------------------------------------------ selection */
function select(sel) {
  state.selection = sel;
  state.isolate = false;
  renderInspector();
  syncTreeSel();
  requestDraw();
}
function clearSelection() {
  state.selection = null; state.isolate = false;
  renderInspector(); syncTreeSel(); requestDraw();
}

/* ------------------------------------------------------ fit / zoom */
function zoomToNodes(ns, dur = 550) {
  const pts = ns.filter(n => n.x != null);
  if (!pts.length) return;
  const x0 = d3.min(pts, n => n.x) - 90, x1 = d3.max(pts, n => n.x) + 90;
  const y0_ = d3.min(pts, n => n.y) - 90, y1 = d3.max(pts, n => n.y) + 90;
  const k = Math.min(2.5, .95 / Math.max((x1 - x0) / W, (y1 - y0_) / H));
  const tx = W / 2 - k * (x0 + x1) / 2, ty = H / 2 - k * (y0_ + y1) / 2;
  d3.select(canvas).transition().duration(dur)
    .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(k));
}
function fit() { zoomToNodes(model.nodes.filter(nodeVisible)); }
function scheduleFit(delay) {   // deferred fit that yields to any user gesture in the meantime
  const t0 = performance.now();
  setTimeout(() => { if (!state.lastGesture || state.lastGesture < t0) fit(); }, delay);
}

/* ========================================================== panels */
function buildLayersPanel() {
  const el = $('#layersPanel');
  el.innerHTML = '<h2>Layers</h2>';
  const counts = layerCounts();
  let lastGroup = null;
  LAYERS.forEach(l => {
    if (l.group !== lastGroup) {
      lastGroup = l.group;
      el.insertAdjacentHTML('beforeend', `<div class="lgroup">${l.group}</div>`);
    }
    const lab = document.createElement('label');
    lab.className = 'lrow';
    const sw = swatchFor(l.id);
    lab.innerHTML = `<input type="checkbox" ${state.layers.has(l.id) ? 'checked' : ''}>${sw}<span class="name">${l.name}</span><span class="cnt">${counts[l.id] ?? ''}</span>`;
    lab.querySelector('input').addEventListener('change', ev => {
      ev.target.checked ? state.layers.add(l.id) : state.layers.delete(l.id);
      requestDraw();
    });
    el.appendChild(lab);
  });
}
function layerCounts() {
  const c = {};
  model.nodes.forEach(n => c[n.vis.layer] = (c[n.vis.layer] || 0) + 1);
  model.hyperedges.forEach(h => { const l = HYPER_TYPES[h.type]?.layer; if (l) c[l] = (c[l] || 0) + 1; });
  return c;
}
function swatchFor(layerId) {
  const nt = Object.values(NODE_TYPES).find(t => t.layer === layerId);
  if (layerId === 'net') return `<span class="sw triangle" style="background:${NODE_TYPES.net.color}"></span>`;
  if (nt && layerId !== 'wl') return `<span class="sw ${cssShape(nt.glyph)}" style="background:${nt.color}"></span>`;
  if (layerId === 'wl') return `<span class="sw circle" style="background:${NODE_TYPES.workload.color}"></span>`;
  const ht = Object.values(HYPER_TYPES).find(t => t.layer === layerId);
  if (ht) return `<span class="sw circle" style="background:${hexA(ht.color, .5)};border:1px solid ${ht.color}"></span>`;
  return `<span class="sw circle" style="background:${MUTED}"></span>`;
}
const cssShape = g => ({ circle: 'circle', square: 'square', diamond: 'diamond', triangle: 'triangle', hex: 'hex', cyl: 'cyl', folder: 'folder' }[g] || 'circle');

function buildLegend() {
  const el = $('#legendPanel');
  el.innerHTML = '<h2>Legend</h2>';
  Object.entries(NODE_TYPES).forEach(([k, t]) => {
    el.insertAdjacentHTML('beforeend',
      `<div class="lrow"><span class="sw ${cssShape(t.glyph)}" style="background:${t.color}"></span><span class="name">${t.label}</span></div>`);
  });
  el.insertAdjacentHTML('beforeend', '<div class="lgroup">edges</div>');
  const edgeLeg = [['link', 'link'], ['tunnel', 'tunnel (wg)'], ['flow', 'flow'], ['dep', 'dependency'], ['nfs', 'storage i/o'], ['sched', 'scheduling']];
  edgeLeg.forEach(([k, name]) => {
    const t = EDGE_TYPES[k];
    const cls = t.dash ? (t.dash[0] <= 2 ? 'dot' : 'dash') : '';
    el.insertAdjacentHTML('beforeend',
      `<div class="lrow"><span class="line ${cls}" style="border-color:${hexA(t.color, Math.max(.65, t.alpha))}"></span><span class="name">${name}</span></div>`);
  });
  el.insertAdjacentHTML('beforeend', '<div class="lgroup">hyperedges</div>');
  Object.values(HYPER_TYPES).forEach(t => {
    el.insertAdjacentHTML('beforeend',
      `<div class="lrow"><span class="hull" style="background:${t.color}"></span><span class="name">${t.label}</span></div>`);
  });
  el.insertAdjacentHTML('beforeend', `<div class="lgroup">net roles (ring)</div>
    <div class="lrow"><span class="sw ring" style="border-color:${NODE_TYPES.net.color}"></span><span class="name">ingress — solid</span></div>
    <div class="lrow"><span class="sw ring" style="border-color:${NODE_TYPES.net.color};border-style:dashed"></span><span class="name">egress — dashed</span></div>
    <div class="lrow"><span class="sw ring" style="border-color:${NODE_TYPES.net.color};border-style:dotted"></span><span class="name">hop — dotted</span></div>
    <div class="lrow"><span class="sw ring" style="border-color:${NODE_TYPES.net.color};box-shadow:0 0 0 2.5px ${SURFACE},0 0 0 3.6px ${NODE_TYPES.net.color}"></span><span class="name">relay — double</span></div>
    <div class="lrow"><span class="sw diamond" style="background:${EDGE_TYPES.tunnel.color}"></span><span class="name">tunnel endpoint</span></div>`);
}

/* ------------------------------------------------------- ns tree */
function buildTree() {
  const root = { kids: new Map(), items: [] };
  const dirOf = path => {
    let d = root;
    for (const seg of path.split('/')) {
      if (!d.kids.has(seg)) d.kids.set(seg, { kids: new Map(), items: [], path: (d.path ? d.path + '/' : '') + seg });
      d = d.kids.get(seg);
    }
    return d;
  };
  model.nodes.forEach(n => {
    if (!n.ns) return;
    const d = dirOf(n.ns);
    if (n.type === 'ns') d.nsNode = n;
    else d.items.push(n);
  });
  const countAll = d => d.items.length + [...d.kids.values()].reduce((a, k) => a + countAll(k), 0);

  const el = $('#nstree');
  el.innerHTML = '<h2>Namespaces</h2>';
  const open = new Set(idx.clouds.map(c => c));
  const TYPE_ORDER = ['cluster', 'storage', 'net', 'hw', 'workload', 'pkg'];

  function renderDir(d, name, depth, container) {
    const row = document.createElement('div');
    row.className = 'trow'; row.dataset.path = d.path;
    const hasKids = d.kids.size > 0 || d.items.length > 0;
    row.innerHTML = `<span class="chev ${open.has(d.path) ? 'open' : ''}">${hasKids ? '▶' : ''}</span>
      <span class="sw folder" style="background:${NODE_TYPES.ns.color}"></span>
      <span>${esc(name)}</span><span class="cnt">${countAll(d)}</span>`;
    container.appendChild(row);
    const kidBox = document.createElement('div');
    kidBox.className = 'tkids' + (open.has(d.path) ? '' : ' hidden');
    container.appendChild(kidBox);
    row.querySelector('.chev').addEventListener('click', ev => {
      ev.stopPropagation();
      kidBox.classList.toggle('hidden');
      row.querySelector('.chev').classList.toggle('open');
    });
    row.addEventListener('click', () => {
      select({ kind: 'ns', path: d.path });
      zoomToNodes(model.nodes.filter(n => inNs(n.ns, d.path) && nodeVisible(n)));
    });
    [...d.kids.entries()].sort((a, b) => a[0].localeCompare(b[0]))
      .forEach(([nm, kid]) => renderDir(kid, nm, depth + 1, kidBox));
    d.items.sort((a, b) => TYPE_ORDER.indexOf(a.type) - TYPE_ORDER.indexOf(b.type) || a.name.localeCompare(b.name))
      .forEach(n => {
        const ir = document.createElement('div');
        ir.className = 'trow'; ir.dataset.nodeId = n.id;
        ir.innerHTML = `<span class="chev"></span><span class="sw ${cssShape(n.vis.glyph)}" style="background:${n.vis.color}"></span><span>${esc(n.name)}</span>`;
        ir.addEventListener('click', () => { select({ kind: 'node', id: n.id }); zoomToNodes([n]); });
        kidBox.appendChild(ir);
      });
  }
  [...root.kids.entries()].sort((a, b) => a[0].localeCompare(b[0]))
    .forEach(([nm, d]) => renderDir(d, nm, 0, el));

  // tenants section (identity-free by design: numbers, not names)
  const tens = model.hyperedges.filter(h => h.type === 'tenancy');
  if (tens.length) {
    el.insertAdjacentHTML('beforeend', '<h2 style="margin-top:12px">Tenants</h2>');
    tens.forEach(h => {
      const r = document.createElement('div');
      r.className = 'trow'; r.dataset.hyperId = h.id;
      r.innerHTML = `<span class="chev"></span><span class="sw ring" style="border-color:${HYPER_TYPES.tenancy.color}"></span><span>${esc(h.name)}</span><span class="cnt">${h.members.length}</span>`;
      r.addEventListener('click', () => {
        select({ kind: 'hyper', id: h.id });
        zoomToNodes(h.members.map(id => idx.nodeById.get(id)).filter(nodeVisible));
      });
      el.appendChild(r);
    });
  }
}
function syncTreeSel() {
  document.querySelectorAll('.trow.sel').forEach(e => e.classList.remove('sel'));
  const s = state.selection; if (!s) return;
  const sel = s.kind === 'node' ? `[data-node-id="${CSS.escape(s.id)}"]`
    : s.kind === 'hyper' ? `[data-hyper-id="${CSS.escape(s.id)}"]`
    : `[data-path="${CSS.escape(s.path)}"]`;
  document.querySelector(sel)?.classList.add('sel');
}

/* ------------------------------------------------------ inspector */
function renderInspector() {
  const el = $('#inspector');
  const s = state.selection;
  if (!s) { el.innerHTML = '<div class="empty">Select a node, hull, or namespace.</div>'; return; }
  const chip = (color, glyph, label) =>
    `<span class="chip"><span class="sw ${cssShape(glyph)}" style="background:${color}"></span>${esc(label)}</span>`;
  const tagRows = tags => Object.entries(tags || {}).map(([k, v]) =>
    `<tr><td>${esc(k)}</td><td>${esc(typeof v === 'string' ? v : JSON.stringify(v))}</td></tr>`).join('');

  if (s.kind === 'node') {
    const n = idx.nodeById.get(s.id); if (!n) return;
    const membs = (idx.hypersByNode.get(n.id) || []);
    const deg = (idx.adj.get(n.id) || []).length;
    const util = n.tags?.util;
    el.innerHTML = `
      ${chip(n.vis.color, n.vis.glyph, n.vis.label)}
      <h3>${esc(n.name)}</h3><div class="path">${esc(n.ns || '—')}</div>
      ${util != null ? `<div style="font-size:11px;color:var(--muted)">utilization ${(util * 100).toFixed(0)}%${util > .9 ? ' <b style="color:var(--s-crit)">▲ critical</b>' : ''}</div>
        <div class="util"><i style="width:${util * 100}%;background:${util > .9 ? CRIT : d3.interpolateRgb(SEQ_LO, SEQ_HI)(util)}"></i></div>` : ''}
      <table class="tags">${tagRows(n.tags)}<tr><td>degree</td><td>${deg}</td></tr>${n.fx != null ? '<tr><td>pinned</td><td>yes</td></tr>' : ''}</table>
      ${membs.length ? `<div class="lgroup">member of</div><div class="memb">${membs.map(h =>
        `<span class="chip" data-h="${esc(h.id)}"><span class="sw ring" style="border-color:${HYPER_TYPES[h.type]?.color || MUTED}"></span>${esc(h.name)}</span>`).join('')}</div>` : ''}
      <div class="irow">
        <button class="btn" id="iPin">${n.fx != null ? 'Unpin' : 'Pin'}</button>
        <button class="btn" id="iIso">${state.isolate ? 'Un-isolate' : 'Isolate'}</button>
        <button class="btn" id="iClr">Clear</button>
      </div>`;
    $('#iPin').onclick = () => {
      if (n.fx != null) { n.fx = n.fy = null; if (state.mode === 'transport') sim.alpha(.15).restart(); }
      else { n.fx = n.x; n.fy = n.y; }
      renderInspector();
    };
  } else if (s.kind === 'hyper') {
    const h = idx.hyperById.get(s.id); if (!h) return;
    const conf = HYPER_TYPES[h.type] || {};
    el.innerHTML = `
      ${chip(conf.color || MUTED, 'circle', conf.label || h.type)}
      <h3>${esc(h.name)}</h3><div class="path">${h.members.length} members</div>
      <table class="tags">${tagRows(h.tags)}</table>
      <div class="lgroup">members</div>
      <div class="memb">${h.members.slice(0, 40).map(id => {
        const n = idx.nodeById.get(id);
        return `<span class="chip" data-n="${esc(id)}"><span class="sw ${cssShape(n.vis.glyph)}" style="background:${n.vis.color}"></span>${esc(n.name)}</span>`;
      }).join('')}${h.members.length > 40 ? `<span class="chip">+${h.members.length - 40} more</span>` : ''}</div>
      <div class="irow"><button class="btn" id="iIso">${state.isolate ? 'Un-isolate' : 'Isolate'}</button>
      <button class="btn" id="iClr">Clear</button></div>`;
  } else if (s.kind === 'ns') {
    const members = model.nodes.filter(n => inNs(n.ns, s.path));
    const byType = d3.rollup(members, v => v.length, n => n.type);
    el.innerHTML = `
      ${chip(NODE_TYPES.ns.color, 'folder', 'namespace')}
      <h3>${esc(s.path.split('/').pop())}</h3><div class="path">${esc(s.path)}</div>
      <table class="tags">${[...byType.entries()].map(([t, c]) =>
        `<tr><td>${esc(NODE_TYPES[t]?.label || t)}</td><td>${c}</td></tr>`).join('')}</table>
      <div class="irow"><button class="btn" id="iIso">${state.isolate ? 'Un-isolate' : 'Isolate'}</button>
      <button class="btn" id="iClr">Clear</button></div>`;
  }
  el.querySelectorAll('[data-h]').forEach(c => c.addEventListener('click', () => select({ kind: 'hyper', id: c.dataset.h })));
  el.querySelectorAll('[data-n]').forEach(c => c.addEventListener('click', () => select({ kind: 'node', id: c.dataset.n })));
  const iso = $('#iIso'); if (iso) iso.onclick = () => { state.isolate = !state.isolate; renderInspector(); requestDraw(); };
  const clr = $('#iClr'); if (clr) clr.onclick = clearSelection;
}

/* ------------------------------------------------------- status */
function updateStatus() {
  if (!model) return;
  const vn = model.nodes.filter(nodeVisible).length;
  const ve = model.edges.filter(edgeVisible).length;
  const vh = model.hyperedges.filter(hyperVisible).length;
  $('#stCounts').textContent = `N ${vn}/${model.nodes.length} · E ${ve}/${model.edges.length} · H ${vh}/${model.hyperedges.length}`;
  $('#stZoom').textContent = `zoom ${(state.t.k * 100).toFixed(0)}%`;
  $('#stMode').textContent = `${state.mode} · ${state.hyperRender}s · seed ${state.seed}`;
  $('#stMatch').textContent = state.q ? `${state.matches.size} match${state.matches.size === 1 ? '' : 'es'}` : '';
}

/* ========================================================= controls */
$('#modeSeg').addEventListener('click', ev => {
  const b = ev.target.closest('button'); if (!b) return;
  setMode(b.dataset.mode);
});
function setMode(mode) {
  if (mode === state.mode) return;
  state.mode = mode;
  document.querySelectorAll('#modeSeg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
  // drop a selection that cannot render in the new projection (it would dim everything toward nothing)
  const s = state.selection;
  if (mode === 'computation' && s && (
    (s.kind === 'node' && !['pkg', 'storage', 'workload'].includes(idx.nodeById.get(s.id)?.type)) ||
    (s.kind === 'hyper' && idx.hyperById.get(s.id)?.type === 'mesh'))) clearSelection();
  if (mode === 'computation') {
    sim.stop();
    layoutDAG();
    startTween();
    setTimeout(() => zoomToNodes(model.nodes.filter(nodeVisible).map(n => ({ x: n.tx ?? n.x, y: n.ty ?? n.y }))), 60);
  } else {
    model.nodes.forEach(n => { n.sx = n.x; n.sy = n.y; n.tx = n.ty = null; });
    sim.alpha(.5).restart();
    scheduleFit(500);
  }
  requestDraw();
}
$('#hyperSeg').addEventListener('click', ev => {
  const b = ev.target.closest('button'); if (!b) return;
  state.hyperRender = b.dataset.hyper;
  document.querySelectorAll('#hyperSeg button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  requestDraw();
});
$('#fitBtn').addEventListener('click', fit);
$('#regenBtn').addEventListener('click', () => {
  state.seed = +$('#seed').value || 0;
  buildAll(generateEstate(state.seed));
  scheduleFit(650);
  toast(`regenerated estate · seed ${state.seed}`);
});
$('#loadBtn').addEventListener('click', () => $('#fileInput').click());
$('#fileInput').addEventListener('change', async ev => {
  const f = ev.target.files[0]; if (!f) return;
  try {
    const j = JSON.parse(await f.text());
    const m = (j.Pkgs && j.Wlds) ? importD9(j)
      : (Array.isArray(j.nodes)) ? { nodes: j.nodes, edges: j.edges || [], hyperedges: j.hyperedges || [], clouds: j.clouds }
      : null;
    if (!m) throw new Error('unrecognized schema — expected {nodes,edges,hyperedges} or d9 {Pkgs,Wlds}');
    buildAll(m);
    scheduleFit(650);
    toast(`loaded ${f.name}: ${m.nodes.length} nodes · ${m.edges.length} edges · ${m.hyperedges.length} hyperedges`);
  } catch (err) {
    toast(`✗ ${f.name}: ${err.message}`, 6000);
  }
  ev.target.value = '';
});
$('#pngBtn').addEventListener('click', () => {
  canvas.toBlob(b => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(b);
    a.download = `entities-${state.mode}-seed${state.seed}.png`;
    a.click();
    URL.revokeObjectURL(a.href);
  });
});
$('#helpBtn').addEventListener('click', () => $('#help').style.display = 'block');
$('#helpClose').addEventListener('click', () => $('#help').style.display = 'none');
$('#help').addEventListener('click', ev => { if (ev.target.id === 'help') $('#help').style.display = 'none'; });

$('#search').addEventListener('input', ev => {
  state.q = ev.target.value.trim().toLowerCase();
  state.matches = new Set();
  if (state.q) {
    model.nodes.forEach(n => {
      const hay = (n.name + ' ' + (n.ns || '') + ' ' + Object.values(n.tags || {}).join(' ')).toLowerCase();
      if (hay.includes(state.q)) state.matches.add(n.id);
    });
  }
  requestDraw();
});
$('#search').addEventListener('keydown', ev => {
  if (ev.key === 'Enter' && state.matches.size) {
    zoomToNodes([...state.matches].map(id => idx.nodeById.get(id)).filter(nodeVisible));
  }
  if (ev.key === 'Escape') { ev.target.value = ''; state.q = ''; state.matches = new Set(); ev.target.blur(); requestDraw(); }
});
window.addEventListener('keydown', ev => {
  if (ev.target.tagName === 'INPUT') return;
  if (ev.key === 'Escape') {
    if ($('#help').style.display === 'block') return void ($('#help').style.display = 'none');
    clearSelection();
  }
  if (ev.key === 'f' || ev.key === 'F') fit();
  if (ev.key === '?') $('#help').style.display = $('#help').style.display === 'block' ? 'none' : 'block';
});

/* ============================================================ boot */
window.Workbench = {
  load: m => { buildAll(m); scheduleFit(650); },
  importD9: j => { const m = importD9(j); buildAll(m); scheduleFit(650); return m; },
  select, clearSelection, fit, zoomToNodes, setMode,
  get model() { return model; },
  get state() { return state; },
  get indexes() { return idx; },
};
if (!window.d3) {
  document.body.innerHTML = '<p style="padding:2em;font-family:sans-serif">d3.v7.min.js not found next to index.html.</p>';
} else {
  resize();
  buildAll(generateEstate(state.seed));
  scheduleFit(800);
}
