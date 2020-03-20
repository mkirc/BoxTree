# 3D Partitioning in rectangular Geometry

## Intro

### Death Volume

This Program tackles the following problem:

Imagine a set of points in 3D space. They represent the top right corner
of a rectangular Box. This position vector defines our object, where the
bottom left corner sits in the origin. It has a Volume denoted by:

```
V = x * e̅,x + y * e̅,y + z * e̅,z 
```

You got a bunch of these scattered in space, and you want to find another
set of Boxes, which enclose all of these Points, and also minimize the
death volume. Death volume is defined by:

```
Vᵦ,d = ∑ⁿ(Vᵦ - Vᵢ)			, where		Vᵦ = Volume of outer Box
							Vᵢ = Volume of Point i 
							n = Number of Points in outer Box
```

```
    ^                                         
 y  |                                         
    |------------------B                      
    |//////////////////|                      
    |---------------P//|   B: Box(x,y)        
    |               |//|   P: Point(x,y)      
    |               |//|   /: Death Volume    
    |               |//|                      
    |               |//|                      
    |               |//|                      
    |               |//|                      
    |               |//|                      
    -------------------------->               
                           x     
```

### kd - Trees

The lets look at a divide-and-conqer strategy: a tree. More precisely,
a 3dimensional bipartion tree or short: kdTree. I'll just summarize some
key details here, you can read read the rest on [wikipedia](https://en.wikipedia.org/wiki/K-d_tree).

The tree takes a set of Points, an axis, a discriminat and a depth.
Now it splits the set of Points along the axis on the discriminant,
which is a value exactly in the center between Zero and the maximal
Value a Point in the set has on that axis. Then the axis is rotated, 
in my code i do

```python
axis = (axis + 1) % 3
```

and the depth is decremented. Those values are passed to the new
children Nodes, and the split is recursively applied, until the 
depth is Zero.

We call the old space Parent and the new ones leftChild, if the Point-
dimension in question was smaller than the discriminator and rightChild,
if its Points had greater values in that dimension. 

After the programm halts, the old Pointspace is partitioned into
2 ^ (depth) Subspaces. 

If such a split makes sense in the context of death volume
minimization, we have to do some (fairly easy) math:

### Death Volume difference 

To adress the 'quality' of a split, lets look at an exmple in 2D:

```
     ^                                         
  y  |-----------B|-----------A                
     |            |           |                
     |            |           |                
     |            |        P  |                
     |            |           |                
     |            |           |                
     |  P'      P'|   P       |                
     |            |           |                
     |        P'  |          P|                
     |            |           |                
     |            |           |                
     -------------|------------>               
                  d         x                
```

In the case the split is done, the total death volume is just the sum
of those of the two spaces A and B, where

```
Vₐ,d + Vᵦ,d = ∑ᴺ(Vₐ - Vᵢ) + ∑ᴷ(Vᵦ - Vᵢ')
```

In the case of no split:

```
    ^                                         
 y  |------------------------A                
    |                        |                
    |                        |                
    |                     P  |                
    |                        |                
    |                        |                
    |  P'     P'     P       |                
    |                        |                
    |        P'             P|                
    |                        |                
    |                        |                
    -------------------------->               
                           x                                                    
```

the death volume of the whole thing is

```
Vₐ,d|notB = ∑ᴺ(Vₐ - Vᵢ) + ∑ᴷ(Vₐ - Vᵢ')
```

To give us an idea of the difference in death volume we do:

```
Vₐ,d|notB – Vₐ,d + Vᵦ,d 	= 	∑ᴺVₐ - ∑ᴺVᵢ + ∑ᴷVₐ - ∑ᴷ Vᵢ'
				       –(∑ᴺVₐ - ∑ᴺVᵢ + ∑ᴷVᵦ - ∑ᴷ Vᵢ')
				=	∑ᴷ(Vₐ - Vᵦ)
```

This leaves us with a quantity i will call ∆V,d(A,B).
As we will see, this is a excellent measure of a split.

### ∆V,d in Nodes

The situation presented above corresponds exactly to parent- 
and children-Nodes in the kdTree, where A = Parent and
B = leftChild. We can now assign to each Node a ∆V,d, where 
leftChild-Nodes get ∆V,d(Parent, leftChild) and rightChild-
Nodes inherit those of their parents. 
After all, their volume is identical, so they make no 
difference in terms of ∆V,d.

### and finally...

Now we can build the tree with a modified split function, which
takes ∆V,d into consideration. We end up with a list of leaves,
in which each has a 3D Point of their top right corner, and a
∆V,d - Value. Now we just compile a list of those having a
positive ∆V,d, plus the largest nonempty Node and sort them in 
descending order.

Here are our best N Boxes, which also minimize the death volume.

## Usage

tbd

## Todo

-	Define a Metric for assessing progress ✔
-	Load Points ✔
-	Build kd Tree over Point Space ✔
-	compare new death volume to initial ✔
-	Rotate / compare initial Placement of Hyperplane
-	Draw Graphs!!

