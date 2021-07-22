import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import SimpleKinematic as sk
import tkinter as tk

a0 = 0.3
f0 = 0.5
delta_f = 0.1

def plotManip(paramsRange, dhMatrix):

    axcolor = 'lightgoldenrodyellow'
    iter = 0
    axisOffset = 0.03

    sliders = {}
    for paramName, parRange in paramsRange.items():
        axVarName = plt.axes([0.1, 0.02 + axisOffset * iter, 0.35, 0.02], facecolor=axcolor)
        init_val = 0
        if dhMatrix.params[paramName[:-1]][paramName] != "var":
            init_val = dhMatrix.params[paramName[:-1]][paramName]
        sVarName = Slider(axVarName, paramName, min(parRange), max(parRange), valinit=init_val, valstep=0.1)
        sliders[paramName] = sVarName
        iter += 1

    ax = plt.axes(projection='3d')
    sct = None

    def update(var):


        ranges = {}
        for sliderName, slider in sliders.items():
            ranges[sliderName] = slider.val

        points = sk.genElemCoordForSingleParams(ranges, dhMatrix)  # lambda_range)

        xdata = [point[0] for point in points]
        ydata = [point[1] for point in points]
        zdata = [point[2] for point in points]

        # print("x", xdata)
        # print("y", ydata)
        # print("z", zdata)
        # print("dupa")
        global sct
        # if sct:
        #     sct.remove()
        ax.clear()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.plot(xdata, ydata, zdata)

        axes = plt.gca()
        axes.set_xlim([-1, 1])
        axes.set_ylim([-1, 1])
        axes.set_zlim([-0.5, 2])

        plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
        sct = ax.scatter3D(xdata, ydata, zdata, c=zdata)
        plt.show()


    for sliderName, slider in sliders.items():
        slider.on_changed(update)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    ax.figure.set_size_inches(5, 5)
    ax.plot([], [], [])
    ax.scatter3D([], [], [], cmap='Greens')
    plt.show()

def plotForConfigVariables(paramsRanges, dhMatrix):

    axcolor = 'lightgoldenrodyellow'
    axVarName = plt.axes([0.1, 0.02, 0.35, 0.02], facecolor=axcolor)
    print("keys: ", paramsRanges.keys())
    idxSlider = Slider(axVarName, "idx", 0, len(paramsRanges[list(paramsRanges.keys())[0]]) - 1, valinit=0, valstep=1)

    ax = plt.axes(projection='3d')
    sct = None
    path = {"x": [], "y" : [], "z" : []}

    genCoordinates = []
    ranges = {}
    paramsRangesLen = len(paramsRanges[list(paramsRanges.keys())[0]])

    for i in range(0, paramsRangesLen):
        for varName in paramsRanges.keys():
            ranges[varName] = paramsRanges[varName][i]
        points = sk.genElemCoordForSingleParams(ranges, dhMatrix)
        genCoordinates.append(points)

    xPoints = [pointsGroup[3][0] for pointsGroup in genCoordinates]
    yPoints = [pointsGroup[3][1] for pointsGroup in genCoordinates]
    zPoints = [pointsGroup[3][2] for pointsGroup in genCoordinates]

    # [val for sublist in matrix for val in sublist]
    # for i in range(0, len(xPoints)):
    #     print("x", xPoints[i], "y", yPoints[i], "z", zPoints[i])

    global it
    it = 0

    def update(var):

        xdata = [point[0] for point in genCoordinates[idxSlider.val]]
        ydata = [point[1] for point in genCoordinates[idxSlider.val]]
        zdata = [point[2] for point in genCoordinates[idxSlider.val]]

        global it
        if idxSlider.val > len(path["x"]) -1:
            path["x"].append(xdata)
            path["y"].append(ydata)
            path["z"].append(zdata)
            it += 1

        ax.clear()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.plot(xdata, ydata, zdata)

        axes = plt.gca()
        axes.set_xlim([-1, 1])
        axes.set_ylim([-1, 1])
        axes.set_zlim([-0.5, 2])

        plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
        sct = ax.scatter3D(xdata, ydata, zdata, c=zdata)
        # sct = ax.scatter3D(path["x"][:idxSlider.val], path["y"][:idxSlider.val], path["z"][:idxSlider.val])

        sct = ax.scatter3D(xPoints[:idxSlider.val], yPoints[:idxSlider.val], zPoints[:idxSlider.val], s=0.5)
        plt.show()

    idxSlider.on_changed(update)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    ax.figure.set_size_inches(5, 5)
    ax.plot([], [], [])
    ax.scatter3D([], [], [], cmap='Greens')
    plt.show()

