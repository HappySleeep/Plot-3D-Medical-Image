# An example from scipy cookbook demonstrating the use of numpy arrays in vtk

import numpy as np
import SimpleITK as sitk
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkImageImport
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkMarchingCubes
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper


from scipy.ndimage.interpolation import zoom
def resample(imgs, spacing, new_spacing=[1.0, 1.0, 1.0],order=2):

    new_shape = np.round(imgs.shape * spacing / new_spacing)
    resize_factor = new_shape / imgs.shape
    imgs = zoom(imgs, resize_factor, mode = 'nearest',order=order)
    return imgs


def plot_3D(_img, setting_color='silver', Spacing=None):

    # 颜色映射表
    _color_dic = {
        'silver': [192, 192, 192, 255],
        'red': [180, 0, 0, 255],
        'green': [0, 180, 0, 255],
        'blue': [0, 0, 180, 255]
    }
    if setting_color not in _color_dic.keys():
        print("color setting error!?!")
        return

    # 设置颜色
    colors = vtkNamedColors()
    # 根据 setting_color 设置actor颜色
    colors.SetColor('SkinColor', _color_dic[setting_color])
    # 轮廓背部颜色
    colors.SetColor('BackfaceColor', [255, 229, 200, 255])
    # 大背景颜色 设置为黑色
    colors.SetColor('BkgColor', [0, 0, 0, 255])


    # 重采样
    if Spacing is not None:
        _img = resample(_img, Spacing)

    # 将图片扩充成 正方体！ 测试发现 当尺寸不是正方体时 会出现显示BUG
    base_x, base_y, base_z = _img.shape
    Max_L = max(base_x, base_y, base_z)
    data_matrix = np.zeros((Max_L, Max_L, Max_L), dtype=np.uint8)
    data_matrix[0:base_x, 0:base_y, 0:base_z] = _img
    dataImporter = vtkImageImport()
    data_string = data_matrix.tobytes()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    # Because the data that is imported only contains an intensity value
    #  (it isnt RGB-coded or someting similar), the importer must be told this is the case.
    dataImporter.SetNumberOfScalarComponents(1)
    # The following two functions describe how the data is stored and the dimensions of the array it is stored in.
    #  For this simple case, all axes are of length 75 and begins with the first element.
    #  For other data, this is probably not the case.
    # I have to admit however, that I honestly dont know the difference between SetDataExtent()
    #  and SetWholeExtent() although VTK complains if not both are used.
    dataImporter.SetDataExtent(0, Max_L-1, 0, Max_L-1, 0, Max_L-1)
    dataImporter.SetWholeExtent(0, Max_L-1, 0, Max_L-1, 0, Max_L-1)


    # 只显示 轮廓
    skin_extractor = vtkFlyingEdges3D()
    skin_extractor.SetInputConnection(dataImporter.GetOutputPort())
    skin_extractor.SetValue(0, 100)
    skin_mapper = vtkPolyDataMapper()
    skin_mapper.SetInputConnection(skin_extractor.GetOutputPort())
    skin_mapper.ScalarVisibilityOff()
    skin = vtkActor()
    skin.SetMapper(skin_mapper)
    skin.GetProperty().SetDiffuseColor(colors.GetColor3d('SkinColor'))

    # 设置轮廓背面的颜色
    back_prop = vtkProperty()
    back_prop.SetDiffuseColor(colors.GetColor3d('BackfaceColor'))
    skin.SetBackfaceProperty(back_prop)

    # With almost everything else ready, its time to initialize the renderer and window, as well as
    #  creating a method for exiting the application
    renderer = vtkRenderer()
    renderWin = vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)

    # We add the volume to the renderer ...
    renderer.AddActor(skin)
    renderer.SetBackground(colors.GetColor3d('BkgColor'))

    # ... and set window size.
    renderWin.SetSize(400, 400)
    renderWin.SetWindowName('VTKWithNumpy')

    # A simple function to be called when the user decides to quit the application.
    def exitCheck(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    # Tell the application to use the function as an exit check.
    renderWin.AddObserver("AbortCheckEvent", exitCheck)

    renderInteractor.Initialize()
    # Because nothing will be rendered without any input, we order the first render manually
    #  before control is handed over to the main-loop.
    renderWin.Render()
    renderInteractor.Start()