from typing import List
from collections import namedtuple
import time


class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y


class Node(namedtuple("Node", "location left right")):
    """
    location: Point
    left: Node
    right: Node
    """

    def __repr__(self):
        return f'{tuple(self)!r}'


class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0

    def insert(self, p: List[Point]):
        """insert a list of points"""
        #The list is none
        if p is None:            
            return None
        #Even number of layers is divided by x, odd number of layers is divided by y
        p.sort(key=lambda k:k[self._n % 2],reverse=False)  
        #Find the median and take the larger one
        middle=len(p)//2 
        #Split point   
        node=p[middle]       
        #Divide data into left and right subtrees
        left_=p[:middle]       
        right_=p[middle+1:]
        #cycle
        self._n+=1     

        #Left child node
        left_node=Node()
        node.left=left_node
        left_node.parent=node
        insert(self,left_)

        #Right child node
        right_node=Node()
        node.right=right_node
        right_node.parent=Node
        insert(self,right_)
        
        pass

    def range(self, rectangle: Rectangle) -> List[Point]:
        """range query"""
        point_list=List()
        node=self._root
        #Judge whether the leaf is within the search range
        if node.left is None & node.right is None:
         if rectangle.is_contains(self,node):
             point_list.__add__(node)
           
        #For nodes with child nodes   
        else:
            #left part
            #if the search range completely enclose the range of split points of the current node,return all points in this node area
            if rectangle.intersection(node.left)==rectangle:
                for m in node.left:
                   point_list.__add__(m)
            #if the range intersects the range of the split point, recursively searching     
            elif rectangle.intersection(node.left) is not None:
                range(node.left,rectangle)
            #right part is similarly
            if rectangle.intersection(node.right)==rectangle:
                for n in node.right:
                   point_list.__add__(n)
            elif rectangle.intersection(node.right) is not None:
                range(node.right,rectangle)
        return point_list            
    pass


def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


if __name__ == '__main__':
    range_test()
    performance_test()