import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import utils

def T(v):
    w = np.zeros((3,1))
    w[0,0] = 3*v[0,0]
    w[2,0] = -2*v[1,0]

    return w 

v = np.array([[3], [5]])
w = T(v)

print (v , w)

u = np.array([[1], [-2]])
v = np.array([[2], [4]])

k = 7

print("T(k*v):\n",T9k*v), "\n k*T(v):\n", k*T(v), "\n\n")
print("T(u+v):\n", T(u+v), "\n\n T(u)+T(v):\n", T(u)+T(v))

def L(v):
    A = np.array([[3,0], [0,0], [0,-2]])
    print("Transformation matrix:\n", A, "\n")
    w = A @ v

    return w 

v = np.array([[3],[5]])
w = L(v)
print("Original vector:\n", v, "\n\n Result of the Transformation:\n", w)

img = np.loadtxt('data/image.txt')
print('Shape: ',img.shape)
print(img)

plt.scatter(img[0], img[1], s = 0.001, color = 'black')

def T_hscaling(v):
    A = np.array([[2,0], [0,1]])
    w = A @ v 
    return w 

def Transform_vectors(T, v1, v2):
    V = np.hstack((v1,v2))
    W = T(V)

    return W 

e1 = np.array([[1], [0]])
e2 = np.array([[0], [1]])

transformation_result_hscaling = Transform_vectors(T_hscaling, e1, e2)

print("Original vectors:\n e1= \n", e1, "\n e2=\n", e2, "\n\n Result of the transformation (matrix form):\n", transformation_result_hscaling)

utils.plot_transformation(T_hscaling,e1,e2)
plt.scatter(img[0], img[1], s = 0.001, color = 'black')
plt.scatter(T_hscaling(img)[0], T_hscaling(img)[1], s = 0.001, color = 'grey')

def T_reflection_yaxis(v):
    A = np.array([[-1,0], [0,1]])
    w = A @ v

    return w 

e1 = np.array([[1], [0]])
e2 = np.array([[00], [1]])

transformation_result_reflection_yaxis = Transform_vectors(T_reflection_yaxis, e1, e2)
print("Original vectors:\n e1= \n", e1, "\n e2=\n", e2, "\n\n Result of the transformation (matrix form):\n", transformation_result_reflection_yaxis)
utils.plot_transformation(T_reflection_yaxis, e1, e2)

plt.scatter(img[0],img[1],s=0.001,color='black')
plt.scatter(T_reflection_yaxis(img)[0], T_reflection_yaxis(img)[1], s=0.001,color='grey')

def T_stretch(a, v):
    """
    Perform a 2D stretching transformation on a vector v using a stretching factor a.

    Args:
        a (float): The stretching factor.
        v (numpy.array): The vector (or vectors) to be stretched.

    Returns:
        numpy.array: The stretched vector.

    """

    T = np.array([[a,0],[0,a]])
    w = T @ v
    return w 

plt.scatter(img[0], img[1], s=0.001, color = 'black')
plt.scatter(T_stretch(2, img)[0], T_stretch(2,img)[1], s=0.001, color='grey')
utils.plot_transformation(lambda v: T_stretch(2,v), e1, e2)

def T_hshear(m, v):
    """
    Performs a 2D horizontal shearing transformation on an array v using a shearing factor m.

    Args:
        m (float): The shearing factor.
        v (np.array): The array to be sheared.

    Returns:
        np.array: The sheared array.
    """

    T = np.array([[1,m],[0,1]])
    w = T @ v
    return w 

plt.scatter(img[0], img[1], s=0.001, color='black')
plt.scatter(T_hshear(2,img)[0], T_hshear(2,img)[1], s=0.001, color='grey')
utils.plot_transformation(lambda v: T_hshear(2, v), e1, e2)


def T_rotation(theta, v):
    """
    Performs a 2D rotation transformation on an array v using a rotation angle theta.

    Args:
        theta (float): The rotation angle in radians.
        v (np.array): The array to be rotated.

    Returns:
        np.array: The rotated array.
    """

    T = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    w = T @ v
    return w 

plt.scatter(img[0],img[1],s=0.001,color='black')
plt.scatter(T_rotation(np.pi,img)[0], T_rotation(np.pi,img)[1],s=0.001,color='grey')

utils.plot_transformation(lambda v: T_rotation(np.pi, v), e1, e2)

def T_rotation_and_stretch(theta, a, v):
    """
    Performs a combined 2D rotation and stretching transformation on an array v using a rotation angle theta and a stretching factor a.

    Args:
        theta (float): The rotation angle in radians.
        a (float): The stretching factor.
        v (np.array): The array to be transformed.

    Returns: 
        np.array: The transformed array.
    """

    rotation_T = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    stretch_T = np.array([[a,0],[0,a]])

    w = stretch_T @ (rotation_T @ v)
    return w

plt.scatter(img[0], img[1], s=0.001, color='black')
plt.scatter(T_rotation_and_stretch(np.pi, 2, img)[0], T_rotation_and_stretch(np.pi, 2, img)[1], s=0.001, color='grey')

utils.plot_transformation(lambda v: T_rotation_and_stretch(np.pi, 2, v), e1, e2)


