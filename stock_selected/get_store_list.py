import re
import json
import ast
import sys
import requests
import js2py

#!/usr/bin/env python3
# get_store_list.py
# Fetch and parse the JS file at the SSE URL and print the extracted data as JSON.


try:
except Exception as e:
    print("requests is required: pip install requests", file=sys.stderr)
    raise

try:
    _HAS_JS2PY = True
except Exception:
    _HAS_JS2PY = False


URL = "https://www.sse.com.cn/js/common/ssesuggestdata.js?v=2025102514"


def fetch_text(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text


def extract_js_value(js_text):
    # try: var NAME = <value> ;
    m = re.search(r"var\s+[\w$]+\s*=\s*([\s\S]*?);", js_text)
    if m:
        return m.group(1).strip()

    # fallback: take content between first {/[ and last }/]
    idx_start = None
    for ch in ("{", "["):
        i = js_text.find(ch)
        if i != -1 and (idx_start is None or i < idx_start):
            idx_start = i
    if idx_start is None:
        raise ValueError("no JSON-like start found in JS")

    idx_end = None
    for ch in ("}", "]"):
        i = js_text.rfind(ch)
        if i != -1 and (idx_end is None or i > idx_end):
            idx_end = i
    if idx_end is None or idx_end <= idx_start:
        raise ValueError("no JSON-like end found in JS")

    return js_text[idx_start: idx_end + 1]


def try_parse_json(text):
    # direct json
    try:
        return json.loads(text)
    except Exception:
        pass

    # try to clean trailing commas and JS null/true/false => Python equivalents, then ast.literal_eval
    s = re.sub(r",\s*([}\]])", r"\1", text)  # remove trailing commas
    s = s.replace("null", "None").replace("true", "True").replace("false", "False")
    try:
        return ast.literal_eval(s)
    except Exception:
        pass

    # try js2py if available
    if _HAS_JS2PY:
        try:
            # Evaluate as a JS expression by assigning to a temp var then returning it
            code = f"var __tmp = {text}; __tmp;"
            val = js2py.eval_js(code)
            # convert js2py objects to native python where possible
            if hasattr(val, "to_dict"):
                return val.to_dict()
            return val
        except Exception:
            pass

    raise ValueError("unable to parse JS value into Python object")


def fetch_sse_suggest(url=URL):
    txt = fetch_text(url)
    js_val = extract_js_value(txt)
    return try_parse_json(js_val)


def main():
    try:
        data = fetch_sse_suggest()
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()