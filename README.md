# ViaStitching for KiCad

ViaStitching 是一款为 KiCAD 设计的实用插件，旨在通过在 PCB 的铜箔区域（Zones）自动生成过孔缝合（Via Stitching），以增强地平面或电源平面的导电性能并降低电磁干扰 (EMI)。

## ✨ 功能特性

- **自动生成过孔**：快速在指定网络的铜箔区域填充过孔阵列。
- **多种填充模式**：支持矩形 (Rectangular)、星形 (Star)、同心圆 (Concentric) 及轮廓 (Outline) 等多种铺设方案。
- **灵活的参数控制**：可自定义过孔尺寸、钻孔直径、过孔间距及安全距离。
- **智能筛选**：支持仅在选中的区域内生成过孔，或在所有指定网络的区域内生成。
- **快速清理**：一键删除由插件生成的过孔组。
- **完全汉化**：界面全面汉化，降低使用门槛。
- **KiCAD 10 兼容**：针对 KiCAD 10.0.0 版本进行了 API 适配与修复。

## 🚀 安装方法

### 方法 1：通过 KiCAD 插件管理器安装 (推荐)
1. 打开 KiCAD $\rightarrow$ **插件和内容管理器 (Plugin and Content Manager)**。
2. 点击 **安装插件 (Install Plugin...)**。
3. 选择下载的 `ViaStitching.zip` 安装包。
4. 重启 KiCAD。

### 方法 2：通过 Git 仓库地址安装
在 KiCAD 插件管理器中，可以使用以下仓库地址直接安装：
`https://github.com/jsreynaud/kicad-action-scripts`

### 方法 3：手动安装
1. 下载仓库中的 `ViaStitching` 文件夹。
2. 将其复制到 KiCAD 插件目录：
   - **Windows**: `%AppData%\kicad\10.0\plugin\`
   - **Linux/macOS**: `~/.kicad_plugin/`
3. 重启 KiCAD。

## 🛠️ 使用说明

1. 在 PCB 编辑器中，点击工具栏的 **Via Stitching** 图标或在菜单中找到 **修改 PCB $\rightarrow$ 过孔缝合生成器**。
2. 在弹出的对话框中设置：
   - **过孔尺寸**：定义铜箔直径。
   - **钻孔尺寸**：定义钻孔直径。
   - **过孔网格**：定义过孔之间的间距。
   - **网络名称**：选择需要缝合的网络（如 GND）。
   - **填充图案**：选择过孔的排布形状。
3. 点击 **运行**，插件将自动计算并放置过孔。
4. **注意**：运行后请记得对 PCB 区域执行一次 **填充 (Refill)** 操作以更新铜箔。

## 📄 许可证
本插件采用 [GNU General Public License v2.0](LICENSE.md) 协议开源。
