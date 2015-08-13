import random
import wikipedia

MAX_LEVEL_TIME = 600000

def next_gem(current_time, gems):
    if len(gems) == 0:
        return None
    elif gems[0][1] <= current_time:
        return gems.pop(0)[0]
    else:
        return None

def randomize_page():
    #return open_page("Anime")
    return open_page(wikipedia.random())

def gemify_page(wiki_page):
    links_len = len(wiki_page.links)
    spawn_time = MAX_LEVEL_TIME / links_len
    if spawn_time > 2000:
        spawn_time = 2000
    
    links = [[link,] for link in wiki_page.links]
    random.shuffle(links)
    for i in range(0, links_len):
        links[i].append(spawn_time * i)
    return links

def open_page(page_title):
    if page_title == "random":
        return randomize_page()
    try:
        page = wikipedia.page(page_title)
    except wikipedia.PageError:
        return randomize_page()
    except Exception as e:
        alternative =  random.randint(0, len(e.options)-1)
        page = wikipedia.page(e.options[alternative])
    return page
    
