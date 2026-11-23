#!/usr/bin/env python3
"""swap_kernel.py — 参考镜像内核载荷替换(已知可开机的 boot + 新编译的 kernel)

两条路径, 按参考镜像自动判别:
  QC (PKG110/Ace5): payload 直接放裸 Image → 原逻辑不变, 实机验证可开机
  MTK (PLC110/Ace5Ultra): bootloader 只认 MTK LZ4 legacy 压缩流, 裸 Image 直接死
    → magic 0x184C2102 + 每块 u32压缩长 + ≤8MB lz4 block (level 12)
    → kernel_size@8 = 流总长, 流后清零到 AVB0 头, AVB 区原封保留

MTK 路径 2026-11-23 实机验证: peek/yolo v4 逐字节即此配方, PLC110 开机稳定。
依赖: MTK 路径需 lz4 (pip install lz4), QC 路径纯标准库 —— import 放分支内。
"""
import struct, sys

ref_path, kernel_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
ref = open(ref_path, 'rb').read()
kern = open(kernel_path, 'rb').read()
out = bytearray(ref)

MTK_MAGIC = b'\x02\x21\x4c\x18'


def find_vbmeta(d):
    """定位 AVB0 头: 从参考镜像自己的 kernel 流结束处往后扫 (PLC110 的 64MB 尾部
    无 AVBf footer, 只能扫头)。命中后做字段交叉校验, 排除残留垃圾里的巧合。"""
    pos = 4096 + struct.unpack('<I', d[8:12])[0]
    sig_of = {0: (0,), 1: (256,), 2: (512,), 3: (1024,), 4: (64, 80), 7: (64, 80)}
    while True:
        pos = d.find(b'AVB0', pos)
        if pos < 0:
            return -1
        auth = struct.unpack_from('>Q', d, pos + 12)[0]
        aux = struct.unpack_from('>Q', d, pos + 20)[0]
        algo = struct.unpack_from('>I', d, pos + 28)[0]
        hash_sz = struct.unpack_from('>Q', d, pos + 40)[0]
        sig_sz = struct.unpack_from('>Q', d, pos + 56)[0]
        pkey_sz = struct.unpack_from('>Q', d, pos + 72)[0]
        if (algo in sig_of and sig_sz in sig_of[algo] and hash_sz in (0, 32, 48, 64)
                and sig_sz <= auth <= 8192 and pkey_sz <= aux <= 8192
                and 256 + auth + aux <= 16384):
            return pos
        pos += 4


if ref[4096:4100] == MTK_MAGIC:
    import lz4.block

    avb_off = find_vbmeta(ref)
    if avb_off < 0:
        sys.exit(f"swap: MTK 参考镜像里找不到合法 AVB0 头 — 参考镜像损坏?")
    budget = avb_off - 4096

    CH = 8 * 1024 * 1024
    blocks = [lz4.block.compress(kern[o:o + CH], mode='high_compression',
                                 compression=12, store_size=False)
              for o in range(0, len(kern), CH)]
    stream = MTK_MAGIC + b''.join(struct.pack('<I', len(c)) + c for c in blocks)
    if len(stream) > budget:
        sys.exit(f"swap: LZ4 流 {len(stream)}B 超 MTK 预算 {budget}B (AVB0@{avb_off:#x}) — 内核变大太多")

    struct.pack_into('<I', out, 8, len(stream))
    out[4096:avb_off] = stream + b'\x00' * (budget - len(stream))
    print(f"swap[MTK]: ref={len(ref)//1024//1024}MB kernel={len(kern)//1024}KB "
          f"-> lz4 stream={len(stream)}B (AVB0@{avb_off:#x}, spare {budget - len(stream)}B) -> {out_path}")
else:
    struct.pack_into('<I', out, 8, len(kern))
    out[4096:4096 + len(kern)] = kern
    ref_ks = struct.unpack('<I', ref[8:12])[0]
    if len(kern) < ref_ks:
        for i in range(4096 + len(kern), 4096 + ref_ks):
            out[i] = 0
    print(f"swap[QC]: ref={len(ref)//1024//1024}MB kernel={len(kern)//1024}KB -> {out_path}")

open(out_path, 'wb').write(out)
