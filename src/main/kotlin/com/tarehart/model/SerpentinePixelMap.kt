package com.tarehart.com.tarehart.model

class SerpentinePixelMap (
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

    val numPixels = width * height

    fun getPixelIndex(row: Int, col: Int): Int {
        return serpentine[row][col]
    }
}