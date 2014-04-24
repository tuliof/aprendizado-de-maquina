# Exercício 4

Data de entrega 24/4 em aula

Use os dados [aqui](http://www.ic.unicamp.br/~wainer/cursos/1s2014/clust.csv) para o projeto de clusterização.

1. Faça a clusterizacao usando o k-means, com k=2 ate k=8. Para estes valores de k, use pelo menos duas medidas relativas de qualidade de cluster (por exemplo, variancia intercluster, Dunn, silhueta, ou outros) para decidir qual é o melhor k. Vamos chamar este k de km (k melhor).
2. Plote os clusters para o km e para um outro valor bem diferente (k=2 ou k=8). Verifique as diferencas entre as 2 clusterizacoes.
3. Para o seu valor de km, gere 3 clusterizacoes com inicializações diferentes. Compare os clusteres. O que a estabilidade ou não estabilidade dos clusteres te diz.
4. Para o seu valor de km, gere uma mistura de gaussianas (GMM) usando EM. Compare os centros das gaussianas com o centro dos seus clusters.
5. Use a clusterização hierarquica com "single linkage", "average linkage" e "complete linkage". Corte as arvores resultantes em km clusters. Compare estas tres particoes com o resultado do k-means.

# Consulta

[Finding the K in K-Means Clustering](http://datasciencelab.wordpress.com/2013/12/27/finding-the-k-in-k-means-clustering/)

[Improved Seeding For Clustering With K-Means++](http://datasciencelab.wordpress.com/2014/01/15/improved-seeding-for-clustering-with-k-means/)

[Selection of K in K-means Clustering, Reloaded](http://datasciencelab.wordpress.com/2014/01/21/selection-of-k-in-k-means-clustering-reloaded/)