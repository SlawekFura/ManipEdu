from TransitionMatrix import *
import numpy as np
from DHMatrix import DHMatrix
import InverseKinematic as ik
import plotter as pl
from sympy import Symbol, nsimplify, eye, sin, cos

theta =  [np.pi,        np.pi/2,    np.pi/2]
alpha =  [np.pi/2,      -np.pi/2,       0.0]
a  =     [0.6,          0.0,            0.0]
lambda_ =[0.7,          0.0,            0.5]

theta1range = np.arange(-np.pi, np.pi, 0.1)
theta2range = np.arange(-np.pi, np.pi, 0.3)
lambda_range = np.arange(-2, 2, 0.5)
numOfIterations = theta1range.size

dhMatrix = DHMatrix()
dhMatrix.addParams({"theta0"    : "var",        "theta1" : "var",       "theta2" : theta[2]})
dhMatrix.addParams({"alpha0"    : alpha[0],     "alpha1" : alpha[1],    "alpha2" : alpha[2]})
dhMatrix.addParams({"a0"        : a[0],             "a1" : a[1],            "a2" : a[2]})
dhMatrix.addParams({"lambda0"   : lambda_[0],  "lambda1" : lambda_[1], "lambda2" : "var"})

# print(dhMatrix.params)
defaultValues = []

# paramsRange = {"theta0" : theta1range, "theta1" : theta2range, "lambda2" : lambda_range}
# points = sk.genPosPointsForRanges(paramsRange, dhMatrix)
# for x, y, z in points:
#     print("x:" + str(x) + " y:" + str(y) + " z:" + str(z))
#
# print(len(points))

# testParamRange = {"theta0" : theta1range, "theta1" : theta2range, "theta2" : np.arange(-np.pi, np.pi, 0.1),
#                   "alpha0" : theta1range, "alpha1" : theta2range, "alpha2" : np.arange(-np.pi, np.pi, 0.1),
#                   "a0" : np.arange(0, 1, 0.1), "a1" : np.arange(0, 1, 0.1), "a2" : np.arange(0, 1, 0.1),
#                   "lambda0" : np.arange(-1, 1, 0.5), "lambda1" : np.arange(-1, 1, 0.5), "lambda2" : lambda_range}
# pl.plotManip(testParamRange, dhMatrix)

A0 = eye(4)
A1 = nsimplify(getSymbolicMatrix(theta_ = "theta1", alpha_ = alpha[0],  a_ = a[0], lambda__ = lambda_[0]), tolerance=1e-10,rational=True)
A2 = nsimplify(getSymbolicMatrix(theta_ = "theta2", alpha_ = alpha[1],  a_ = a[1], lambda__ = lambda_[1]), tolerance=1e-10,rational=True)
A3 = nsimplify(getSymbolicMatrix(theta_ = theta[2], alpha_ = alpha[2],  a_ = a[2], lambda__ = "lambda3" ), tolerance=1e-10,rational=True)

T00 = A0
T10 = A0 * A1
T20 = A0 * A1 * A2
T30 = A0 * A1 * A2 * A3
rows = T30.rows
cols = T30.cols


jacobianMatrix = ik.genJacobianMatrix(T30, [T00, T10, T20, T30], "RRT")
# jacobianMatrix = ik.genJacobianMatrix(T30, [T10, T20, T30])
# print("genJacobi", ik.genJacobianMatrix(T30, [T00, T10, T20, T30]))
d_x = 0.0
d_y = 0.0
d_z = 0.0

invertJacobianMatrix = jacobianMatrix[:3, :3].inv()

d_theta1sym =  invertJacobianMatrix[0,0] * d_x + invertJacobianMatrix[0,1] * d_y + invertJacobianMatrix[0,2] * d_z
d_theta2sym =  invertJacobianMatrix[1,0] * d_x + invertJacobianMatrix[1,1] * d_y + invertJacobianMatrix[1,2] * d_z
d_lambda3sym = invertJacobianMatrix[2,0] * d_x + invertJacobianMatrix[2,1] * d_y + invertJacobianMatrix[2,2] * d_z

currentTheta1 = np.pi/2
currentTheta2 = np.pi/2
currentLambda3 = 0.5

theta1Val = [currentTheta1]
theta2Val = [currentTheta2]
lambda3Val = [currentLambda3]

print("d_theta2sym", d_theta2sym)
delta_t = 0.03
# for i in np.arange(0, 4.5, delta_t):
#     d_x = sin(i*2*np.pi/4.5)/5
#     d_y = cos(i*2*np.pi/4.5)/5
#     d_theta1sym = invertJacobianMatrix[0, 0] * d_x + invertJacobianMatrix[0, 1] * d_y + invertJacobianMatrix[0, 2] * d_z
#     d_theta2sym = invertJacobianMatrix[1, 0] * d_x + invertJacobianMatrix[1, 1] * d_y + invertJacobianMatrix[1, 2] * d_z
#     d_lambda3sym = invertJacobianMatrix[2, 0] * d_x + invertJacobianMatrix[2, 1] * d_y + invertJacobianMatrix[2, 2] * d_z
#
#     d_theta1  = d_theta1sym.subs({Symbol("theta1") : currentTheta1, Symbol("theta2") : currentTheta2, Symbol("lambda3") : currentLambda3})
#     d_theta2  = d_theta2sym.subs({Symbol("theta1") : currentTheta1, Symbol("theta2") : currentTheta2, Symbol("lambda3") : currentLambda3})
#     d_lambda3  = d_lambda3sym.subs({Symbol("theta1") : currentTheta1, Symbol("theta2") : currentTheta2, Symbol("lambda3") : currentLambda3})
#     currentTheta1 += d_theta1 * delta_t
#     currentTheta2 += d_theta2 * delta_t
#     currentLambda3 += d_lambda3 *delta_t
#     theta1Val.append(currentTheta1)
#     theta2Val.append(currentTheta2)
#     lambda3Val.append(currentLambda3)
    # print("theta1: " + str(currentTheta1) + "\ttheta2" + str(currentTheta2) + "\tlambda3" + str(currentLambda3))

# pl.plotForConfigVariables({"theta0" : theta1Val, "theta1" : theta2Val, "lambda2" : lambda3Val}, dhMatrix)

pl.plotContinuous([],[])