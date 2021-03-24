import nibabel as nib
import pandas as pd
import os
import sys
import shutil
from neuroglancer_scripts.scripts.volume_to_precomputed_pyramid import volume_to_precomputed_pyramid
from neuroglancer_scripts.scripts.volume_to_precomputed import main as volume_to_precomputed
from neuroglancer_scripts.scripts.generate_scales_info import main as generate_scales_info
from neuroglancer_scripts.scripts.compute_scales import main as compute_scales
import gzip

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

    info = open(os.path.normpath(os.path.join(dirnam, "info")), "w")
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

    volume_to_precomputed(argv=["Placeholder", os.path.normpath(os.path.join(dirnam, sys.argv[1])), "--generate-info", "Output"])

    fin = open(os.path.join(os.getcwd(), "Output/info_fullres.json"), "rt")
    data = fin.read()
    data = data.replace("float32", "uint32")
    fin.close()
    fout = open(os.path.join(os.getcwd(), "Output/info_fullres.json"), "wt")
    fout.write(data)
    fout.close()

    generate_scales_info(argv=["Placeholder", "Output/info_fullres.json", "Output", "--type=segmentation"])
    volume_to_precomputed(argv=["Placeholder", os.path.normpath(os.path.join(dirnam, sys.argv[1])), "Output"])
    compute_scales(argv=["Placeholder", "Output", "--downscaling-method=majority"])

    shutil.move(str(os.path.join(os.getcwd(), "Output")), str(os.path.join(dirnam, "Output")))

    for subdir, dirs, files in os.walk(os.path.join(dirnam, "Output\\100um")):
        #print(subdir)
        for file in files:
            #print(file)
            subdirSplit = subdir.split("\\")
            fileSplit = file.split(".")
            fileName = subdirSplit[-2] + "_" + subdirSplit[-1] + "_" + fileSplit[0]
            print(os.path.join(subdir, file))
            fin = gzip.open(os.path.join(subdir, file), "r")
            fout = open(os.path.join(dirnam, "Output/100um/", fileName), "wb")
            data = fin.read()
            fout.write(data)

    for subdir, dirs, files in os.walk(os.path.join(dirnam, "Output\\200um")):
        # print(subdir)
        for file in files:
            # print(file)
            subdirSplit = subdir.split("\\")
            fileSplit = file.split(".")
            fileName = subdirSplit[-2] + "_" + subdirSplit[-1] + "_" + fileSplit[0]
            print(os.path.join(subdir, file))
            fin = gzip.open(os.path.join(subdir, file), "r")
            fout = open(os.path.join(dirnam, "Output/200um/", fileName), "wb")
            data = fin.read()
            fout.write(data)


if __name__ == "__main__":
    main()
