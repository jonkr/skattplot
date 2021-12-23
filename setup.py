from distutils.core import setup

setup(
    name='atax',
    version='0.1dev',
    packages=['atax',],
    license='MIT',
    package_dir={
        'atax': 'atax'
    },
    package_data={
        'atax': ['data/*.txt']
    },
    include_package_data=True,
)
