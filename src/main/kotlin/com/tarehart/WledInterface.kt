package com.tarehart.com.tarehart

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
    val ipAddress: String,
    val udpPort: Int
) {

    val address = InetAddress.getByName(ipAddress)
    val udpSocket = DatagramSocket()

    /**
     * Byte	Description
     * 2 + n*4	LED Index
     * 3 + n*4	Red Value
     * 4 + n*4	Green Value
     * 5 + n*4	Blue Value
     */
    fun sendWarls(drawBuffer: LedDrawBuffer) {

        val pixels = drawBuffer.getPixelsToDraw()
        val bytes = ByteArray(2 + pixels.size * 4)

        bytes[0] = 1
        bytes[1] = 2

        var index = 2
        pixels.forEach {
            bytes[index++] = it.first.toByte()
            bytes[index++] = it.second.red.toByte()
            bytes[index++] = it.second.green.toByte()
            bytes[index++] = it.second.blue.toByte()
        }

        val packet = DatagramPacket(bytes, bytes.size, address, udpPort)

        udpSocket.send(packet)
    }

}