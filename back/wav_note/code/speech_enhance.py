import numpy as np
import wave
import math
import ctypes as ct


class FloatBits(ct.Structure):
    _fields_ = [
        ('M', ct.c_uint, 23),
        ('E', ct.c_uint, 8),
        ('S', ct.c_uint, 1)
    ]


class Float(ct.Union):
    _anonymous_ = ('bits',)
    _fields_ = [
        ('value', ct.c_float),
        ('bits', FloatBits)
    ]


def nextpow2(x): #y=nextpow2 当y是最小的满足 2^y>=x 的整数
    if x < 0:
        x = -x
    if x == 0:
        return 0
    d = Float()
    d.value = x
    if d.M == 0:
        return d.E - 127
    return d.E - 127 + 1

def noise_reduction(filename, output_file):
    f = wave.open(filename) # 打开.wav文件
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4] #读取文件格式信息
    fs = framerate
    str_data = f.readframes(nframes) # 波形数据
    f.close()
    x = np.fromstring(str_data, dtype=np.short) # 波形数据转数组
    
    # 参数设置
    len0 = 20 * fs // 1000 # 样本中帧的大小
    PCT = 50 # 窗口重叠占帧百分比
    len1 = len0 * PCT // 100  # 重叠窗口大小
    len2 = len0 - len1   # 非重叠窗口
    Thres = 3 # 阈值
    Expnt = 2.0 # 指数γ
    beta = 0.002 
    G = 0.9
    
    win = np.hamming(len0) # 初始化hamming窗
    win_gain = len2 / sum(win)  # 归一化因子
    nFFT = 2 * 2 ** (nextpow2(len0))
    noise_mean = np.zeros(nFFT)

    j = 0
    for i in range(1, 6):
        noise_mean = noise_mean + abs(np.fft.fft(win * x[j:j + len0], nFFT))
        j = j + len0
    noise_mu = noise_mean / 5 # 根据前5帧计算底噪

    k = 1
    img = 1j
    x_old = np.zeros(len1)
    Nframes = len(x) // len2 - 1
    xfinal = np.zeros(Nframes * len2)

    # =========================    Start Processing   ===============================
    for n in range(0, Nframes):
        insign = win * x[k-1:k + len0 - 1]  # Windowing
        spec = np.fft.fft(insign, nFFT) # 傅里叶变换
        sig = abs(spec)   
        theta = np.angle(spec) # 相位
        SNRseg = 10 * np.log10(np.linalg.norm(sig, 2) ** 2 / np.linalg.norm(noise_mu, 2) ** 2) # 段信噪比

        def berouti(SNR):
            a = 0
            if -5.0 <= SNR <= 20.0:
                a = 4 - SNR * 3 / 20
            else:
                if SNR < -5.0:
                    a = 5
                if SNR > 20:
                    a = 1
            return a

        def berouti1(SNR):
            a = 0
            if -5.0 <= SNR <= 20.0:
                a = 3 - SNR * 2 / 20
            else:
                if SNR < -5.0:
                    a = 4
                if SNR > 20:
                    a = 1
            return a

        if Expnt == 1.0:  # 幅度谱
            alpha = berouti1(SNRseg)
        else:  # 功率谱
            alpha = berouti(SNRseg)
      
        sub_speech = sig ** Expnt - alpha * noise_mu ** Expnt
        diffw = sub_speech - beta * noise_mu ** Expnt

        def find_index(x_list):
            index_list = []
            for i in range(len(x_list)):
                if x_list[i] < 0:
                    index_list.append(i)
            return index_list

        z = find_index(diffw)
        if len(z) > 0:
            sub_speech[z] = beta * noise_mu[z] ** Expnt # 下限值
           
        if SNRseg < Thres:  # 更新
            noise_temp = G * noise_mu ** Expnt + (1 - G) * sig ** Expnt  # 平滑处理噪声功率谱
            noise_mu = noise_temp ** (1 / Expnt)  # 新的噪声幅度谱
        
        sub_speech[nFFT // 2 + 1:nFFT] = np.flipud(sub_speech[1:nFFT // 2]) # 矩阵上下翻转
        x_phase = (sub_speech ** (1 / Expnt)) * (np.array([math.cos(x) for x in theta]) + img * (np.array([math.sin(x) for x in theta])))
        xi = np.fft.ifft(x_phase).real # 傅里叶反变换
        xfinal[k-1:k + len2 - 1] = x_old + xi[0:len1]
        x_old = xi[0 + len1:len0]
        k = k + len2
    wf = wave.open(output_file, 'wb') # 保存文件
    wf.setparams(params)
    wave_data = (win_gain * xfinal).astype(np.short) 
    wf.writeframes(wave_data.tostring())
    wf.close()