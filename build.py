from __future__ import ( division, absolute_import, print_function, unicode_literals )
import glob
import os
import sys
import tarfile
import shutil, errno
import subprocess
from zipfile import ZipFile

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

from pybuilder.core import init, task, Author
from git import Repo


name = 'pynlp-sandbox'
authors = [Author('Paulius Danenas', 'danpaulius@gmail.com')]
license = 'Apache License, Version 2.0'
summary = 'Sandbox for NLP related tasks'
url = 'https://github.com/paudan/pynlp-sandbox'
version = '0.1'

default_task = ['create_sandbox']

languages = ['en', 'nl', 'de']
install_dir = os.getcwd()

## TreeTagger settings
TREETAGGER_VER = '3.2'
TREETAGGER_DIR = 'treetagger'
treetagger_url = "http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/"
treetagger_win = "tree-tagger-windows-{}.zip".format(TREETAGGER_VER)
treetagger_linux = "tree-tagger-linux-{}.1.tar.gz".format(TREETAGGER_VER)

## OpenNLP settings
OPENNLP_DIR = 'apache-opennlp'
OPENNLP_MODELS_DIR = 'opennlp_models'
opennlp_url = 'http://opennlp.sourceforge.net/models-1.5'
opennlp_file = 'http://www-eu.apache.org/dist/opennlp/opennlp-1.8.0/apache-opennlp-1.8.0-bin.zip'


# Adopted from https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
def download_file(url, desc=None):
    u = urllib2.urlopen(url)
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename


def get_file(source, url, targetDir, logger):
    if not targetDir is None:
        source = os.path.join(targetDir, source)
    if not os.path.isfile(source):
        try:
            download_file(url, desc=targetDir)
        except urllib2.HTTPError, exc:
            logger.error("Error downloading file from '{}'".format(url))


def extract_file(source, targetdir):
    topdir = targetdir
    if source.endswith(".tar.gz") or source.endswith(".tar.bz2"):
        tar = tarfile.open(source)
        tar.extractall(targetdir)
        topdir = os.path.commonprefix(tar.getnames()).rstrip("/")
        tar.close()
    elif source.endswith(".zip"):
        zip = ZipFile(source, 'r')
        zip.extractall(targetdir)
        topdir = os.path.commonprefix(zip.namelist()).rstrip("/")
        zip.close()
    return topdir if targetdir is None else targetdir


