package com.tarehart.touch

import org.hid4java.HidManager
import org.hid4java.HidServicesSpecification
import org.junit.jupiter.api.Test

/**
 * Testing the ability to read data from a multi-touch overlay frame on Windows OS.
 *
 * So far I've been unable to read any data. Avenues of investigation:
 * - Using Wireshark + https://desowin.org/usbpcap/ to inspect the data flowing to / from the Windows driver and replicating
 * - Running as administrator
 */
class TouchOverlayTest {

    companion object {
        // These correspond to this multi-touch overlay product:
        // https://www.amazon.com/Point-Multi-Touch-Infrared-Screen-Overlay/dp/B07H5P6VY4
        // The values were taken from Device Manager (Windows)
        const val VENDOR_ID: Int = 0xAAEC
        const val PRODUCT_ID: Int = 0xC021
    }

    @Test
    fun testDevices() {
        val spec = HidServicesSpecification()
        val services = HidManager.getHidServices(spec)

        // There are four devices that match the vendor id and product ID:
        // 1. HID-compliant touch screen
        // 2. Microsoft Input Configuration Device
        // 3. HID-compliant mouse
        // 4. HID-compliant vendor-defined device
        val devices = services.attachedHidDevices
            .filter { it.vendorId == VENDOR_ID && it.productId == PRODUCT_ID }


        devices.forEach { device ->

            println("Attempting device $device")

            if (device.open()) {

                println("Opened device")
                device.setNonBlocking(true)

                // Corresponds to the data captured in wireshark
                val initializationReport = byteArrayOf(0x07, 0x02, 0x00)
                val reportBytesWritten = device.sendFeatureReport(initializationReport, 0x00)

                if (reportBytesWritten > 0) {
                    println("Successfully sent initialization report.")
                }

                val bytes = ByteArray(0x40)
                val numRead = device.read(bytes, 500)
                println("Num read: $numRead data: $bytes")

                if (numRead >= 0) {
                    for (i in 0..5) {
                        val nowRead = device.read(bytes, 500)
                        println(nowRead)
                        Thread.sleep(100)
                    }
                }

                device.close()
            }

        }
    }

}

/*

path = \VID_AAEC&PID_C021&MI_01&Col01\8&3a33fc1f&0&0000
- Not seen by hid4java, apparently
- Shows as "HID-compliant touch screen" in device manager


path=\\?\HID#VID_AAEC&PID_C021&MI_01&Col02#8&3a33fc1f&0&0001#{4d1e55b2-f16f-11cf-88cb-001111000030}
- Successfully sends init
- Shows as "Microsoft Input Configuration Device" in device manager
- Gives -1 on read


path=\\?\HID#VID_AAEC&PID_C021&MI_01&Col03#8&3a33fc1f&0&0002#{4d1e55b2-f16f-11cf-88cb-001111000030}
- This shows in device manager as "HID-compliant mouse"
- Fails to send init
- Gives -1 on read


path=\\?\HID#VID_AAEC&PID_C021&MI_00#8&165cbe5d&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}
- Fails to send init
- Gives 0 on read, consistently
- Appears as HID-compliant vendor-defined device in device manager
 */


