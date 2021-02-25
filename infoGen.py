import nibabel as nib
import pandas as pd
import os
import sys

dirnam = os.path.dirname(__file__)

def main():
    image = nib.load(os.path.normpath(os.path.join(dirnam, sys.argv[1])))
    image = image.get_fdata()
    df = pd.read_excel(os.path.normpath(os.path.join(dirnam, sys.argv[2])))

    using1000Method = False
    for x in range(0, len(image)):
        for y in range(0, len(image[0])):
            for z in range(0, len(image[0, 0])):
                if image[x, y, z] > 1000:
                    using1000Method = True

    maxLabelFound = False
    i = -1
    while not maxLabelFound:
        maxLabel = df['AlexIndexL'].iat[i]
        maxLabelFound = maxLabel.is_integer()
        i -= 1

    maxLabel = int(maxLabel)

    info = open("info", "w")
    info.write("{\"@type\": \"neuroglancer_segment_properties\", \"inline\": {\"ids\": [\"")
    for x in range(1, maxLabel + 1):
        info.write(str(x))
        info.write("\", \"")

    if using1000Method:
        for x in range(1, maxLabel):
            info.write(str(x + 1000))
            info.write("\", \"")
        info.write(str(x + 1001))
    else:
        for x in range(1, maxLabel):
            info.write(str(x + maxLabel))
            info.write("\", \"")
        info.write(str(x + maxLabel + 1))

    info.write("\"], \"properties\": [{\"id\": \"label\", \"type\": \"label\", \"values\": [\"")
    for x in range(0, maxLabel):
        info.write(df['Alex_Abbreviation'].iat[x] + "_L")
        info.write("\", \"")
    for x in range(0, maxLabel - 1):
        info.write(df['Alex_Abbreviation'].iat[x] + "_R")
        info.write("\", \"")
    info.write(df['Alex_Abbreviation'].iat[x + 1] + "_R")
    info.write("\"]}]}}")


if __name__ == "__main__":
    main()