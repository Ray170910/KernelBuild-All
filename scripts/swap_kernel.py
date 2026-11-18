#!/usr/bin/env python3
"""swap_kernel.py — 参考镜像内核载荷替换(已知可开机的 boot + 新编译的 kernel)"""
import struct, sys

ref_path, kernel_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
ref = open(ref_path, 'rb').read()
kern = open(kernel_path, 'rb').read()
out = bytearray(ref)
struct.pack_into('<I', out, 8, len(kern))
out[4096:4096+len(kern)] = kern
ref_ks = struct.unpack('<I', ref[8:12])[0]
if len(kern) < ref_ks:
    for i in range(4096+len(kern), 4096+ref_ks): out[i] = 0
open(out_path, 'wb').write(out)
print(f"swap: ref={len(ref)//1024//1024}MB kernel={len(kern)//1024}KB -> {out_path}")
