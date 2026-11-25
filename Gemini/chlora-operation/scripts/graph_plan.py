#!/usr/bin/env python3
"""Offline Graph recipe planning; opt-in execution through one MCP stdio client."""
import argparse
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import stat
import subprocess
import sys
import time

BIND = ('instanceId', 'bindingGeneration', 'graphTopology', 'graphLifetime')
BUILTIN_KINDS = ('bundle', 'fanout', 'router', 'channel', 'lfo',
                 'nebula', 'spectrogram', 'lfespectrum')
SIZED_BUILTINS = ('router', 'channel', 'nebula', 'spectrogram', 'lfespectrum')


def default_adapter():
    env = os.environ.get('CHLORA_MCP_ADAPTER')
    if env:
        return env
    for candidate in (Path.cwd() / 'tools/chlora_mcp.py',
                      Path(__file__).resolve().parents[4] / 'tools/chlora_mcp.py'):
        if candidate.is_file():
            return str(candidate)
    which_clara = shutil.which('clara')
    if which_clara:
        return which_clara
    apps = sorted(
        [*Path.home().glob('Desktop/Chlora*.app/Contents/Helpers/clara'),
         *Path('/Applications').glob('Chlora*.app/Contents/Helpers/clara')],
        key=lambda p: p.stat().st_mtime if p.exists() else 0,
        reverse=True,
    )
    if apps:
        return str(apps[0])
    return str(Path.cwd() / 'tools/chlora_mcp.py')


def binding(state):
    return {k: state.get('activeInstanceId') if k == 'instanceId' and
            'activeInstanceId' in state else state[k] for k in BIND}


def nodes(state):
    return {str(n['nodeKey']): n for n in state.get('nodes', state.get('graphNodes', []))}


def wires(state):
    ns = state.get('nodes', state.get('graphNodes', []))
    index = {n.get('index'): str(n['nodeKey']) for n in ns}
    out = []
    for raw in state.get('wires', state.get('graphWires', [])):
        w = dict(raw)
        w['sourceNodeKey'] = str(w.get('sourceNodeKey', index.get(w.get('from'))))
        w['destinationNodeKey'] = str(w.get('destinationNodeKey', index.get(w.get('to'))))
        out.append(w)
    return out


def edge_id(w):
    return (w['sourceNodeKey'], w['destinationNodeKey'], w.get('fromCh', 0),
            w.get('toCh', 0), bool(w.get('isBundle')), w.get('snakeBranch', 0),
            w.get('snakeInputBranch', 0), w.get('fromRole', 'main'),
            w.get('toRole', 'main'), w.get('bundleWidth', 1) if w.get('isBundle') else 1)


def step(tool, arguments, capture=None):
    row = {'tool': 'chlora_graph_' + tool, 'arguments': arguments}
    if capture:
        row['capture'] = capture
    return row


def disconnect(w):
    if w.get('fromRole', 'main') != 'main' or w.get('toRole', 'main') != 'main':
        wire = {
            'sourceNodeKey': w['sourceNodeKey'],
            'destinationNodeKey': w['destinationNodeKey'],
            'fromRole': w.get('fromRole', 'main'),
            'fromCh': w.get('fromCh', 0),
            'toRole': w.get('toRole', 'sidechain'),
            'toCh': w.get('toCh', 0),
            'isBundle': bool(w.get('isBundle', False)),
        }
        if wire['isBundle']:
            wire.update(bundleWidth=w['bundleWidth'],
                        snakeBranch=w.get('snakeBranch', 0),
                        snakeInputBranch=w.get('snakeInputBranch', 0))
        return step('delete_selection', {
            'nodeKeys': [], 'groupIds': [], 'commentIds': [], 'wires': [wire]
        })
    a = {k: w[k] for k in ('sourceNodeKey', 'destinationNodeKey')}
    if w.get('isBundle'):
        a.update(sourceBranch=w.get('snakeBranch', 0),
                 destinationBranch=w.get('snakeInputBranch', 0))
        return step('disconnect_snake', a)
    a.update(sourceChannel=w.get('fromCh', 0), destinationChannel=w.get('toCh', 0))
    return step('disconnect_channel', a)


