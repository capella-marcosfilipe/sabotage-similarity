import scrapy
import re


class SabotageSpider(scrapy.Spider):
    name = "sabotage"
    allowed_domains = ["vagalume.com.br"]
    start_urls = ["https://www.vagalume.com.br/sabotage/"]

    def parse(self, response):
        """
        Página do artista: coleta os links de cada música.
        Padrão de URL das letras: /sabotage/{slug}.html
        """
        links = response.css("a[href*='/sabotage/']::attr(href)").getall()

        # Filtra só URLs de letras: /sabotage/{slug}.html
        links_letras = [
            l for l in links  # noqa: E741
            if re.match(r"^/sabotage/[^/]+\.html$", l)
            and not any(excluir in l for excluir in [
                "discografia", "fotos", "relacionados",
                "popularidade", "noticias", "cifras"
            ])
        ]

        links_letras = list(dict.fromkeys(links_letras))  # remove duplicatas

        self.logger.info(f"Encontradas {len(links_letras)} músicas.")

        for href in links_letras:
            yield response.follow(href, callback=self.parse_letra)

    def parse_letra(self, response):
        """
        Página de cada música: extrai título e letra.

        Estrutura real do vagalume:
          <div id="lyrics">
            Linha 1<br>
            Linha 2<br>
            <br>
            Linha 3<br>
          </div>

        A letra está em texto direto separado por <br>, não em <p>.
        """

        # Título
        titulo = response.css("div#lyricContent h1::text").get()
        if not titulo:
            titulo = response.css("h1::text").get()
        if not titulo:
            titulo = (
                response.url.split("/")[-1]
                .replace(".html", "")
                .replace("-", " ")
                .title()
            )

        # Letra: texto direto dentro de div#lyrics (separado por <br>)
        container = response.css("div#lyrics")

        if not container:
            self.logger.warning(f"Container #lyrics não encontrado em: {response.url}")
            return

        # Pega todos os nós de texto dentro do container
        textos = container.css("::text").getall()

        # Limpa e filtra linhas vazias
        linhas = [t.strip() for t in textos if t.strip()]

        if not linhas:
            self.logger.warning(f"Letra vazia em: {response.url}")
            return

        letra_completa = "\n".join(linhas)

        yield {
            "titulo": titulo.strip(),
            "url": response.url,
            "letra": letra_completa,
        }