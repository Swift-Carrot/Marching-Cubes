import random
from ursina import Mesh, Vec3
from opensimplex import OpenSimplex


def generateMeshFromNoise(noise:list, surface:int = 0):
    '''
    Generates a mesh with the given noise.
    surface: The min value for a point to be considered out of the mesh
    '''
    
    vertices = []
    triangles = []
    sizeY = len(noise) - 1
    sizeZ = len(noise[0]) - 1
    sizeX = len(noise[0][0]) - 1
    offset = (sizeX * .5, sizeY * .5, sizeZ * .5)

    for y in range(sizeY):
        for z in range(sizeZ):
            for x in range(sizeX):
                i = ''
                corners = [
                    noise[y + 1][ z + 1][ x], noise[y + 1][ z + 1][ x + 1],
                    noise[y + 1][ z][ x + 1], noise[y + 1][ z][ x],
                    noise[y][ z + 1][ x], noise[y][ z + 1][ x + 1],
                    noise[y][ z][ x + 1], noise[y][ z][ x]]
                for c in corners: i += str(int(c >= surface))
                newTriangles = getTriangles(i)
                
                if newTriangles == None: continue
                newVertices = mapSegmentPoints(tuple(x - x0 for x, x0 in zip((x, y, z), offset)))
                vertices, triangles = add2Mesh(vertices, triangles, newVertices, newTriangles)
    
    m = Mesh(vertices=vertices, triangles=triangles)
    m.generate_normals()
    return m

def getNoiseGrid(shape:tuple=(1, 1, 1), s:int=.5, seed:int=None):
    '''
    Generates a noise grid
    shape: A tuple with the shape of the noise
    s: The scale of the noise. Default is .5 (I recomend values lower than 1)
    seed: The random seed for the noise. Default is a random int between -65536 and 65536
    '''
    
    if len(shape) < 3: return []
    if seed == None: 
        seed = random.randint(-65536, 65536)
        print('seed: %s' % seed)
    tmp = OpenSimplex(seed)

    return [[[tmp.noise3d(x*s + 0.2, y*s + 0.2, z*s + 0.2) for z in range(shape[0])] 
        for y in range(shape[2])] for x in range(shape[1])]

def add2Mesh(vertices, triangles, newVertices, newTriangles):
    '''
    Combines the given vertices and triangles into a single mesh removing the duplicates
    '''
    
    # Creating the abs triangles
    absTriangles = []
    for triangle in newTriangles:
        absTriangle = []
        for c in triangle:
            absTriangle.append(newVertices[c])
        absTriangles.append(absTriangle)    
    
    # Combine and de-abs
    for vertex in newVertices:
        if not vertex in vertices: vertices.append(vertex)

    for absTriangle in absTriangles:
        triangles.append([vertices.index(v) for v in absTriangle])
    
    return vertices, triangles

def mapSegmentPoints(vertex:tuple = (0, 0, 0), size:float = 1):
    '''
    Maps the given vertex to the segments of a cube of size: size
    '''

    vertices = [
        [.5, 0, 0], [1, 0, .5], [.5, 0, 1], [0, 0, .5],
        [.5, 1, 0], [1, 1, .5], [.5, 1, 1], [0, 1, .5],
        [0, .5, 0], [1, .5, 0], [1, .5, 1], [0, .5, 1]]
    
    for v in range(12):
        for c in range(3):
            vertices[v][c] = vertices[v][c] * size + vertex[c]
    
    return vertices

