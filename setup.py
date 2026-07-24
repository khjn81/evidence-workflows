from setuptools import find_packages, setup


setup(
    name="evidence-workflows",
    version="0.1.0",
    description="Deterministic, privacy-aware policy interviews for evidence-ready work updates",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    entry_points={"console_scripts": ["evidence-workflows=evidence_workflows.cli:main"]},
)
