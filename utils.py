import os
import sys
import signal
import subprocess

# Місце де знаходиться url-shrtnr
if sys.platform == 'win32':
    """Not Implemented"""
    HOME = os.getenv("HOME")
    PATH_SHRTNR = f"{HOME}/labs/url-shrtnr-le-gushqua"
    JAVA_HOME = "C:\\Program Files\\Java\\"
    CMD = f"{PATH_SHRTNR}\\gradlew.bat run -p {PATH_SHRTNR} -Dorg.gradle.java.home={JAVA_HOME}"
else:
    HOME = os.getenv("HOME")
    PATH_SHRTNR = f"{HOME}/labs/url-shrtnr-pepegasquad-tests"
    JAVA_HOME = "/usr/lib/jvm/java-15-openjdk"
    CMD = f"{PATH_SHRTNR}/gradlew run -p {PATH_SHRTNR} -Dorg.gradle.java.home={JAVA_HOME}"


def up_micronaut():
    app = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    return app


def down_micronaut(app):
    os.killpg(os.getpgid(app.pid), signal.SIGTERM)


def clean_db():
    if os.path.exists(f"{PATH_SHRTNR}/user-repository.json"):
        os.remove(f"{PATH_SHRTNR}/user-repository.json")
    if os.path.exists(f"{PATH_SHRTNR}/url-repository.json"):
        os.remove(f"{PATH_SHRTNR}/url-repository.json")
