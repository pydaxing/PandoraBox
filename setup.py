from setuptools import setup, find_packages

setup(
    name='PandoraBox',
    version='1.0.0',
    packages=find_packages(),
    description='Pandora Box Is All You Need. You Can Create Python Environment, Execut Python, Close Python Environment Freely and Easily.',
    long_description=open('README.MD').read(),
    long_description_content_type='text/markdown',
    author='pydaxing',
    author_email='pydaxing@gmail.com',
    url='https://github.com/pydaxing/PandoraBox',
    entry_points={
        'console_scripts': [
            'pbox=pbox.app:main'
        ],
    },
    package_data={
        # 如果a.txt在pbox包中
        'pbox': ['API_KEYS.txt'],
    },
    install_requires=[
        # 依赖列表
        'requests',
        'anyio==3.*',
        'h11>=0.11,<0.13',
        'fastapi',
        'uvicorn',
        'pydantic',
        'jupyter-client',
        'ipython',
        'ipykernel',
        'pandas',
        'numpy',
        'matplotlib',
        'jsonlines',
    ],

)


