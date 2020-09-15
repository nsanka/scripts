class Solution:
  def reverse(self, string):
    if len(string) == 0:
      return string
    else:
      return self.reverse(string[1:]) + string[0]

  def reverseIterative(self, string):
    answer = ''
    stack = [string]
    while len(stack):
      item = stack.pop()
      answer += item[-1]

      nextItem = item[:-1]
      if len(nextItem):
        stack.append(nextItem)
    return answer

a = 'hello'
print Solution().reverseIterative(a)
