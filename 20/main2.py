class LinkedListNode:
    def __init__(self, val, orig_index, prev, next):
        self.val = val
        self.orig_index = orig_index
        self.prev = prev
        self.next = next

    def print_loop(self):
        print(self.val, end=", ")
        curr = self.next

        while curr != self:
            print(curr.val, end=", ")
            curr = curr.next

        print()

file = []

with open("input.txt") as f:
    for line in f.readlines():
        num = int(line)

        file.append(num * 811589153)

original_file = file[:]

head = LinkedListNode(file[0], 0, None, None)
curr = head

zero_node = None
nodes = [head]

for i in range(1, len(file)):
    curr.next = LinkedListNode(file[i], i, curr, None)
    curr = curr.next

    nodes.append(curr)

    if file[i] == 0:
        zero_node = curr

curr.next = head
head.prev = curr


# zero_node.print_loop()

for i in range(10):
    for orig_index, num in enumerate(original_file):
        print(orig_index)

        moves_left = num

        if moves_left <= -len(file):
            moves_left = moves_left % (len(file)-1) - (len(file)-1)

        while moves_left >= len(file):
            moves_left = moves_left % (len(file)-1)

        print(num, moves_left)

        if moves_left == 0:
            continue

        node_of_interest = head
        while node_of_interest.orig_index != orig_index:
            node_of_interest = node_of_interest.next

        insertion_node = node_of_interest

        old_prev = node_of_interest.prev
        old_next = node_of_interest.next

        old_prev.next = old_next
        old_next.prev = old_prev

        if moves_left > 0:
            while moves_left != 0:
                insertion_node = insertion_node.next
                moves_left -= 1

            new_prev = insertion_node
            new_next = insertion_node.next

        else:
            while moves_left != 0:
                insertion_node = insertion_node.prev
                moves_left += 1

            new_prev = insertion_node.prev
            new_next = insertion_node

        print(old_prev.orig_index, old_next.orig_index, new_prev.orig_index, new_next.orig_index)

        new_prev.next = node_of_interest
        node_of_interest.prev = new_prev

        new_next.prev = node_of_interest
        node_of_interest.next = new_next

    print()
    zero_node.print_loop()
    print()

_1k = 0
_2k = 0
_3k = 0

curr = zero_node

for i in range(3001):
    if i == 1000:
        _1k = curr.val

    if i == 2000:
        _2k = curr.val

    if i == 3000:
        _3k = curr.val

    curr = curr.next

zero_node.print_loop()

print(_1k + _2k + _3k)

pass