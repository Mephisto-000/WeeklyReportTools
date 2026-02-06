# Weekly Report Tool (週報小工具)

一個輕量級且具備生產力品質的 Python 桌面應用程式，用於管理您的每日工作紀錄。
使用 `customtkinter` 與 `openpyxl` 建置。

## 功能特色
- **行事曆檢視 (Calendar View)**: 瀏覽月份並選擇特定日期。
- **每日紀錄 (Daily Records)**: 檢視特定日期的工作日誌。
- **資料維護 (Maintenance)**: 輕鬆新增、編輯與刪除紀錄。
- **Excel 持久化儲存**: 所有資料皆自動儲存於本地端的 `work_reports.xlsx` 檔案中。

## 系統需求
- Python 3.13+
- `uv` (用於相依套件管理)

## 安裝與執行

1. **初始化環境**
   ```bash
   uv sync
   ```

2. **執行應用程式**
   ```bash
   uv run src/main.py
   ```
   *注意：如果您遇到模組匯入錯誤 (ModuleNotFoundError)，請確認您的 PYTHONPATH 包含目前目錄：*
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   uv run src/main.py
   ```

## 專案結構
```
src/
├── gui/          # UI 元件 (視窗框架、主程式)
├── models/       # 資料模型 (WorkRecord)
├── services/     # 商業邏輯 (Excel 存取服務)
├── utils/        # 工具模組 (日誌記錄)
└── main.py       # 程式進入點
```

## 資料儲存
應用程式會自動在專案根目錄建立 `work_reports.xlsx`。
**請勿在應用程式執行時手動修改此檔案，以免資料損壞。**

## 打包應用程式 (Packaging)

本專案使用 `Nuitka` 進行打包。

### macOS 版本 (.app)
若要在 macOS 上建立可執行的 `.app` 應用程式：

```bash
uv run python -m nuitka --standalone --enable-plugin=tk-inter --include-package-data=customtkinter --output-dir=dist --macos-create-app-bundle --macos-app-name="WeeklyReport" --macos-app-mode=gui src/main.py
```
打包完成後，您可以在 `dist/` 資料夾中找到 `WeeklyReport.app`。

### Windows 版本 (.exe)
若要建立 Windows 執行檔，請在 Windows 環境下執行：

```bash
uv run python -m nuitka --standalone --enable-plugin=tk-inter --include-package-data=customtkinter --output-dir=dist src/main.py
```
打包完成後，您可以在 `dist/` 資料夾中找到 `main.exe`。