def plan(state, spec):
    """Components compose in order. Explicit steps cover less common native operations."""
    result = {'version': 1, 'expectedBinding': binding(state), 'steps': [], 'checks': []}
    ns, existing = nodes(state), wires(state)
    approved = spec.get('replaceEdges', [])
    approved_ids = {edge_id(w) for w in approved}
    if not approved_ids <= {edge_id(w) for w in existing}:
        raise ValueError('replaceEdges must match current exact wires')
    result['steps'].extend(disconnect(w) for w in approved)
    cleared = approved_ids
    for c in spec['components']:
        kind, name = c['recipe'], c.get('name', 'component')
        x, y = c.get('x', 0), c.get('y', 0)
        if kind == 'subset':
            selected = c['channels']
            if not selected or len(set(selected)) != len(selected) or selected != sorted(selected):
                raise ValueError('subset channels must be nonempty, unique, and ascending (native order)')
            for side, owner in [('output', c['source']), ('input', c['destination'])]:
                n = ns[owner]
                if n.get('snakeWrapped') and not n.get('isRouter'):
                    raise ValueError('PortSnake owner must be unwrapped or a native Router')
                width = n['mainOut' if side == 'output' else 'mainIn']
                if any(type(ch) is not int or not 0 <= ch < width for ch in selected):
                    raise ValueError('subset channel outside owner bus')
                for w in existing:
                    key = 'sourceNodeKey' if side == 'output' else 'destinationNodeKey'
                    start = w.get('fromCh' if side == 'output' else 'toCh', 0)
                    span = w.get('bundleWidth', 1) if w.get('isBundle') else 1
                    if w[key] == owner and set(range(start, start + span)) & set(selected):
                        if edge_id(w) not in cleared:
                            raise ValueError('occupied PortSnake: approve exact replaced edge first')
                result['steps'].append(step('create_port_snake', dict(ownerNodeKey=owner,
                    direction=side, channels=selected, x=x, y=y), name + '_' + side))
            result['checks'].append({'subsetWidth': len(selected), 'channelOrder': selected,
                'source': c['source'], 'destination': c['destination']})
        elif kind == 'stack':
            count, width = c['count'], c['width']
            if (type(count) is not int or not 1 <= count <= 128
                    or type(width) is not int or width not in (1, 2)):
                raise ValueError('Stack requires 1..128 mono or stereo lanes')
            if count * width > 128:
                raise ValueError('Stack aggregate exceeds supported width')
            if c.get('pluginPath') and c.get('pluginUid'):
                raise ValueError('Stack accepts either pluginPath or pluginUid, not both')
            result['steps'].append(step('create_stack', dict(count=count, width=width, x=x, y=y), name))
            if c.get('pluginPath'):
                result['steps'].append(step('load_stack_file',
                    {'groupId': '$' + name + '.groupId', 'pluginPath': c['pluginPath']}))
            elif c.get('pluginUid'):
                result['steps'].append(step('load_stack',
                    {'groupId': '$' + name + '.groupId', 'pluginUid': c['pluginUid']}))
            result['checks'].append({'stack': name, 'aggregateWidth': count * width,
                'namesAvailable': None,
                'namesReadback': 'get_view_preferences after routing'})
        elif kind == 'builtin':
            builtin = c['kind']
            if builtin == 'merge':
                if 'channels' not in c:
                    raise ValueError('Merge creation requires its path width')
                a = dict(channels=c['channels'], inputs=c.get('inputs', 2), x=x, y=y)
                result['steps'].append(step('add_merge', a, name))
            elif builtin == 'ir':
                if 'channels' in c:
                    raise ValueError('add_ir uses native linked I/O width; adjust width via set_ir_empty_channels/set_ir_channels')
                result['steps'].append(step('add_ir', dict(x=x, y=y), name))
            elif builtin == 'levelmeter':
                a = dict(action='add', x=x, y=y)
                if 'channels' in c:
                    a['channels'] = c['channels']
                if 'groupId' in c:
                    a['groupId'] = c['groupId']
                result['steps'].append(step('level_meter', a, name))
            elif builtin in ('stack', 'stack_v2'):
                a = dict(action='add', x=x, y=y)
                if 'channels' in c:
                    a['channels'] = c['channels']
                if 'groupId' in c:
                    a['groupId'] = c['groupId']
                result['steps'].append(step('stack_control', a, name))
            elif builtin in BUILTIN_KINDS:
                if 'channels' in c and builtin not in SIZED_BUILTINS:
                    raise ValueError(f'{builtin} add_builtin does not accept channels')
                if builtin == 'router' and 'channels' not in c:
                    raise ValueError('Router creation requires channels')
                a = dict(kind=builtin, x=x, y=y)
                if 'channels' in c:
                    a['channels'] = c['channels']
                result['steps'].append(step('add_builtin', a, name))
            else:
                raise ValueError('builtin kind unsupported; use its specific native recipe/tool')
        elif kind == 'series':
            source = c['source']
            for endpoint, bus in ((source, 'mainOut'), (c['destination'], 'mainIn')):
                if endpoint in ns and ns[endpoint][bus] != c['channels']:
                    raise ValueError('series endpoint bus width mismatch')
            for endpoint in (source, c['destination']):
                if endpoint in ns and not ns[endpoint].get('snakeWrapped'):
                    raise ValueError('series endpoints must already be wrapped; plan approved wrap separately')
            has_paths, has_uids = bool(c.get('pluginPaths')), bool(c.get('pluginUids'))
            if has_paths == has_uids:
                raise ValueError('series requires either nonempty pluginPaths or nonempty pluginUids')
            step_x = c.get('stepX', 600)
            items = c['pluginPaths'] if has_paths else c['pluginUids']
            for i, target in enumerate(items):
                alias = name + str(i)
                if has_paths:
                    result['steps'].append(step('add_plugin_file', dict(pluginPath=target,
                        channels=c['channels'], x=x+i*step_x, y=y), alias))
                else:
                    result['steps'].append(step('add_plugin', dict(pluginUid=target,
                        channels=c['channels'], x=x+i*step_x, y=y), alias))
                node = '$' + alias + '.nodeKey'
                result['steps'].append(step('set_snake', {'nodeKey': node, 'wrapped': True}))
                result['steps'].append(step('connect_snake', dict(sourceNodeKey=source,
                    destinationNodeKey=node, sourceBranch=0, destinationBranch=0)))
                source = node
            result['steps'].append(step('connect_snake', dict(sourceNodeKey=source,
                destinationNodeKey=c['destination'], sourceBranch=0, destinationBranch=0)))
            result['checks'].append({'seriesWidth': c['channels'],
                'precondition': 'existing endpoints already wrapped; approved removed edges only'})
        elif kind == 'insert_on_wire':
            has_plugins = 'plugins' in c
            has_node = 'nodeKey' in c
            if has_plugins == has_node:
                raise ValueError('insert_on_wire requires either plugins list or existing detached nodeKey')
            src_key = c['source']
            src_ch = c.get('sourceChannel', 0)
            dst_key = c['destination']
            dst_ch = c.get('destinationChannel', 0)
            if has_plugins:
                plugins = c['plugins']
                if not isinstance(plugins, list) or not plugins:
                    raise ValueError('insert_on_wire plugins must be a nonempty list')
                if len(plugins) == 1:
                    item = plugins[0]
                    has_uid = bool(item.get('pluginUid'))
                    has_path = bool(item.get('pluginPath'))
                    if has_uid == has_path:
                        raise ValueError('insert_on_wire plugin requires exactly one of pluginUid or pluginPath')
                    alias = item.get('name', name + '0')
                    a = dict(
                        sourceNodeKey=src_key,
                        sourceChannel=src_ch,
                        destinationNodeKey=dst_key,
                        destinationChannel=dst_ch,
                        channels=item['channels'],
                        x=item.get('x', x),
                        y=item.get('y', y),
                    )
                    if has_uid:
                        a['pluginUid'] = item['pluginUid']
                    else:
                        a['pluginPath'] = item['pluginPath']
                    if 'groupId' in item:
                        a['groupId'] = item['groupId']
                    elif 'groupId' in c:
                        a['groupId'] = c['groupId']
                    result['steps'].append(step('insert_plugin_on_wire', a, alias))
                else:
                    aliases = []
                    for i, item in enumerate(plugins):
                        has_uid = bool(item.get('pluginUid'))
                        has_path = bool(item.get('pluginPath'))
                        if has_uid == has_path:
                            raise ValueError('insert_on_wire plugin requires exactly one of pluginUid or pluginPath')
                        alias = item.get('name', name + str(i))
                        aliases.append((alias, item))
                        if has_uid:
                            result['steps'].append(step('add_plugin', dict(
                                pluginUid=item['pluginUid'],
                                channels=item['channels'],
                                x=item.get('x', x),
                                y=item.get('y', y),
                            ), alias))
                        else:
                            result['steps'].append(step('add_plugin_file', dict(
                                pluginPath=item['pluginPath'],
                                channels=item['channels'],
                                x=item.get('x', x),
                                y=item.get('y', y),
                            ), alias))
                        node_ref = '$' + alias + '.nodeKey'
                        result['steps'].append(step('set_snake', {'nodeKey': node_ref, 'wrapped': False}))
                        gid = item.get('groupId', c.get('groupId'))
                        if gid is not None:
                            result['steps'].append(step('set_node_group', {'nodeKey': node_ref, 'groupId': gid}))
                    span_width = int(aliases[0][1]['channels'])
                    for offset in range(span_width):
                        result['steps'].append(step('disconnect_channel', dict(
                            sourceNodeKey=src_key,
                            sourceChannel=src_ch + offset,
                            destinationNodeKey=dst_key,
                            destinationChannel=dst_ch + offset,
                        )))
                    prev_key, prev_ch = src_key, src_ch
                    for alias, item in aliases:
                        node_ref = '$' + alias + '.nodeKey'
                        result['steps'].append(step('connect_bus', dict(
                            sourceNodeKey=prev_key,
                            destinationNodeKey=node_ref,
                            sourceChannel=prev_ch,
                            destinationChannel=0,
                            channels=item['channels'],
                            replaceExisting=True,
                        )))
                        prev_key, prev_ch = node_ref, 0
                    result['steps'].append(step('connect_bus', dict(
                        sourceNodeKey=prev_key,
                        destinationNodeKey=dst_key,
                        sourceChannel=0,
                        destinationChannel=dst_ch,
                        channels=aliases[-1][1]['channels'],
                        replaceExisting=True,
                    )))
            else:
                a = dict(
                    action='insertNodeOnWire',
                    nodeKey=c['nodeKey'],
                    sourceNodeKey=src_key,
                    sourceChannel=src_ch,
                    destinationNodeKey=dst_key,
                    destinationChannel=dst_ch,
                    x=x,
                    y=y,
                )
                if 'groupId' in c:
                    a['groupId'] = c['groupId']
                result['steps'].append(step('node_advanced', a, name if 'name' in c else None))
        elif kind == 'group':
            groups = {g['id']: g for g in state.get('groups', state.get('graphGroups', []))}
            if any(groups[i].get('stackCount', 0) for i in c['arguments'].get('childGroupIds', [])):
                raise ValueError('regular Group cannot contain a Stack')
            result['steps'].append(step('create_group', c['arguments'], name))
        elif kind == 'steps':
            result['steps'].extend(c['steps'])
        else:
            raise ValueError('recipe unsupported; compose documented explicit native steps: ' + kind)
    return result


