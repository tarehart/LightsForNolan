package com.tarehart

import com.tarehart.com.tarehart.Animation
import com.tarehart.com.tarehart.LedDrawBuffer
import com.tarehart.com.tarehart.WledInterface
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.websocket.*
import io.ktor.http.*
import io.ktor.websocket.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import java.awt.Rectangle
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress


const val wledHost = "192.168.0.109"
const val udpPort = 21324

val address = InetAddress.getByName(wledHost)

val udpInterface = WledInterface(wledHost, udpPort)

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
fun main() {

    val client = HttpClient(CIO) {
        install(WebSockets)
    }

    val ledDiff = LedDrawBuffer(18, 11)
    val animation = Animation(Rectangle(0, 0, ledDiff.width, ledDiff.height))
    val frameMillis = 50
    val commandMillis = 10L

    runBlocking {
        client.webSocket(method = HttpMethod.Get, host = wledHost, port = 80, path = "/ws") {
            async(Dispatchers.IO) {
                while(true) {
                    val othersMessage = incoming.receive() as? Frame.Text
                    println(othersMessage?.readText())
                }
            }

            while(true) {
                animation.step(frameMillis, ledDiff)
                udpInterface.sendWarls(ledDiff)
                delay(33)

//                val commands = buildWebsocketCommands(ledDiff)
//                commands.forEach {
//                    send(it)
//                    println(it)
//                    delay(10)
//                }
//                if (commands.size > 1) {
//                    println("Multiple commands: " + commands.size)
//                }
//                delay(frameMillis - commands.size * commandMillis)
                ledDiff.prepareNextFrame()
            }
        }
    }
    client.close()

}

fun buildWebsocketCommands(ledDiff: LedDrawBuffer): List<String> {

    return ledDiff.getPixelsToDraw()
        .chunked(100)
        .map {
            val commandContent = it.joinToString(",") { (index, color) ->
                val hex = String.format("%02x%02x%02x", color.red, color.green, color.blue)
                """$index,"$hex""""
            }

            """
            {"seg":[{"i":[$commandContent]}]}
            """.trimIndent()
        }
}
