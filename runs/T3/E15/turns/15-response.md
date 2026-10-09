Now I have exact short lines. Note `self.conn` is at line 441, not 397. Let me find the Summary query lines with avg_bytes_sent too.

RUN grep -n "avg(bytes_sent)" ngxtop/ngxtop.py && grep -n "AS count," ngxtop/ngxtop.py | head -2

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n "avg(bytes_sent)" ngxtop/ngxtop.py | head && echo "---exact lines---" && sed -n '91p;100p' ngxtop/ngxtop.py | cat -A | head</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
