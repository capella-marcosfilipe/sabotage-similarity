# Web Scraping com Scrapy

Scrapy é uma ferramenta de scraping e crawling de dados em Python. Ele é usado para extrair informações de sites e armazená-las em um formato estruturado, como CSV, JSON ou bancos de dados.

Para este projeto usei como referência o tutorial <https://medium.com/@marlessonsantana/utilizando-o-scrapy-do-python-para-monitoramento-em-sites-de-not%C3%ADcias-web-crawler-ebdf7f1e4966>.

O alvo deste projeto foi o site vagalume.com.br. Inicialmente, tentei extrair de letras.mus.br, mas como ele renderiza as letras via JavaScript, o Scrapy não conseguiu extrair os dados. O vagalume, por outro lado, tem as letras diretamente no HTML, o que facilitou a extração.

Foram coletadas 40 letras de músicas!

Os resultados foram salvos em um arquivo CSV, que pode ser encontrado em `data/sabotage_letras.csv`. Este arquivo contém as letras das músicas da banda Sabotage, extraídas do site vagalume.com.br.
