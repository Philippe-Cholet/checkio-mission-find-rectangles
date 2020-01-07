import re

SPECS = '''
6x6:3d2_2b4c5d3a3_2d2b6c4b

9x9:6f2b2a2b4h5c12_2a5f2a3a2i2i7b3b12d2c4b4

8x11:2_6e3a2k8b4b2f6c2_2a2e6_2h2h8e3b3_14b4d4a3a

11x11:e5b12g2j2d3_5b10_4b4d4c2f6c2b8a3b2c5f2_2_2r6_3g18i9a

16x9:c2a3_4a4c3b2a6q6b2a3b6_6b4d3a3m20f16a4b21m3o6d2i5g3b4c3c

15x15:b2c12h4_9a3e36g2z4c2_4y6f6a10d2f5d4f20b16i3l2k2_3b2e16d2_3k2_3a2b6f14c2_4d2e7e3

19x19:3_2p2d32r3f5e5b14q3n18l2_2b2b8a4_2l4j15j4m42z5_8zo33k10a3f36g14c3a2g8c2b4b2_4c3d6e3i4b5d12b2e2e5f2g5c2e4

17x25:d7b6j3g3v9g12b4d3c5_4_2c16i5e3a2j2a6d8l14h8a8u2_2g44a6b2_4b12b2h3c4c3d3b6i2a5c2i32zu3m40f2_3l3b2b12i2b3d6m39h9q3m32o2q

27x27:j4a5e2c6b2b20e2b5d8a3b2c4e15f4_2i5c18h8d4d8w14g2f5h105s16b3zzq16e2a10z12r2_9b2e3v6d5_2b12j2f2s119zzm2zs14f14za9s13r3e5_3k6i2c4j10c18d6e4zh65e51x2q2g4i11c3c2

40x25:a2d6p26m5d6d2y20f6m100w2_3zo30e3ze4t26m4c2h6i5a4d7n10a24u3c9h2a3ze2h3v6_2a12d2g14g80zd8b3d2r18e3l2g12e7k3b18l3a2ze11_5d2a2_2_2q46i2g2b10y21b8_4m4a4c2q7i14i3u4a5b16j2a2a3v18d8g6b2g70s5g30e57p3d2l2a2u2d4c2f2y2k17f16q4n18e2b21r

30x40:c4d12g14m2x27g18g18_2g7b4c52b2c3_3zn99m2h8b3_10p2d2zc2b12c15s4f7w4zzzg14n3f8h9q2e3r2e24n13l6f2_2b3n10i7e6b24u2a4_2_2d3c84h16a2h3s3l8l2p2zzb150d2d60j14l2zb12b3i12r2c12h2a2o2_8j5zg14zo6zc2zc3zb3o192zg2_2a3a2a3a3r3e3a6x11i4z2zd6r6e18b6_3c

40x40:e7i14j2b4c2g6a6zg4_4_6c2ze6_5g2zzl145e2d12c2zc3a2_2_2m26zc20zzzzs8f95zc4b3zx2a4b3b2zj5_2zf8g9d196zb2a7ze96k36zzd2_3k3zn6zj30c2g12f2g16ze2zzzr140u3b27w32zzzg204zzb130zo32zo3f6zf12zt6zzr2_2j24zi27f6x6f5_2c18zh5w19f2d17v10b8g4a2

50x50:2_2a2c4c28zm2a2_2a4a4f2_2b2_4c3_2zk30i3zf30o3zb36s3zw6a4a24zg3c5zv10h4ze3d3k2zh2_2o3_3zn2g3zg14zu8_2n2b3zd3i3l154v2b5q10a3zb2a3h18k6za2_2q2za4d6h4zj3d6_2f3h28za3a2p8a4zv4a4d8b63zd21e168zzzzf4p325ze2c8zd16za3f2_2k88ze6_2_6zt6c12a4_2m28za2_2zf40zm30y2d4b2zzzi312zi3a36zzzg48k2zzn12zzzzt9zzza171p2_2zo200f2a2_2x3s3o3ze3_2h2e9za8f2a3_6a4a2zp2_2d5a3_6u5n36f2b3f87_12b2zi7d6f4o2x7b4d2j11d5j
'''.strip().split('\n'*2)


def spec2grid(spec: str):
    dim, line = spec.split(':')
    nb_cols, nb_rows = map(int, dim.split('x'))
    L = []
    # Ignore '_' chars in line, it only separates contiguous numbers.
    for item in re.findall(r'(\d+|[a-z])', line):
        if item.isdigit():
            L.append(int(item))
        else:
            L.extend(0 for _ in range(ord(item) - ord('a') + 1))
    return [L[k * nb_cols: (k + 1) * nb_cols] for k in range(nb_rows)]


GRIDS = tuple(map(spec2grid, SPECS))
TESTS = {'Basic': [], 'Extra': []}
for n, grid in enumerate(GRIDS):
    category = ('Basic', 'Extra')[n >= 3]
    TESTS[category].append({'input': grid, 'answer': grid})


if __name__ == '__main__':
    # For editor/initial_code/python_3
    from pprint import pprint
    pprint(GRIDS[:3])

    # For info/task_description.html
    url = 'https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/rect.html'
    for test_nb, (spec, grid) in enumerate(zip(SPECS, GRIDS), 1):
        title = f'{len(grid)} rows, {len(grid[0])} columns'
        print(f'    <a href="{url}#{spec}" title="{title}">{test_nb}</a>')
