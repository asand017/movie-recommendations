import os
import scrapy
from pathlib import Path
import pandas as pd

# TODO: crawling rotten tomatoes blocked, find work around, secure proxies?
class RottenTomatoesSpider(scrapy.Spider):
    name = "rotten_tomatoes"
    allowed_domains = ["rottentomatoes.com"]

    def start_requests(self):
        urls = []
        base_url = "https://www.rottentomatoes.com/m/"
        relative_path = '../raw/movies.csv'
        absolute_path = os.path.abspath(relative_path)
        meta = {'real_title': 'Civil War'}
        # df = pd.read_csv(absolute_path)
        # df['primaryTitle'] = df['primaryTitle'].str.replace(' ', '_').str.replace(r"[,\'\:\-\?]", '', regex=True)
        # df['primaryTitle'] = df['primaryTitle'].str.lower()

        # for title in df['primaryTitle']:
        #     cleaned_title = self.clean_titles(title)
        #     urls.append(str(base_url) + str(cleaned_title))

        urls = [
            # "https://www.rottentomatoes.com/m/civil_war_2024",
            # "https://www.rottentomatoes.com/m/bad_boys_ride_or_die",
            "https://www.rottentomatoes.com/m/furiosa_a_mad_max_saga",
            # "https://www.rottentomatoes.com/m/civil_war",
            # "https://www.rottentomatoes.com/m/dune_part_two",
            # "https://www.rottentomatoes.com/m/am_i_ok",
            # "https://www.rottentomatoes.com/m/were_all_going_to_the_worlds_fair"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        # self.log(f'RESPONSE: {response.body}')
        print("response text: " + response.request.body)
        real_title = response.meta.get('real_title')
        title = response.css('title::text').re(r'^(.*?)(?: \(\d{4}\))? \|')[0]
        release_date = response.xpath('//section[@class="media-info"]/div[@class="content-wrap"]/dl/div[@class="category-wrap"]/dt[contains(.,"Release Date")]/following-sibling::dd/rt-text/text()').get()
        director = str(response.xpath('//section[@class="media-info"]/div[@class="content-wrap"]/dl/div[@class="category-wrap"]/dt[contains(.,"Director")]/following-sibling::dd/rt-link/text()').getall())
        critic_rating = response.css('rt-button[slot="criticsScore"] > rt-text::text').get() 
        audience_rating = response.css('rt-button[slot="audienceScore"] > rt-text::text').get()
        description = response.css('drawer-more[slot="description"] > rt-text::text').get()
        
        if critic_rating is None:
            critic_rating = ''
            
        if audience_rating is None:
            audience_rating = ''
            
        if description is None:
            description = ''

        print("title: " + title)
        print("release date: " + release_date)
        print("director: " + director)
        print("critic_rating: " + critic_rating)
        print("audience rating: " + audience_rating)
        print("description: " + description)

        if(title == 'Civil War'):
            print("Civil war check")

        payload = {
            "title": title,
            "release_date": release_date,
            "director": director,
            "critic_rating": critic_rating,
            "audience_rating": audience_rating,
            "description": description
        }
        
        print("real title: " + real_title)
        print("checking for title: " + title)
        if (title != real_title):
            print("WRONG TITLE, crawl new url")
            base_url = "https://www.rottentomatoes.com/m/"
            relative_path = '../raw/movies.csv'
            absolute_path = os.path.abspath(relative_path)
            df = pd.read_csv(absolute_path)
            release_year = df[df['primaryTitle'] == real_title]['release_date']
            new_url = str(base_url) + self.clean_titles(real_title)+"_"+release_year
            print("new url: " + str(new_url))
            # yield scrapy.Request(url=new_url, callback=self.continue_parsing, )
            pass
        else:
            yield payload
            
        # if title not in df['primaryTitle']:
        #     print('crawled the wrong page, try again')
        #     nr = df['primaryTitle'].apply(lambda title_target: str(title_target).contains(title))
        #     matches = df[nr]
        #     print("next movie to search:")
            # print(matches)
            
        # target_movie = df[df['primaryTitle'] == title]
        # print(target_movie)
        
        
    def continue_parsing(self, response):
        pass
            
    def clean_titles(self, raw_title):
        # cleaned_title = '' 
        cleaned_title = raw_title.replace(' ', '_').str.replace(r"[,\'\:\-\?]", '', regex=True).lower()
        return cleaned_title
        # page = response.url.split("/")[-1]
        # filename = f"{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
