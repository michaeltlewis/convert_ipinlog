# convert_ipinlog
Reads stdin and replaces any IPv4 address into a name[ip] by doing a reverse dns lookup, and writes the converted line to stdout.

Requires Python (v2.x or 3.x)

Example:

$ echo "some host 12.34.56.78 did something" | python convert_ipinlog.py

some host *testbox1[12.34.56.78]* did something
