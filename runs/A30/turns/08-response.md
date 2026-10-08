So `-f main` is treated as a literal format string. The user wants `main` to be looked up from the nginx config as a format name. Let me check the existing tests to understand expectations and conventions.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">cat tests/test_config_parser.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
