from setuptools import setup,find_packages

setup(
    name='CarPlateGenerator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pillow'
    ],
    entry_points={
        'console_scripts': [
            'car-plate-generator=CarPlateGenerator:main',
        ]
    }
)