$ cd /tmp/t2c30/repo && awk 'NR==452 || NR==457 {printf "%d: [%s]\n", NR, $0}' ngxtop/ngxtop.py
452: [    def report(self):]
457: [        status = 'running for %.0f seconds, %d records processed: %.2f req/sec']

[exit code: 0]