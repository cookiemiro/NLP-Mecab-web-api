import setuptools
import os

"""
참고링크
    - Setuptools reference : https://setuptools.readthedocs.io/en/latest/setuptools.html
    - Pytorch : https://discuss.pytorch.org/t/torch-cpu-as-a-dependency-of-package/53978/2
    - Setuptools 사용법(1) : https://rampart81.github.io/post/python_package_publish/
    - Setuptools 사용법(2) : http://egloos.zum.com/mcchae/v/10546273
    - setup에서 shell script를 입력하는 방법 : https://stackoverflow.com/questions/17887905/python-setup-py-to-run-shell-script
    - Setuptools 사용법(3) : https://code.tutsplus.com/ko/tutorials/how-to-write-your-own-python-packages--cms-26076
"""

setuptools.setup(
    name="keywordExtraction",
    version="0.7",
    author="Sangyoun Paik",
    author_email="sangyoun.paik@actionpower.kr",
    description="Keyword Extraction by TF-IDF",
    package_dir={"" : "src"},
    packages=setuptools.find_packages('src'),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'nltk==3.7',
        'konlpy'
    ],
    python_requires='>=3.6',
)
