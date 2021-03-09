pluginManagement {
    plugins {
        id("com.pswidersk.python-plugin") version "1.2.2"

        id("org.jetbrains.gradle.plugin.idea-ext") version "1.0"

        id("ru.vyarus.use-python") version "2.3.0"

        id("org.kordamp.gradle.base") version "0.44.0"

        id("com.github.ben-manes.versions") version "0.38.0"
    }

    repositories {
        mavenCentral()
        gradlePluginPortal()
        maven {
            url = uri("https://repo.spring.io/milestone")
        }
        maven {
            url = uri("https://plugins.gradle.org/m2")
        }
        maven {
            url = uri("https://dl.bintray.com/konform-kt/konform")
        }
        jcenter()
        google()
    }
}

rootProject.name = "git-hooks"
