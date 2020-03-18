"""Video processing with opencv and matplotlib
Author: Cheney
License: GPLv3
Date: 20200318
"""

import argparse
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import cv2


def main():
    # retval, return value
    # rc, running configuration
    parser = argparse.ArgumentParser(description='Day N video')
    parser.add_argument(
        'day_n',
        metavar='N',
        type=int,
        #  nargs='+',
        help='an integer for the accumulator')
    args = parser.parse_args()
    day_n = args.day_n

    # video path
    video_path = str(Path(f'./day{day_n}.mp4').absolute())
    # instantiation, and initialization with cap.open function
    cap = cv2.VideoCapture(video_path)
    #  cap.set(cv2.CAP_PROP_POS_FRAMES, 100)  # specify a video frame
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 344
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 1920
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 1080
    frame_fps = int(cap.get(cv2.CAP_PROP_FPS))  # 30

    # Determine the figures size in inches to fit the image
    dpi = mpl.rcParams['figure.dpi']
    figsize = frame_width / float(dpi), frame_width / float(dpi)
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(
        left=0.0, bottom=0.0, right=1.0, top=1.0, hspace=0.0, wspace=0.0)

    ax = fig.add_subplot(111)  # , aspect='auto')
    ax.axis('off')

    init_img = np.zeros([frame_width, frame_height, 3])

    img = ax.imshow(init_img)
    day_text = ax.text(10, 50, '', fontsize=30, color='k', alpha=0.8)
    num_text = ax.text(150, 50, '', fontsize=30, color='r', alpha=0.8)

    def init():
        img.set_data(init_img)
        day_text.set_text('')
        num_text.set_text('')
        return img, day_text, num_text

    def animate(i):
        if i > frame_count:
            raise ValueError(f'Number of frames: {frame_count}, but got {i}')
        if cap.isOpened():
            retval, frame = cap.read()  # return the next video frame
            #  print(type(frame), frame.shape)  # 1080, 1920, 3
            #  cv2 and matplotlib have different array order (C order, F order)
            this_frame = frame.transpose(1, 0, 2)[:, ::-1, ::-1]
        else:
            this_frame = init_img
        img.set_data(this_frame)
        day_text.set_text('Day')
        num_text.set_text(f'{day_n}')
        return img, day_text, num_text

    ani = animation.FuncAnimation(
        fig,
        animate,
        range(0, frame_count),
        interval=1000 / frame_fps,
        blit=True,
        init_func=init)

    ani.save(f"{day_n}.mp4")
    cap.release()  # turn off video file or camera

    #  plt.show()


def test():
    """code test"""
    working_dir = Path().absolute()
    print(working_dir)


if __name__ == '__main__':
    # test()
    main()
