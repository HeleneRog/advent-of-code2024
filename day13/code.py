#!/usr/bin/env python
from math import gcd
import sympy as sp
from sympy.solvers import solve

file = 'input'

f = open(file,'r')
lines = list(f)


def bezout(a, b):
    if b == 0:
        return 1, 0
    else:
        u , v = bezout(b , a % b)
        return v , u - (a//b)*v


def solve_system(xa, xb, x_res, ya, yb, y_res):
    ux, vx = bezout(xa, xb)
    uy, vy = bezout(ya, yb)
    
    kx, ky = sp.var('kx ky')
    eq1 = sp.Eq(x_res*(ux + xb * kx), y_res*(uy + yb * ky))
    eq2 = sp.Eq(x_res*(vx - xa * kx), y_res*(vy - ya * ky))
    output = solve([eq1, eq2], kx, ky, dict=True)[0]
    
    x = x_res*(ux + xb * output[kx])
    y = x_res*(vx - xa * output[kx])
    
    if x % 1 == 0 and y % 1 == 0:
        return x, y
    else:
        return None


class Problem:
    x_res = 0
    y_res = 0
    xa = 0
    xb = 0
    ya = 0
    yb = 0
    
    def solve_eq(self, limit, prize_factor):
        dx = gcd(self.xa, self.xb)
        dy = gcd(self.ya, self.yb)
        
        x_res_fact = prize_factor + self.x_res
        y_res_fact = prize_factor + self.y_res
        
        if (x_res_fact % dx != 0) or (y_res_fact % dy != 0):
            return 0
        
        sol = solve_system(self.xa // dx, self.xb // dx, x_res_fact // dx,
                           self.ya // dy, self.yb // dy, y_res_fact // dy)
        
        if not sol:
            return 0
        x, y = sol
        if limit and x > 100 and y > 100:
            return 0
        return 3*x + y


problems = [Problem()]

for index, line in enumerate(lines):
    if (index % 4) == 3:
        problems.append(Problem())
    elif (index % 4) == 2:
        x_res, y_res = [int(x.split("=")[1]) for x in line.rstrip().split(":")[1].split(",")]
        problems[-1].x_res = x_res
        problems[-1].y_res = y_res
    else:
        x, y = [int(x.split("+")[1]) for x in line.rstrip().split(":")[1].split(",")]
        if (index % 4 == 0):
            problems[-1].xa = x
            problems[-1].ya = y
        else:
            problems[-1].xb = x
            problems[-1].yb = y
            

res_part1 = sum(pb.solve_eq(True, 0) for pb in problems)
print("Part1:", res_part1)
        
res_part2 = sum(pb.solve_eq(False, int(1e13)) for pb in problems)
print("Part2:", res_part2)