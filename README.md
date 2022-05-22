# Plot-3D-Medical-Image
  This tool is used for plot 3D-mask from medical images.
```
                              def plot_3D(_img, setting_color='silver', Spacing=None)
```
&emsp;&emsp;The function has three parameters：_img、setting_color and Spacing

## **Parameters**

&emsp;&emsp; **_img**: 3D image data, which is a **numpy** array in **np.uint8** format.The value is **255** or **0** (foreground or background)
 
&emsp;&emsp;**setting_color** : select the color of foreground，by default **"silver"**."red"、"green" and "blue" are also available

&emsp;&emsp;**Spacing**: set the spacing of the orignal image, by default **None**. When Spacing is **not None** ,this function will resample the image to the new spacing [1.0, 1.0, 1.0].Notably, Spacing must be a **numpy** array.


## **Requirements**

&emsp;&emsp;numpy

&emsp;&emsp;scipy

&emsp;&emsp;Simpleitk

&emsp;&emsp;vtk

## **Install**

```
                        pip install Plot-3D-Medical-Image
```
## **Example**
```
from Medical_Image_Plot import plot_3D
import numpy as np

image = np.zeros((64, 64, 64), dtype=np.uint8)
for i in range(64):
    image[i, i:64-i, i:64-i]=255
# plot
plot_3D(image)
```
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![image](https://github.com/DreamthreePi/Plot-3D-Medical-Image/blob/main/0.PNG)
