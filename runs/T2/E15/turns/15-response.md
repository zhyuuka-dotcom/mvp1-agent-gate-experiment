I need to check line lengths of my quotes and add cross-file references. Let me check actual line content.

RUN grep -n "running for" ngxtop/ngxtop.py

RUN grep -n "Summary:" ngxtop/ngxtop.py

RUN grep -n "args = docopt" ngxtop/ngxtop.py

RUN grep -n "default: combined" ngxtop/ngxtop.py

RUN grep -n "def report" ngxtop/ngxtop.py

RUN awk 'NR==453' ngxtop/ngxtop.py | wc -c

RUN awk 'NR==92' ngxtop/ngxtop.py | wc -c
