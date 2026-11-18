# KernelBuild-All — 一键全量内核编译

## 使用

1. **Repository Secrets**: Settings → Secrets → Actions → 添加 `PATCH_TOKEN`
   (GitHub PAT, 需 `contents:read` 权限于 `Ray170910/--------` 私有补丁仓库)

2. **一键全量**: Actions → 🚀 一键全量编译 → Run workflow

3. **单线构建**: 各 workflow 独立可用, 默认选项已按规范锁定

## 构建规范(全部锁定)

| 选项 | 值 |
|---|---|
| KernelSU | **禁用** |
| KPM | **禁用** |
| BBG 防格机 | **启用** |
| CVE-2026-43499 rtmutex | **应用**(守卫式) |
| ZRAM 增强(lz4+zstd) | **启用** |
| LZ4KD | 禁用 |
| SUSFS | 禁用 |
| ADIOS | 保持上游 |
| Droidspaces | 保持上游 |

## 上游对照表(跟上游更新时 diff 基准 commit)

| 本仓库 workflow | 上游仓库 | 上游文件 | 基准 | 产物名 |
|---|---|---|---|---|
| `fastbuild_6.12.23_mtk.yml` | `sm8850` | `.github/workflows/fastbuild_6.12.23_mtk.yml` | `b32090d84c` | `AK3-一加天玑6.12.23` |
| `fastbuild_6.12.58_mtk.yml` | `sm8850` | `.github/workflows/fastbuild_6.12.58_mtk.yml` | `aa0632f4a0` | `AK3-一加天玑6.12.58` |
| `fastbuild_6.12.23_gki.yml` | `sm8850` | `.github/workflows/fastbuild_6.12.23_gki.yml` | `50486433f6` | `AK3-一加骁龙6.12.23` |
| `fastbuild_6.12.69_gki.yml` | `sm8850` | `.github/workflows/fastbuild_6.12.69_gki.yml` | `bef88aa301` | `AK3-android16-6.12-69` |
| `fastbuild_6.12.58.yml` | `sm8850` | `.github/workflows/fastbuild_6.12.58.yml` | `9397ab4068` | `AK3-一加骁龙6.12.58` |
| `fastbuild_6.1.118_peek.yml` | `sm8650` | `.github/workflows/fastbuild_6.1.118_peek.yml` | `c77c30df74` | `Peek-AK3-一加骁龙6.1.118` |
| `fastbuild_6.1.118.yml` | `sm8650` | `.github/workflows/fastbuild_6.1.118.yml` | `9732b7c12a` | `AK3-一加骁龙6.1.118` |
| `fastbuild_6.1.141.yml` | `sm8650` | `.github/workflows/fastbuild_6.1.141.yml` | `ba8f3bc4ed` | `AK3-一加骁龙6.1.141` |
| `fastbuild_6.6.89_mtk_peek.yml` | `sm8750` | `.github/workflows/fastbuild_6.6.89_mtk_peek.yml` | `3e05457c5d` | `Peek-AK3-一加天玑6.6.89` |
| `fastbuild_6.6.89_mtk.yml` | `sm8750` | `.github/workflows/fastbuild_6.6.89_mtk.yml` | `02c436abfa` | `AK3-一加天玑6.6.89` |
| `fastbuild_6.6.89.yml` | `sm8750` | `.github/workflows/fastbuild_6.6.89.yml` | `8c75e9e62a` | `AK3-一加骁龙6.6.89` |
| `Build_Lenovo_sm8750.yml` | `Lenovo_sm8750` | `.github/workflows/Build_Lenovo_sm8750.yml` | `e3cdaae376` | `Boot-四代` |
| `Build_Lenovo_sm8750_peek.yml` | `Lenovo_sm8750` | `.github/workflows/Build_Lenovo_sm8750_peek.yml` | `ba70ecb1eb` | `Peek-Boot-四代` |
| `kernel-a12-5-10.yml` | `GKI` | `.github/workflows/kernel-a12-5-10.yml` | `3be8663416` | `AK3-android12-5.10-*` |
| `kernel-a13-5-15.yml` | `GKI` | `.github/workflows/kernel-a13-5-15.yml` | `3be8663416` | `AK3-android13-5.15-*` |
| `kernel-a14-6-1.yml` | `GKI` | `.github/workflows/kernel-a14-6-1.yml` | `0288cee9b3` | `AK3-android14-6.1-*` |
| `kernel-a15-6-6.yml` | `GKI` | `.github/workflows/kernel-a15-6-6.yml` | `ceba8c6457` | `AK3-android15-6.6-118` |
| `kernel-a16-6-12.yml` | `GKI` | `.github/workflows/kernel-a16-6-12.yml` | `ef0d7edba9` | `AK3-android16-6.12-30` |
| `gki-build.yml` | GKI | `.github/workflows/build.yml` | 原样 | — (共享引擎) |
| `gki-get-manager.yml` | GKI | `.github/workflows/get-manager.yml` | 原样 | — |

> 日期前缀 `$(date +%Y%m%d)-` 动态生成, 如 `20261118-AK3-一加天玑6.12.23.zip`
