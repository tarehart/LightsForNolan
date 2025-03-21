package com.tarehart.wled

import com.tarehart.draw.LedDrawBuffer
import com.tarehart.model.SerpentinePixelMap
import java.awt.Color

class PixelPusher(
    private val pixelMap: SerpentinePixelMap,
    val wledInterface: WledInterface,
) {

    var buffer = LedDrawBuffer(pixelMap)

    fun sendOpaquePixels() {
        val pixels = buffer.getOpaquePixels()
        wledInterface.sendSpecificPixels(pixels)
        buffer = LedDrawBuffer(pixelMap)
    }

    fun sendAllPixels() {
        val pixels = buffer.getAllPixels()
        val pixelArray = Array<Color>(pixelMap.numPixels) { Color.BLACK }

        pixels.forEach {
            pixelArray[it.index] = it.color
        }

        wledInterface.sendAllPixels(pixelArray)
        buffer = LedDrawBuffer(pixelMap)
    }
}