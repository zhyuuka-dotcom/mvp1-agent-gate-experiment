Now let me look at the tests and repro files to understand conventions.

RUN ls repro/ && echo "---ACCESS---" && cat repro/access.log && echo "---COMBINED---" && cat repro/combined.log && echo "---CONF---" && cat repro/nginx.conf && echo "---MULTI---" && cat repro/nginx_multiline.conf

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">ls repro/ && echo "---ACCESS---" && cat repro/access.log && echo "---COMBINED---" && cat repro/combined.log && echo "---CONF---" && cat repro/nginx.conf && echo "---MULTI---" && cat repro/nginx_multiline.conf</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
