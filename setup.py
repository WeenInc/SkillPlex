from setuptools import setup, find_packages

setup(
    name='SkillPlex',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'openai>=0.27.0',
    ],
    extras_require={
        'test': ['pytest'],
    },
    include_package_data=True,
    package_data={
        '': ['*.sql'],  # Include all .sql files, if you have any
    },
    author='Leonardo Cuco',  # Replace with your name
    author_email='leonardo@ween.ai',  # Replace with your email
    description='Expand your LLM with an infinity of skills built by the community',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://forelight.ai/SkillPlex',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)