/*
Data dump from USB Device Viewer
https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/usbview


[Port3]  :  USB Composite Device


Is Port User Connectable:         yes
Is Port Debug Capable:            no
Companion Port Number:            0
Companion Hub Symbolic Link Name:
Protocols Supported:
 USB 1.1:                         yes
 USB 2.0:                         yes
 USB 3.0:                         no

Device Power State:               PowerDeviceD0

       ---===>Device Information<===---
English product name: "Multi touch overlay device"

ConnectionStatus:
Current Config Value:              0x01  -> Device Bus Speed: Full (is not SuperSpeed or higher capable)
Device Address:                    0x06
Open Pipes:                           3

          ===>Device Descriptor<===
bLength:                           0x12
bDescriptorType:                   0x01
bcdUSB:                          0x0200
bDeviceClass:                      0x00  -> This is an Interface Class Defined Device
bDeviceSubClass:                   0x00
bDeviceProtocol:                   0x00
bMaxPacketSize0:                   0x40 = (64) Bytes
idVendor:                        0xAAEC = Vendor ID not listed with USB.org
idProduct:                       0xC021
bcdDevice:                       0x0200
iManufacturer:                     0x01
     English (United States)  "Multi touch  "
iProduct:                          0x02
     English (United States)  "Multi touch overlay device"
iSerialNumber:                     0x03
     English (United States)  "7F7E7CA70534"
bNumConfigurations:                0x01

          ---===>Open Pipes<===---

          ===>Endpoint Descriptor<===
bLength:                           0x07
bDescriptorType:                   0x05
bEndpointAddress:                  0x81  -> Direction: IN - EndpointID: 1
bmAttributes:                      0x03  -> Interrupt Transfer Type
wMaxPacketSize:                  0x0040 = 0x40 bytes
bInterval:                         0x01

          ===>Endpoint Descriptor<===
bLength:                           0x07
bDescriptorType:                   0x05
bEndpointAddress:                  0x01  -> Direction: OUT - EndpointID: 1
bmAttributes:                      0x03  -> Interrupt Transfer Type
wMaxPacketSize:                  0x0040 = 0x40 bytes
bInterval:                         0x01

          ===>Endpoint Descriptor<===
bLength:                           0x07
bDescriptorType:                   0x05
bEndpointAddress:                  0x82  -> Direction: IN - EndpointID: 2
bmAttributes:                      0x03  -> Interrupt Transfer Type
wMaxPacketSize:                  0x0040 = 0x40 bytes
bInterval:                         0x01

       ---===>Full Configuration Descriptor<===---

          ===>Configuration Descriptor<===
bLength:                           0x09
bDescriptorType:                   0x02
wTotalLength:                    0x0042  -> Validated
bNumInterfaces:                    0x02
bConfigurationValue:               0x01
iConfiguration:                    0x00
bmAttributes:                      0xA0  -> Bus Powered
  -> Remote Wakeup
MaxPower:                          0xFA = 500 mA

          ===>Interface Descriptor<===
bLength:                           0x09
bDescriptorType:                   0x04
bInterfaceNumber:                  0x00
bAlternateSetting:                 0x00
bNumEndpoints:                     0x02
bInterfaceClass:                   0x03  -> HID Interface Class
bInterfaceSubClass:                0x00
bInterfaceProtocol:                0x00
iInterface:                        0x00

          ===>HID Descriptor<===
bLength:                           0x09
bDescriptorType:                   0x21
bcdHID:                          0x0110
bCountryCode:                      0x00
bNumDescriptors:                   0x01
bDescriptorType:                   0x22 (Report Descriptor)
wDescriptorLength:               0x005F

          ===>Endpoint Descriptor<===
bLength:                           0x07
bDescriptorType:                   0x05
bEndpointAddress:                  0x81  -> Direction: IN - EndpointID: 1
bmAttributes:                      0x03  -> Interrupt Transfer Type
wMaxPacketSize:                  0x0040 = 0x40 bytes
bInterval:                         0x01

          ===>Endpoint Descriptor<===
bLength:                           0x07
bDescriptorType:                   0x05
bEndpointAddress:                  0x01  -> Direction: OUT - EndpointID: 1
bmAttributes:                      0x03  -> Interrupt Transfer Type
wMaxPacketSize:                  0x0040 = 0x40 bytes
bInterval:                         0x01

          ===>Interface Descriptor<===
bLength:                           0x09
bDescriptorType:                   0x04
bInterfaceNumber:                  0x01
bAlternateSetting:                 0x00
bNumEndpoints:                     0x01
bInterfaceClass:                   0x03  -> HID Interface Class
bInterfaceSubClass:                0x00
bInterfaceProtocol:                0x00
iInterface:                        0x00

          ===>HID Descriptor<===
bLength:                           0x09
bDescriptorType:                   0x21
bcdHID:                          0x0100
bCountryCode:                      0x00
bNumDescriptors:                   0x01
bDescriptorType:                   0x22 (Report Descriptor)
wDescriptorLength:               0x024B

          ===>Endpoint Descriptor<===
bLength:                           0x07
bDescriptorType:                   0x05
bEndpointAddress:                  0x82  -> Direction: IN - EndpointID: 2
bmAttributes:                      0x03  -> Interrupt Transfer Type
wMaxPacketSize:                  0x0040 = 0x40 bytes
bInterval:                         0x01

 */