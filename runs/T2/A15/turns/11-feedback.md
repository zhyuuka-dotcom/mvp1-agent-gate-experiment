$ cat > /tmp/patch1.py << 'PYEOF'
import re
p = 'ngxtop/ngxtop.py'
s = open(p).read()

# 1. Add docopt option after the -a line
old = "    -a <exp> ..., --a <exp> ...  add exp (must be aggregation exp: sum, avg, min, max, etc.) into output\n"
new = old + "    --output-format <fmt>  output format for the default report: table or json [default: table]\n"
assert old in s, "docopt option anchor missing"
s = s.replace(old, new, 1)

# 2. Add VALID_OUTPUT_FORMATS constant after DEFAULT_FIELDS
old = "DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])\n"
new = old + "\nVALID_OUTPUT_FORMATS = ('table', 'json')\n"
assert old in s, "DEFAULT_FIELDS anchor missing"
s = s.replace(old, new, 1)

open(p,'w').write(s)
print("patched docopt + const")
PYEOF
.venv/bin/python /tmp/patch1.py && grep -n "output-format\|VALID_OUTPUT_FORMATS" ngxtop/ngxtop.py
patched docopt + const
23:    --output-format <fmt>  output format for the default report: table or json [default: table]
119:VALID_OUTPUT_FORMATS = ('table', 'json')

[exit code: 0]