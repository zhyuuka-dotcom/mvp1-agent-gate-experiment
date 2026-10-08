$ sed -n '290,470p' ngxtop/ngxtop.py
    return record['status'] // 100 if 'status' in record else None


def to_int(value):
    return int(value) if value and value != '-' else 0


def to_float(value):
    return float(value) if value and value != '-' else 0.0


def parse_caddy_log(lines):
    """Parse Caddy JSON log format and convert to ngxtop's expected format."""
    for line in lines:
        try:
            # Extract the JSON part of the line
            # Caddy logs have format: timestamp INFO http.log.access.log2 handled request {json}
            # Find "handled request" first, then find the JSON after it
            handled_pos = line.find('handled request')
            if handled_pos == -1:
                # Try to parse as pure JSON if no "handled request" prefix
                json_start = line.find('{')
            else:
                # Find the first { after "handled request"
                json_start = line.find('{', handled_pos + len('handled request'))
            
            if json_start == -1:
                continue
                
            json_str = line[json_start:].strip()
            
            # Basic check for complete JSON: should start with { and end with }
            if not json_str.endswith('}'):
                # Likely truncated line, skip it
                continue
            
            # Handle potential truncated JSON by trying to parse
            entry = json.loads(json_str)
            if 'request' not in entry:
                continue
                
            # Extract request info
            req = entry.get('request', {})
            method = req.get('method', '-')
            uri = req.get('uri', '-')
            headers = req.get('headers', {})
            
            # Get response info (nested in the logged JSON)
            status = entry.get('status', 0)
            size = entry.get('size', 0)
            try:
                # Try different fields that might contain response size
                if 'size' in entry:
                    size = int(entry['size'])
                elif 'bytes_read' in entry:
                    size = int(entry['bytes_read'])
            except (ValueError, TypeError):
                size = 0
                
            # Build record with fields ngxtop expects
            record = {
                'remote_addr': req.get('remote_ip', '-'),
                'remote_user': '-',
                'time_local': entry.get('ts', '-'),
                'request': f"{method} {uri} HTTP/1.1",
                'status': int(status),
                'body_bytes_sent': size,
                'http_referer': headers.get('Referer', ['-'])[0] if isinstance(headers.get('Referer', '-'), list) else headers.get('Referer', '-'),
                'http_user_agent': headers.get('User-Agent', ['-'])[0] if isinstance(headers.get('User-Agent', '-'), list) else headers.get('User-Agent', '-'),
                'request_uri': uri,
                'request_time': float(entry.get('duration', 0)),
                'host': req.get('host', '-'),  # Add host field from Caddy logs
            }
            
            # Add derived fields
            record['status_type'] = record['status'] // 100
            record['bytes_sent'] = record['body_bytes_sent']
            record['request_path'] = urlparse.urlparse(uri).path if uri else None
            
            yield record
            
        except (json.JSONDecodeError, KeyError, ValueError, AttributeError) as e:
            # For JSON decode errors, provide appropriate level of detail
            if isinstance(e, json.JSONDecodeError):
                # Always show a concise warning
                line_preview = line[:200] + "..." if len(line) > 200 else line
                logging.warning(f"Error parsing log line: {e} - Line preview: {line_preview.strip()}")
                
                # Show detailed debugging info only in verbose mode (INFO level)
                if logging.getLogger().isEnabledFor(logging.INFO):
                    logging.info("="*80)
                    logging.info(f"Detailed JSON parsing error: {e}")
                    logging.info(f"Error position: line {e.lineno}, column {e.colno} (char {e.pos})")
                    logging.info(f"Line length: {len(line)} characters")
                    logging.info(f"Line ends with newline: {line.endswith(chr(10))}")
                    logging.info(f"JSON start position: {json_start}")
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
                        logging.info(f"{prefix}...{json_area}...")
                    else:
                        logging.info(line.rstrip())
                    
                    # Output the extracted JSON string
                    logging.info(f"Extracted JSON string ({len(json_str)} chars):")
                    logging.info(json_str)
                    logging.info("="*80)
            else:
                logging.warning(f"Error parsing log line: {e}")
            continue


def parse_log(lines, pattern):
    # Handle Caddy format separately
    if pattern == 'caddy':
        return parse_ca
…[RUN 输出截断：全长 8272 字符]
 logging.info('sqlite insert: %s', insert)
        with closing(self.conn.cursor()) as cursor:
            for r in records:
                cursor.execute(insert, r)

    def report(self):
        if not self.begin:
            return ''
        count = self.count()
        duration = time.time() - self.begin
        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
        output = [status % (duration, count, count / duration)]
        with closing(self.conn.cursor()) as cursor:
            for query in self.report_queries:
                if isinstance(query, tuple):
                    label, query = query
                else:
                    label = ''
                cursor.execute(query)
                columns = (d[0] for d in cursor.description)
                result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')
                output.append('%s\n%s' % (label, result))
        return '\n\n'.join(output)


[exit code: 0]