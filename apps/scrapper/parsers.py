import requests
import codecs
from bs4 import BeautifulSoup as BS
from lxml import etree
from random import randint


headers = [
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' },
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
]


def work(url):
    jobs = []
    errors = []
    domain = "https://www.work.ua"
    url = "https://www.work.ua/ru/jobs-kyiv-python/"
    resp = requests.get(url, headers=headers[randint(0, 1)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find("div", attrs={"id": "pjax-job-list"})
        if main_div:
            div_list = main_div.find_all("div", attrs={"class": "job-link"})

            for div in div_list:
                title = div.find("h2")
                href = title.a["href"]
                content = div.p.text
                company = 'no name'
                logo = div.find("img")
                if logo:
                    company = logo["alt"]
                jobs.append({
                    "title": title.text,
                    "url": domain + href,
                    "description": content,
                    "company": company
                })
        else:
            errors.append({"url": url, "title": "Div does not exists!"})
    else:
        errors.append({"url": url, "title": "Page does not response!"})
    return jobs, errors


def rabota(url):
    jobs = []
    errors = []
    domain = "https://rabota.ua"
    resp = requests.get(url, headers=headers[randint(0, 1)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        dom = etree.HTML(str(soup))
        main_div = dom.xpath("/html/body/app-root/div/alliance-jobseeker-vacancies-root-page/div/alliance-jobseeker-desktop-vacancies-page/main/section/div/div/alliance-jobseeker-desktop-vacancies-list/div")
        if main_div:
            div_list = main_div.find_all("div", attrs={"class": "job-link"})

            for div in div_list:
                title = div.find("h2")
                href = title.a["href"]
                content = div.p.text
                company = 'no name'
                logo = div.find("img")
                if logo:
                    company = logo["alt"]
                jobs.append({
                    "title": title.text,
                    "url": domain + href,
                    "description": content,
                    "company": company
                })
        else:
            errors.append({"url": url, "title": "Div does not exists!"})
    else:
        errors.append({"url": url, "title": "Page does not response!"})
    return jobs, errors


def dou(url):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0, 1)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find("div", attrs={"id": "vacancyListId"})
        if main_div:
            li_list = main_div.find_all("li", attrs={"class": "l-vacancy"})

            for li in li_list:
                if '__hot' not in li['class']:
                    title = li.find("div", attrs={"class": "title"})
                    href = title.a["href"]
                    cont = li.find("div", attrs={"class": "sh-info"})
                    content = cont.text
                    company = "no name"
                    a = title.find("a", attrs={"class": "company"})
                    if a:
                        company = a.text
                    jobs.append({
                        "title": title.text,
                        "url": href,
                        "description": content,
                        "company": company
                    })
        else:
            errors.append({"url": url, "title": "Div does not exists!"})
    else:
        errors.append({"url": url, "title": "Page does not response!"})
    return jobs, errors


def djinni(url):
    jobs = []
    errors = []
    domain = "https://djinni.co"
    resp = requests.get(url, headers=headers[randint(0, 1)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find("ul", attrs={"class": "list-jobs"})
        if main_ul:
            li_list = main_ul.find_all("li", attrs={"class": "list-jobs__item"})

            for li in li_list:
                title = li.find("div", attrs={"class": "list-jobs__title"})
                href = title.a["href"]
                cont = li.find("div", attrs={"class": "list-jobs__description"})
                content = cont.text
                company = 'no name'
                comp = li.find("div", attrs={"class": "list-jobs__details__info"})
                if comp:
                    company = comp.text
                jobs.append({
                    "title": title.text,
                    "url": domain + href,
                    "description": content,
                    "company": company
                })
        else:
            errors.append({"url": url, "title": "Ul does not exists!"})
    else:
        errors.append({"url": url, "title": "Page does not response!"})
    return jobs, errors


if __name__ == "__main__":
    url = 'https://jobs.dou.ua/vacancies/?search=python'
    jobs, errors = dou(url)
    with codecs.open("work.txt", "w", "utf-8") as file:
        file.write(str(jobs))
