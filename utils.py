import os
import signal
import subprocess
import time


# Місце де знаходиться url-shrtnr
HOME = os.getenv("HOME")
PATH_SHRTNR = f"{HOME}/labs/url-shrtnr-le-gushqua"

JAVA_HOME = "/usr/lib/jvm/java-15-openjdk"
CMD = f"{PATH_SHRTNR}/gradlew run -p {PATH_SHRTNR} -Dorg.gradle.java.home={JAVA_HOME}"


def up_micronaut():
    app = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    return app


def down_micronaut(app):
    os.killpg(os.getpgid(app.pid), signal.SIGTERM)


def clean_db():
    os.remove(f"{PATH_SHRTNR}/users.json")
    os.remove(f"{PATH_SHRTNR}/tokens.json")
    os.remove(f"{PATH_SHRTNR}/alias.json")