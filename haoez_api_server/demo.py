import numpy as np
import spectral.io.envi as envi
from skimage import filters
import matplotlib.pyplot as plt


def coffee(w, b, s, s_d, ref_raw_path=None, ref_hdr_path=None):
    try:
        if ref_raw_path is not None and ref_hdr_path is not None:
            img = envi.open(ref_hdr_path, ref_raw_path)
            load_data = img.open_memmap(writeable=True)
            ref = np.array(load_data)
            filename = ref_raw_path.split("/")[-1]
        else:
            ref = calibration(w, b, s, s_d)  # ref反射率
            filename = s.filename

        bands_num = 5




        a = np.load(
            "./haoez_api_server/coffee_demo/data/hp280_bs.npz"
        )  # load bdm bs 的結果 (未給波段選擇資料位置)
        Bdm = a["bad_bs"]

        data_DN = Data_Normalization(ref).copy()  # 資料標準化
        mask = data_DN[:, :, 10].copy()  # 取一個band 當mask9
        mask[mask < 0.25] = 0  # 把底去掉
        mask[mask > 0] = 1  # 其他都為1

        for i in range(24):  # 濾雜質
            data_DN[:, :, i] = data_DN[:, :, i] * mask  # 濾雜質

        bs_data = data_DN[:, :, Bdm[:bands_num, 0]].copy()  # 波段選擇後的結果

        x, y, _ = data_DN.shape

        print(data_DN.shape)

        badim = np.zeros((x, y))
        non = np.nonzero(mask)  #  將非零值位置記錄下來
        HIM = []
        HIM.append(bs_data[non[0], non[1]])
        HIM = np.array(HIM)

        d = np.load("./haoez_api_server/coffee_demo/data/hp280_D_fornew.npz")["D"]
        d = d[Bdm[:bands_num, 0]].copy()

        result = weight_Winner_Take_All_CEM(HIM, d)  # 感興趣點尚未給
        end = otsu(result, 2)

        for i in range(non[0].shape[0]):
            badim[non[0][i], non[1][i]] = end[0, i]

        img = badim + mask

        plt.imsave("./haoez_api_server/coffee_demo/result/" + filename + ".png", img)
        return filename + ".png"
    except Exception as e:
        print("demo")
        print(e)
        return ""


def read(array):
    float_array = np.fromfile(array, dtype="i2")
    return float_array


import xml.etree.ElementTree as ET


def calibration(w, b, s, s_d):
    ss = read(s)
    ww = read(w)
    dd = read(b)
    ss_dd = read(s_d)
    r = ((ss - ss_dd) / ((ww - dd) + 1e-10)).reshape(1088, 2048)[8:, 3:]

    xml = "./haoez_api_server/coffee_demo/data/CMV2K-SSM5x5-600_1000-5.6.17.9.xml"
    data = ET.parse(xml)

    virs = data.findall(".//virtual_band/coefficients")[24:]
    coefficients = []
    for band in virs:
        coefficients.append(
            np.fromstring(band.text, sep=",", dtype=float).reshape(5, 5)
        )

    ref = np.zeros((216, 409, 24))
    arr_width, arr_height = r.shape
    for idx, filt in enumerate(coefficients):
        filt_width, filt_height = filt.shape
        for width in range(0, arr_width, filt_width):
            for height in range(0, arr_height, filt_height):
                arr_slice = r[width : width + filt_width, height : height + filt_height]
                ref[int(width / filt_width), int(height / filt_height), idx] = np.sum(
                    arr_slice * filt
                )
    return ref


def Data_Normalization(input_data):
    input_data = np.array(input_data) * 1.0
    maximum = np.max(np.max(input_data))
    minimum = np.min(np.min(input_data))
    normal_data = (input_data - minimum) / (maximum - minimum) * 1.0
    return normal_data


def CEM(HIM, D):
    x, y, band = HIM.shape
    image = np.mat(HIM.reshape((x * y, band)))
    R = np.zeros((band, band))
    for i in range(x * y):
        DB = image[i, :] - D
        norm_DB = np.linalg.norm(DB)
        R = R + (norm_DB * (image[i, :].T * image[i, :]))
    R = R / (x * y * 1.0)
    try:
        iR = np.linalg.inv(R)
    except:
        iR = np.linalg.pinv(R)
    Desired_Signature = np.mat(D.reshape((band, 1)))
    CEM_w = (1 / (Desired_Signature.T * iR * Desired_Signature)) * (
        (iR * Desired_Signature).T
    )
    CEM_result = np.zeros((x * y, 1))
    CEM_result = image * CEM_w.T
    CEM_result = CEM_result.reshape((x, y))
    return CEM_result


def Winner_Take_All_CEM(HIM, d):
    CEM_result = CEM(HIM, d)
    Winner_Take_All_CEM_result = 1 - np.power(CEM_result, 2)
    return Winner_Take_All_CEM_result


def weight_Winner_Take_All_CEM(HIM, d):
    x, y, z = HIM.shape
    X = np.reshape(np.transpose(HIM), (z, x * y))
    Winner_Take_All_CEM_result = Winner_Take_All_CEM(HIM, d)
    Winner_Take_All_CEM_result = Winner_Take_All_CEM_result.reshape(
        Winner_Take_All_CEM_result.shape[0] * Winner_Take_All_CEM_result.shape[1], 1
    )
    R = np.zeros([z, z])

    for i in range(x * y):
        r = X[:, i].reshape(z, 1)
        R = float(Winner_Take_All_CEM_result[i]) * np.dot(r, np.transpose(r)) + R

    R = R / (x * y)
    IR = np.linalg.inv(R)
    A = (np.dot(np.transpose(X), np.dot(IR, d))) / (
        np.dot(np.transpose(d), np.dot(IR, d))
    )
    weight_Winner_Take_All_CEM_result = np.transpose(
        np.reshape(np.transpose(A), (y, x))
    )

    return weight_Winner_Take_All_CEM_result


def otsu(HIM, c):
    x, y = HIM.shape
    him = HIM.copy()
    if c == 1:
        val = filters.threshold_otsu(him, nbins=256)
        him[him <= val] = 0
        him[him > val] = 1
    else:
        tmp = him.copy()
        for i in range(c):
            val = filters.threshold_otsu(tmp, nbins=256)
            tmp[tmp <= val] = 0
            tmpnon = np.nonzero(tmp)
            tmp = tmp[tmpnon].copy()
        him[him <= val] = 0
        him[him > val] = 1
    return him
