$ .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json </dev/null 2>/dev/null | .venv/bin/python -c "import sys,json; d=json.load(sys.stdin); print(sorted(d.keys())); print(sorted(d['summary'].items())); print(sorted(d['detailed'], key=lambda x: x['request_path']))"

[stderr]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/z/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12/json/__init__.py", line 293, in load
    return loads(fp.read(),
           ^^^^^^^^^^^^^^^^
  File "/home/z/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/z/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12/json/decoder.py", line 338, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/z/.local/share/uv/python/cpython-3.12.14-linux-x86_64-gnu/lib/python3.12/json/decoder.py", line 356, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

[exit code: 1]