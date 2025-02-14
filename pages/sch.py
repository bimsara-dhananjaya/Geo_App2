import streamlit as st
import requests
from bs4 import BeautifulSoup


def scrape_university_titles(urls):
    titles = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.text.strip()
                titles.append({'University': url, 'Title': title})
        except Exception as e:
            st.error(f'Error occurred while scraping {url}: {e}')
    return titles


def scrape_masters_courses(urls, keywords):
    masters_courses = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Modify this section based on the HTML structure of the university's website
                courses = soup.find_all('div', class_='master-course')
                for course in courses:
                    title = course.find('h2').text.strip()
                    description = course.find('p').text.strip()
                    link = url + course.find('a')['href'] if course.find(
                        'a')['href'].startswith('/') else course.find('a')['href']
                    if any(keyword.lower() in title.lower() for keyword in keywords):
                        masters_courses.append(
                            {'University': url, 'Title': title, 'Description': description, 'Link': link})
        except Exception as e:
            st.error(f'Error occurred while scraping {url}: {e}')
    return masters_courses


# Display the Streamlit application
st.title('Australian University Web Pages and Master\'s Courses')

# Input field for URLs
urls_input = st.text_area(
    'Enter URLs of Australian university websites (one URL per line):')

if st.button('Scrape University Titles'):
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    if urls:
        university_titles = scrape_university_titles(urls)
        if university_titles:
            st.write('Scraped university web page titles:')
            for title in university_titles:
                st.write(title)
        else:
            st.write('No titles found on the provided URLs.')
    else:
        st.warning('Please enter at least one URL.')

# Input field for master's course keywords
keywords_input = st.text_input(
    'Enter keywords to search for master\'s courses (comma-separated):')

if st.button('Scrape Master\'s Courses'):
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    keywords = [keyword.strip()
                for keyword in keywords_input.split(',') if keyword.strip()]
    if urls and keywords:
        masters_courses = scrape_masters_courses(urls, keywords)
        if masters_courses:
            st.write('Scraped master\'s courses matching the keywords:')
            for course in masters_courses:
                st.write(course)
        else:
            st.write(
                'No master\'s courses found matching the provided keywords on the provided URLs.')
    else:
        st.warning('Please enter at least one URL and keywords.')
