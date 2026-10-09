My WRITE was the earlier version (the corrected one apparently didn't take — actually the file on disk is the first version with `5.0`). Wait, the last WRITE said "WROTE tests/test_median.py (2113 bytes)" but the test shows `assert m.finalize() == 5.0  # (4 + 2) / 2? ...` — that's the first version's comment. So the second WRITE wasn't applied? The harness reported only one WROTE. Let me re-read to see actual content.

Actually the failure line shows the comment `# (4 + 2) / 2? sorted [2,4,8,10] -> (4+8)/2 = 6.0` which is from the FIRST version. So the second WRITE didn't overwrite. Let me just fix that line with RUN.

RUN .venv/bin/python -c "p='tests/test_median.py';s=open(p).read();nl=chr(10);old='        assert m.finalize() == 5.0  # (4 + 2) / 2? sorted [2,4,8,10] -> (4+8)/2 = 6.0'+nl;assert s.count(old)==1;s=s.replace(old,'        assert m.finalize() == 6.0'+nl,1);open(p,'w').write(s);print('ok')"

Send.The second WRITE didn't apply (stale version on disk). Fix the assertion via RUN.

RUN .venv/bin/python -c "p='tests/test_median.py';s=open(p).read();nl=chr(10);old='        assert m.finalize() == 5.0  # (4 + 2) / 2? sorted [2,4,8,10] -> (4+8)/2 = 6.0'+nl;assert s.count(old)==1;s=s.replace(old,'        assert m.finalize() == 6.0'+nl,1);open(p,'w').write(s);print('ok')"

Send.
