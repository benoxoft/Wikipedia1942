import random
import wikipedia

MAX_LEVEL_TIME = 600 #seconds

def next_gem(current_time, gems):
    if gems[0][1] < current_time:
        return gems.pop(0)
    else:
        return None

def randomize_page():
    return open_page(wikipedia.random())

def gemify_page(wiki_page):
    links_len = len(wiki_page.links)
    spawn_time = MAX_LEVEL_TIME / links_len
    if spawn_time > 10:
        spawn_time = 10
    
    links = [[link,] for link in wiki_page.links]
    random.shuffle(links)
    for i in range(0, links_len):
        links[i].append(spawn_time * (i+1))
    return links

def open_page(page_title):
    try:
        page = wikipedia.page(page_title)
    except Exception as e:
        alternative =  random.randint(0, len(e.options)-1)
        page = wikipedia.page(e.options[alternative])
    return page
    
