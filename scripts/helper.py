import subprocess


def post_install():
    print("Running post-install actions...")
    subprocess.run("poetry run pre-commit install", shell=True, check=False)


def sonar():
    print("Running SonarQube...")
    sonar_url = "http://localhost:9000"
    subprocess.run(
        "poetry run pysonar-scanner -Dsonar.host.url=" + sonar_url,
        shell=True,
        check=False,
    )


def lint():
    print("Running linting actions...")
    subprocess.run("poetry run pre-commit run --all-files", shell=True, check=False)


if __name__ == "__main__":
    post_install()
