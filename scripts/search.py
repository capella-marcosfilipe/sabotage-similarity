import torch
from sentence_transformers import SentenceTransformer, util

# 1. Carregar o modelo (como já foi baixado antes, ele carrega rapidinho do cache local)
print("Carregando o modelo...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Carregar o índice de vetores salvo no disco
caminho_indice = '/home/elyyihz/PycharmProjects/av-2-pesquisa-por-similaridade-com-llm-v2-llm-sabotage/data/indice_letras.pt'
print("Carregando o banco de embeddings...")
dados_salvos = torch.load(caminho_indice, weights_only=False)

chunks_data = dados_salvos['chunks_data']
corpus_embeddings = dados_salvos['embeddings']


# 3. Criar a função que recebe o texto de entrada (Query) e busca
def buscar_similaridade(query, top_k=3):
    print(f"\n🔍 Buscando por: '{query}'")

    # Gerar o vetor da query usando o modelo
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Calcular a Similaridade do Cosseno entre a query e todos os chunks
    # O [0] no final é porque passamos apenas 1 query, então pegamos a primeira lista de resultados
    resultados = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)[0]

    print("\n" + "=" * 50)
    print(" RESULTADOS ENCONTRADOS ".center(50, "="))
    print("=" * 50)

    for hit in resultados:
        # Recuperar o ID do chunk para buscar os dados originais no JSON
        id_chunk = hit['corpus_id']
        score = hit['score']

        # Puxar os metadados do chunk usando o ID
        chunk_encontrado = chunks_data[id_chunk]

        print(f"🎵 Música: {chunk_encontrado['titulo']}")
        print(f"🎯 Score de Similaridade: {score:.4f}")  # Quão próximo de 1.0 (perfeito)
        print(f"📝 Trecho: {chunk_encontrado['texto']}")
        print(f"🔗 Link: {chunk_encontrado['url']}")
        print("-" * 50)


# 4. Testar a aplicação recebendo um texto de entrada!
texto_entrada = "Como é a dura realidade e a sobrevivência nas ruas do Brooklin?"
buscar_similaridade(texto_entrada, top_k=3)