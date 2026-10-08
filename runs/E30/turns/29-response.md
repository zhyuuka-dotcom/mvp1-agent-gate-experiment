Now I have the full file. Let me implement the fix.

First, add a `resolve_log_format` helper to config_parser.py. I'll append it after `detect_log_config` and also handle it in build_pattern/extract_variables is not strictly needed since process() will pass the resolved string. But `info` uses extract_variables(log_format) — resolves before that.

Let me write config_parser.py with the new helper. I'll add `is_format_name` and `resolve_log_format`.

Now for ngxtop.py process(): insert resolution. Let me modify:

```python
    if access_log is None:
        access_log, log_format = detect_log_config(arguments)

    # Resolve a named log format (e.g. `-f main`) into its format string by
    # looking it up in the nginx config, so that formats other than the
    # built-in ones can be used together with an explicit access log file.
    log_format = resolve_log_format(log_format, arguments['--config'])
```

And update the import.

Let me write both files now.

WRITE ngxtop/config_parser.py
<<<FILE_CONTENTS
"""
Nginx config parser and pattern builder.
"""
import os
import re
import subprocess

from pyparsing import Literal, Word, ZeroOrMore, OneOrMore, Group, \
    printables, quotedString, pythonStyleComment, removeQuotes

from .utils import choose_one, error_exit


REGEX_SPECIAL_CHARS = r'([\.\*\+\?\|\(\)\{\}\[\]])'
REGEX_LOG_FORMAT_VARIABLE = r'\$([a-zA-Z0-9\_]+)'
LOG_FORMAT_COMBINED = '$remote_addr - $remote_user [$time_local] ' \
                      '"$request" $status $body_bytes_sent ' \
                      '"$http_referer" "$http_user_agent"'
LOG_FORMAT_COMMON   = '$remote_addr - $remote_user [$time_local] ' \
                      '"$request" $status $body_bytes_sent ' \
                      '"$http_x_forwarded_for"'
LOG_FORMAT_CADDY    = 'caddy'

# built-in format names that do not need to be resolved from a config file
LOG_FORMAT_NAMES = ('combined', 'common', 'caddy')

# common parser element
semicolon = Literal(';').suppress()
# nginx string parameter can contain any character except: { ; " '
parameter = Word(''.join(c for c in printables if c not in set('{;"\'')))
# which can also be quoted
parameter = parameter | quotedString.setParseAction(removeQuotes)


def detect_config_path():
    """
    Get nginx configuration file path based on `nginx -V` output
    :return: detected nginx configuration file path
    """
    try:
        proc = subprocess.Popen(['nginx', '-V'], stderr=subprocess.PIPE)
    except OSError:
        error_exit('Access log file or format was not set and nginx config file cannot be detected. ' +
                   'Perhaps nginx is not in your PATH?')

    stdout, stderr = proc.communicate()
    version_output = stderr.decode('utf-8')
    conf_path_match = re.search(r'--conf-path=(\S*)', version_output)
    if conf_path_match is not None:
        return conf_path_match.group(1)

    prefix_match = re.search(r'--prefix=(\S*)', version_output)
    if prefix_match is not None:
        return prefix_match.group(1) + '/conf/nginx.conf'
    return '/etc/nginx/nginx.conf'


def get_access_logs(config):
    """
    Parse config for access_log directives
    :return: iterator over ('path', 'format name') tuple of found directives
    """
    access_log = Literal("access_log") + ZeroOrMore(parameter) + semicolon
    access_log.ignore(pythonStyleComment)

    for directive in access_log.searchString(config).asList():
        path = directive[1]
        if path == 'off' or path.startswith('syslog:'):
            # nothing to process here
            continue

        format_name = 'combined'
        if len(directive) > 2 and '=' not in directive[2]:
            format_name = directive[2]

        yield path, format_name


