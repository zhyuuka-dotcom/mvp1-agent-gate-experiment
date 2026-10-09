$ python3 -c "p='ngxtop/ngxtop.py';s=open(p).read();s=s.replace('    -n <number>','    --output-format <fmt>  output format: table or json [default: table]\n    -n <number>',1);open(p,'w').write(s);print('count',open(p).read().count('output-format'))"
count 1

[exit code: 0]