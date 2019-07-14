# Problem Set 4A
# Name: <仲逊>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    #只有一个字符为递归基，直接返回
    if len(sequence)<=1:
        return list(sequence)
    #否则递归调用获取除去第一个字符之后字符串的全排列
    tem=get_permutations(sequence[1:])
    ans=[]
    #将第一个字符依次添加到tem中每个字符串中的不同位置
    for instance in tem:
        for i in range(len(instance)+1):
            tem_list=list(instance)
            tem_list.insert(i,sequence[0])
            ans.append("".join(tem_list))
    #将ans去重(防止重复字符产生的重复排列),然后按字典序排好后返回
    ans=list(set(ans))
    ans.sort()
    return ans

if __name__ == '__main__':
#    #EXAMPLE
    example_input1 = 'abc'
    print('Input:', example_input1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input1))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input2 = 'qwp'
    print('Input:', example_input2)
    print('Expected Output:', ['pqw', 'pwq', 'qpw', 'qwp', 'wpq', 'wqp'])
    print('Actual Output:', get_permutations(example_input2))
    
    example_input3 = 'aap'
    print('Input:', example_input3)
    print('Expected Output:', ['aap', 'apa', 'paa'])
    print('Actual Output:', get_permutations(example_input3))
    
    example_input4 = 'eiu'
    print('Input:', example_input4)
    print('Expected Output:', ['eiu', 'eui', 'ieu', 'iue', 'uei', 'uie'])
    print('Actual Output:', get_permutations(example_input4))