def layout(geometry, node_keys, origin=(0, 0), gap=240):
    """Complete loose-node inventory only; place envelopes, preserve anchors."""
    from graph_layout import geometry_document, row_rows
    _, items = geometry_document(geometry)
    rows = row_rows(items, node_keys, origin, gap)
    return [step('move_node', row) for row in rows]


def resolve(value, captures, state):
    if isinstance(value, str) and value.startswith('$'):
        path = value[1:].split('.')
        current = captures[path.pop(0)]
        for k in path:
            current = current[int(k)] if isinstance(current, list) else current[k]
        return current
    if isinstance(value, dict):
        return {k: resolve(v, captures, state) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve(v, captures, state) for v in value]
    return value


def validate(value, schema):
    """Validate the adapter's JSON Schema subset; Host remains final capability gate."""
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool,
             'integer': int, 'number': (int, float)}
    if kind in types and (not isinstance(value, types[kind]) or
                          kind in ('integer', 'number') and isinstance(value, bool)):
        raise ValueError('schema type mismatch: ' + kind)
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError('schema enum mismatch')
    if kind == 'object':
        if set(schema.get('required', [])) - value.keys():
            raise ValueError('missing required arguments')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False and value.keys() - props.keys():
            raise ValueError('unknown arguments')
        for k, v in value.items():
            if k in props:
                validate(v, props[k])
    elif kind == 'array':
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', float('inf')):
            raise ValueError('array size outside schema')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise ValueError('duplicate array items')
        for v in value:
            validate(v, schema.get('items', {}))
    elif kind == 'string':
        if not schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', float('inf')):
            raise ValueError('string length outside schema')
        if schema.get('pattern') and not re.search(schema['pattern'], value):
            raise ValueError('string pattern mismatch')
    elif kind in ('integer', 'number'):
        if not schema.get('minimum', -float('inf')) <= value <= schema.get('maximum', float('inf')):
            raise ValueError('number outside schema')


