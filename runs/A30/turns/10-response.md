So parsing works fine when given the actual format string. The issue is that `-f main` is treated as a literal format string "main". The user expects `-f main` to resolve the named format from the nginx config.

Let me check the README and how `-f` is documented to determine the correct fix.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n "log-format\|log_format\|-f \|-c \|config" README.rst | head -30; echo "=====DOC====="; sed -n '1,60p' ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
