#! /usr/bin/env python3
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent

"""
License
-------
(c) 2021 Klaus Zerwes zero-sys.net
This package is free software.
This software is licensed under the terms of the
GNU GENERAL PUBLIC LICENSE version 3 or later,
as published by the Free Software Foundation.
See https://www.gnu.org/licenses/gpl.html
"""

import json
import subprocess

pr = subprocess.run(
        ['configctl', 'interface gateways status'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

jo = json.loads(pr.stdout)
for gw in jo:
    ecode = 0
    status = 'OK'
    if gw['status'] != 'none':
        ecode = 2
        status = "ERROR"
    gwname = gw['name']
    for c in ['_', ' ']:
        gwname = gwname.replace(c, '-')
    perf = ''
    for p in ['loss', 'delay', 'stddev']:
        if perf:
            perf = '%s|' % perf
        perf = '%s%s=%s' % (perf, p, gw[p].split(' ')[0])
    txt = '%s (%s) : %s' % (gw['name'], gw['address'], gw['status_translated'])
    print('%s GWSTATUS-%s %s %s - %s' % (ecode, gwname, perf, status, txt))
