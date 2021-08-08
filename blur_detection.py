import cv2
import argparse
import glob
import os

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', required=True,)
ap.add_argument('-t', '--threshold', type=float)
args = vars(ap.parse_args())

fnames = glob.glob("{}/**/*.JPG".format(args['images']),
                   recursive=True)
fnames = [fname for fname in glob.glob("{}/**/*.JPG".format(args['images']), recursive=True) if 'blurry' not in fname]

counts = {}
for idx,fname in enumerate(fnames):
    try:
        image = cv2.imread(fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        if fm < args["threshold"]:
            parent_dir = '/'.join(fname.split('/')[0:-1])
            jpg = fname.split('/')[-1]
            new_dir = f"{parent_dir}/blurry"
            key = parent_dir.replace('/','_').replace(' ','_')
            if not os.path.isdir(new_dir):
                os.mkdir(new_dir)
                counts[key] = 0
                print(f"Found blurry image in: {parent_dir}")
            os.rename(fname, f"{new_dir}/{jpg}")
            counts[key] += 1
    except Exception as e:
        print(f"fname broke: {fname}. Error: {e}")

print(counts)
