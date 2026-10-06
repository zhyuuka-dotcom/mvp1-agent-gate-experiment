$ grep -n "detect_config_path\|from .config_parser\|def process(arguments)" ngxtop/ngxtop.py
83:from .config_parser import detect_log_config, detect_config_path, extract_variables, build_pattern
580:def process(arguments):
595:        print('nginx configuration file:\n ', detect_config_path())

[exit code: 0]