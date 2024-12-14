for candidato in range(len(poblacion[individuo][0])):
                costeCand = 0

                if poblacion[individuo][0][candidato][0] in cacheGlobalCandidatos:
                    costeCand = cacheGlobalCandidatos[poblacion[individuo][0][candidato][0]]
                else :    
                    for i in range(len(self.problema.candidatos)):
                        inicial = self.problema.intersecciones[self.problema.candidatos[i][0]]
                        final = self.problema.intersecciones[poblacion[individuo][0][candidato][0]]
                        costeCand += self.aEstrella(inicial, final) * poblacion[individuo][0][candidato][1]

                    cacheGlobalCandidatos[poblacion[individuo][0][candidato][0]] = costeCand

                if costeCand < solucionMin:
                    solucionMin = costeCand  



cache[posActual] = (nodo.estado.interseccion, nodo.coste) #Coste de inicio a nodo
                posActual += 1
                #Si tenemos A-B y A-C, tenemos B-C
                if posActual > 1:
                    for i in range(posActual-1):
                        if cache[i][0] == nodo.estado.interseccion:
                            continue
                        
                        cacheCandidatos[cache[i][0], nodo.estado.interseccion] = cache[i][0] - nodo.coste