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