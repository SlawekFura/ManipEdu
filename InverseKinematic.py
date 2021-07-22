from sympy import Matrix, pprint

def genJacobianMatrix(SystemTransMatrix, TransMatrices, KinPairMode):
    idx = 0
    JacobianMatrix = Matrix()
    filterMatrix = Matrix([[0], [0], [1]])
    emptyMatrix = Matrix([[0], [0], [0]])
    for transMat in TransMatrices[:-1]:
        if KinPairMode[idx] == "R":
            # print("T" + str(idx) + "0")
            # print("transMat[:3, :3]-------------", transMat[:3, :3])
            # print("transMat[:3, :3] * filterMatrix--------", transMat[:3, :3] * filterMatrix)
            # print("SystemTransMatrix[:3, -1]----------", SystemTransMatrix[:3, -1])
            # print("TransMatrices[idx][:3, -1]-----------", TransMatrices[idx][:3, -1])
            col_top_left = transMat[:3, :3] * filterMatrix
            col_top_right = SystemTransMatrix[:3, -1] - TransMatrices[idx][:3, -1]
            # print("col_top_left", col_top_left)
            # print("col_top_right", col_top_right)
            col_top = col_top_left.cross(col_top_right)
            col_bot = TransMatrices[idx][:3, :3] * filterMatrix
            jacobi_col = col_top.row_insert(4, col_bot)
            # print("col_top", col_top)
            JacobianMatrix = JacobianMatrix.col_insert(idx, jacobi_col)
        else:
            jacobi_col = transMat[:3, :3] * filterMatrix
            jacobi_col = jacobi_col.row_insert(4, emptyMatrix)
            JacobianMatrix = JacobianMatrix.col_insert(idx, jacobi_col)
        idx += 1


    return JacobianMatrix