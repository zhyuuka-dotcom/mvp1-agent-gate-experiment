$ 
grep -n "records processed\|Summary:\|def run_cli" tests/test_characterization.py | head; echo "==="; grep -n "result = tabulate" ngxtop/ngxtop.py; grep -n "print(processor.report())" ngxtop/ngxtop.py; grep -n "args = docopt" ngxtop/ngxtop.py
15:def run_cli(*args):
27:    assert "2 records processed" in r.stdout
28:    assert "Summary:" in r.stdout
43:    assert "Summary:" in r.stdout
===
467:                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
502:    print(processor.report())  # this will only run when start in --no-follow mode
609:    args = docopt(__doc__, version='xstat 0.1')

[exit code: 0]