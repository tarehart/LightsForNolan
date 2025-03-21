plugins {
    kotlin("jvm") version "2.1.10"
    id("org.openjfx.javafxplugin") version "0.1.0"
}

group = "com.tarehart"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.hid4java:hid4java:0.8.0")

//    val javafxVersion = "17.0.9" // Use latest version
//
//    implementation("org.openjfx:javafx-controls:$javafxVersion")
//    implementation("org.openjfx:javafx-fxml:$javafxVersion")
//    implementation("org.openjfx:javafx-base:$javafxVersion")

    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}
kotlin {
    jvmToolchain(17)
}

javafx {
    version = "17"
    modules("javafx.controls", "javafx.fxml")
}

tasks.register<JavaExec>("run") {
    group = "application"
    description = "Runs the main application"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.tarehart.MainKt")
}
