// TODO python-cli is outdated and and maybe abandoned

plugins {
    id("com.pswidersk.python-plugin")

    id("ru.vyarus.use-python")

    id("org.kordamp.gradle.base")

    id("com.github.ben-manes.versions")
}


config {
    info {
        name = "BrandenPortal Git Hooks"
        description = "Client side git hooks used for the BrandenPortal gradle project structure"
        inceptionYear = "2021"
        tags = listOf("bash", "python", "git", "hooks", "pre-commit")

        specification {
            version = "1.0.0"
        }
        implementation {
            version = "1.0.0"
        }
    }

    licensing {
        licenses {
            isInherits = false

            license {
                id = "MPL-2.0"
                name = "Mozilla Public License 2.0"
                url = "https://www.mozilla.org/en-US/MPL/2.0/"
                primary = true
            }
            license {
                id = "Unlicense"
                name = "The Unlicense"
                url = "https://unlicense.org/"
            }
        }
    }
}

python {
    minPythonVersion = "3.8"
}


pythonPlugin {
    pythonVersion.set("3.8.5")
}
