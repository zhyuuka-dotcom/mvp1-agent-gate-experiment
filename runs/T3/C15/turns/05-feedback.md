$ grep -n "bytes_sent\|median\|avg_bytes\|DEFAULT_QUERIES\|Summary\|Detailed" tests/test_characterization.py README.rst | head -60
tests/test_characterization.py:28:    assert "Summary:" in r.stdout
tests/test_characterization.py:43:    assert "Summary:" in r.stdout
README.rst:75:    Summary:
README.rst:76:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:80:    Detailed:
README.rst:81:    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:137:    Summary:
README.rst:138:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:142:    Detailed:
README.rst:143:    | request_path                             |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:164:    Summary:
README.rst:165:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:169:    Detailed:
README.rst:170:    | request_path                        |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:191:    Summary:
README.rst:192:    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
README.rst:196:    Detailed:
README.rst:197:    | host                |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |

[exit code: 0]