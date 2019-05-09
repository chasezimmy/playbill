import json
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from helpers.connection import DB
import env


def get_auditions():

    session = HTMLSession()
    r = session.get(url=env.URL)

    auditions = {}
    
    rows = json.loads(r.content)['tiles']
    
    for row in rows: 
        soup = BeautifulSoup(row, 'html.parser')

        audition_id = soup.find('a').get('href')[-36:]
        title = soup.find(class_="pb-tile-title").text.strip()
        category = soup.find(class_="pb-tile-category").text.strip()
        organization = str(soup.find(class_="pb-tile-location")).split('>')[1].split('<')[0].strip()
        state = soup.find(class_="pb-tile-location").text.strip()[-2:]
        paid = soup.find(class_="pb-tile-tag-job-paid").text.strip() if soup.find(class_="pb-tile-tag-job-paid") else None
        date = soup.find(class_="pb-tile-post-date").text.strip()
        link = soup.find('a').get('href')

        audition = {
            'audition_id': audition_id,
            'title': title,
            'category': category,
            'organization': organization,
            'state': state,
            'paid': paid,
            'date': date,
            'link': link
        }

        auditions[audition_id] = audition

    return auditions


def save_auditions(auditions):

    with DB() as db:
        c = db.cur

        for key, audition in auditions.items():

            row = c.execute("SELECT audition_id FROM auditions WHERE audition_id=?", (audition['audition_id'],)).fetchone()

            if row:
                pass
            else:
                sql = """
                      INSERT INTO auditions (audition_id, title, category, organization, state, paid, date, link, group_id)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """
                sql_vars = (audition['audition_id'],
                            audition['title'],
                            audition['category'],
                            audition['organization'],
                            audition['state'],
                            audition['paid'],
                            audition['date'],
                            audition['link'],
                            None)
                c.execute(sql, sql_vars)

        db.conn.commit()
        db.conn.close()