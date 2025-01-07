import random
from typing import List, Tuple

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.spatial.transform import Rotation


def sample(ratio: int, lst: List[int]) -> List[int]:
    """
    从给定的列表中按指定比例抽样。样本大小由比例和列表长度的 1% 中的较大值决定。

    参数:
        ratio (int): 抽样比例。
        lst (List[int]): 要抽样的列表。

    返回:
        List[int]: 抽样后的列表，包含从原始列表中选出的元素。
    """
    sample_size = max(int(ratio * len(lst)), len(lst) // 100)
    sampled_list = random.sample(lst, sample_size)
    return sampled_list


def rt_to_homogeneous_matrix(rotation: ArrayLike, translation: ArrayLike) -> NDArray:
    """
    将旋转矩阵和平移向量转换为4x4的齐次变换矩阵.

    Args:
        rotation (ArrayLike): 3x3旋转矩阵
        translation (ArrayLike): 3x1平移向量

    Returns:
        NDArray: 4x4齐次变换矩阵，包含旋转和平移信息
    """
    matrix = np.identity(4)
    matrix[:3, :3] = np.array(rotation)
    matrix[:3, 3] = np.array(translation)
    return matrix


def inverse_homogeneous_matrix(rotation: ArrayLike, translation: ArrayLike) -> NDArray:
    """
    计算给定旋转矩阵和平移向量对应的逆变换矩阵.

    Args:
        rotation (ArrayLike): 3x3旋转矩阵
        translation (ArrayLike): 3x1平移向量

    Returns:
        NDArray: 4x4齐次变换矩阵的逆矩阵
    """
    matrix = rt_to_homogeneous_matrix(rotation, translation)
    return np.linalg.inv(matrix)


def inverse_rt(rotation: ArrayLike, translation: ArrayLike) -> Tuple[NDArray, NDArray]:
    """
    计算给定旋转矩阵和平移向量对应的逆变换.

    Args:
        rotation (ArrayLike): 3x3旋转矩阵
        translation (ArrayLike): 3x1平移向量

    Returns:
        Tuple[NDArray, NDArray]:
            - rotation_inv: 旋转矩阵的逆矩阵
            - translation_inv: 平移向量的逆
    """
    matrix_inv = inverse_homogeneous_matrix(rotation, translation)
    return matrix_inv[:3, :3], matrix_inv[:3, 3]


def decompose_homogeneous_matrix(
    matrix: ArrayLike,
) -> Tuple[NDArray, NDArray]:
    """
    将4x4齐次变换矩阵分解为旋转矩阵和平移向量.

    Args:
        matrix (ArrayLike): 4x4齐次变换矩阵

    Returns:
        Tuple[NDArray, NDArray]:
            - rotation: 3x3旋转矩阵
            - translation: 3x1平移向量
    """
    matrix = np.array(matrix)
    return matrix[:3, :3], matrix[:3, 3]


def rotation_matrix(axis: str, degrees: float, original_matrix: ArrayLike) -> Rotation:
    """
    通过旋转矩阵将一个原始矩阵进行旋转.

    Args:
        axis (str): 旋转轴，可选值为'x', 'y', 'z'
        degrees (float): 旋转角度，单位为度
        original_matrix (ArrayLike): 输入的原始旋转矩阵

    Returns:
        R: 旋转后的旋转矩阵（scipy.spatial.transform.Rotation对象）
    """
    rotation = Rotation.from_euler(axis, degrees, degrees=True).as_matrix()
    matrix = Rotation.from_matrix(original_matrix).as_matrix()
    return Rotation.from_matrix(matrix @ rotation)


def rotation_euler(
    axis: str,
    degrees: float,
    original_euler: ArrayLike,
    seq: str = "xyz",
    is_degrees: bool = False,
) -> Rotation:
    """
    通过欧拉角将一个原始欧拉角进行旋转.

    Args:
        axis (str): 旋转轴，可选值为'x', 'y', 'z'
        degrees (float): 旋转角度
        original_euler (ArrayLike): 输入的原始欧拉角
        seq (str, optional): 欧拉角序列。默认为"xyz"
        is_degrees (bool, optional): 输入的欧拉角是否为角度制。默认为False（弧度制）

    Returns:
        R: 旋转后的旋转矩阵（scipy.spatial.transform.Rotation对象）
    """
    rotation = Rotation.from_euler(axis, degrees, degrees=True).as_matrix()
    matrix = Rotation.from_euler(
        seq=seq, angles=original_euler, degrees=is_degrees
    ).as_matrix()
    return Rotation.from_matrix(matrix @ rotation)


def extend_intrinsic_matrix(k: ArrayLike) -> NDArray:
    """
    将3x3相机内参矩阵扩展为3x4矩阵.

    Args:
        k (ArrayLike): 3x3相机内参矩阵

    Returns:
        NDArray: 扩展后的3x4矩阵，右侧补充一列零
    """
    k = np.array(k)
    if k.shape != (3, 3):
        raise ValueError("Input matrix K must be 3x3")

    k_ext = np.zeros((3, 4))
    k_ext[:, :3] = k
    return k_ext


def recover_intrinsic_matrix(k_ext: ArrayLike) -> NDArray:
    """
    从扩展的3x4相机内参矩阵中恢复3x3矩阵.

    Args:
        k_ext (ArrayLike): 3x4扩展相机内参矩阵

    Returns:
        NDArray: 恢复后的3x3矩阵
    """
    k_ext = np.array(k_ext)
    if k_ext.shape != (3, 4):
        raise ValueError("Input matrix K_ext must be 3x4")

    return k_ext[:, :3]


def parse_distortion_params(
    params: ArrayLike,
) -> Tuple[NDArray, NDArray, NDArray, NDArray]:
    """
    解析相机畸变参数。

    参数：
        params (ArrayLike): 输入的畸变参数数组。

    返回：
        Tuple[NDArray, NDArray, NDArray, NDArray]:
        包括径向畸变参数 (k)，切向畸变参数 (p)，薄棱镜失真参数 (s) 和附加项 (r)。

    异常：
        ValueError: 当输入参数长度不是 4、5、8、12 或 14 时抛出。
    """
    # 转换为 NumPy 数组
    params = np.array(params)

    # 获取参数长度
    n = len(params)

    # 根据长度解析对应的参数
    if n == 4:
        # 长度为 4：径向畸变 (k) 和切向畸变 (p)
        k = params[:2]
        p = params[2:]
        return k, p, np.array([]), np.array([])

    if n == 5:
        # 长度为 5：径向畸变 (k) 和切向畸变 (p)
        k = np.append(params[:2], params[-1])
        p = params[2:4]
        return k, p, np.array([]), np.array([])

    if n == 8:
        # 长度为 8：径向畸变 (k) 和切向畸变 (p)
        k = np.append(params[:2], params[4:8])
        p = params[2:4]
        return k, p, np.array([]), np.array([])

    if n == 12:
        # 长度为 12：增加薄棱镜失真参数 (s)
        k = np.append(params[:2], params[4:8])
        p = params[2:4]
        s = params[8:12]
        return k, p, s, np.array([])

    if n == 14:
        # 长度为 14：增加附加项 (r)
        k = np.append(params[:2], params[4:8])
        p = params[2:4]
        s = params[8:12]
        r = params[12:14]
        return k, p, s, r

    # 参数长度无效时抛出异常
    raise ValueError(
        "The length of distortion coefficients must be 4, 5, 8, 12, or 14."
    )


def extract_fisheye_distortion(distortion_params: ArrayLike) -> NDArray:
    """
    提取鱼镜头的畸变参数。

    参数：
        distortion_params (ArrayLike): 鱼眼镜的失真参数。

    返回：
        NDArray: 前 4 个失真参数。

    异常：
        ValueError: 当参数长度小于 4 时抛出。
    """
    distortion_params = np.array(distortion_params)

    if len(distortion_params) < 4:
        raise ValueError("Length of distortion params should be greater than 4.")

    return distortion_params[:4]
