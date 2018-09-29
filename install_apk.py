import os
import shutil

import requests
from ptest.assertion import assert_equals
from ptest.plogger import preporter

JENKINS_HOST_ANDROID = "http://10.128.42.168:8080"
USERNAME = 'mobileauto'
PASSWORD = 'password'


class Jenkins:
    def __init__(self):
        self._session = self.get_login_session()

        self.env = "qa"
        self.type = "debug"
        self.product = "smartenglish"

        type = "daily"

        if type == "release":

            self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-android-release/lastSuccessfulBuild/api/json"
        elif type == "daily":
            self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-ec-testing/lastSuccessfulBuild/api/json"

    def get_login_session(self):
        data = {
            'j_username': USERNAME,
            'j_password': PASSWORD,
            'from': '/',
            'Submit': 'log in',
            'json': '{"j_username": "mobileauto", "j_password": "password", "remember_me": false, "from": "/"}'
        }

        session = requests.Session()
        response = session.post(JENKINS_HOST_ANDROID + '/j_acegi_security_check', data=data)

        try:
            assert_equals(response.status_code, 200)

            return session
        except:
            raise ("cannot login jenkins server!")

    def get_build_url(self, debug=True):
        preporter.info(self.Jenkins_build_url)

        try:
            builds_urls = self._session.get(self.Jenkins_build_url)

            builds = [each_build['relativePath'] for each_build in builds_urls.json()['artifacts']]
            preporter.info("build detail info: \n %s " % builds)

            build_type = 'debug' if debug else 'release'
            current_build = list(filter(
                lambda b: b.lower() == "engage/build/outputs/apk/{}{}/{}/engage-{}-{}-{}.apk".format(self.product,
                                                                                                     self.env,
                                                                                                     build_type,
                                                                                                     self.product,
                                                                                                     self.env,
                                                                                                     build_type).lower(),
                builds))[0]

            preporter.info("current build: %s" % current_build)

            if current_build:
                apk_url = builds_urls.json()['url'].replace("165","168") + "artifact/" + current_build
                apk_name = current_build.split("/")[-1]
                preporter.info(apk_url)
                preporter.info(apk_name)
                return apk_url, apk_name

            else:
                preporter.info("cannot find the build")

        except:
            preporter.info(
                "cannot access the {url} of jenkins, please check your jenkins!".format(url=self.Jenkins_build_url))

    def check_folder(sef, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    def is_apk_exist(self, path):
        if os.path.isfile(path) and path.endswith('apk'):
            preporter.info("{file} exist".format(file=path))
            return True

        else:
            preporter.info("{file} does't exist".format(file=path))
            return False

    def download_file(self, url, path):
        try:
            file = self._session.get(url).content
            with open(path, 'wb') as f:
                f.write(file)
        except:
            preporter.info("Download file from jenkins {url} fail, please check your jenkins".format(url=url))

    def download_build(self, apk_local_path, apk_name=None, debug=True):
        apk_url, apk_name_from_jenkins = self.get_build_url(debug)
        self.check_folder(apk_local_path)
        file_local_abs_path = os.path.join(apk_local_path, apk_name if apk_name else apk_name_from_jenkins)
        self.download_file(apk_url, file_local_abs_path)

        if self.is_apk_exist(file_local_abs_path):
            preporter.info("Download file {file} success!".format(file=file_local_abs_path))

        else:
            preporter.info("Download file {file} fail!".format(file=file_local_abs_path))


if __name__ == '__main__':
    apk_path = "/Users/anderson/Downloads/builds"
    jen = Jenkins()
    jen.download_build(apk_path)
