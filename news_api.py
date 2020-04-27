#Credit to News API for API Key
import requests
from tangelo.models import CustomPost, Widget, User
from tangelo import app, db, log

error_msg_global = "hmmm, something\'s not right."
MAX_POSTS = 10
def updateNews():

    news_url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=02f90cf35f2b4176a559db2847011096')

    try:
        response = requests.get(news_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        log.error('Error updating news widget', exc_info=True)
        raise Exception(error_msg_global)
    articles = data.get('articles')
    if not articles:
        return
    new_articles = []
    for i, article in enumerate(articles):
        if i >= MAX_POSTS:
            break
        if not article:
            continue
        title = article.get('title')
        content = article.get('content')
        source = article.get('source')
        if source:
            source = source.get('name')
        url = article.get('url')
        new_articles.append({'title': title, 'content': content, 'source': source})


    with app.app_context():
        news_widget = None
        try:
            news_widget = Widget.query.filter_by(alias_name='news').first()
            if not news_widget:
                log.critical('News widget not found')
                return
        except Exception as e:
            log.error('Error retrieving News Widget', exc_info=True)

        try:
            db.session.query(CustomPost).filter(CustomPost.widget_id==news_widget.id).delete()
            for a in new_articles:
                article_post = CustomPost(content=a['title'], custom_author=a['source'], widget=news_widget)
                db.session.add(article_post)
            news_widget.active = True
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            log.error('Error updating News Widget')
            try:
                news_widget.active = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                log.error('Error updating News Widget active status')



if __name__ =='__main__':
    updateNews()
