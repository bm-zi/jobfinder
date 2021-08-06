import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import mechanize


def get_html_body_element(url):

    tags = ['style', 'script', 'svg', 'img', 'input', 'a',
            'button', 'head', 'title', 'meta', '[document]']

    page = urllib.request.urlopen(url).read().decode("ISO-8859-1")
    soup = BeautifulSoup(page, 'html.parser')
    html_body = soup.find_all("body")

    for tag in tags:
        [s.extract() for s in soup(tag)]

    els = ''
    for el in soup:
        els = els + str(el) + "\n"

    return els


def indeed_search_filter(withallofthesewords,
                         withtheexactphrase,
                         withatleastoneofthesewords,
                         withnoneofthesewords,
                         withthesewordsinthetitle,
                         fromthiscompany):
    
    # br.set_handle_robots(False)
    # br.addheaders = [("User-agent","Mozilla/5.0")]

    br = mechanize.Browser()
    indeed_search = br.open("https://ca.indeed.com/advanced_search")
    br.select_form(nr=0)

    br['as_and'] = withallofthesewords
    br['as_phr'] = withtheexactphrase
    br['as_any'] = withatleastoneofthesewords
    br['as_not'] = withnoneofthesewords
    br['as_ttl'] = withthesewordsinthetitle
    br['as_cmp'] = fromthiscompany

    br.submit()  # Submit current form
    base_url = br.geturl()  # Get URL of current document
    result_page = urllib.request.urlopen(base_url).read()
    soup = BeautifulSoup(result_page, "html.parser")
    tags = soup.findAll('a', attrs={'data-tn-element': 'companyName'})
    
    
    all_found_jobs = []
    for tag in tags:
        job = []
        title = tag.text
        job_url = 'https://ca.indeed.com' + tag['href']
        job_data = get_html_body_element(job_url)
        job.append(title)
        job.append(job_url)
        job.append(job_data)
        all_found_jobs.append(job)

    return all_found_jobs


# print(indeed_search_filter('Python', 'Python', 'develop', 'windows', 'python', ''))
