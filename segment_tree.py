class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()  # Store the array for updates
        self.tree = [None] * (4 * self.n)
        self.build(0, 0, self.n - 1)

    def build(self, node, start, end):
        if start == end:
            self.tree[node] = {
                "sum": self.arr[start],
                "min": self.arr[start],
                "max": self.arr[start],
                "product": self.arr[start]
            }
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self.build(left_child, start, mid)
            self.build(right_child, mid + 1, end)
            
            self.tree[node] = {
                "sum": self.tree[left_child]["sum"] + self.tree[right_child]["sum"],
                "min": min(self.tree[left_child]["min"], self.tree[right_child]["min"]),
                "max": max(self.tree[left_child]["max"], self.tree[right_child]["max"]),
                "product": self.tree[left_child]["product"] * self.tree[right_child]["product"]
            }

    def update(self, index, value, node=0, start=0, end=None):
        if end is None:
            end = self.n - 1
        
        if start == end:
            self.tree[node] = {
                "sum": value,
                "min": value,
                "max": value,
                "product": value
            }
            self.arr[index] = value  # Update the stored array
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            if index <= mid:
                self.update(index, value, left_child, start, mid)
            else:
                self.update(index, value, right_child, mid + 1, end)
            
            self.tree[node] = {
                "sum": self.tree[left_child]["sum"] + self.tree[right_child]["sum"],
                "min": min(self.tree[left_child]["min"], self.tree[right_child]["min"]),
                "max": max(self.tree[left_child]["max"], self.tree[right_child]["max"]),
                "product": self.tree[left_child]["product"] * self.tree[right_child]["product"]
            }

    def query(self, L, R, op, node=0, start=0, end=None):
        if end is None:
            end = self.n - 1
        
        if R < start or L > end:
            if op == "sum":
                return 0
            elif op == "min":
                return float("inf")
            elif op == "max":
                return float("-inf")
            elif op == "product":
                return 1  # Neutral element for multiplication
        
        if L <= start and end <= R:
            return self.tree[node][op]
        
        mid = (start + end) // 2
        left_result = self.query(L, R, op, 2 * node + 1, start, mid)
        right_result = self.query(L, R, op, 2 * node + 2, mid + 1, end)
        
        if op == "sum":
            return left_result + right_result
        elif op == "min":
            return min(left_result, right_result)
        elif op == "max":
            return max(left_result, right_result)
        elif op == "product":
            return left_result * right_result
