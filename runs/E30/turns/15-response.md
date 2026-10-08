Config parsing works and produces the correct format string. Now let me test building the pattern and parsing against the multiline format:

RUN .venv/bin/python -c "from ngxtop import config_parser; p=config_parser.build_pattern(dict(config_parser.get_log_formats(open('repro/nginx_multiline.conf').read()))['main']); print(p.pattern)"
