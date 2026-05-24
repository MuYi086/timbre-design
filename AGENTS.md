# Repository Guidelines

## 宪章与语言 (Constitution & Language)

修改代码、数据、文档或生成资产前，先阅读 [CONSTITUTION.md](CONSTITUTION.md)。本项目面向用户和贡献者的文档、总结、评审意见和代理输出默认中文优先。必须保留英文术语时，首次出现应补中文说明，例如 `voice casting`（角色配音映射）。

## 项目结构与模块组织 (Project Structure)

- `src/timbre_design/`：包源码，包含音色库加载、校验、匹配、控制提示渲染、角色配音映射和资产生成逻辑。
- `src/timbre_design/data/`：内置音色库数据，重点维护 `voices_v2_106.json` 和字段说明文档。
- `tests/`：pytest（Python 测试框架）测试套件，按模块行为组织。
- `samples/generated/<voice_id>/`：一音色一目录的派生资产，包含 `voice.json`、`README.md`、`sample.wav`、`sample.mp3` 等。

## 构建、测试与开发命令 (Commands)

- `PYTHONPATH=src python -m timbre_design validate --json`：校验内置音色库。
- `python -m pytest`：运行全部测试。
- `python -m compileall src tests`：检查 Python 语法和导入编译。
- `PYTHONPATH=src python -m timbre_design assets --output-dir samples/generated`：刷新全部音色目录元数据。
- `PYTHONPATH=src python -m timbre_design match --name 林黛玉 --gender female --age young --hint "清冷、敏感"`：从命令行测试音色匹配。

## 代码风格与命名 (Style)

使用 Python 3.11+、4 空格缩进、类型标注和小型可测试函数。JSON 字段保持稳定并使用 `snake_case`（小写下划线），例如 `voice_id`、`style_tags`、`fit_roles`、`not_good_for`。音色 ID 必须稳定，格式为 `v_zh_{group}_{nnn}`，例如 `v_zh_narr_001`。

## 测试规范 (Testing)

测试文件放在 `tests/test_<module>.py`，测试函数命名为 `test_<behavior>()`。修改匹配、校验、控制提示、角色映射或资产输出时，必须增加聚焦的回归测试。

## 提交与 PR 规范 (Commit & Pull Request)

近期提交使用简短的 conventional commits（约定式提交），例如 `feat: schema文档`。优先使用 `feat:`、`fix:`、`test:`、`docs:` 加中文或英文摘要。PR（合并请求）应说明变更内容、原因、验证命令和生成资产影响；若音频有变化，说明是否重新生成 `samples/generated` 以及 WAV/MP3 数量。

## 安全与配置提示 (Security)

不要提交密钥、本地环境文件或机器专属路径。大体积音频资产提交前必须单独确认，因为会显著增加仓库体积。
