import argparse
import os

from PIL import Image

image_extensions = {'png', 'jpg', 'jpeg'}


def crop_center(img, width, height):
    x = img.size[0] // 2
    y = img.size[1] // 2

    x1 = x - (width // 2)
    x2 = x + (width - width // 2)

    y1 = y - (height // 2)
    y2 = y + (height - height // 2)

    try:
        return img.crop((x1, y1, x2, y2))
    except OSError as e:
        print(e)
        return None


def main(indir, outdir, width, height):
    for fname in os.listdir(indir):
        parts = fname.rsplit('.', 1)
        if len(parts) == 2 and parts[1] in image_extensions:
            name, ext = parts
            img = Image.open(os.path.join(indir, fname))

            if img.size[0] >= width and img.size[1] >= height:
                img = crop_center(img, width, height)
                if img:
                    img.save(os.path.join(outdir, name + '.png'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', required=True)
    parser.add_argument('--outdir', required=True)
    parser.add_argument('--width', type=int, default=608)
    parser.add_argument('--height', type=int, default=608)

    args = parser.parse_args()

    main(
        indir=args.indir,
        outdir=args.outdir,
        width=args.width,
        height=args.height)
