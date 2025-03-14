package com.tarehart.com.tarehart.animation

import com.tarehart.com.tarehart.draw.LedDrawBuffer
import com.tarehart.com.tarehart.draw.RainbowVendor
import java.awt.Color
import java.awt.Rectangle
import java.time.Instant

class BouncyBallAnimation(bounds: Rectangle) {

    var x = 0
    var y = 0

    var vx = 1
    var vy = 1

    val rainbowVendor = RainbowVendor(20)
    val ballSize = 3
    val ballBounds = Rectangle(bounds.x, bounds.y, bounds.width - ballSize, bounds.height - ballSize)

    fun step(elapsedMillis: Long, drawBuffer: LedDrawBuffer) {
        x += vx
        y += vy

        if (y > ballBounds.maxY) {
            vy *= -1
            y = ballBounds.maxY.toInt()
        }
        if (y < ballBounds.minY) {
            vy *= -1
            y = ballBounds.minY.toInt()
        }
        if (x > ballBounds.maxX) {
            vx *= -1
            x = ballBounds.maxX.toInt()
        }
        if (x < ballBounds.minX) {
            vx *= -1
            x = ballBounds.minX.toInt()
        }

        if (Instant.now().epochSecond % 10 > 2) {
            drawBuffer.fillRect(x, y, 3, 3, rainbowVendor.nextColor())
        } else {
            drawBuffer.fillRect(x, y, 5, 5, Color.BLACK)
        }

    }
}