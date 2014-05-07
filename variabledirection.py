# -*- coding: utf-8 -*-

from math import *

def vardir(f, U, psi1, psi2, psi3, psi4, M, K, N, x0, X, y0, Y, t0, T, n): 
    
    Un = []
    
    tau = (T-t0)/float(N)
    h1 = (X-x0)/float(M)
    h2 = (Y-y0)/float(K)
    
    # Первый шаг
    
    n -= 0.5
    
    S = [] # Промежуточный (дробный) слой
    s = [0]*(M+1) # Ряд дробного слоя
       
    for m in xrange(M+1):
        s[m] = psi3(t0+n*tau, x0+m*h1) # Граничное условие 3 (нижняя граница)
    
    S.append(list(s))
    
    for k in xrange(1,K):
        s[0] = psi1(t0+n*tau, y0+k*h2) # Граничное условие 1 (левая граница)
        
        # Прогонка
                
        A = -tau/(2*h1*h1)
        B = 1 + tau/(h1*h1)
        C = -tau/(2*h1*h1)
        D = lambda m: tau/2.0 * ( f(t0+n*tau, x0+m*h1, y0+k*h2) + (U[k+1][m]-2*U[k][m]+U[k-1][m])/(h2*h2) ) + U[k][m]
        
        Alpha = [-C/B]*M
        Beta  = [D(0)/B]*M    
        
        # Прогонка вперёд    
        
        for m in xrange(1,M):
            Alpha[m] = -C / (A*Alpha[m-1] + B)
            Beta[m] = (D(m) - A*Beta[m-1]) / (A*Alpha[m-1] + B)
            
        s[M] = psi2(t0+n*tau, y0+k*h2) # Граничное условие 2 (правая граница)
        
        # Прогонка назад
        
        for m in xrange(M-1,0,-1):
            s[m] = Alpha[m]*s[m+1] + Beta[m]     
        
        S.append(list(s))
           
    for m in xrange(M+1):
        s[m] = psi4(t0+n*tau, x0+m*h1) # Граничное условие 4 (верхняя граница)
        
    S.append(list(s))
            
    ############################################################################
    ############################################################################
    ############################################################################
        
    # Второй шаг
    
    n += 0.5
    
    # Сначала инициализируем итоговую матрицу
    
    Un = [] # Результирующий слой
    
    for k in xrange(K+1):
        Un.append([0]*(M+1))   
        
    for k in xrange(K+1):
        Un[k][0] = psi1(t0+n*tau, y0+k*h2) # Граничное условие 1 (левая граница)
        Un[k][M] = psi2(t0+n*tau, y0+k*h2) # Граничное условие 2 (правая граница)        
    
    for m in xrange(1,M):
        
        Un[0][m] = psi3(t0+n*tau, x0+m*h1) # Граничное условие 3 (нижняя граница)
        
        # Прогонка
                
        A = -tau/(2*h2*h2)
        B = 1 + tau/(h2*h2)
        C = -tau/(2*h2*h2)
        D = lambda k: tau/2.0 * ( f(t0+n*tau, x0+m*h1, y0+k*h2) + (S[k][m+1]-2*S[k][m]+S[k][m-1])/(h1*h1) ) + S[k][m]
        
        Alpha = [-C/B]*K
        Beta  = [D(0)/B]*K   
        
        # Прогонка вперёд    
        
        for k in xrange(1,K):
            Alpha[k] = -C / (A*Alpha[k-1] + B)
            Beta[k] = (D(k) - A*Beta[k-1]) / (A*Alpha[k-1] + B)
            
        Un[K][m] = psi4(t0+n*tau, x0+m*h1) # Граничное условие 4 (верхняя граница)
            
        # Прогонка назад
        
        for k in xrange(K-1,0,-1):
            Un[k][m] = Alpha[k]*Un[k+1][m] + Beta[k] 
               
    return Un