import sys
from math import ceil, sqrt, floor
from copy import deepcopy


def main():
    _input = input().split(" ")
    n = int(_input[0])
    m = int(_input[1])
    k = int(_input[2])

    h, w = calculate_sample_sides(n, m, k)

    blurred_image = get_blurred_image(n, m, h, w, k)
    image = get_image(n, m, h, w, blurred_image)
    # sharpened = sharpen_laplacian(n, m, image)
    # smoothed = smooth_mean(3, n, m, image)

    print("Ready")
    print_image(n, m, image)


def smooth_mean(lens_side, n, m, image):
    div = lens_side * lens_side - 1
    res = deepcopy(image)
    half_side = floor(lens_side/2)
    for i in range(half_side, n - half_side):
        for j in range(half_side, m - half_side):
            r, g, b = 0, 0, 0
            for k in range(i - half_side, i + half_side + 1):
                for l in range(j - half_side, j + half_side + 1):
                    if k == i and l == j:
                        continue
                    pixel = res[k][l]
                    r += pixel[0]
                    g += pixel[1]
                    b += pixel[2]
            res[i][j] = (normalize(r/div),
                         normalize(g/div), normalize(b/div))
    return res


def sharpen_laplacian(n, m, image):
    res = []
    for i in range(n):
        row = []
        for j in range(m):
            ti = i-1 if i > 0 else 0
            bi = i+1 if i < n-2 else i
            lj = j-1 if j > 0 else 0
            rj = j+1 if j < m - 2 else j
            center = image[i][j]
            top = image[ti][j]
            bottom = image[bi][j]
            left = image[i][lj]
            right = image[i][rj]
            result_pixel = (
                normalize(-4 * center[0] + top[0] +
                          bottom[0] + left[0] + right[0]),
                normalize(-4 * center[1] + top[1] +
                          bottom[1] + left[1] + right[1]),
                normalize(-4 * center[2] + top[2] +
                          bottom[2] + left[2] + right[2]),
            )
            row.append(result_pixel)
        res.append(row)
    return res


def normalize(val):
    if val < 0:
        return 0
    if val > 255:
        return 255
    return int(val)


def get_image(n, m, h, w, blurred_image):
    image = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(blurred_image[i//ceil(h)][j//ceil(w)])
        image.append(row)
    return image


def print_image(n, m, image):
    for i in range(n):
        row = ""
        for j in range(m):
            row += color_as_str(image[i][j]) + " "
        row = row[:-1]
        print(row)


def get_blurred_image(n, m, h, w, k):
    image = []
    i = 0
    j = 0
    counter = 0
    while i < n:
        row = []
        while j < m:
            counter += 1
            color = ask(i, j, min(ceil(i + h), n - 1),
                        min(ceil(j + w), m - 1))
            row.append(color)
            j += ceil(w)
        image.append(row)
        i += ceil(h)
        j = 0
    return image


def calculate_sample_sides(n, m, k):
    k1 = floor(sqrt(k)) * floor(sqrt(k))
    area = n * m
    sample_area = area / k1
    h = sqrt(n * sample_area / m)
    w = m / n * h
    return (h, w)


def fake_ask(x1, y1, x2, y2):
    # print("{} {} {} {}".format(x1, y1, x2, y2))
    return (1, 1, 1)


def ask(x1, y1, x2, y2):
    print("{} {} {} {}".format(x1, y1, x2, y2))
    sys.stdout.flush()
    r, g, b = input().split(" ")
    return (int(r), int(g), int(b))


def color_as_str(color):
    return "{} {} {}".format(color[0], color[1], color[2])
    # return "x"


main()
