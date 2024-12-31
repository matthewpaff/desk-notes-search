"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value


def day(value):
    from datetime import date
    import re
    if not isinstance(value,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
        raise ValueError("Use YYYY-MM-DD")
    return date.fromisoformat(value)


def text(value,maximum=10000):
    if not isinstance(value,str) or len(value)>maximum:
        raise ValueError("Expected bounded text")
    return value

def evaluate(data):
    import re
    from collections import Counter
    fields(data,("query","notes","limit"))
    def terms(value):
        return set(re.findall(r"[^\W_]+",value.casefold(),flags=re.UNICODE))
    query=terms(text(data["query"],1000))
    limit=integer(data["limit"],1,50)
    documents,seen=[],set()
    for note in sequence(data["notes"],200):
        fields(note,("id","text"))
        ident,body=label(note["id"]),text(note["text"])
        if ident in seen:
            raise ValueError("Duplicate note ID")
        seen.add(ident)
        documents.append((ident,terms(body)))
    frequency=Counter(term for _,terms in documents for term in terms)
    ranked=[]
    for ident,terms in documents:
        matched=sorted(terms&query)
        if matched:
            score=sum(1/(frequency[term]+1) for term in matched)/len(terms)
            ranked.append({"id":ident,"score":round(score,6),"matched_terms":matched})
    return {"results":sorted(ranked,key=lambda row:(-row["score"],row["id"]))[:limit]}
