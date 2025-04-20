from setuptools import setup, find_packages

setup(
    name='echo_ria',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['torch', 'opencv-python', 'numpy', 'matplotlib'],
    author='Youngkook Kim',
    description='Echo-RIA: Lightweight AI Model for Dermatological Marker Robustness',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/youngkookkim/echo-ria',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
