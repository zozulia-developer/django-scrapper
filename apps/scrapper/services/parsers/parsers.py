from dataclasses import dataclass, field
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from apps.scrapper.services.parsers import base, constants


@dataclass
class MainParser:
    jobs: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    domain: str = field(default_factory=str)
    user_agent: UserAgent = UserAgent()

    def get_random_header(self):
        return {"User-Agent": self.user_agent.random}


class WorkUaParser(MainParser, base.BaseParser):
    domain = constants.WORK_UA_DOMAIN

    def parse(self, url: str, city=None, language=None) -> Tuple[list, list]:
        resp = requests.get(url, headers=self.get_random_header())
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find("div", attrs={"id": "pjax-job-list"})
            if main_div:
                div_list = main_div.find_all("div", attrs={"class": "job-link"})
                for div in div_list:
                    title = div.find("h2").text.strip()
                    href = title.a["href"]
                    content = div.p.text.strip()
                    company = 'no name'
                    logo = div.find("img")
                    if logo:
                        company = logo["alt"]
                    self.jobs.append({
                        "title": title,
                        "url": self.domain + href,
                        "description": content,
                        "company": company,
                        "city_id": city,
                        "language_id": language
                    })
            else:
                self.errors.append({"url": url, "title": "Div does not exists!"})
        else:
            self.errors.append({"url": url, "title": "Page does not response!"})
        return self.jobs, self.errors


class DouParser(MainParser, base.BaseParser):
    def parse(self, url: str, city=None, language=None) -> Tuple[list, list]:
        resp = requests.get(url, headers=self.get_random_header())
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find("div", attrs={"id": "vacancyListId"})
            if main_div:
                li_list = main_div.find_all("li", attrs={"class": "l-vacancy"})
                for li in li_list:
                    if '__hot' not in li['class']:
                        title = li.find("div", attrs={"class": "title"}).text.strip()
                        href = title.a["href"]
                        cont = li.find("div", attrs={"class": "sh-info"})
                        content = cont.text.strip()
                        company = "no name"
                        a = title.find("a", attrs={"class": "company"})
                        if a:
                            company = a.text
                        self.jobs.append({
                            "title": title,
                            "url": href,
                            "description": content,
                            "company": company,
                            "city_id": city,
                            "language_id": language
                        })
            else:
                self.errors.append({"url": url, "title": "Div does not exists!"})
        else:
            self.errors.append({"url": url, "title": "Page does not response!"})
        return self.jobs, self.errors


class DjinniParser(MainParser, base.BaseParser):
    domain = constants.DJINNI_DOMAIN

    def parse(self, url: str, city=None, language=None):
        resp = requests.get(url, headers=self.get_random_header())
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_ul = soup.find("ul", attrs={"class": "list-jobs"})
            if main_ul:
                li_list = main_ul.find_all("li", attrs={"class": "list-jobs__item"})
                for li in li_list:
                    title = li.find("div", attrs={"class": "list-jobs__title"}).text.strip()
                    href = title.a["href"]
                    cont = li.find("div", attrs={"class": "list-jobs__description"})
                    content = cont.text.strip()
                    company = 'no name'
                    comp = li.find("div", attrs={"class": "list-jobs__details__info"})
                    if comp:
                        company = comp.text
                    self.jobs.append({
                        "title": title,
                        "url": self.domain + href,
                        "description": content,
                        "company": company,
                        "city_id": city,
                        "language_id": language
                    })
            else:
                self.errors.append({"url": url, "title": "Ul does not exists!"})
        else:
            self.errors.append({"url": url, "title": "Page does not response!"})
        return self.jobs, self.errors
