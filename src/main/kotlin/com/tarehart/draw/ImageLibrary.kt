package com.tarehart.com.tarehart.draw

import java.awt.image.BufferedImage
import java.io.FileNotFoundException
import javax.imageio.ImageIO

object ImageLibrary {

    val flag: BufferedImage = javaClass.getResourceAsStream("/flag.png")
        ?.let { stream -> ImageIO.read(stream) }
        ?: throw FileNotFoundException("Could not find image")

}