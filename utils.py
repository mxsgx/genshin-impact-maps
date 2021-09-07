import os
import cv2
import json
import requests


def get_tiles_info(url):
    res = requests.get(url)

    if res.ok:
        res.encoding = 'utf-8'

        data = json.loads(res.text)

        if data['message'] == 'OK':
            data['data']['info']['detail'] = json.loads(
                data['data']['info']['detail'])

            return data['data']['info']
        else:
            return False
    else:
        res.raise_for_status()

    return False


def download_tiles(slices, dir):
    result = []
    dir = os.path.join(os.curdir, dir)

    if not os.path.exists(dir):
        os.makedirs(dir)

    for row_index, row in enumerate(slices):
        tiles = []

        for cell_index, cell in enumerate(row):
            filename = str(row_index) + '-' + str(cell_index) + '.jpeg'
            filepath = dir + '/' + filename

            if not os.path.exists(filepath):
                download = download_file(cell.get('url'), filepath)

                if download:
                    tiles.append(cv2.imread(filepath))
                else:
                    pass
            else:
                tiles.append(cv2.imread(filepath))

        result.append(tiles)

    return result


def download_file(url, path):
    with open(path, 'wb') as handle:
        res = requests.get(url, stream=True)

        if not res.ok:
            res.raise_for_status()

        for block in res.iter_content(1024):
            if not block:
                break

            handle.write(block)

    return True


def combine_tiles(tiles):
    return cv2.vconcat([cv2.hconcat(row_tiles) for row_tiles in tiles])
