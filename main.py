from playwright.sync_api import sync_playwright
import yaml
import os
from urllib.parse import urlparse


PLACEHOLDER = "<replace>"
NOTIFICATION_SCRIPT = f'osascript -e \'display alert "New Property found on {PLACEHOLDER}"\''



def get_links(site, css_locator):

    links = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        try:

            page = browser.new_page()
            page.goto(site)
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(css_locator)

            links_on_page = page.locator(css_locator)
            for i in range(links_on_page.count()):
                links.append(links_on_page.nth(i).get_attribute('href'))

        except:
            print('Error while scraping, try again later.')

        browser.close()


    return links

def read_links():
    links = []
    with open('links.txt') as f:
        for line in f.readlines():
            links.append(line.strip())
    return links

def write_new_links(new_links):
    links = []
    with open('links.txt', 'a') as w:
        for link in new_links:
            w.write(f'\n{link}')

def compare_links(new, old):
    new_links = []
    for link in new:
        if link not in old:
            new_links.append(link)

    return new_links

def normalize_link(link, domain):
    if link.startswith('/'):
        link = f'{domain}{link}'
    return link

if __name__ == '__main__':

    config = {}
    with open("settings.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    old_links = read_links()

    for site in config['websites']:
        name = site["name"]
        url = urlparse(site["link"])
        domain = f'{url.scheme}://{url.netloc}'
        print(f'Checking: { name }')
        new_links = get_links(site['link'], site['selector'])

        difference = compare_links(new_links, old_links)

        print('Links found: ')
        for link in new_links:
            print(normalize_link(link, domain))

        if len(difference) == 0:
            print(f'No new links found in {name}')
        else:
            os.system(NOTIFICATION_SCRIPT.replace(PLACEHOLDER, name))
            print(f'New links found in {site["name"]}')
            for link in difference:
                print(normalize_link(link, domain))
            write_new_links(difference)
    
    