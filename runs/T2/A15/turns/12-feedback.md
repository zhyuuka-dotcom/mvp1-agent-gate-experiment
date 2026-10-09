$ sed -n '360,440p' ngxtop/ngxtop.py
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
        return parse_caddy_log(lines)
        
    # Regular nginx/apache log parsing
    matches = (pattern.match(l) for l in lines)
    records = (m.groupdict() for m in matches if m is not None)
    records = map_field('status', to_int, records)
    records = add_field('status_type', parse_status_type, records)
    records = add_field('bytes_sent', lambda r: r['body_bytes_sent'], records)
    records = map_field('bytes_sent', to_int, records)
    records = map_field('request_time', to_float, records)
    records = add_field('request_path', parse_request_path, records)
    return records


# =================================
# Records and statistic processor
# =================================
class SQLProcessor(object):
    def __init__(self, report_queries, fields, index_fields=None):
        self.begin = False
        self.report_queries = report_queries

[exit code: 0]