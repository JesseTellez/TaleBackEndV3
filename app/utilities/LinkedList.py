
class Node(object):
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next


class DoubleList(object):
    head = None
    first = head
    last = None

    def getLast(self):
        if self.head != None:
            self.last = self.head
            while (self.last.next != None):
                self.last = self.last.next
            return self.last
        else:
            return None

    def isEmpty(self):
        return self.head == None

    def count(self):
        if self.head != None:
            node = self.head
            count = 1
            while node.next != None:
                node = node.next
                count += 1
            return count
        else:
            return 0

    def node_at_index(self, index):
        if index >= 0:
            node = self.head
            i = index
            while node != None:
                if i == 0:
                    return node
                i -= 1
                node = node.next
        return None

    def nodesBeforeAndAfter(self, index):
        assert (index >= 0)
        i = index
        next = self.head

        while next != None and i > 0:
            i -= 1
            prev = self.head
            next = next.next

        assert (i == 0)
        return (prev, next)

    def insert(self, value, atIndex):
        prev, next = self.nodesBeforeAndAfter(atIndex)
        new_node = Node(value, None, None)
        new_node.prev = prev
        new_node.next = next
        prev.next = new_node
        next.prev = new_node

        if prev == None:
            self.head = new_node

    def removeAll(self):
        self.head = None

    def remove_node(self, node):
        prev = node.prev
        next = node.next

        if prev is not None:
            prev.next = next
        else:
            self.head = next

        next.prev = prev
        node.prev = None
        node.next = None
        return node.data

    def remove_last(self):
        assert (self.isEmpty is not True)
        return self.remove_node(self.last)

    def remove_at_index(self, index):
        node = self.node_at_index(index)
        assert (node is not None)
        return self.remove_node(node)
