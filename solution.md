## 题目 1

### 1. 算法设计

矩阵 $A$ 与向量 $v$ 的乘积可以被转换为循环矩阵与向量的乘积，然后使用快速傅里叶变换 (FFT) 来加速计算。

#### 伪代码
```plaintext
function ToeplitzVectorMultiply(A_compressed, v):
  // A_compressed 是包含 a_0, ..., a_{2n-2} 的数组
  
  n = length(v)
  m = next_power_of_2(2 * n - 1) // 找到大于等于 2n-1 的最小的2的幂

  // 构造循环矩阵的第一列c
  c = create_vector(m)
  for i from 0 to n-1:
    c[i] = A_compressed[n - 1 + i]
  for i from 1 to n-1:
    c[m - i] = A_compressed[n - 1 - i]

  // 扩展v
  v_padded = create_vector(m)
  for i from 0 to n-1:
    v_padded[i] = v[i]

  // FFT
  fft_c = FFT(c)
  fft_v = FFT(v_padded)
  
  // 逐元素相乘
  fft_w = create_vector(m)
  for i from 0 to m-1:
    fft_w[i] = fft_c[i] * fft_v[i]

  // 逆FFT
  w_padded = IFFT(fft_w)

  result = create_vector(n)
  for i from 0 to n-1:
    result[i] = w_padded[i]
    
  return result
```

### 2. 复杂度分析

 - 构造循环列向量 $c$ 和填充向量 $v_padded$ 需要的时间与它们的长度 $m$ 成正比。由于 $m≈2n$，这个步骤的复杂度是 $O(n)$。 
 - 对长度为 $m$ 的向量进行FFT的标准算法的时间复杂度是 $O(mlogm)$。 进行了两次FFT，所以这步的复杂度是 $2⋅O(mlogm)=O(mlogm)$。 
 - 对两个长度为 $m$ 的向量进行逐元素相乘，需要 $m$ 次乘法操作。因此复杂度是 $O(m)$。 
 - 与FFT类似，逆FFT的时间复杂度也是 $O(mlogm)$。 
 - 从 $w_padded$ 中取出前 $n$ 个元素需要 $O(n)$ 的时间。

总体复杂度: $O(n)+O(mlogm)+O(m)+O(mlogm)+O(n)$，由于 $m$ 的选择是 $m≥2n−1$，通常取 $m≈2n$，因此总复杂度为 $O(nlogn)$。


## 题目 2

### 2. (1) 算法步骤

**预处理**:
 - 选择一个FFT的长度 $N$，要求 $N$ 是2的幂且 $N \ge n+m$。由于 $n \gg m$，$N$ 的数量级为 $O(n)$。
 - 主串转换: 将字符串`S`转换为两个数值序列 $s_1$ 和 $s_2$，长度都为 $n$。
   - $s_1[i] = \text{value}(S[i])$
   - $s_2[i] = (\text{value}(S[i]))^2$
 - 模式串转换: 将模式串`P`反转，然后转换为两个数值序列 $p_1$ 和 $p_2$，长度都为 $m$。
   - $p_1[j] = \alpha_{m-1-j} \cdot \text{value}(P_{m-1-j})$
   - $p_2[j] = \alpha_{m-1-j}$
 - 填充: 将 $s_1, s_2, p_1, p_2$ 的末尾都用0填充，使它们的长度达到 $N$。

**FFT计算**:
 - 对四个填充后的序列进行 FFT：
   - `FFT_s1 = FFT(s1_padded)`
   - `FFT_s2 = FFT(s2_padded)`
   - `FFT_p1 = FFT(p1_padded)`
   - `FFT_p2 = FFT(p2_padded)`

**频域卷积**:
 - 计算两个卷积结果（在频域中是逐点相乘）：
   - `Conv1 = FFT_s1 * FFT_p1` (对应第二项)
   - `Conv2 = FFT_s2 * FFT_p2` (对应第一项)

**逆 FFT**:
 - 将两个卷积结果从频域转换回时域：
   - `Result1 = IFFT(Conv1)`
   - `Result2 = IFFT(Conv2)`

**整合与查找**:
 - 预计算常数 `C = 第三项`。
 - 遍历所有可能的起始位置 $i$ (从 $0$ 到 $n-m$)：
   - $E(i) = \text{Result2}[i+m-1] - 2 \cdot \text{Result1}[i+m-1] + C$
   - 由于浮点数精度问题，检查 `abs(E(i))` 是否小于一个很小的阈值 (例如 $10^{-6}$)。
   - 如果满足条件，则位置 `i` 是一个匹配点。

### (2) 复杂度分析:

 - 预处理: 转换和填充字符串需要 $O(n+m)$。因为 $n \gg m$，所以是 $O(n)$。
 - FFT计算: 对长度为 $N$ 的序列进行 FFT 的复杂度是 $O(N \log N)$。我们执行了4次。 
 - 频域卷积: 逐点相乘需要 $O(N)$。 
 - 逆FFT: 两次 IFFT 需要 $O(N \log N)$。 
 - 整合: 遍历检查需要 $O(n)$。

因为 $N=O(n)$, 因此总时间复杂度为 $O(n \log n)$。

### 3. 优化想法

上述算法需要对4个序列（$s_1, s_2, p_1, p_2$）进行FFT，这构成了主要的计算开销，可以利用复数的虚部来将两个实数序列的FFT合并为一次复数FFT。
 - 构造两个复数序列：$A = s_2 + i \cdot s_1$，$B = p_2 + i \cdot p_1$
 - 只进行两次 FFT：`FFT_A = FFT(A)` 和 `FFT_B = FFT(B)`。
 - 计算频域乘积 `C_fft = FFT_A * FFT_B`。
 - `C_fft` 的结果是 `(FFT_s2 + i*FFT_s1) * (FFT_p2 + i*FFT_p1)`。展开后，其实部和虚部分别包含了我们需要的两个卷积 `s2*p2` 和 `s1*p1` 的信息（以及另外两个我们不需要的交叉卷积）。
 - 通过一些代数技巧，可以从 `IFFT(C_fft)` 的实部和虚部中分离出我们需要的两个卷积结果 `Result1` 和 `Result2`。这样，FFT/IFFT的总次数可以从4/2次减少到2/1次，大约能将这部分的计算量减半。







