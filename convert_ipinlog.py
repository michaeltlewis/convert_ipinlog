import sys
import re
import collections
import socket

def main():
    for line in sys.stdin:
        newline = replace_ip_with_nameip(line)
        sys.stdout.write(newline)

ip_name_cache = dict()
def get_name_for_ip(ip):
    global ip_name_cache
    try:
        cached_name = ip_name_cache[ip]
        return cached_name
    except:
        try:
            name = socket.gethostbyaddr(ip)[0]
            ip_name_cache[ip] = name
            return name
        except:
            ip_name_cache[ip] = None
            return None

ip_regex = re.compile("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
def replace_ip_with_nameip(line):
    lastmatch = None
    global ip_regex

    for match in ip_regex.finditer(line):
        ip = match.group(1)
        name = get_name_for_ip(ip)
        if name is None:
            continue

        replacement = "{}[{}]".format(name, ip)

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
