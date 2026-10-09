The median_bytes_sent column appears in both Summary and Detailed. But 0 records parsed — `-f main` isn't a recognized format name; it needs the actual format string or a config file. The repro nginx.conf defines log_format main. Let me pass the format string directly by extracting it, or use `-c repro/nginx.conf` with `-l`. Let me check how build_pattern/detect handles 'main'.

The `-f main` treats "main" as a format string literal, so no matches. I need the actual format. Let me get it from nginx.conf.

RUN cat repro/nginx.conf

Send.
