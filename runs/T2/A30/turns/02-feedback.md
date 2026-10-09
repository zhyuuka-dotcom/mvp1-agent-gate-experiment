$ sed -n 100,400p ngxtop/ngxtop.py
    ('Detailed:',
     '''SELECT
       %(--group-by)s,
       count(1)                                    AS count,
       avg(bytes_sent)                             AS avg_bytes_sent,
       count(CASE WHEN status_type = 2 THEN 1 END) AS '2xx',
       count(CASE WHEN status_type = 3 THEN 1 END) AS '3xx',
       count(CASE WHEN status_type = 4 THEN 1 END) AS '4xx',
       count(CASE WHEN status_type = 5 THEN 1 END) AS '5xx'
     FROM log
     GROUP BY %(--group-by)s
     HAVING %(--having)s
     ORDER BY %(--order-by)s DESC
     LIMIT %(--limit)s''')
]

DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])

# Global flag for log rotation signal
_rotation_requested = False


# ======================
# generator utilities
# ======================
def follow(the_file):
    """
    Follow a given file and yield new lines when they are available, like `tail -f`.
    Handles log rotation by detecting inode changes and file size resets.
    """
    f = None
    current_inode = None
    current_size = 0
    retry_count = 0
    max_retries = 5
    
    try:
        while True:
            # Check if we need to (re)open the file
            if f is None or _should_reopen_file(the_file, current_inode, current_size) or _check_rotation_signal():
                if f is not None:
                    f.close()
                    if _check_rotation_signal():
                        logging.info(f"SIGHUP received, reopening {the_file}...")
                        _clear_rotation_signal()
                    else:
                        logging.info(f"Detected log rotation for {the_file}, reopening...")
                
                # Try to open the file with retries
                f, current_inode, current_size = _open_file_with_retry(the_file, max_retries)
                if f is None:
                    logging.error(f"Failed to open {the_file} after {max_retries} retries")
                    break
                
                f.seek(0, 2)  # seek to eof
                retry_count = 0
            
            # Read new lines
            line = f.readline()
            if not line:
                time.sleep(0.1)  # sleep briefly before trying again
                continue
            
            # Update current size
            current_size = f.tell()
            yield line
            
    except KeyboardInterrupt:
        if f is not None:
            f.close()
        raise
    except Exception as e:
        logging.error(f"Error in follow(): {e}")
        if f is not None:
            f.close()
        raise


def _should_reopen_file(file_path, current_inode, current_size):
    """
    Check if file should be reopened due to rotation.
    Returns True if file has been rotated (inode changed or size decreased significantly).
    """
    try:
        file_stat = os.stat(file_path)
        new_inode = file_stat.st_ino
        new_size = file_stat.st_size
        
        # File has been rotated if:
        # 1. Inode changed (file was moved/renamed)
        # 2. File size decreased significantly (> 1000 bytes, indicating truncation/rotation)
        if current_inode is not None and new_inode != current_inode:
            return True
        
        if new_size < current_size - 1000:  # Allow for some buffer, but detect major size drops
            return True
            
        return False
        
    except (OSError, IOError):
        # File doesn't exist or can't be accessed - we should try to reopen
        return True


def _open_file_with_retry(file_path, max_retries):
    """
    Open file with retry logic, handling temporary file absence during rotation.
    Returns (file_handle, inode, size) or (None, None, 0) if failed.
    """
    for attempt in range(max_retries):
        try:
            file_stat = os.stat(file_path)
            f = open(file_path, 'r')
            return f, file_stat.st_ino, file_stat.st_size
            
        except (OSError, IOError) as e:
            if attempt < max_retries - 1:
                # Wait with exponential backoff: 0.1, 0.2, 0.4, 0.8, 1.6 seconds
                wait_time = 0.1 * (2 ** attempt)
                logging.warning(f"Failed to open {file_path} (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logging.error(f"Failed to open {file_path} after {max_retries} attempts: {e}")
    
    return None, None, 0


def _sighup_handler(signum, frame):
    """Signal handler for SIGHUP - marks rotation as requested."""
    global _rotation_requested
    _rotation_requested = True
    logging.info("SIGHUP received - will reopen log file on next check")


def _check_rotation_signal():
    """Check if log rotation was requested via signal."""
    global _rotation_requested
    return _rotation_requested


def _clear_rotation_signal():
    """Clear the rotation request flag."""
    global _rotation_requested
    _rotation_requested = False


def map_field(field, func, dict_sequence):
    """
    Apply given function to value of given key in every dictionary in sequence and
    set the result as new value for that key.
    """
    for item in dict_sequence:
        try:
            item[field] = func(item.get(field, None))
            yield item
        except ValueError:
            pass


def add_field(field, func, dict_sequence):
    """
    Apply given function to the record and store result in given field of current record.
    Do nothing if record already contains given field.
    """
    for item in dict_sequence:
        if field not in item:
            item[field] = func(item)
        yield item


def trace(sequence, phase=''):
    for item in sequence:
        logging.debug('%s:\n%s', phase, item)
        yield item


# ======================
# Access log parsing
# ======================
def parse_request_path(record):
    if 'request_uri' in record:
        uri = record['request_uri']
    elif 'request' in record:
        uri = ' '.jo
…[RUN 输出截断：全长 11545 字符]
SON start position: {json_start}")
                    logging.info(f"Extracted JSON length: {len(json_str)} characters")
                    
                    # Show the area around the error
                    if e.pos is not None and e.pos < len(json_str):
                        start = max(0, e.pos - 20)
                        end = min(len(json_str), e.pos + 20)
                        logging.info(f"JSON around error position: ...{json_str[start:end]}...")
                        logging.info(f"                            {' ' * (e.pos - start - 3)}^")
                    
                    # Output the complete line for analysis
                    logging.info(f"Complete line from beginning ({len(line)} chars):")
                    # Show first 100 chars to see the prefix, then ... then area around JSON start
                    if len(line) > 200:
                        prefix = line[:100]
                        json_area = line[max(0, json_start-20):json_start+80]

[exit code: 0]