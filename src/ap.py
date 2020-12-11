import argparse

def custom_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-u', '--url', default=None, help='Pass the URL of a song')
    args = vars(ap.parse_args())

    return args