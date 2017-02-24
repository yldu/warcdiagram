import collections
import json


data = collections.OrderedDict()


def _finditem(obj, key):
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _finditem(v, key)
            if item is not None:
                return item

with open("/Users/shirleydu/Documents/Waterloo/4B/warcbase2017w/summary/dist.txt", "r") as f, open('/Users/shirleydu/Documents/Waterloo/4B/warcdiagram/sites_hierarchy.json', 'w') as output:
    prefixes = ["root"]
    data[prefixes[0]] = {}
    for line in f:
        url, count, is_leaf = line.split(",")
        count, is_leaf = map(int, [count, is_leaf])

        found = None
        should_reset = True
        for i in range(len(prefixes)):
            p = prefixes[i]
            found = _finditem(data, p)

            if found is not None and url.startswith(p) or p == "root":
                if url[len(p)] == "/" or p == "root":
                    if should_reset:
                        prefixes = prefixes[i:]  # reset head
                    if is_leaf == 1:
                        _finditem(data, p)[url] = count
                    elif is_leaf == 0:
                        _finditem(data, p)[url] = {}
                        prefixes.insert(0, url)
                    break
                else:
                    should_reset = False

        if is_leaf == 2:
            temp_prefix = url[:url.rfind("/")] if "/" in url else url
            if _finditem(data, temp_prefix) is None:
                data["root"][url] = count
            else:
                _finditem(data, temp_prefix)[url] = count

        elif found is None:
            if is_leaf:
                data[url] = count
            else:
                data["root"][url] = {}
                prefixes.insert(0, url)

    json.dump(data, output)