def copy_source(source, target, logger, isTargetDir=False):

    def copytree(src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    if isTargetDir and not (os.path.exists(target) and os.path.isdir(target)):
        os.mkdir(target)
    try:
        copytree(source, target)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(source, target)
        else:
            logger.error(exc.strerror)


def download_treetagger_files(langlist, logger):
    lang_map = {
        'bg': ['bulgarian'],
        'es': ['catalan', 'galician', 'spanish', 'spanish-ancora'],
        'cz': ['czech'],
        'nl': ['dutch'], # dutch2 model uses numerical tags
        'en': ['english'],
        'ee': ['estonian'],
        'fi': ['finnish'],
        'fr': ['french'],
        'de': ['german', 'middle-high-german'],
        'it': ['italian', 'latin', 'latinIT'],
        'mo': ['mongolian'],
        'pl': ['polish'],
        'pt': ['portuguese', 'portuguese-finegrained'],
        'ro': ['romanian'],
        'ru': ['russian'],
        'sk': ['slovak', 'slovak2'],
        'sl': ['slovenian']
    }
    chunker_map = {
        'en': 'english',
        'fr': 'french',
        'de': 'german',
        'es': 'spanish'
    }
    for lang in langlist:
        for path in lang_map.get(lang, []):
            if not os.path.isfile(os.path.join(TREETAGGER_DIR, "{0}-par-linux-{1}-utf8.bin.gz".format(path, TREETAGGER_VER))):
                try:
                    download_file("{0}/{1}-par-linux-{2}-utf8.bin.gz".format(treetagger_url, path, TREETAGGER_VER),
                                  desc=TREETAGGER_DIR)
                except urllib2.HTTPError, exc:
                    logger.error(exc.message)
        if lang == 'it':
            if not os.path.isfile(os.path.join(TREETAGGER_DIR,"italian-par2-linux-{0}-utf8.bin.gz".format(TREETAGGER_VER))):
                try:
                    download_file("{0}/italian-par2-linux-{1}-utf8.bin.gz".format(treetagger_url, TREETAGGER_VER),
                                  desc=TREETAGGER_DIR)
                except urllib2.HTTPError, exc:
                    logger.error(exc.message)
        # Download chunker files as well
        if chunker_map.has_key(lang):
            if not os.path.isfile(os.path.join(TREETAGGER_DIR,
                                               "{0}-chunker-par-linux-{1}-utf8.bin.gz".format(chunker_map[lang], TREETAGGER_VER))):
                try:

                    download_file("{0}/{1}-chunker-par-linux-{2}-utf8.bin.gz".format(treetagger_url, chunker_map[lang], TREETAGGER_VER),
                                  desc=TREETAGGER_DIR)
                except urllib2.HTTPError, exc:
                    logger.error(exc.message)



def download_opennlp_files(langlist, logger):
    lang_map = {
        'da': ['da-token.bin', 'da-sent.bin', 'da-pos-maxent.bin', 'da-pos-perceptron.bin'],
        'de': ['de-token.bin', 'de-sent.bin', 'de-pos-maxent.bin', 'de-pos-perceptron.bin'],
        'en': ['en-token.bin', 'en-sent.bin', 'en-pos-maxent.bin', 'en-pos-perceptron.bin',
               'en-ner-date.bin', 'en-ner-location.bin', 'en-ner-money.bin', 'en-ner-organization.bin',
               'en-ner-percentage.bin', 'en-ner-person.bin', 'en-ner-time.bin', 'en-chunker.bin',
               'en-parser-chunking.bin'],
        'es': ['es-ner-person.bin', 'es-ner-organization.bin', 'es-ner-location.bin', 'es-ner-misc.bin'],
        'nl': ['nl-token.bin', 'nl-sent.bin', 'nl-pos-maxent.bin', 'nl-pos-perceptron.bin',
               'nl-ner-person.bin', 'nl-ner-location.bin', 'nl-ner-misc.bin', 'nl-ner-organization.bin'],
        'pt': ['pt-token.bin', 'pt-sent.bin', 'pt-pos-maxent.bin', 'pt-pos-perceptron.bin'],
        'se': ['se-token.bin', 'se-sent.bin', 'se-pos-maxent.bin', 'se-pos-perceptron.bin'],
    }
    for lang in langlist:
        for file in lang_map.get(lang, []):
            if not os.path.isfile(os.path.join(OPENNLP_MODELS_DIR, file)):
                try:
                    download_file("{0}/{1}".format(opennlp_url, file), desc=OPENNLP_MODELS_DIR)
                except urllib2.HTTPError, exc:
                    logger.error(exc.message)


@init
def initialize(project):
    project.depends_on_requirements("requirements.txt")
    global install_dir
    install_dir = project.get_property('install_dir')
    if install_dir is None:
        project.set_property('install_dir', os.getcwd())
    if not (os.path.exists(install_dir) and os.path.isdir(install_dir)):
        os.mkdir(install_dir)
    install_dir = os.path.realpath(install_dir)
    os.chdir(install_dir)


@task
def setup_treetagger(logger):
    logger.info('Downloading and setting up TreeTagger')
    if os.path.exists(TREETAGGER_DIR) and os.path.isdir(TREETAGGER_DIR):
        shutil.rmtree(TREETAGGER_DIR)
    os.mkdir(TREETAGGER_DIR)
    treetagger_install_dir = os.path.join(os.getcwd(), TREETAGGER_DIR)
    os.environ['TREETAGGER_PATH'] = treetagger_install_dir
    if sys.platform.startswith("win"):
        get_file(treetagger_win, treetagger_url + treetagger_win, TREETAGGER_DIR, logger)
        extract_file(treetagger_win, TREETAGGER_DIR)
    elif sys.platform.startswith("linux"):
        get_file(treetagger_linux, treetagger_url + treetagger_linux, TREETAGGER_DIR, logger)
        get_file("tagger-scripts.tar.gz", treetagger_url + "tagger-scripts.tar.gz", TREETAGGER_DIR, logger)
        download_treetagger_files(languages, logger)
        get_file("install-tagger.sh", treetagger_url + "install-tagger.sh", TREETAGGER_DIR, logger)
        os.chmod(os.path.join(treetagger_install_dir, 'install-tagger.sh'), 0777)
        os.chdir(treetagger_install_dir)
        subprocess.Popen(['bash', 'install-tagger.sh'])
        # Return to installation directory
        dirname = os.path.dirname(os.getcwd())
        os.chdir(dirname)
    logger.info("Done")


@task
def setup_opennlp(logger):
    logger.info('Downloading OpenNLP')
    if os.path.exists(OPENNLP_DIR) and os.path.isdir(OPENNLP_DIR):
        shutil.rmtree(OPENNLP_DIR)
    opennlp_filename = opennlp_file.split("/")[-1]
    get_file(opennlp_filename, opennlp_file, None, logger)
    extracted_dir = extract_file(opennlp_filename, None)
    os.remove(opennlp_filename)
    os.rename(extracted_dir, OPENNLP_DIR)
    for root, dirs, files in os.walk(os.path.join(OPENNLP_DIR, 'bin')):
        for file in files:
            os.chmod(os.path.join(root, file), 0777)
    logger.info('Downloading OpenNLP models for selected languages')
    if not (os.path.exists(OPENNLP_MODELS_DIR) and os.path.isdir(OPENNLP_MODELS_DIR)):
        os.mkdir(OPENNLP_MODELS_DIR)
    download_opennlp_files(languages, logger)
    # Download additional nl-chunker for dutch language
    if 'nl' in languages:
        get_file('nl-chunker.bin', 'https://github.com/jodaiber/model-quickstarter/raw/master/nl/nl-chunker.bin',
                 OPENNLP_MODELS_DIR, logger)
    logger.info("Done")


@task
def setup_opendutchwordnet(logger):
    if 'nl' in languages:
        # Clone OpenDutchWordnet
        logger.info('Cloning OpenDutchWordnet repository')
        repo_dir = "OpenDutchWordnet"
        if os.path.isdir(repo_dir):
            shutil.rmtree(repo_dir)
        os.mkdir(repo_dir)

        repo = Repo.init(repo_dir)
        origin = repo.create_remote('origin', "https://github.com/cltl/OpenDutchWordnet.git")
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)
        logger.info('Done')


@task
def copy_files(logger):
    logger.info("Copying required files..")
    srcdir, filename = os.path.split(os.path.abspath(__file__))
    global install_dir
    shutil.copy(os.path.join(srcdir, 'chunkers.py'), install_dir)
    shutil.copy(os.path.join(srcdir, 'taggers.py'), install_dir)
    # Copy test files
    shutil.copy(os.path.join(srcdir, 'tests.py'), install_dir)
    shutil.copy(os.path.join(srcdir, 'tox.ini'), install_dir)
    # Copy all Jupyter Notebook files
    for file in glob.iglob(os.path.join(srcdir, "*.ipynb")):
        shutil.copy(file, install_dir)
    logger.info("Done")


@task
def create_sandbox(logger):
    setup_treetagger(logger)
    setup_opennlp(logger)
    setup_opendutchwordnet(logger)
    copy_files(logger)




