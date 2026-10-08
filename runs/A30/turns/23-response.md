The original file ended with `if __name__ == '__main__': unittest.main()`. My append put the new class after that block, which means it won't run under `python -m unittest` but pytest will still collect it. Let me check the file's tail and fix ordering.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">tail -20 tests/test_config_parser.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
