package com.tarehart.touch

import javafx.application.Application
import javafx.scene.Scene
import javafx.scene.input.TouchEvent
import javafx.scene.layout.StackPane
import javafx.scene.text.Text
import javafx.stage.Stage


class TouchPane: Application() {
    override fun start(stage: Stage) {
        val label = Text("Touch Here")
        val root = StackPane(label)
        val scene = Scene(root, 400.0, 300.0)

        root.setOnTouchPressed { e: TouchEvent ->
            label.text = "Touched at: " + e.touchPoint.x + ", " + e.touchPoint.y
            println("Touch detected at " + e.touchPoint.x + ", " + e.touchPoint.y)
        }

        root.setOnTouchMoved { e: TouchEvent ->
            println("Touch moved: " + e.touchPoints)
        }

        scene.addEventFilter(TouchEvent.ANY) { event ->
            label.text = "Touch event detected: ${event.eventType}"
            println("Touch event: ${event.eventType}")
        }

        scene.setOnMouseMoved { event ->
            label.text = "Mouse moved ${event.x} ${event.y}"
        }


        stage.title = "Lights For Nolan"
        stage.scene = scene
        stage.isFullScreen = true
        stage.show()
    }
}