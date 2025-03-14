package com.tarehart.com.tarehart.wled

import com.tarehart.com.tarehart.model.IndexedPixel
import java.awt.Color
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress


/**
 * https://kno.wled.ge/interfaces/udp-realtime/
 *
 * In every protocol, Byte 1 tells the server how many seconds to wait after the last received packet before
 * returning to normal mode, in practice you should use 1-2 (seconds) here in most cases so that the module
 * returns to normal mode quickly after the end of transmission. Use 255 to stay on the UDP data without a
 * timeout until a request is requested via another method.
 */
class WledInterface(
    ipAddress: String,
    private val udpPort: Int
) {

    companion object {
        private const val WARLS_FORMAT: Byte = 1
        private const val DRGB_FORMAT: Byte = 2
    }


    private val address = InetAddress.getByName(ipAddress)
    private val udpSocket = DatagramSocket()

    /**
     * WARLS Byte Description
     * 2 + n*4	LED Index
     * 3 + n*4	Red Value
     * 4 + n*4	Green Value
     * 5 + n*4	Blue Value
     */
    fun sendSpecificPixels(pixels: Collection<IndexedPixel>, secondsToPersist: Int = 10) {

        require(secondsToPersist <= 255)

        val bytes = ByteArray(2 + pixels.size * 4)

        bytes[0] = WARLS_FORMAT
        bytes[1] = secondsToPersist.toByte()

        var index = 2
        pixels.forEach {
            bytes[index++] = it.index.toByte()
            bytes[index++] = it.color.red.toByte()
            bytes[index++] = it.color.green.toByte()
            bytes[index++] = it.color.blue.toByte()
        }

        val packet = DatagramPacket(bytes, bytes.size, address, udpPort)

        udpSocket.send(packet)
    }

    /**
     * DRGB
     *
     * Byte	Description
     * 2 + n*3	Red Value
     * 3 + n*3	Green Value
     * 4 + n*3	Blue Value
     */
    fun sendAllPixels(pixels: Array<Color>, secondsToPersist: Int = 10) {

        require(secondsToPersist <= 255)

        val bytes = ByteArray(2 + pixels.size * 3)

        bytes[0] = DRGB_FORMAT
        bytes[1] = secondsToPersist.toByte()

        var index = 2
        pixels.forEach {
            bytes[index++] = it.red.toByte()
            bytes[index++] = it.green.toByte()
            bytes[index++] = it.blue.toByte()
        }

        val packet = DatagramPacket(bytes, bytes.size, address, udpPort)

        udpSocket.send(packet)
    }

}