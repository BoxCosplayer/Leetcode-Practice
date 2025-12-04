# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = ListNode()
        tail, currentCarry = head, 0

        while l1 or l2 or currentCarry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            addition = v1 + v2 + currentCarry

            digit = addition % 10
            carry = 1 if addition > 9 else 0

            currentCarry = carry
            tail.next = ListNode(digit)
            
            tail = tail.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return head.next
        