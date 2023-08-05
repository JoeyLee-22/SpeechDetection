def get_score(S1, S1_prime):
    scores = []
    
    for i in range(len(S1)):
        if (S1_prime[i] == ''):
            scores.append(0)
        elif (S1[i] == S1_prime[i]):
            scores.append(1)
        else:
            counter = 0
            for word_prime in S1_prime[i].split(' '):
                if word_prime in S1[i].split(' '):
                    counter+=1
                else:
                    counter+=0.75
            scores.append(counter/len(S1[i].split(' ')))

    return scores