$ .venv/bin/python -c "p='tests/test_median.py';s=open(p).read();nl=chr(10);old='        assert m.finalize() == 5.0  # (4 + 2) / 2? sorted [2,4,8,10] -> (4+8)/2 = 6.0'+nl;assert s.count(old)==1;s=s.replace(old,'        assert m.finalize() == 6.0'+nl,1);open(p,'w').write(s);print('ok')"

[stderr]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AssertionError

[exit code: 1]