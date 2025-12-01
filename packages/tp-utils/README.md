## tp-utils 
topia 工具类发布模版
该项目工程基于 [poetry](https://python-poetry.org/) 管理依赖和发布。

### 安装依赖
```bash
poetry install
```

### 测试
```bash
poetry run test
```

### 构建
```bash
poetry run build
```

### 发布
```bash
poetry run publish
```

### 环境变量
- `POETRY_REPOSITORY`：发布到的 poetry 仓库名称，默认 `cnb-pypi`
- `TWINE_REPOSITORY`：发布到的 twine 仓库名称，默认 `cnb-pypi`
- `TWINE_REPOSITORY_URL`：发布到的 twine 仓库 URL，默认 `https://pypi.org/legacy/`



