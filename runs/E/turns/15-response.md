Now let me check the README for how `-f` should behave with named formats, and check git history / existing behavior.

RUN grep -n "log_format\|-f \|--log-format\|--config\|named\|format name" README.rst | head -40
