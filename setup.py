import setuptools

setuptools.setup(
    name="tgmb",
    version="1.1.1",
    author="SomesH S",
    author_email="ksssomesh12@gmail.com",
    description="A Telegram Bot written in Python language to mirror files on the internet to Google Drive",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ksssomesh12/tg-mirror-bot",
    project_urls={
        "Bug Tracker": "https://github.com/ksssomesh12/tg-mirror-bot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt', 'r', encoding='utf-8').read().split('\n'),
    scripts=['extract'],
    python_requires=">=3.8",
)
