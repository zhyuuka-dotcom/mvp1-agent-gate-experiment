$ grep -n "avg(bytes_sent)" ngxtop/ngxtop.py | head && echo "---exact lines---" && sed -n '91p;100p' ngxtop/ngxtop.py | cat -A | head
45:    $ ngxtop --order-by 'avg(bytes_sent) * count'
91:       avg(bytes_sent)                             AS avg_bytes_sent,
104:       avg(bytes_sent)                             AS avg_bytes_sent,
---exact lines---
       avg(bytes_sent)                             AS avg_bytes_sent,$
    ('Detailed:',$

[exit code: 0]