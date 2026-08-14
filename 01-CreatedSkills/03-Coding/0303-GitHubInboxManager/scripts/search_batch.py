#!/usr/bin/env python3
"""Batch GitHub repo search with rate-limit protection.

Usage:
    echo '["item1","item2"]' > /tmp/queries_batch.json
    python3 ~/.claude/skills/0303-GitHubInboxManager/scripts/search_batch.py

Output: /tmp/search_results.json — {query: [full_name, html_url, desc, stars]}
"""
import json, os, time, urllib.request, urllib.parse

with open('/Users/quzinan/Downloads/Code/.mcp.json') as f:
    token = json.load(f)['mcpServers']['github']['env']['GITHUB_PERSONAL_ACCESS_TOKEN']

QUERIES = json.load(open('/tmp/queries_batch.json'))

results = {}
if os.path.exists('/tmp/search_results.json'):
    results = json.load(open('/tmp/search_results.json'))

for q in QUERIES:
    encoded = urllib.parse.quote(q)
    req = urllib.request.Request(
        f"https://api.github.com/search/repositories?q={encoded}&sort=stars&per_page=1",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "claude-mcp",
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        items = data.get('items', [])
        if items:
            r = items[0]
            results[q] = (r['full_name'], r['html_url'], (r.get('description') or '')[:60], r['stargazers_count'])
            print(f"{q} → {r['full_name']} ⭐{r['stargazers_count']}")
        else:
            results[q] = ('', '', '', 0)
            print(f"{q} → NOT FOUND")
    except Exception as e:
        print(f"{q} → ERROR {e}")
        results[q] = ('', '', '', 0)
    time.sleep(3)

with open('/tmp/search_results.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
