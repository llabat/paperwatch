from pyzotero import zotero

def collect_urls(collection_name, zotero_user_id, zotero_api_key):

    #zot = zotero.Zotero('13530352', 'user', '2y98RyOHrwTFeMC0FhReEwfW')
    zot = zotero.Zotero(zotero_user_id, 'user', zotero_api_key)

    collection2key = {col['data']['name'] :  col['data']['key'] for col in zot.collections()}
    collection_key = collection2key.get(collection_name)
    if not collection_key:
        raise ValueError(f"Collection name {collection_name} not found.")
    
    all_items = zot.collection_items(collection_key)
    main_items = {}
    snapshot_urls = {}

    # First, build a map of main items (by their key)
    for item in all_items:
        data = item['data']
        if data['itemType'] not in ['attachment', 'note']:
            main_items[data['key']] = {
                'title': data.get('title', '[No title]'),
                'url': data.get('url', None),
            }

    # Then, find associated snapshot URLs
    for item in all_items:
        data = item['data']
        if data.get('title') == 'Snapshot' and data.get('url'):
            parent = data.get('parentItem')
            if parent and parent in main_items:
                snapshot_urls[parent] = data['url']

    # Now merge: prefer snapshot URL if available
    merged_links = []
    for key, meta in main_items.items():
        url = snapshot_urls.get(key) or meta['url']
        if url:
            merged_links.append({'title': meta['title'], 'url': url})

    return [entry["url"] for entry in merged_links]