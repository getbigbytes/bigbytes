import setuptools


def readme():
    with open('README.md', encoding='utf8') as f:
        README = f.read()
    return README


requirements = []
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        if line.startswith('# extras'):
            break
        requirements.append(line)

setuptools.setup(
    name='bigbytes-integrations',
    version='0.0.0',
    author='Digitrans Inc',
    author_email='eng@bigbytes.ai',
    description='',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/digitranslab/bigbytes',
    packages=setuptools.find_packages('.'),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={},
    extras_require={},
)
