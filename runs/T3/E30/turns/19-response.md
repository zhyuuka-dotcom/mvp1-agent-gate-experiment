"ok 2" — the class was inserted (Median appears twice). But I expected 3 occurrences (class def + create_aggregate 'Median' = 2 actually, since query uses 'median' lowercase). So 2 is correct. Let me verify all three edits landed.

RUN grep -n "Median\|median\|create_aggregate" ngxtop/ngxtop.py

Send.
