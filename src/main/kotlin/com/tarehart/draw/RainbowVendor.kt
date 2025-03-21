package com.tarehart.draw

import java.awt.Color
import java.util.concurrent.atomic.AtomicInteger

class RainbowVendor(private val segments: Int) {
    private val index = AtomicInteger(0)

    fun nextColor(): Color {
        val hue = (index.getAndIncrement() % segments) / segments.toFloat() // Normalize to [0, 1]
        return Color.getHSBColor(hue, 1.0f, 1.0f) // Full saturation and brightness
    }
}