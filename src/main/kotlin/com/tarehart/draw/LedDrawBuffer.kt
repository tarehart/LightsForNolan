package com.tarehart.draw

import com.tarehart.model.IndexedPixel
import com.tarehart.model.SerpentinePixelMap
import java.awt.Color
import java.awt.Font
import java.awt.image.BufferedImage

class LedDrawBuffer(
    private val pixelMap: SerpentinePixelMap
) {

    private val width = pixelMap.width
    private val height = pixelMap.height

    private val image = BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB)
    private val graphics = image.createGraphics()


    fun drawImage(image: BufferedImage, x: Int = 0, y: Int = 0, width: Int = this.width, height: Int = this.height) {
        graphics.drawImage(image, x, y, width, height, null)
    }

    fun fillRect(x: Int, y: Int, width: Int, height: Int, color: Color) {
        graphics.color = color
        graphics.fillRect(x, y, width, height)
    }

    fun drawText(text: String, x: Int, y: Int, color: Color, size: Int) {
        graphics.color = color
        graphics.font = Font("Default", Font.PLAIN, size)
        graphics.drawString(text, x, y)
    }

    fun clearAll(color: Color = Color.BLACK) {
        fillRect(0, 0, this.width, this.height, color)
    }

    fun getAllPixels(): Collection<IndexedPixel> {
        val pixels = image.getRGB(0, 0, width, height, null, 0, width)

        return pixels
            .mapIndexed { index, colorValue ->
                val row = index / width
                val col = index % width
                IndexedPixel(pixelMap.getPixelIndex(row, col), Color(colorValue, true))
            }
    }

    fun getOpaquePixels(): Collection<IndexedPixel> {
        return getAllPixels()
            .filter { it.color.alpha > 0 }
    }
}