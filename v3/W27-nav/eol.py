import hashlib, pathlib
R = pathlib.Path('.')
for p in ['site/assets/commit.css', 'site/assets/stories.js', 'site/checkout.js',
          'site/assets/ring.js', 'site/assets/ring.css', 'site/assets/deck.js', 'site/assets/site.js']:
    f = R / p
    if not f.exists():
        print('%-30s MISSING' % p); continue
    b = f.read_bytes()
    print('%-30s bytes %7d crlf %5d key %s (lf-key %s)' % (p, len(b), b.count(b'\r\n'),
          hashlib.md5(b).hexdigest()[:8], hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest()[:8]))
ga = R / '.gitattributes'
print('.gitattributes:', ga.read_text() if ga.exists() else 'none')
