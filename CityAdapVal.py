"""
    求适应值，路径总长（欧式路径和）
"""
def EucPathSum(D, path) -> float:
    sum = 0
    len = path.size
    for i in range(len):
        sum += D[path[i % len]][path[(i + 1) % len]]
    return sum