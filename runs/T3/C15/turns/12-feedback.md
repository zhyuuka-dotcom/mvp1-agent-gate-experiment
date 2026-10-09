$ grep -n "def build_pattern\|def detect_log_config\|combined\|common\|caddy\|PREDEFINED\|main" ngxtop/config_parser.py | head -40
22:LOG_FORMAT_CADDY    = 'caddy'
24:# common parser element
69:        format_name = 'combined'
91:def detect_log_config(arguments):
111:        if format_name == 'combined':
126:def build_pattern(log_format):
132:    if log_format == 'combined':
134:    elif log_format == 'common':
136:    elif log_format == 'caddy':
137:        return 'caddy'  # Special case for Caddy JSON format
149:    if log_format == 'combined':
151:    elif log_format == 'common':
153:    elif log_format == 'caddy':

[exit code: 0]