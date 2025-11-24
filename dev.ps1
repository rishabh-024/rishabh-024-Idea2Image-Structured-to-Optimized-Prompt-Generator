<#
  PowerShell helper for Idea2Image Makefile targets
  Usage: .\dev.ps1 -Task dev-install
#>
Param(
    [string]$Task = 'help'
)

function Show-Help {
    Write-Host "Idea2Image dev helper - available tasks:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  -Task install        : Install production dependencies"
    Write-Host "  -Task dev-install    : Install dev dependencies"
    Write-Host "  -Task run            : Run the application"
    Write-Host "  -Task test           : Run tests"
    Write-Host "  -Task test-cov       : Run tests with coverage"
    Write-Host "  -Task lint           : Run linters (flake8 + mypy)"
    Write-Host "  -Task format         : Format code (black + isort)"
    Write-Host "  -Task clean          : Clean Python caches and build artifacts"
    Write-Host "  -Task docker-build   : Build docker image"
    Write-Host "  -Task docker-run     : Run docker container"
    Write-Host "  -Task help           : Show this help"
}

function Run-Command([string]$cmd) {
    Write-Host "PS> $cmd" -ForegroundColor Yellow
    Invoke-Expression $cmd
    return $LASTEXITCODE
}

switch ($Task) {
    'help' { Show-Help; break }
    'install' {
        Run-Command 'python -m pip install -r requirements.txt'
        break
    }
    'dev-install' {
        Run-Command 'python -m pip install -e ".[dev]"'
        break
    }
    'run' {
        Run-Command 'python -m app.ui'
        break
    }
    'test' {
        Run-Command 'pytest tests/ -v'
        break
    }
    'test-cov' {
        Run-Command 'pytest tests/ -v --cov=app --cov-report=html'
        break
    }
    'lint' {
        Run-Command 'flake8 app/ tests/'
        Run-Command 'mypy app/ --ignore-missing-imports'
        break
    }
    'format' {
        Run-Command 'black app/ tests/'
        Run-Command 'isort app/ tests/'
        break
    }
    'clean' {
        Write-Host 'Cleaning __pycache__, .pyc, coverage and build artifacts...' -ForegroundColor Cyan
        Get-ChildItem -Path . -Recurse -Force -Include '__pycache__' -Directory -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
        Get-ChildItem -Path . -Recurse -Force -Include '*.pyc' -File -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue }
        Remove-Item -Path .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -Path .mypy_cache -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -Path build -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -Path dist -Recurse -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path . -Force -Filter '*.egg-info' -Directory -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
        Remove-Item -Path .coverage -Force -ErrorAction SilentlyContinue
        Remove-Item -Path htmlcov -Recurse -Force -ErrorAction SilentlyContinue
        break
    }
    'docker-build' {
        Run-Command 'docker build -t idea2image:latest .'
        break
    }
    'docker-run' {
        if (-not $env:OPENAI_API_KEY) { Write-Host 'Warning: OPENAI_API_KEY not set in environment.' -ForegroundColor Red }
        Run-Command 'docker run -p 7860:7860 -e OPENAI_API_KEY=$env:OPENAI_API_KEY idea2image:latest'
        break
    }
    Default {
        Write-Host "Unknown task: $Task`n" -ForegroundColor Red
        Show-Help
        break
    }
}
