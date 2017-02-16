#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import collections
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

import psutil

AD = '-'
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
    }


def main():
    pid_num_of_connections_map = {}
    pid_connections_map = {}

    templ = '%-5s %-30s %-30s %-13s %-6s %s'
    print templ % (
        'Proto',
        'Local address',
        'Remote address',
        'Status',
        'PID',
        'Program name',
        )
    proc_names = {}
    for p in psutil.process_iter():
        try:
            proc_names[p.pid] = p.name()
        except psutil.Error:
            pass
    for c in psutil.net_connections(kind='inet'):
        print c

        if pid_num_of_connections_map.get(c.pid):
            connections = pid_num_of_connections_map[c.pid] + 1
            pid_num_of_connections_map[c.pid] = connections
        else:

            pid_num_of_connections_map[c.pid] = 1
        pid_connections_map.setdefault(c.pid, []).append(c)
    pid_connections_descending = \
        collections.OrderedDict(sorted(pid_num_of_connections_map.items(),
                                key=lambda (k, v): v, reverse=True))

    for pid in pid_connections_descending:
        for c in pid_connections_map[pid]:
            laddr = '%s:%s' % c.laddr
            raddr = ''
            if c.raddr:
                raddr = '%s:%s' % c.raddr
            print templ % (
                proto_map[(c.family, c.type)],
                laddr,
                raddr or AD,
                c.status,
                c.pid or AD,
                proc_names.get(c.pid, '?')[:15],
                )


if __name__ == '__main__':
    main()