def getTriangles(i):
    '''
    Get the corresponding triangles for the desired I
    '''

    aCases = [
        [],
        [ 8, 3, 0],
        [ 9, 0, 1],
        [ 8, 3, 1, 8, 1, 9],
        [10, 1, 2],
        [ 8, 3, 0, 1, 2, 10],
        [ 9, 0, 2, 9, 2, 10],
        [ 3, 2, 8, 2, 10, 8, 8, 10, 9],
        [11, 2, 3],
        [11, 2, 0, 11, 0, 8],
        [11, 2, 3, 0, 1, 9],
        [ 2, 1, 11, 1, 9, 11, 11, 9, 8],
        [10, 1, 3, 10, 3, 11],
        [ 1, 0, 10, 0, 8, 10, 10, 8, 11],
        [ 0, 3, 9, 3, 11, 9, 9, 11, 10],
        [ 8, 10, 9, 8, 11, 10],
        [ 8, 4, 7],
        [ 3, 0, 4, 3, 4, 7],
        [ 1, 9, 0, 8, 4, 7],
        [ 9, 4, 1, 4, 7, 1, 1, 7, 3],
        [10, 1, 2, 8, 4, 7],
        [ 2, 10, 1, 0, 4, 7, 0, 7, 3],
        [ 4, 7, 8, 0, 2, 10, 0, 10, 9],
        [ 2, 7, 3, 2, 9, 7, 7, 9, 4, 2, 10, 9],
        [ 2, 3, 11, 7, 8, 4],
        [ 7, 11, 4, 11, 2, 4, 4, 2, 0],
        [ 3, 11, 2, 4, 7, 8, 9, 0, 1],
        [ 2, 7, 11, 2, 1, 7, 1, 4, 7, 1, 9, 4],
        [ 8, 4, 7, 11, 10, 1, 11, 1, 3],
        [11, 4, 7, 1, 4, 11, 1, 11, 10, 1, 0, 4],
        [ 3, 8, 0, 7, 11, 4, 11, 9, 4, 11, 10, 9],
        [ 7, 11, 4, 4, 11, 9, 11, 10, 9],
        [ 9, 5, 4],
        [ 3, 0, 8, 4, 9, 5],
        [ 5, 4, 0, 5, 0, 1],
        [ 4, 8, 5, 8, 3, 5, 5, 3, 1],
        [ 2, 10, 1, 9, 5, 4],
        [ 0, 8, 3, 5, 4, 9, 10, 1, 2],
        [10, 5, 2, 5, 4, 2, 2, 4, 0],
        [ 3, 4, 8, 3, 2, 4, 2, 5, 4, 2, 10, 5],
        [11, 2, 3, 9, 5, 4],
        [ 9, 5, 4, 8, 11, 2, 8, 2, 0],
        [ 3, 11, 2, 1, 5, 4, 1, 4, 0],
        [ 8, 5, 4, 2, 5, 8, 2, 8, 11, 2, 1, 5],
        [ 5, 4, 9, 1, 3, 11, 1, 11, 10],
        [ 0, 9, 1, 4, 8, 5, 8, 10, 5, 8, 11, 10],
        [ 3, 4, 0, 3, 10, 4, 4, 10, 5, 3, 11, 10],
        [ 4, 8, 5, 5, 8, 10, 8, 11, 10],
        [ 9, 5, 7, 9, 7, 8],
        [ 0, 9, 3, 9, 5, 3, 3, 5, 7],
        [ 8, 0, 7, 0, 1, 7, 7, 1, 5],
        [ 1, 7, 3, 1, 5, 7],
        [ 1, 2, 10, 5, 7, 8, 5, 8, 9],
        [ 9, 1, 0, 10, 5, 2, 5, 3, 2, 5, 7, 3],
        [ 5, 2, 10, 8, 2, 5, 8, 5, 7, 8, 0, 2],
        [10, 5, 2, 2, 5, 3, 5, 7, 3],
        [11, 2, 3, 8, 9, 5, 8, 5, 7],
        [ 9, 2, 0, 9, 7, 2, 2, 7, 11, 9, 5, 7],
        [ 0, 3, 8, 2, 1, 11, 1, 7, 11, 1, 5, 7],
        [ 2, 1, 11, 11, 1, 7, 1, 5, 7],
        [ 3, 9, 1, 3, 8, 9, 7, 11, 10, 7, 10, 5],
        [ 9, 1, 0, 10, 7, 11, 10, 5, 7],
        [ 3, 8, 0, 7, 10, 5, 7, 11, 10],
        [11, 5, 7, 11, 10, 5],
        [10, 6, 5],
        [ 8, 3, 0, 10, 6, 5],
        [ 0, 1, 9, 5, 10, 6],
        [10, 6, 5, 9, 8, 3, 9, 3, 1],
        [ 1, 2, 6, 1, 6, 5],
        [ 0, 8, 3, 2, 6, 5, 2, 5, 1],
        [ 5, 9, 6, 9, 0, 6, 6, 0, 2],
        [ 9, 6, 5, 3, 6, 9, 3, 9, 8, 3, 2, 6],
        [ 3, 11, 2, 10, 6, 5],
        [ 6, 5, 10, 2, 0, 8, 2, 8, 11],
        [ 1, 9, 0, 6, 5, 10, 11, 2, 3],
        [ 1, 10, 2, 5, 9, 6, 9, 11, 6, 9, 8, 11],
        [11, 6, 3, 6, 5, 3, 3, 5, 1],
        [ 0, 5, 1, 0, 11, 5, 5, 11, 6, 0, 8, 11],
        [ 0, 5, 9, 0, 3, 5, 3, 6, 5, 3, 11, 6],
        [ 5, 9, 6, 6, 9, 11, 9, 8, 11],
        [10, 6, 5, 4, 7, 8],
        [ 5, 10, 6, 7, 3, 0, 7, 0, 4],
        [ 5, 10, 6, 0, 1, 9, 8, 4, 7],
        [ 4, 5, 9, 6, 7, 10, 7, 1, 10, 7, 3, 1],
        [ 7, 8, 4, 5, 1, 2, 5, 2, 6],
        [ 4, 1, 0, 4, 5, 1, 6, 7, 3, 6, 3, 2],
        [ 9, 4, 5, 8, 0, 7, 0, 6, 7, 0, 2, 6],
        [ 4, 5, 9, 6, 3, 2, 6, 7, 3],
        [ 7, 8, 4, 2, 3, 11, 10, 6, 5],
        [11, 6, 7, 10, 2, 5, 2, 4, 5, 2, 0, 4],
        [11, 6, 7, 8, 0, 3, 1, 10, 2, 9, 4, 5],
        [ 6, 7, 11, 1, 10, 2, 9, 4, 5],
        [ 6, 7, 11, 4, 5, 8, 5, 3, 8, 5, 1, 3],
        [ 6, 7, 11, 4, 1, 0, 4, 5, 1],
        [ 4, 5, 9, 3, 8, 0, 11, 6, 7],
        [ 9, 4, 5, 7, 11, 6],
        [10, 6, 4, 10, 4, 9],
        [ 8, 3, 0, 9, 10, 6, 9, 6, 4],
        [ 1, 10, 0, 10, 6, 0, 0, 6, 4],
        [ 8, 6, 4, 8, 1, 6, 6, 1, 10, 8, 3, 1],
        [ 9, 1, 4, 1, 2, 4, 4, 2, 6],
        [ 1, 0, 9, 3, 2, 8, 2, 4, 8, 2, 6, 4],
        [ 2, 4, 0, 2, 6, 4],
        [ 3, 2, 8, 8, 2, 4, 2, 6, 4],
        [ 2, 3, 11, 6, 4, 9, 6, 9, 10],
        [ 0, 10, 2, 0, 9, 10, 4, 8, 11, 4, 11, 6],
        [10, 2, 1, 11, 6, 3, 6, 0, 3, 6, 4, 0],
        [10, 2, 1, 11, 4, 8, 11, 6, 4],
        [ 1, 4, 9, 11, 4, 1, 11, 1, 3, 11, 6, 4],
        [ 0, 9, 1, 4, 11, 6, 4, 8, 11],
        [11, 6, 3, 3, 6, 0, 6, 4, 0],
        [ 8, 6, 4, 8, 11, 6],
        [ 6, 7, 10, 7, 8, 10, 10, 8, 9],
        [ 9, 3, 0, 6, 3, 9, 6, 9, 10, 6, 7, 3],
        [ 6, 1, 10, 6, 7, 1, 7, 0, 1, 7, 8, 0],
        [ 6, 7, 10, 10, 7, 1, 7, 3, 1],
        [ 7, 2, 6, 7, 9, 2, 2, 9, 1, 7, 8, 9],
        [ 1, 0, 9, 3, 6, 7, 3, 2, 6],
        [ 8, 0, 7, 7, 0, 6, 0, 2, 6],
        [ 2, 7, 3, 2, 6, 7],
        [ 7, 11, 6, 3, 8, 2, 8, 10, 2, 8, 9, 10],
        [11, 6, 7, 10, 0, 9, 10, 2, 0],
        [ 2, 1, 10, 7, 11, 6, 8, 0, 3],
        [ 1, 10, 2, 6, 7, 11],
        [ 7, 11, 6, 3, 9, 1, 3, 8, 9],
        [ 9, 1, 0, 11, 6, 7],
        [ 0, 3, 8, 11, 6, 7],
        [11, 6, 7],
        [11, 7, 6],
        [ 0, 8, 3, 11, 7, 6],
        [ 9, 0, 1, 11, 7, 6],
        [ 7, 6, 11, 3, 1, 9, 3, 9, 8],
        [ 1, 2, 10, 6, 11, 7],
        [ 2, 10, 1, 7, 6, 11, 8, 3, 0],
        [11, 7, 6, 10, 9, 0, 10, 0, 2],
        [ 7, 6, 11, 3, 2, 8, 8, 2, 10, 8, 10, 9],
        [ 2, 3, 7, 2, 7, 6],
        [ 8, 7, 0, 7, 6, 0, 0, 6, 2],
        [ 1, 9, 0, 3, 7, 6, 3, 6, 2],
        [ 7, 6, 2, 7, 2, 9, 2, 1, 9, 7, 9, 8],
        [ 6, 10, 7, 10, 1, 7, 7, 1, 3],
        [ 6, 10, 1, 6, 1, 7, 7, 1, 0, 7, 0, 8],
        [ 9, 0, 3, 6, 9, 3, 6, 10, 9, 6, 3, 7],
        [ 6, 10, 7, 7, 10, 8, 10, 9, 8],
        [ 8, 4, 6, 8, 6, 11],
        [11, 3, 6, 3, 0, 6, 6, 0, 4],
        [ 0, 1, 9, 4, 6, 11, 4, 11, 8],
        [ 1, 9, 4, 11, 1, 4, 11, 3, 1, 11, 4, 6],
        [10, 1, 2, 11, 8, 4, 11, 4, 6],
        [10, 1, 2, 11, 3, 6, 6, 3, 0, 6, 0, 4],
        [ 0, 2, 10, 0, 10, 9, 4, 11, 8, 4, 6, 11],
        [ 2, 11, 3, 6, 9, 4, 6, 10, 9],
        [ 3, 8, 2, 8, 4, 2, 2, 4, 6],
        [ 2, 0, 4, 2, 4, 6],
        [ 1, 9, 0, 3, 8, 2, 2, 8, 4, 2, 4, 6],
        [ 9, 4, 1, 1, 4, 2, 4, 6, 2],
        [ 8, 4, 6, 8, 6, 1, 6, 10, 1, 8, 1, 3],
        [ 1, 0, 10, 10, 0, 6, 0, 4, 6],
        [ 8, 0, 3, 9, 6, 10, 9, 4, 6],
        [10, 4, 6, 10, 9, 4],
        [ 9, 5, 4, 7, 6, 11],
        [ 4, 9, 5, 3, 0, 8, 11, 7, 6],
        [ 6, 11, 7, 4, 0, 1, 4, 1, 5],
        [ 6, 11, 7, 4, 8, 5, 5, 8, 3, 5, 3, 1],
        [ 6, 11, 7, 1, 2, 10, 9, 5, 4],
        [11, 7, 6, 8, 3, 0, 1, 2, 10, 9, 5, 4],
        [11, 7, 6, 10, 5, 2, 2, 5, 4, 2, 4, 0],
        [ 7, 4, 8, 2, 11, 3, 10, 5, 6],
        [ 4, 9, 5, 6, 2, 3, 6, 3, 7],
        [ 9, 5, 4, 8, 7, 0, 0, 7, 6, 0, 6, 2],
        [ 4, 0, 1, 4, 1, 5, 6, 3, 7, 6, 2, 3],
        [ 7, 4, 8, 5, 2, 1, 5, 6, 2],
        [ 4, 9, 5, 6, 10, 7, 7, 10, 1, 7, 1, 3],
        [ 5, 6, 10, 0, 9, 1, 8, 7, 4],
        [ 5, 6, 10, 7, 0, 3, 7, 4, 0],
        [10, 5, 6, 4, 8, 7],
        [ 5, 6, 9, 6, 11, 9, 9, 11, 8],
        [ 0, 9, 5, 0, 5, 3, 3, 5, 6, 3, 6, 11],
        [ 0, 1, 5, 0, 5, 11, 5, 6, 11, 0, 11, 8],
        [11, 3, 6, 6, 3, 5, 3, 1, 5],
        [ 1, 2, 10, 5, 6, 9, 9, 6, 11, 9, 11, 8],
        [ 1, 0, 9, 6, 10, 5, 11, 3, 2],
        [ 6, 10, 5, 2, 8, 0, 2, 11, 8],
        [ 3, 2, 11, 10, 5, 6],
        [ 9, 5, 6, 3, 9, 6, 3, 8, 9, 3, 6, 2],
        [ 5, 6, 9, 9, 6, 0, 6, 2, 0],
        [ 0, 3, 8, 2, 5, 6, 2, 1, 5],
        [ 1, 6, 2, 1, 5, 6],
        [10, 5, 6, 9, 3, 8, 9, 1, 3],
        [ 0, 9, 1, 5, 6, 10],
        [ 8, 0, 3, 10, 5, 6],
        [10, 5, 6],
        [11, 7, 5, 11, 5, 10],
        [ 3, 0, 8, 7, 5, 10, 7, 10, 11],
        [ 9, 0, 1, 10, 11, 7, 10, 7, 5],
        [ 3, 1, 9, 3, 9, 8, 7, 10, 11, 7, 5, 10],
        [ 2, 11, 1, 11, 7, 1, 1, 7, 5],
        [ 0, 8, 3, 2, 11, 1, 1, 11, 7, 1, 7, 5],
        [ 9, 0, 2, 9, 2, 7, 2, 11, 7, 9, 7, 5],
        [11, 3, 2, 8, 5, 9, 8, 7, 5],
        [10, 2, 5, 2, 3, 5, 5, 3, 7],
        [ 5, 10, 2, 8, 5, 2, 8, 7, 5, 8, 2, 0],
        [ 9, 0, 1, 10, 2, 5, 5, 2, 3, 5, 3, 7],
        [ 1, 10, 2, 5, 8, 7, 5, 9, 8],
        [ 1, 3, 7, 1, 7, 5],
        [ 8, 7, 0, 0, 7, 1, 7, 5, 1],
        [ 0, 3, 9, 9, 3, 5, 3, 7, 5],
        [ 9, 7, 5, 9, 8, 7],
        [ 4, 5, 8, 5, 10, 8, 8, 10, 11],
        [ 3, 0, 4, 3, 4, 10, 4, 5, 10, 3, 10, 11],
        [ 0, 1, 9, 4, 5, 8, 8, 5, 10, 8, 10, 11],
        [ 5, 9, 4, 1, 11, 3, 1, 10, 11],
        [ 8, 4, 5, 2, 8, 5, 2, 11, 8, 2, 5, 1],
        [ 3, 2, 11, 1, 4, 5, 1, 0, 4],
        [ 9, 4, 5, 8, 2, 11, 8, 0, 2],
        [11, 3, 2, 9, 4, 5],
        [ 3, 8, 4, 3, 4, 2, 2, 4, 5, 2, 5, 10],
        [10, 2, 5, 5, 2, 4, 2, 0, 4],
        [ 0, 3, 8, 5, 9, 4, 10, 2, 1],
        [ 2, 1, 10, 9, 4, 5],
        [ 4, 5, 8, 8, 5, 3, 5, 1, 3],
        [ 5, 0, 4, 5, 1, 0],
        [ 3, 8, 0, 4, 5, 9],
        [ 9, 4, 5],
        [ 7, 4, 11, 4, 9, 11, 11, 9, 10],
        [ 3, 0, 8, 7, 4, 11, 11, 4, 9, 11, 9, 10],
        [11, 7, 4, 1, 11, 4, 1, 10, 11, 1, 4, 0],
        [ 8, 7, 4, 11, 1, 10, 11, 3, 1],
        [ 2, 11, 7, 2, 7, 1, 1, 7, 4, 1, 4, 9],
        [ 3, 2, 11, 4, 8, 7, 9, 1, 0],
        [ 7, 4, 11, 11, 4, 2, 4, 0, 2],
        [ 2, 11, 3, 7, 4, 8],
        [ 2, 3, 7, 2, 7, 9, 7, 4, 9, 2, 9, 10],
        [ 4, 8, 7, 0, 10, 2, 0, 9, 10],
        [ 2, 1, 10, 0, 7, 4, 0, 3, 7],
        [10, 2, 1, 8, 7, 4],
        [ 9, 1, 4, 4, 1, 7, 1, 3, 7],
        [ 1, 0, 9, 8, 7, 4],
        [ 3, 4, 0, 3, 7, 4],
        [ 8, 7, 4],
        [ 8, 9, 10, 8, 10, 11],
        [ 0, 9, 3, 3, 9, 11, 9, 10, 11],
        [ 1, 10, 0, 0, 10, 8, 10, 11, 8],
        [10, 3, 1, 10, 11, 3],
        [ 2, 11, 1, 1, 11, 9, 11, 8, 9],
        [11, 3, 2, 0, 9, 1],
        [11, 0, 2, 11, 8, 0],
        [11, 3, 2],
        [ 3, 8, 2, 2, 8, 10, 8, 9, 10],
        [ 9, 2, 0, 9, 10, 2],
        [ 8, 0, 3, 1, 10, 2],
        [10, 2, 1],
        [ 8, 1, 3, 8, 9, 1],
        [ 9, 1, 0],
        [ 8, 0, 3],
        []]
    
    i = int(i, base=2)
    
    if not i in (0, 256):
        return [aCases[i][x:x+3] for x in range(0, len(aCases[i]), 3)]
    else:
        return None