
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

RSS_FEED_URL = "http://feeds.bbci.co.uk/news/rss.xml"

def get_articles_from_rss(rss_url):
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries:
        url = entry.link
        title = entry.title
        category = entry.tags[0]['term'] if 'tags' in entry else "Non catégorisé"
        domain = urlparse(url).netloc  # Extraire le domaine

        # Récupérer le contenu de l'article avec BeautifulSoup
        content, page_title, image_url = extract_article_content(url)

        articles.append({
            "title": title,
            "url": url,
            "domain": domain,
            "category": category,
            "page_title": page_title,
            "content": content,
            "image": image_url
        })
    
    return articles

def extract_article_content(url):
    """Scrape le contenu de l'article."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Trouver le titre de la page
        page_title = soup.title.string if soup.title else "Titre inconnu"

        # Trouver le contenu principal de l'article (exemple : balises <p>)
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])

        # Trouver une image (facultatif)
        image_tag = soup.find("img")
        image_url = image_tag['src'] if image_tag else "Pas d'image"

        return content, page_title, image_url

    except Exception as e:
        print(f"Erreur lors de la récupération de l'article {url}: {e}")
        return "Erreur", "Erreur", "Erreur"

# Exécution du script
articles = get_articles_from_rss(RSS_FEED_URL)

# Affichage des articles récupérés
for article in articles[:5]:  # Limité aux 5 premiers articles
    print("Titre :", article["title"])
    print("URL :", article["url"])
    print("Domaine :", article["domain"])
    print("Catégorie :", article["category"])
    print("Titre de la page :", article["page_title"])
    print("Contenu (extrait) :", article["content"][:200], "...")  # Limite l'affichage du contenu
    print("Image :", article["image"])
    print("=" * 80)