class Client:
    def __init__(self, socket, transcript, adapter, timeout=30):
        self.log = Path(transcript).open('x')
        self.err = Path(str(transcript) + '.stderr').open('x')
        self.p = None
        self.sel = selectors.DefaultSelector()
        self.seq, self.timeout = 0, timeout
        try:
            adapter_str = str(adapter)
            cmd = ([sys.executable, adapter_str, '--socket', socket, '--profile', 'full']
                   if adapter_str.endswith('.py') else
                   [adapter_str, 'mcp', 'serve', '--stdio', '--socket', socket, '--profile', 'full'])
            self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self.err, text=True, bufsize=1)
            self.sel.register(self.p.stdout, selectors.EVENT_READ)
            self.rpc('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': 'chlora-graph-plan', 'version': '1'}})
            self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
            definitions = self.rpc('tools/list', {})['tools']
            self.schemas = {t['name']: t['inputSchema'] for t in definitions}
            self.read_only = {t['name'] for t in definitions
                              if t.get('annotations', {}).get('readOnlyHint')}
        except BaseException:
            self.close()
            raise

    def send(self, message):
        self.record('request', message)
        self.p.stdin.write(json.dumps(message) + '\n')
        self.p.stdin.flush()

    def record(self, direction, message):
        self.log.write(json.dumps(dict(time_ns=time.time_ns(), direction=direction, message=message))+'\n')
        self.log.flush()

    def rpc(self, method, params):
        self.seq += 1
        self.send(dict(jsonrpc='2.0', id=self.seq, method=method, params=params))
        deadline = time.monotonic() + self.timeout
        while self.sel.select(max(0, deadline-time.monotonic())):
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError('adapter exited; outcome unknown, no replay')
            r = json.loads(line)
            self.record('response', r)
            if 'id' not in r:
                continue
            if r['id'] != self.seq or 'error' in r:
                raise RuntimeError(r)
            return r['result']
        raise TimeoutError('outcome unknown; stop, never replay a write')

    def tool(self, name, arguments):
        validate(arguments, self.schemas[name])
        r = self.rpc('tools/call', {'name': name, 'arguments': arguments})
        if r.get('isError') or 'structuredContent' not in r:
            raise RuntimeError(r)
        return r['structuredContent']

    def close(self):
        if self.p:
            self.p.stdin.close()
            try:
                self.p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.p.terminate()
                try:
                    self.p.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.p.kill()
                    self.p.wait(timeout=3)
            self.p.stdout.close()
        self.sel.close()
        self.log.close()
        self.err.close()


