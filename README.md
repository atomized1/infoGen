# infoGen

To create your precomputed file, call the infoGen.py with your labels as the first arg and the included spreadsheet as the second arg.
So your command line should look something like:
  infoGen.py B51315_invivoAPOE1_labels.nii.gz CHASSSYMM3_to_ABA.xlsx
  
To upload this to neuroglancer:
  start up cors_webserver in a folder containing the info file, labels, and image
  Load in the image via nifti method, as an image
  Load in the labels via nifti method, as a segmentation
  Load in the info file via precomputed method, as a segmentation
    The info file cannot be in the root directory of the cors_webserver, or it gets confused
  Under the render tab of the labels, you can link the info file
