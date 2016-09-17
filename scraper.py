import requests
from bs4 import BeautifulSoup
import re


def find_serial_page(homepage, serial_title):
    serial_title = serial_title.replace(' ', '+')
    html_data = requests.get(homepage).text
    soup = BeautifulSoup(html_data, 'html.parser')
    for link in soup.findAll('a'):
        url = link.get('href')
        if is_url_valid(url):
            if serial_title in url:
                return url
    return None


def get_seasons(serial_url):
    season_urls = []
    serial_page_html_data = requests.get(serial_url).text
    soup = BeautifulSoup(serial_page_html_data, 'html.parser')
    for link in soup.findAll('a'):
        next_url = link.get('href')
        if is_url_valid(next_url):
            if re.search(r'Season\+\d+$', next_url):
                season_urls.append(next_url)
    return season_urls


def get_episodes(seasons_urls):
    all_episodes = set()
    for season_url in seasons_urls:
        season_html_data = requests.get(season_url).text
        soup = BeautifulSoup(season_html_data, 'html.parser')
        for link in soup.findAll('a'):
            episode_url = link.get('href')
            if is_url_valid(episode_url):
                if re.search(r'Season\+\d+/(\w*\+*)+$', episode_url):
                    all_episodes.add(episode_url)
    return list(all_episodes)


def get_songs(all_episodes):
    all_song_titles = []
    all_song_artists = []
    for episode in all_episodes:
        episode_html_data = requests.get(episode).text
        soup = BeautifulSoup(episode_html_data, 'html.parser')
        for span in soup.findAll('span', {'class': 'song_title'}):
            all_song_titles.append(span.string)
        for span in soup.findAll('span', {'class': 'song_artist'}):
            all_song_artists.append(span.string)
    title_artist_dictionary = {}
    for i in range(len(all_song_artists)):
        title_artist_dictionary.update({all_song_artists[i]: all_song_titles[i]})
    return title_artist_dictionary


def songs_to_yt_search_links(all_songs):
    all_links = []
    for artist, title in all_songs.items():
        new_link = 'https://www.youtube.com/results?search_query=' + artist + ' ' + title
        all_links.append(new_link.replace(' ', '+'))
    return all_links


def search_to_video_links(search_links):
    all_video_links = []
    for link in search_links:
        search_page_html_data = requests.get(link).text
        link_id = re.search(r'watch\?v=\w+', search_page_html_data)
        if link_id:
            all_video_links.append('https://www.youtube.com/' + link_id.group(0))
    return all_video_links


def is_url_valid(url):
    if url is not None and '#' not in url:
        return True
    return False


# Testing here
u = find_serial_page('http://www.heardontv.com/tvshows', 'Unforgettable')
s = get_seasons(u)
e = get_episodes(s)
m = get_songs(e)
l = songs_to_yt_search_links(m)
search_to_video_links(l)


