import sys
import numpy as np
import spectral.io.envi as envi
from skimage import filters, measure
import matplotlib.pyplot as plt
import pickle
from sklearn.svm import SVC
import xml.etree.ElementTree as ET


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

        data_DN = Data_Normalization(ref).copy()  # 資料標準化
        mask = data_DN[:, :, 10].copy()  # 取一個band 當mask
        
        mask[mask < 0.25] = 0  # 把底去掉
        mask[mask > 0] = 1  # 其他都為1

        for i in range(24):  # 濾雜質
            data_DN[:, :, i] = data_DN[:, :, i] * mask  # 濾雜質

        x, y, _ = data_DN.shape

        badim = np.zeros((x, y))
        non = np.nonzero(mask)  #  將非零值位置記錄下來
        HIM = []
        HIM.append(data_DN[non[0], non[1]])
        HIM = np.array(HIM)

        d = np.load("./haoez_api_server/coffee_demo/data/20200819_hp280_D.npz")["D"]

        result = weight_Winner_Take_All_CEM(HIM, d)  
        end = otsu(result, 2)

        input1 = open("./haoez_api_server/coffee_demo/data/svm_model_0820.pkl", "rb")
        svm = pickle.load(input1)
        input1.close()

        y_predict = svm.predict(end.T)

        for i in range(non[0].shape[0]):
            badim[non[0][i], non[1][i]] = y_predict[i]

        img = badim + mask
        plt.imsave("./haoez_api_server/coffee_demo/result/" + filename + ".png", img)

        # 處理成分類的圖
        label_image = measure.label(img)
        for region in measure.regionprops(label_image):
            if region.area < 200:
                continue
            minr, minc, maxr, maxc = region.bbox
            all_p = img[minr:maxr, minc:maxc].reshape(-1).shape[0]
            bad_p = np.where(img[minr:maxr, minc:maxc] == 3)[0].shape[0] # CEM壞的要改2 SVM要改3 因為胖哥SVM label給1,2
            bg_p = np.where(img[minr:maxr, minc:maxc] == 0)[0].shape[0]
            bad_ratio = bad_p / (all_p - bg_p)
            print(bad_ratio, all_p, bad_p, bg_p)
            if bad_ratio > 0.03:  # 壞點容忍值
                mask = np.where(img[minr:maxr, minc:maxc]!=0)
                img[minr:maxr, minc:maxc][mask] = 2
            else:
                mask = np.where(img[minr:maxr, minc:maxc]!=0)
                img[minr:maxr, minc:maxc][mask] = 1
        plt.imsave("./haoez_api_server/coffee_demo/result/" + filename + "_classes.png", img)
        return filename + ".png"
    except Exception as e:
        print("demo")
        print(e, file=sys.stderr)
        return ""


def calibration(w, b, s, s_d):
    _cali_xml = "./haoez_api_server/coffee_demo/data/CMV2K-SSM5x5-600_1000-5.6.17.9.xml"
    _xml_data = ET.parse(_cali_xml)

    _virs = _xml_data.findall(".//virtual_band/coefficients")[-24:]
    coefficients = []
    for band in _virs:
        coefficients.append(
            np.fromstring(band.text, sep=",", dtype=float).reshape(5, 5)
        )

    sample_spectral = read(s)
    white_spectral = read(w)
    dark_spectral = read(b)
    sample_dark_spectral = read(s_d)
    uncali_ref = (
        (sample_spectral - dark_spectral) / (white_spectral - sample_dark_spectral)
    ).reshape(1088, 2048)[3:-5, :2045]

    ref_result = np.zeros((216 * 409, 24))
    for _idx, filt in enumerate(coefficients):
        filt = np.tile(filt, [216, 409])
        ref_result[:, _idx] = im2col(filt * uncali_ref, 5, 5).sum(1)
    return ref_result.reshape((216, 409, 24))


def read(file, dtype="i2"):
    unsigned_int_array = np.fromfile(file, dtype=dtype)
    file.close()
    return unsigned_int_array


def im2col(input_data, filter_h, filter_w, stride=5):
    H, W = input_data.shape
    out_h = (H - filter_h) // stride + 1  # 輸出資料的高
    out_w = (W - filter_w) // stride + 1  # 輸出資料的長
    col = np.zeros((1, 1, filter_h, filter_w, out_h, out_w))

    for y in range(filter_h):
        y_max = y + stride * out_h
        for x in range(filter_w):
            x_max = x + stride * out_w
            col[:, :, y, x, :, :] = input_data[y:y_max:stride, x:x_max:stride]
    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(1 * out_h * out_w, -1)
    return col


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
