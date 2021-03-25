import os
import signal
import subprocess
import time


# Місце де знаходиться url-shrtnr
PATH_SHRTNR = "~/labs/url-shrtnr-le-gushqua"

JAVA_HOME = "/usr/lib/jvm/java-15-openjdk"
CMD = f"{PATH_SHRTNR}/gradlew run -p {PATH_SHRTNR} -Dorg.gradle.java.home={JAVA_HOME}"

if __name__ == '__main__':
    app = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    time.sleep(30)
    os.killpg(os.getpgid(app.pid), signal.SIGTERM)