# toolshop-automation-SonSy
# toolshop-automation-SonSy

![CI](https://github.com/vensson/toolshop-automation-SonSy/actions/workflows/ci.yml/badge.svg)

## Sprint 2B - Automation Testing

Dự án kiểm thử tự động website Toolshop sử dụng Python, Pytest, Playwright và pytest-bdd.

### Công nghệ sử dụng
- Python + Pytest
- Playwright
- pytest-bdd
- Docker Compose
- GitHub Actions

### Chạy kiểm thử BDD

```bash
pytest tests/bdd -v
```

### Chạy toàn bộ kiểm thử

```bash
pytest -v
```

## CI - GitHub Actions

Workflow CI thực hiện kiểm thử trên 3 trình duyệt:
- Chromium
- Firefox
- WebKit

### Minh chứng CI trên nhánh main

![CI Green](docs/screenshots/ci-green.png)

### Minh chứng Playwright Trace Viewer

![Trace Viewer](docs/screenshots/trace-viewer.png)

## Pull Request
<img width="1175" height="407" alt="image" src="https://github.com/user-attachments/assets/1016c4fc-91ad-451d-b13b-71b19b58543b" />

[Sprint 2B - BDD and CI workflow (#3)](https://github.com/vensson/toolshop-automation-SonSy/pull/3)