def execute(client, p, operation_timeout=120):
    state = client.tool('chlora_graph_get_summary', {})
    if binding(state) != p['expectedBinding'] or state.get('pendingPluginLoads', 0):
        raise ValueError('planned session identity/topology changed or load pending; replan')
    captures = {}
    session_controls = False
    for row in p['steps']:
        args = resolve(row['arguments'], captures, state)
        schema = client.schemas[row['tool']]
        props = schema.get('properties', {})
        if 'graphTopology' in props:
            args.update(binding(state))
        elif 'instanceId' in props:
            current = binding(state)
            args.update({k: v for k, v in current.items() if k in props})
            session_controls = True
        if 'channelLayoutToken' in props and 'channelLayoutToken' not in args:
            state = client.tool('chlora_get_state', {})
            if binding(state)['instanceId'] != p['expectedBinding']['instanceId']:
                raise ValueError('session changed before layout-dependent step')
            current = binding(state)
            args.update({k: v for k, v in current.items() if k in props})
            args['channelLayoutToken'] = state['channelLayoutToken']
        # No implicit session switching, undo, write retry, or automatic recovery.
        r = client.tool(row['tool'], args)
        if row['tool'] in ('chlora_undo', 'chlora_redo'):
            deadline = time.monotonic() + operation_timeout
            while r.get('stateRestoreInFlight'):
                if time.monotonic() >= deadline:
                    raise TimeoutError('stateRestoreInFlight did not clear after undo/redo')
                time.sleep(.1)
                r = client.tool('chlora_get_state', {})
        if all(k in r for k in BIND[1:]):
            if binding(r)['instanceId'] != p['expectedBinding']['instanceId']:
                raise ValueError('session changed during operation')
            state = r
        detail = r.get('mcpResult', r)
        op = r.get('operationId') or detail.get('operationId')
        if op:
            deadline = time.monotonic() + operation_timeout
            while True:
                terminal = client.tool('chlora_get_operation', {'operationId': op})
                if terminal.get('status') in ('failed', 'cancelled'):
                    raise RuntimeError(terminal)
                if terminal.get('status') == 'succeeded':
                    res = terminal.get('result')
                    if isinstance(res, dict):
                        detail = dict(res)
                        if 'nodeKey' in terminal and 'nodeKey' not in detail:
                            detail['nodeKey'] = terminal['nodeKey']
                    else:
                        detail = terminal
                    if row['tool'] not in getattr(client, 'read_only', set()):
                        state = client.tool('chlora_graph_get_summary', {})
                    if binding(state)['instanceId'] != p['expectedBinding']['instanceId']:
                        raise ValueError('session changed during async operation')
                    break
                if time.monotonic() >= deadline:
                    raise TimeoutError('async outcome unresolved; no mutation replay')
                time.sleep(.2)
        elif ('graphTopology' in props and not all(k in r for k in BIND[1:])
              and row['tool'] not in getattr(client, 'read_only', set())):
            state = client.tool('chlora_graph_get_summary', {})
        if row.get('capture'):
            captures[row['capture']] = detail.get('mcpResult', detail)
            capture = captures[row['capture']]
            if isinstance(capture, dict) and 'groupId' in capture:
                group = next((g for g in state.get('groups', state.get('graphGroups', []))
                              if g['id'] == capture['groupId']), None)
                if group:
                    index_to_key = {n['index']: str(n['nodeKey']) for n in
                                    state.get('graphNodes', state.get('nodes', []))
                                    if 'index' in n}
                    for fanout in group.get('fanouts', []):
                        key = fanout.get('nodeKey')
                        if key is None:
                            key = index_to_key[fanout['node']]
                        capture[fanout['side'] + 'NodeKey'] = str(key)
    final_tool = 'chlora_get_state' if session_controls else 'chlora_graph_get_summary'
    final_state = client.tool(final_tool, {})
    if binding(final_state)['instanceId'] != p['expectedBinding']['instanceId']:
        raise ValueError('session changed before final readback')
    return {'state': final_state, 'captures': captures,
            'plannedChecks': p.get('checks', []), 'verification': 'readback available; assess requested topology'}


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--state'); a.add_argument('--spec'); a.add_argument('--output', required=True)
    a.add_argument('--apply', metavar='PLAN'); a.add_argument('--socket')
    a.add_argument('--socket-identity', help='exact current socket st_dev:st_ino')
    a.add_argument('--transcript')
    a.add_argument('--adapter', default=default_adapter())
    args = a.parse_args()
    if Path(args.output).exists():
        a.error('output must be unique')
    if args.apply:
        if not all((args.socket, args.socket_identity, args.transcript)) or not os.path.isabs(args.socket):
            a.error('--apply requires exact absolute socket, socket identity, and unique transcript')
        st = os.stat(args.socket)
        if not stat.S_ISSOCK(st.st_mode) or f'{st.st_dev}:{st.st_ino}' != args.socket_identity:
            a.error('socket identity mismatch')
        p = json.loads(Path(args.apply).read_text())
        client = Client(args.socket, args.transcript, args.adapter)
        try:
            result = execute(client, p)
        except BaseException as exc:
            Path(args.output).write_text(json.dumps({'status': 'stopped', 'error': str(exc),
                'transcript': args.transcript, 'writeReplay': False}, indent=2)+'\n')
            raise
        finally:
            client.close()
    else:
        if not args.state or not args.spec:
            a.error('offline planning requires --state and --spec')
        result = plan(json.loads(Path(args.state).read_text()), json.loads(Path(args.spec).read_text()))
    with Path(args.output).open('x') as f:
        json.dump(result, f, indent=2); f.write('\n')


if __name__ == '__main__':
    main()
