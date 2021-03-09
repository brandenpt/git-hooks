/*
 * SPDX-License-Identifier: Unlicense
 *
 * This is free and unencumbered software released into the public domain.
 *
 * Anyone is free to copy, modify, publish, use, compile, sell, or
 * distribute this software, either in source code form or as a compiled
 * binary, for any purpose, commercial or non-commercial, and by any
 * means.
 *
 * In jurisdictions that recognize copyright laws, the author or authors
 * of this software dedicate any and all copyright interest in the
 * software to the public domain. We make this dedication for the benefit
 * of the public at large and to the detriment of our heirs and
 * successors. We intend this dedication to be an overt act of
 * relinquishment in perpetuity of all present and future rights to this
 * software under copyright law.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 * For more information, please refer to <http://unlicense.org>
 *
 */

plugins {
    id("com.pswidersk.python-plugin")

    id("ru.vyarus.use-python")

    id("org.kordamp.gradle.base")

    id("com.github.ben-manes.versions")
}


config {
    info {
        name = "BrandenPortal Git Hooks"
        description = "Client side git hooks used for the BrandenPortal gradle project structure."
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
