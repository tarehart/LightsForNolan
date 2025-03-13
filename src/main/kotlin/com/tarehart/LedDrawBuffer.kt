package com.tarehart.com.tarehart

import java.awt.Color
import java.awt.Graphics2D
import java.awt.image.BufferedImage
import java.awt.image.BufferedImage.TYPE_INT_ARGB

class LedDrawBuffer(
    val width: Int,
    val height: Int,
) {

    private val serpentine = Array(height) { Array(width) { 0 } }

    init {
        var ledIndex = 0

        for (col in 0 until width) {
            val range = 0 until height
            val serpentineRange = if (col % 2 == 0) range.reversed() else range
            for (row in serpentineRange) {
                serpentine[row][col] = ledIndex++
            }
        }
    }


    private var pendingImage = BufferedImage(width, height, TYPE_INT_ARGB)
    private var pendingGraphics = pendingImage.createGraphics()

    val graphics: Graphics2D
        get() = pendingGraphics


    fun drawImage(image: BufferedImage, x: Int = 0, y: Int = 0, width: Int = this.width, height: Int = this.height) {
        graphics.drawImage(image, x, y, width, height, null)
    }

    fun fillRect(x: Int, y: Int, width: Int, height: Int, color: Color) {
        graphics.color = color
        graphics.fillRect(x, y, width, height)
    }

    fun clearAll(color: Color = Color.BLACK) {
        fillRect(0, 0, this.width, this.height, color)
    }

    fun getPixelsRaw(): Collection<Pair<Int, Color>> {
        val pixels = pendingImage.getRGB(0, 0, width, height, null, 0, width)

        return pixels
            .mapIndexed { index, colorValue ->
                val row = index / width
                val col = index % width
                serpentine[row][col] to Color(colorValue, true)
            }
    }

    fun getPixelsToDraw(): Collection<Pair<Int, Color>> {
        return getPixelsRaw()
            .filter { it.second.alpha > 0 }
    }

    fun getByteArray(): ByteArray {
        val pixels = getPixelsRaw()
            .associate { it.first to it.second }

        val byteArray = ByteArray(height * width * 3)

        var index = 0
        for (ledIndex in 0 until height * width) {
            val color = pixels.getOrElse(ledIndex) { Color.BLACK }
            byteArray[index++] = color.red.toByte()
            byteArray[index++] = color.green.toByte()
            byteArray[index++] = color.blue.toByte()
        }

        return byteArray
    }

    fun prepareNextFrame() {
        pendingImage = BufferedImage(width, height, TYPE_INT_ARGB)
        pendingGraphics = pendingImage.createGraphics()
    }
}