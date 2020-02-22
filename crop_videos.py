import pympi
import ffmpeg
import glob


def create_videos(type, name, eaf, tiers):
    if type == 'active_hand':
        hand_data = eaf.get_annotation_data_for_tier(tiers[0])
    else:
        hand_data = eaf.get_annotation_data_for_tier(tiers[1])
    print("check if number of retrieved annotations match", len(hand_data))

    for i, annotation in enumerate(hand_data[1:3]):  # change to `hand_data[1:]` in the production mode
        start_ts = annotation[0]
        end_ts = annotation[1]
        print(start_ts, "======", end_ts)
        path = '.\\' + type + '\\'
        i += 1
        print("Making %d-th trim in %s video" % (i, name))

        suffix = '_ah_' if type == 'active_hand' else '_ph_'
        cut_name = path + name + suffix + str(i) + '.mp4'     # PATH TO A FOLDER WITH NEW CUT FILES

        (
            ffmpeg
            .input(name + '.mp4')
            .trim   (start_pts = start_ts, end_pts = end_ts)
            .setpts ('PTS-STARTPTS')
            .output (cut_name)
            .run(quiet=False)                             # change to `quiet=True` in the production mode
        )


def trim():
    video_name = 'RSLM-cr1-s18'  # PATH TO A FILE TO TRIM
    elan_file_path = video_name + '.eaf'

    # Initialize the elan file
    eaf = pympi.Elan.Eaf(elan_file_path)

    tiers = list(eaf.get_tier_names())
    # print(tiers)
    print("ACTIVE HAND...")
    print('number of active hand annotations: ', len(list(eaf.tiers.values())[0][0]))

    create_videos('active_hand', video_name, eaf, tiers)

    print("PASSIVE HAND...")
    print('number of passive hand annotations: ', len(list(eaf.tiers.values())[1][0]))

    create_videos('passive_hand', video_name, eaf, tiers)


if __name__ == '__main__':
    """
    for file in glob:
        trim(file)
        
        
    In the folder with this script there should be two folders
    for new files. One called "active_hand", for all the videos
    with active hand. And another called "passive_hand", for all
    the videos with passive hand.
    The input videos and eafs should be in the same folder as this script
    
    .------ active_hand
        |
        --- passive_hand
        |
        crop_videos.py
        |
        RSLM-cr1-s10.eaf
        |
        RSLM-cr1-s10.mp4
    """
    trim()
