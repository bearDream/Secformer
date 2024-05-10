import itertools
from Compiler import types, library, instructions

def dest_comp(B):
    Bt = B.transpose()
    St_flat = Bt.get_vector().prefix_sum()
    Tt_flat = Bt.get_vector() * St_flat.get_vector()
    Tt = types.Matrix(*Bt.sizes, B.value_type)
    Tt.assign_vector(Tt_flat)
    return sum(Tt) - 1

def reveal_sort(k, D, reverse=False):
    """ Sort in place according to "perfect" key. The name hints at the fact
    that a random order of the keys is revealed.

    :param k: vector or Array of sint containing exactly :math:`0,\dots,n-1`
      in any order
    :param D: Array or MultiArray to sort
    :param reverse: wether :py:obj:`key` is a permutation in forward or
      backward order

    """
    assert len(k) == len(D)
    library.break_point()
    shuffle = types.sint.get_secure_shuffle(len(k))
    k_prime = k.get_vector().secure_permute(shuffle).reveal()
    idx = types.Array.create_from(k_prime)
    if reverse:
        D.assign_vector(D.get_slice_vector(idx))
        library.break_point()
        D.secure_permute(shuffle, reverse=True)
    else:
        D.secure_permute(shuffle)
        library.break_point()
        v = D.get_vector()
        D.assign_slice_vector(idx, v)
    library.break_point()
    instructions.delshuffle(shuffle)

def radix_sort(k, D, n_bits=None, signed=True):
    """ Sort in place according to key.

    :param k: keys (vector or Array of sint or sfix)
    :param D: Array or MultiArray to sort
    :param n_bits: number of bits in keys (int)
    :param signed: whether keys are signed (bool)

    """
    assert len(k) == len(D)
    bs = types.Matrix.create_from(k.get_vector().bit_decompose(n_bits))
    if signed and len(bs) > 1:
        bs[-1][:] = bs[-1][:].bit_not()
    radix_sort_from_matrix(bs, D)

def radix_sort_from_matrix(bs, D):
    n = len(D)
    for b in bs:
        assert(len(b) == n)
    B = types.sint.Matrix(n, 2)
    h = types.Array.create_from(types.sint(types.regint.inc(n)))
    @library.for_range(len(bs))
    def _(i):
        b = bs[i]
        B.set_column(0, 1 - b.get_vector())
        B.set_column(1, b.get_vector())
        c = types.Array.create_from(dest_comp(B))
        reveal_sort(c, h, reverse=False)
        @library.if_e(i < len(bs) - 1)
        def _():
            reveal_sort(h, bs[i + 1], reverse=True)
        @library.else_
        def _():
            reveal_sort(h, D, reverse=True)

def topK_sort(keys, D, K, n_bits=None):
    """
    :param k: keys (Array of sint or sfix)
    :param D: Array or MultiArray to sort
    :param K: number of top elements to find
    :param n_bits: number of bits in keys (int)
    """
    assert len(keys) == len(D)
    n = len(D)

    # 用于存储当前找到的 top K 元素的数组
    top_values = types.sfix.Matrix(K, 1)
    top_indices = types.sint.Matrix(K, 1)

    # 初始化 top K 数组
    for i in range(K):
        top_values[i][0] = types.sfix(-100)  # 一个很小的初始值
        top_indices[i][0] = types.sint(-1)    # 无效的索引

    @library.for_range(n)
    def _(i):
        current_value = keys[i]
        current_index = i

        # 遍历当前 top K 列表，查找插入位置
        for j in range(K):
            # 检查当前值是否应该插入 top K 列表
            should_insert = current_value > top_values[j][0]

            # 如果应该插入，更新 top K 列表
            if should_insert & types.sintbit(1):
                # 将当前值插入 top K 列表，并将剩余元素向下移动
                for k in range(K - 1, j, -1):
                    top_values[k][0] = top_values[k - 1][0]
                    top_indices[k][0] = top_indices[k - 1][0]
                top_values[j][0] = current_value
                top_indices[j][0] = current_index

    # 使用找到的 top K 索引来更新 D 数组
    # @library.for_range(K)
    # def _(i):
    #     D[i] = top_indices[i][0]
        # D[i] = D.get_vector()[top_indices[i][0]]
