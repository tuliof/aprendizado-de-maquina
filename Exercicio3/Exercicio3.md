# Exercício 3

Data de entrega 10/4 em aula

Use os dados [Sonar, Mines vs Rocks dataset](http://archive.ics.uci.edu/ml/datasets/Connectionist+Bench+%28Sonar,+Mines+vs.+Rocks%29) do UCI Machine Learning Repository.

1. Discuta se é preciso normalizar os dados ou não. Se for preciso faça a normalizaçao.
2. Faça um PCA para redução da dimensionalidade. Quantas dimensões manter?

Voce vai verificar qual dentre os algoritmos abaixo é o melhor para classificar os dados.

  * SVM Linear (C de 1e-3 a 1e4 em multiplos de 10)
  * SVM RBF (C e gamma de 1e-3 a 1e4 em multiplos de 10)
  * K vizinhos (K = 1,3,5,11,21,31)
  * Random forest (mtry = 2,3,5,10,20,40,60)

1. Verifique que algoritmo tem a melhor acuracia media. Vamos usar o desenho experimental discutido em classe, de um k-fold para medir a acuracia media e um k-fold interno para escolher os hiperparametros (para cada conjunto de folds de treino). O algoritmo experimental esta descrito abaixo. Use 5-fold tanto para a avaliacao externa (para calcular a acuracia media) quanto para o loop interno (para escolher os hiperparametros.
2. Verifique se há diferenca entre usar ou nao a reducao de dimensionalidade discutida acima para cada algoritmo - ou seja reducao de dimensionalidade ajuda um SVM linear, etc?
3. Verificque para os dados originais se há muita diferenca entre escolha dos melhores hiperparametros entre os diferentes folds, para cada um dos algoritmos acima.

```
divida os dados em k folds
usando o fold i como teste e os outros como treino (-i)
    para todos os valores dos hiperparametros
       divida o treino (-i) em q folds
       usando o fold j para teste e os outros (-j) para treino
          treine o classificador com (-j) e com os valores dos hiperparametros
          calcule a acuracia do classificador em j
       calcule a acuracia media para esse conjunto de hiperparametros
    h_i e o conjunto de hiperparametros com maior acuracia media
    treine (-i) com h_i e meca a acuracia a_i
reporte a acuracia media entre os a_i
```

**ou em python**
```python
out=0
for TR,TE in kfold(DADOS,k):
    maxacc=0
    for H in hipergrid():
        accur=0
        for TR2,TE2 in kfold(TR,q):
            classific=train(TR2,H)
            accur+=test(classific,TE2)
        if accur>maxacc:
            maxacc=accur
            maxhiper=H
    class2=train(TR,maxhiper)
    out+=test(class2,TE)
print out/k
```

onde:
  * kfold(X,k) dado um conjunto de dados X e um parametro k, retorna tuplas (TREINO, TESTE) segundo o protocolo de k-folds.
  * hipergrid() retorna tuplas com as varias combinacoes de valores para os hiperparametros
  * train(TREINO,hiperpar) retorna um classificador treinado no conjunto TREINO e com hiperparametros hiperpar.
  * teste(CL,TESTE), retorna a acuracia do classificador CL nos dados TESTE

É tambem possivel trocar a ordem dos dois "for" de dentro

```python
    for TR2,TE2 in kfold(TR,q):
         for H in hipergrid():
```