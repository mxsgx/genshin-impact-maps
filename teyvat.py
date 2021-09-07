import cv2
from utils import get_tiles_info, download_tiles, combine_tiles

if __name__ == '__main__':
    info = get_tiles_info(
        'https://api-os-takumi-static.mihoyo.com/common/map_user/ys_obc/v1/map/info?map_id=2&app_sn=ys_obc&lang=en-us')
    tiles = download_tiles(info.get('detail').get('slices'), 'tiles/teyvat')
    combined_img = combine_tiles(tiles)
    cv2.imwrite('teyvat.jpeg', combined_img)
