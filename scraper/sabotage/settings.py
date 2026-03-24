BOT_NAME = "sabotage_scraper"

SPIDER_MODULES = ["sabotage.spiders"]
NEWSPIDER_MODULE = "sabotage.spiders"

# Respeita o robots.txt
ROBOTSTXT_OBEY = True

# Delay entre requisições
DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True  # varia entre 0.5x e 1.5x o delay

# Máximo de requisições simultâneas
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# User-agent
USER_AGENT = (
    "Mozilla/5.0 (compatible; SabotageResearchBot/1.0; academic project)"
)

FEEDS = {
    "../data/letras_raw.json": {
        "format": "json",
        "encoding": "utf8",
        "indent": 2,
        "overwrite": True,
    }
}

# Log level (muda pra DEBUG se precisar depurar)
LOG_LEVEL = "INFO"