def get_log_formats(config):
    """
    Parse config for log_format directives
    :return: iterator over ('format name', 'format string') tuple of found directives
    """
    # log_format name [params]
    log_format = Literal('log_format') + parameter + Group(OneOrMore(parameter)) + semicolon
    log_format.ignore(pythonStyleComment)

    for directive in log_format.searchString(config).asList():
        name = directive[1]
        format_string = ''.join(directive[2])
        yield name, format_string


def is_log_format_name(log_format):
    """
    Return True if given value looks like the name of a ``log_format`` directive
    rather than a literal format string.

    A literal format string always contains at least one nginx variable (``$name``);
    a format name is a single token without spaces or ``$`` characters.
    """
    if not log_format:
        return False
    if '$' in log_format:
        return False
    return re.search(r'\s', log_format) is None


def resolve_log_format(log_format, config=None):
    """
    Resolve a ``log_format`` name (e.g. ``main``) into the format string defined
    in the nginx configuration.

    Built-in formats (combined/common/caddy) and literal format strings are
    returned unchanged. If a name is given, the nginx config is parsed (auto
    detected when ``config`` is not set) and the matching format string is
    returned; if the name cannot be found an error is raised.
    """
    if log_format in LOG_FORMAT_NAMES:
        return log_format
    if not is_log_format_name(log_format):
        # a literal format string; use it as is
        return log_format

    if config is None:
        config = detect_config_path()
    if not os.path.exists(config):
        error_exit('Nginx config file not found: %s' % config)

    with open(config) as f:
        config_str = f.read()

    log_formats = dict(get_log_formats(config_str))
    if log_format not in log_formats:
        error_exit('Incorrect format name set: "%s"' % log_format)
    return log_formats[log_format]


def detect_log_config(arguments):
    """
    Detect access log config (path and format) of nginx. Offer user to select if multiple access logs are detected.
    :return: path and format of detected / selected access log
    """
    config = arguments['--config']
    if config is None:
        config = detect_config_path()
    if not os.path.exists(config):
        error_exit('Nginx config file not found: %s' % config)

    with open(config) as f:
        config_str = f.read()
    access_logs = dict(get_access_logs(config_str))
    if not access_logs:
        error_exit('Access log file is not provided and ngxtop cannot detect it from your config file (%s).' % config)

    log_formats = dict(get_log_formats(config_str))
    if len(access_logs) == 1:
        log_path, format_name = list(access_logs.items())[0]
        if format_name == 'combined':
            return log_path, LOG_FORMAT_COMBINED
        if format_name not in log_formats:
            error_exit('Incorrect format name set in config for access log file "%s"' % log_path)
        return log_path, log_formats[format_name]

    # multiple access logs configured, offer to select one
    print('Multiple access logs detected in configuration:')
    log_path = choose_one(list(access_logs.keys()), 'Select access log file to process: ')
    format_name = access_logs[log_path]
    if format_name not in log_formats:
        error_exit('Incorrect format name set in config for access log file "%s"' % log_path)
    return log_path, log_formats[format_name]


def build_pattern(log_format):
    """
    Build regular expression to parse given format.
    :param log_format: format string to parse
    :return: regular expression to parse given format
    """
    if log_format == 'combined':
        log_format = LOG_FORMAT_COMBINED
    elif log_format == 'common':
        log_format = LOG_FORMAT_COMMON
    elif log_format == 'caddy':
        return 'caddy'  # Special case for Caddy JSON format
    pattern = re.sub(REGEX_SPECIAL_CHARS, r'\\\1', log_format)
    pattern = re.sub(REGEX_LOG_FORMAT_VARIABLE, '(?P<\\1>.*)', pattern)
    return re.compile(pattern)


def extract_variables(log_format):
    """
    Extract all variables from a log format string.
    :param log_format: format string to extract
    :return: iterator over all variables in given format string
    """
    if log_format == 'combined':
        log_format = LOG_FORMAT_COMBINED
    elif log_format == 'common':
        log_format = LOG_FORMAT_COMMON
    elif
