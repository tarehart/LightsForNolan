plugins {
    kotlin("jvm") version "2.1.10"
}

group = "com.tarehart"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.hid4java:hid4java:0.8.0")

    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}
kotlin {
    jvmToolchain(17)
}

tasks.register<JavaExec>("run") {
    group = "application"
    description = "Runs the main application"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.tarehart.MainKt")
}
