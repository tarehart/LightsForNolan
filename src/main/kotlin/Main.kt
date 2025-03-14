package com.tarehart

import com.tarehart.com.tarehart.animation.BouncyBallAnimation
import com.tarehart.com.tarehart.draw.ImageLibrary
import com.tarehart.com.tarehart.wled.PixelPusher
import com.tarehart.com.tarehart.wled.WledInterface
import com.tarehart.com.tarehart.model.SerpentinePixelMap
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.websocket.*
import io.ktor.http.*
import io.ktor.websocket.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import java.awt.Color
import java.awt.Rectangle


const val wledHost = "192.168.0.109"
const val udpPort = 21324

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
fun main() {

    val client = HttpClient(CIO) {
        install(WebSockets)
    }

    val width = 18
    val height = 11

    val udpInterface = WledInterface(wledHost, udpPort)
    val pixelPusher = PixelPusher(SerpentinePixelMap(width, height), udpInterface)
    val animation = BouncyBallAnimation(Rectangle(0, 0, width, height))
    val frameMillis = 50L

    runBlocking {
        client.webSocket(method = HttpMethod.Get, host = wledHost, port = 80, path = "/ws") {
            async(Dispatchers.IO) {
                while(true) {
                    val othersMessage = incoming.receive() as? Frame.Text
                    println(othersMessage?.readText())
                }
            }

            pixelPusher.buffer.clearAll()
            pixelPusher.sendOpaquePixels()

            pixelPusher.buffer.drawText("Hello", -1, 9, Color.GREEN, 9)
            pixelPusher.sendOpaquePixels()
            delay(5000)

            pixelPusher.buffer.drawImage(ImageLibrary.flag)
            pixelPusher.sendAllPixels()
            delay(5000)

            while(true) {
                animation.step(frameMillis, pixelPusher.buffer)
                pixelPusher.sendOpaquePixels()
                delay(frameMillis)
            }
        }
    }
    client.close()

}
