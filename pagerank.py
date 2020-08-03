import os
import random
import re
import sys
from pomegranate import *
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    ans = dict()
    n = len(corpus[page])
    m = len(corpus.keys())
    for x in corpus.keys():
        if (x in corpus[page]):
            ans[x] = ((damping_factor * (1/n)) + ((1-damping_factor)* (1/m)))
        else:
            ans[x] = ((1-damping_factor)* (1/m))
    return ans


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    x = random.choices([x for x in corpus.keys()])[0]
    pagerrank = dict()
    for key in corpus.keys():
        pagerrank[key] = 0
    pagerrank[x] += (1/n)
    for i in range(1,n):
        model = transition_model(corpus,x,damping_factor)
        keys = list(model.keys())
        probability = list(model.values())
        x = random.choices(keys,weights=probability)[0]
        pagerrank[x] += (1/n)
    return pagerrank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerrank = dict()
    # no of links in corpus
    n = len(corpus.keys())
    # set having all the links of corpus in it
    s = set()
    # initializing pagerank of all links equally
    for x in corpus.keys():
        pagerrank[x] = 1/n
        s.add(x)

    # creating dict which shows 'x' link can be accessed by which all links    
    thru = dict()
    for x in s:
        temp = set()
        for t in s:
            if (x in corpus[t]):
                temp.add(t)
        thru[x] = temp 
    
    # loop goes untill pagerrank[x] new - before > 0.001 for all x which is link
    while(1):
        before = [pagerrank[v] for v in pagerrank.keys()]
        for x in s:
            belong = thru[x]
            # calculating page rank of page x
            pg = 0
            for v in belong:
                pg += (pagerrank[v]/len(corpus[v]))
            pg = pg*damping_factor
            pg += ((1-damping_factor)/n)
            pagerrank[x] = pg
        
        if (nochange(before, [pagerrank[v] for v in pagerrank.keys()])):
            break

    # print(pagerrank)
    return pagerrank

def nochange(before,new):
    n = len(before)
    count=0
    for i in range(n):
        if (abs(before[i]-new[i]) <= 0.001):
            count+=1
    if (count==n):
        return 1
    else:
        return 0
        

if __name__ == "__main__":
    main()
