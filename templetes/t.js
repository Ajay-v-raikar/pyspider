def solution(A):
    for i in A:
        for j in A:
            if i-j==1:
                return True
    return False

print(solution([1,3,6,4,1,2]))