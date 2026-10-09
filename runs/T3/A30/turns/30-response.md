Implementation complete and verified:

- Added a `Median` SQLite aggregate in `ngxtop/ngxtop.py`, registered via `create_aggregate('median', 1, Median)`. It ignores NULLs (like `avg()`), handles odd/even counts, and returns `None` for empty sets.
- Added `median(bytes_sent) AS median_bytes_sent` to both default report tables (Summary and Detailed), placed directly next to `avg_bytes_sent` so the typical request size is visible alongside the average — satisfying the request.
- Column name follows the existing `avg_bytes_sent` convention.
- Added regression tests in `tests/test_median_bytes_sent.py`.
- Full suite: 33 passed (28 pre-existing + 5 new).

Verified outputs: for the 5-record custom-format sample, the median is 512 (vs. average 1626.6), correctly demonstrating the outlier-insensitive behavior the request asks for.

DONE
