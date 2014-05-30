#Exercício 2

Data de entrega 25/3 em aula

ATENCAO - Mudanca na parte do PCA - 21/3

No arquivo zip train17.zip contém uma coleção de imagens PGM de dígitos 1 e 7 manuscritos. Cada imagem do conjunto possui 64 x 64 pixels no formato PGM onde cada pixel tem um valor 0 ou 1. Cada imagem tem um nome no formato X_yyy.BMP.inv.pgm onde X é o dígito representado na imagem.

O arquivo test17.zip contem images de teste no mesmo formato.

Os arquivos PGM começam com 3 linhas:
> P2
> 64 64
> 1

Que não nos interessam, seguido de 64x64 digitos, separados por um branco ou mudança de linha. Este projeto trata estes 64x64 digitos como os atributos/dimensões de cada dado. A classe do dado é o digito representado (de 0 a 9) que esta no nome do arquivo.

 - Leia os dados do treino e teste
 
 - Use os dados do treino para o aprendizado k-NN. e rode o k-NN para os dados do teste. Meça a taxa de erro - a proporção de dados do conjunto de teste que o k-NN atribui uma classe que não é a correta (voce tem a classe correta no nome do arquivo).
 
 - Faça o processo para k=1,3,5,11,17,21.
 	- Qual k tem a menor taxa de acerto?
 
 - Reduza significativamente (para 100 e depois 40 dimensões) as dimensões do conjunto de treino usando o PCA.
 
 - Repita o experimento acima, para os dados de treino com a dimensão reduzida. Não se esqueça de transformar os dados de teste pela rotação do PCA dos dados de treino (veja abaixo).
 	- Qual é o novo melhor k?
 	- Houve modificação na taxas de erro?

ATENCAO Há uma complicação quanto ao PCA. Há mais dimensões do que dados e por isso as técnicas de PCA que usam a matriz de covariância não funcionam - eles não conseguem extrair os autovetores (não sei exatamente por que). Mas a técnica mais comum de calcular o PCA é através da decomposição SVD da matriz original. Essa técnica funciona nos casos onde há mais dimensões que dados. Portanto usem PCAs baseados em SVD (por exemplo prcomp do R)

Repita o exercicio para os arquivos train49.zip de treino e test49.zip de teste para os digitos 4 e 9.


Como usar o PCA no R.
n é o numero de dimensoes a manter

pca<- prcomp(treino)
novotreino<-pca$x[,1:n]
novoteste<-scale(teste,pca$center,pca$scale)%*%pca$rotation[,1:n]
A primeira linha calcula o PCA. A segunda retorna os dados de treino convertidos pelo PCA - voces devem ter feito algo parecido no Exercicio 1. A terceira linha usa o PCA dos dados de treino para converter os dados de teste para as mesmas dimensoes tranformadas do dado de treino

|    Name   |   Phone   |
|-----------|-----------|
| Anna      | 123456789 |
| Alexander | 987654321 |
| _         |           |