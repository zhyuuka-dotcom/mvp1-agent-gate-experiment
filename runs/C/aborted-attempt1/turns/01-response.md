I'll start by exploring the repository structure and reproducing the issue.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">ls -la && echo "---REPRO---" && ls -la repro/ 2>/dev/null && echo "---NGINXCONF---" && cat repro/nginx.conf 2>/dev/null && echo "---MULTILINE---" && cat repro/nginx_multiline.conf 2>/dev/null</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
