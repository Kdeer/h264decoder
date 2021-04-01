from riff import RIFF
import random
import sys
import numpy as np
import os



def test_frag(video_filepath):
    riff = RIFF(video_filepath)
    all_entry = riff.getAllMovieEntry()
    idxs = riff.getIdx()



def fragment_frames(video_filepath):

    frame_size_list = [100, 200, 300]
    riff = RIFF(video_filepath)
    all_entry = riff.getAllMovieEntry()
    # all_video_entry = riff.getRawVideoEntry()
    idxs = riff.getIdx()

    print(type(all_entry[0]))

    print(sys.getsizeof(all_entry))
    print(sys.getsizeof(idxs))
    print(idxs[0])
    print(all_entry[0])

    all_entry_mixed = []
    i = 0
    j = 100
    while i < len(all_entry):
        all_entry_mixed.append(all_entry[i:j])
        i = j
        j += frame_size_list[random.randint(0, 2)]
        if j > len(all_entry):
            j = len(all_entry)

    all_entry_mixed.append(idxs)

    return all_entry_mixed


def load_saved_frangment(input_file):
    np_fragment = np.load(input_file, allow_pickle=True)
    np_fragment = np.array(np_fragment)
    print(np_fragment[0][0])

    return np_fragment


def fragments_combine(video_folder):

    mixed_fragment_list = []
    for file in os.listdir(video_folder):
        frag = fragment_frames(video_folder+file)
        for x in frag:
            mixed_fragment_list.append(x)

    random.shuffle(mixed_fragment_list)
    return mixed_fragment_list


def fragments_clustering():
    print()


if __name__ == '__main__':
    filepath = "E:/VMwares all/Forensic/Kali-Linux-2020.4-vmware-i386.vmwarevm/sharedFolder/videos/test/"
    filename = "item-1.avi"

    # mixed_fragment_list = fragments_combine(filepath)
    # print(len(mixed_fragment_list))
    #
    # file_fragment_list = np.array(mixed_fragment_list, dtype="object")
    # np.save("frag.npy", mixed_fragment_list)

    saved_npy = "frag.npy"
    saved_npy = load_saved_frangment(saved_npy)




    # load_saved_frangment()