def plotContinuous(basePosition, dhMatrix):
    def key(event):
        """shows key or tk code for the key"""
        print("dupa")
        if event.keysym == 'Escape':
            root.destroy()
        if event.char == event.keysym:
            # normal number and letter characters
            print('Normal Key %r' % event.char)
        elif len(event.char) == 1:
            # charcters like []/.,><#$ also Return and ctrl/key
            print('Punctuation Key %r (%r)' % (event.keysym, event.char))
        else:
            # f1 to f12, shift keys, caps lock, Home, End, Delete ...
            print('Special Key %r' % event.keysym)

    root = tk.Tk()
    print("Press a key (Escape key to exit):")
    root.bind_all('<Key>', key)
    # don't show the tk window
    root.withdraw()
    root.mainloop()


    # for i in range(0, paramsRangesLen):
    #     for varName in paramsRanges.keys():
    #         ranges[varName] = paramsRanges[varName][i]
    #     points = sk.genElemCoordForSingleParams(ranges, dhMatrix)
    #     genCoordinates.append(points)
    #
    # xPoints = [pointsGroup[3][0] for pointsGroup in genCoordinates]
    # yPoints = [pointsGroup[3][1] for pointsGroup in genCoordinates]
    # zPoints = [pointsGroup[3][2] for pointsGroup in genCoordinates]
    #
    # # [val for sublist in matrix for val in sublist]
    # # for i in range(0, len(xPoints)):
    # #     print("x", xPoints[i], "y", yPoints[i], "z", zPoints[i])
    #
    # global it
    # it = 0
    #
    # def update(var):
    #
    #     xdata = [point[0] for point in genCoordinates[idxSlider.val]]
    #     ydata = [point[1] for point in genCoordinates[idxSlider.val]]
    #     zdata = [point[2] for point in genCoordinates[idxSlider.val]]
    #
    #     global it
    #     if idxSlider.val > len(path["x"]) - 1:
    #         path["x"].append(xdata)
    #         path["y"].append(ydata)
    #         path["z"].append(zdata)
    #         it += 1
    #
    #     ax.clear()
    #
    #     ax.set_xlabel('x')
    #     ax.set_ylabel('y')
    #     ax.set_zlabel('z')
    #     ax.plot(xdata, ydata, zdata)
    #
    #     axes = plt.gca()
    #     axes.set_xlim([-1, 1])
    #     axes.set_ylim([-1, 1])
    #     axes.set_zlim([-0.5, 2])
    #
    #     plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    #     sct = ax.scatter3D(xdata, ydata, zdata, c=zdata)
    #     # sct = ax.scatter3D(path["x"][:idxSlider.val], path["y"][:idxSlider.val], path["z"][:idxSlider.val])
    #
    #     sct = ax.scatter3D(xPoints[:idxSlider.val], yPoints[:idxSlider.val], zPoints[:idxSlider.val], s=0.5)
    #     plt.show()
    #
    # idxSlider.on_changed(update)
    #
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    #
    # plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    # ax.figure.set_size_inches(5, 5)
    # ax.plot([], [], [])
    # ax.scatter3D([], [], [], cmap='Greens')
    # plt.show()