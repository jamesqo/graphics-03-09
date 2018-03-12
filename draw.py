import math

from display import *
from matrix import *

def make_h_inverse():
    mat = new_matrix(rows=4, cols=4)
    # Note: Indexed by column, then by rows
    mat[0][0] = 2
    mat[1][0] = -2
    mat[2][0] = 1
    mat[3][0] = 1

    mat[0][1] = -3
    mat[1][1] = 3
    mat[2][1] = -2
    mat[3][1] = -1

    mat[0][2] = 0
    mat[1][2] = 0
    mat[2][2] = 1
    mat[3][2] = 0

    mat[0][3] = 1
    mat[1][3] = 0
    mat[2][3] = 0
    mat[3][3] = 0
    
    return mat

def make_b():
    mat = new_matrix(rows=4, cols=4)

    mat[0][0] = 1
    mat[1][0] = 3
    mat[2][0] = -3
    mat[3][0] = 1
    
    mat[0][1] = 3
    mat[1][1] = -6
    mat[2][1] = 3
    mat[3][1] = 0
    
    mat[0][2] = -3
    mat[1][2] = 3
    mat[2][2] = 0
    mat[3][2] = 0

    mat[0][3] = 1
    mat[1][3] = 0
    mat[2][3] = 0
    mat[3][3] = 0

    return mat

H_INV = make_h_inverse()
B = make_b()

def make_curve_coefs(numbers, curve_type):
    vec = new_matrix(rows=4, cols=1)
    vec[0] = numbers[:]
    
    if curve_type == 'hermite':
        matrix_mult(H_INV, vec)
        return vec
    elif curve_type == 'bezier':
        matrix_mult(B, vec)
        return vec

def add_circle( points, numbers, step=0.01):
    cx, cy, cz, r = numbers
    t = 0
    prev_x, prev_y = r * 1 + cx, r * 0 + cy
    while t <= 1:
        theta = 2 * math.pi * t
        x = r * math.cos(theta) + cx
        y = r * math.sin(theta) + cy
        add_edge(points, x0=prev_x, y0=prev_y, z0=cz, x1=x, y1=y, z1=cz)
        prev_x, prev_y = x, y
        

def add_curve( points, curve_type, numbers, step=0.01):
    x0, y0, x1, y1, rx0, ry0, rx1, ry1 = numbers
    xnumbers = [x0, x1, rx0, rx1]
    ynumbers = [y0, y1, ry0, ry1]
    xcoefs = make_curve_coefs(xnumbers, curve_type)[0]
    ycoefs = make_curve_coefs(ynumbers, curve_type)[0]
    
    t = 0
    prev_x, prev_y = x0, y0
    while t <= 1:
        x = xcoefs[0] * (t**3) + xcoefs[1] * (t**2) + xcoefs[2] * (t) + xcoefs[3]
        y = ycoefs[0] * (t**3) + ycoefs[1] * (t**2) + ycoefs[2] * (t) + ycoefs[3]
        add_edge(points, x0=prev_x, y0=prev_y, z0=0, x1=x, y1=y, z1=0)
        prev_x, prev_y = x, y
        t += step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
