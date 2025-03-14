package com.tarehart

import com.tarehart.com.tarehart.animation.BouncyBallAnimation
import com.tarehart.com.tarehart.draw.ImageLibrary
import com.tarehart.com.tarehart.model.SerpentinePixelMap
import com.tarehart.com.tarehart.wled.PixelPusher
import com.tarehart.com.tarehart.wled.WledInterface
import java.awt.Color
import java.awt.Rectangle
import java.lang.Thread.sleep


const val wledHost = "192.168.0.109"
const val udpPort = 21324

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
fun main() {

    val width = 18
    val height = 11

    val udpInterface = WledInterface(wledHost, udpPort)
    val pixelPusher = PixelPusher(SerpentinePixelMap(width, height), udpInterface)
    val animation = BouncyBallAnimation(Rectangle(0, 0, width, height))
    val frameMillis = 50L

    pixelPusher.buffer.clearAll()
    pixelPusher.sendOpaquePixels()

    pixelPusher.buffer.drawText("Hello", -1, 9, Color.GREEN, 9)
    pixelPusher.sendOpaquePixels()
    sleep(5000)

    pixelPusher.buffer.drawImage(ImageLibrary.flag)
    pixelPusher.sendAllPixels()
    sleep(5000)

    while(true) {
        animation.step(frameMillis, pixelPusher.buffer)
        pixelPusher.sendOpaquePixels()
        sleep(frameMillis)
    }
}
