$ .venv/bin/python -m pytest tests/test_median.py -q
..F..                                                                    [100%]
=================================== FAILURES ===================================
______________________ test_median_aggregate_even_and_odd ______________________

    def test_median_aggregate_even_and_odd():
        from ngxtop.ngxtop import Median
    
        m = Median()
        for v in [10, 2, 8, 4]:
            m.step(v)
>       assert m.finalize() == 5.0  # (4 + 2) / 2? sorted [2,4,8,10] -> (4+8)/2 = 6.0
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
E       assert 6.0 == 5.0
E        +  where 6.0 = finalize()
E        +    where finalize = <ngxtop.ngxtop.Median object at 0x7f49b9888320>.finalize

tests/test_median.py:50: AssertionError
=============================== warnings summary ===============================
tests/test_median.py::test_median_aggregate_even_and_odd
  /tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:165: SyntaxWarning: invalid escape sequence '\S'
    name = re.findall('(<\S*?>)', source)[0]

tests/test_median.py::test_median_aggregate_even_and_odd
  /tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:166: SyntaxWarning: invalid escape sequence '\['
    value = re.findall('\[default: (.*)\]', source, flags=re.I)

tests/test_median.py::test_median_aggregate_even_and_odd
  /tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:207: SyntaxWarning: invalid escape sequence '\['
    matched = re.findall('\[default: (.*)\]', description, flags=re.I)

tests/test_median.py::test_median_aggregate_even_and_odd
  /tmp/t3e30/repo/.venv/lib/python3.12/site-packages/docopt.py:456: SyntaxWarning: invalid escape sequence '\S'
    split = re.split('\n *(<\S+?>|-\S+?)', doc)[1:]

tests/test_median.py::test_median_aggregate_even_and_odd
  /tmp/t3e30/repo/ngxtop/config_parser.py:29: PyparsingDeprecationWarning: 'setParseAction' deprecated - use 'set_parse_action'
    parameter = parameter | quotedString.setParseAction(removeQuotes)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_median.py::test_median_aggregate_even_and_odd - assert 6.0 ...
1 failed, 4 passed, 5 warnings in 0.81s

[exit code: 1]