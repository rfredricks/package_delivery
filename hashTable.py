# chaining hash table represents a hash table that handles collisions by chaining
class ChainingHashTable:
    # constructor, initial capacity of 10
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # insert function
    def insert(self, item):
        key = item[0]
        bucket = key % 10
        bucket_list = self.table[bucket]
        bucket_list.append(item)

    # lookup function
    def search(self, key):
        bucket = key % 10
        bucket_list = self.table[bucket]
        for list_item in bucket_list:
            if list_item[0] == key:
                return list_item
        return None

    # remove function
    def remove(self, key):
        bucket = key % 10
        bucket_list = self.table[bucket]
        for list_item in bucket_list:
            if list_item[0] == key:
                bucket_list.remove(list_item)

    # function to replace an item
    def replace(self, key, item):
        self.remove(key)
        self.insert(item)
