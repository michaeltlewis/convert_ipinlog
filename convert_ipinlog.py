import sys
import re
import socket
import argparse


def main():
    name_cache = resolver()

    args = parse_args()
    if args.hosts is not None:
        name_cache.preload_cache_with_hosts(args.hosts)

    if args.infile == '-':
        infile = sys.stdin
    else:
        infile = open(args.infile, 'r')

    for line in infile:
        newline = replace_ip_with_nameip(line, args.replacement, name_cache)
        sys.stdout.write(newline)

    infile.close()

def parse_args():
    parser = argparse.ArgumentParser(description='convert IP addresses in stdin to DNS names)')
    parser.add_argument('--hosts', help='file in host file format')
    parser.add_argument('--infile', '-i', default='-', help='input filename (defaults to stdin)')
    parser.add_argument('--replacement', help='replacement pattern (defaults to "{hostname}[{ip}]")')
    return parser.parse_args()

class resolver:
    ip_name_cache = dict()
    def get_name_for_ip(self, ip):
        try:
            cached_name = self.ip_name_cache[ip]
            return cached_name
        except:
            try:
                name = socket.gethostbyaddr(ip)[0]
                self.ip_name_cache[ip] = name
                return name
            except:
                self.ip_name_cache[ip] = None
                return None

    def preload_cache_with_hosts(self, hostfile):
        with open(hostfile, "r") as f:
            for line in f:
                match = re.search("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+(\S+)", line)
                if match is not None:
                    self.ip_name_cache[match.group(1)] = match.group(2)


def get_hostname_from_fqdn(fqdn):
    return fqdn.split('.')[0]


ip_regex = re.compile("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
def replace_ip_with_nameip(line, replacement_pattern, name_cache):

    lastmatch = None
    global ip_regex

    for match in ip_regex.finditer(line):
        ip = match.group(1)
        fqdn = name_cache.get_name_for_ip(ip)
        if fqdn is None:
            continue
        hostname = get_hostname_from_fqdn(fqdn)

        if replacement_pattern is None:
            replacement_pattern = "{hostname}[{ip}]"

        replacement = replacement_pattern.format(hostname=hostname, fqdn=fqdn, ip=ip)

        if lastmatch is None:
            newline = line[ 0 : match.start()] + replacement
        else:
            newline += line[lastmatch.end() : match.start()] + replacement

        lastmatch = match
    if lastmatch is None:
        return line
    else:
        newline += line[lastmatch.end():]
        return newline


main()

