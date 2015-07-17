Output of `lshw` on my [Compaq Presario CQ61](LinuxOnCompaqPresarioCQ61.md):

```
rose
    description: Notebook
    product: Presario CQ61 Notebook PC
    vendor: Hewlett-Packard
    version: 0396100000010D10000000000
    serial: CNF94536QF
    width: 32 bits
    capabilities: smbios-2.6 dmi-2.6
    configuration: boot=normal chassis=notebook uuid=434E4639-3435-3336-5146-00269E8D2CBB
  *-core
       description: Motherboard
       product: 363F
       vendor: Quanta
       physical id: 0
       version: 42.14
       serial: Base Board Serial Number
       slot: Base Board Chassis Location
     *-firmware
          description: BIOS
          vendor: Hewlett-Packard
          physical id: 0
          version: F.07 (10/10/2009)
          size: 1MiB
          capacity: 1984KiB
          capabilities: isa pci pnp upgrade shadowing escd cdboot bootselect int5printscreen int9keyboard int14serial int17printer acpi usb agp smartbattery biosbootspecification
     *-cpu
          description: CPU
          product: AMD Sempron(tm) M100
          vendor: Advanced Micro Devices [AMD]
          physical id: c
          bus info: cpu@0
          version: 15.6.2
          serial: NotSupport
          slot: Socket S1G3
          size: 2GHz
          capacity: 2GHz
          width: 64 bits
          clock: 200MHz
          capabilities: fpu fpu_exception wp vme de pse tsc msr pae mce cx8 apic mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx mmxext fxsr_opt pdpe1gb rdtscp x86-64 3dnowext 3dnow constant_tsc up nonstop_tsc extd_apicid pni monitor cx16 popcnt lahf_lm svm extapic cr8_legacy abm sse4a 3dnowprefetch osvw ibs skinit wdt cpufreq
        *-cache:0 DISABLED
             description: L1 cache
             physical id: d
             slot: L1 Cache
             size: 128KiB
             capacity: 128KiB
             capabilities: pipeline-burst internal write-through unified
        *-cache:1
             description: L1 cache
             physical id: e
             slot: L2 Cache
             size: 512KiB
             capacity: 512KiB
             capabilities: pipeline-burst internal write-back unified
     *-memory
          description: System Memory
          physical id: 10
          slot: System board or motherboard
          size: 2GiB
        *-bank:0
             description: DIMM DDR2 Synchronous 800 MHz (1.2 ns)
             product: HMP112S6EFR6C-S6
             vendor: Hynix
             physical id: 0
             serial: AD000000000000000109415151952F
             slot: Bottom - Slot 1 (top)
             size: 1GiB
             width: 64 bits
             clock: 800MHz (1.2ns)
        *-bank:1
             description: DIMM DDR2 Synchronous 800 MHz (1.2 ns)
             product: HMP112S6EFR6C-S6
             vendor: Hynix
             physical id: 1
             serial: AD000000000000000109415111990E
             slot: Bottom - Slot 2 (under)
             size: 1GiB
             width: 64 bits
             clock: 800MHz (1.2ns)
     *-pci:0
          description: Host bridge
          product: RS780 Host Bridge Alternate
          vendor: Advanced Micro Devices [AMD]
          physical id: 100
          bus info: pci@0000:00:00.0
          version: 00
          width: 32 bits
          clock: 66MHz
        *-pci:0
             description: PCI bridge
             product: Hewlett-Packard Company
             vendor: Hewlett-Packard Company
             physical id: 1
             bus info: pci@0000:00:01.0
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: pci ht bus_master cap_list
             resources: ioport:3000(size=4096) memory:90200000-903fffff ioport:80000000(size=268435456)
           *-display
                description: VGA compatible controller
                product: M880G [Mobility Radeon HD 4200]
                vendor: ATI Technologies Inc
                physical id: 5
                bus info: pci@0000:01:05.0
                version: 00
                width: 32 bits
                clock: 33MHz
                capabilities: pm msi bus_master cap_list rom
                configuration: driver=radeon latency=0
                resources: irq:18 memory:80000000-8fffffff(prefetchable) ioport:3000(size=256) memory:90300000-9030ffff memory:90200000-902fffff
           *-multimedia
                description: Audio device
                product: RS880 Audio Device [Radeon HD 4200]
                vendor: ATI Technologies Inc
                physical id: 5.1
                bus info: pci@0000:01:05.1
                version: 00
                width: 32 bits
                clock: 33MHz
                capabilities: pm msi bus_master cap_list
                configuration: driver=HDA Intel latency=0
                resources: irq:19 memory:90310000-90313fff
        *-pci:1
             description: PCI bridge
             product: RS780 PCI to PCI bridge (PCIE port 1)
             vendor: Advanced Micro Devices [AMD]
             physical id: 5
             bus info: pci@0000:00:05.0
             version: 00
             width: 32 bits
             clock: 33MHz
             capabilities: pci pm pciexpress msi ht bus_master cap_list
             configuration: driver=pcieport
             resources: irq:25 memory:90100000-901fffff
           *-network
                description: Wireless interface
                product: AR9285 Wireless Network Adapter (PCI-Express)
                vendor: Atheros Communications Inc.
                physical id: 0
                bus info: pci@0000:02:00.0
                logical name: wlan0
                version: 01
                serial: 00:22:68:8e:86:1c
                width: 64 bits
                clock: 33MHz
                capabilities: pm msi pciexpress bus_master cap_list ethernet physical wireless
                configuration: broadcast=yes driver=ath9k latency=0 multicast=yes wireless=IEEE 802.11bgn
                resources: irq:17 memory:90100000-9010ffff
        *-pci:2
             description: PCI bridge
             product: RS780 PCI to PCI bridge (PCIE port 2)
             vendor: Advanced Micro Devices [AMD]
             physical id: 6
             bus info: pci@0000:00:06.0
             version: 00
             width: 32 bits
             clock: 33MHz
             capabilities: pci pm pciexpress msi ht bus_master cap_list
             configuration: driver=pcieport
             resources: irq:26 ioport:2000(size=4096) memory:70000000-700fffff ioport:90000000(size=1048576)
           *-network
                description: Ethernet interface
                product: RTL8101E/RTL8102E PCI Express Fast Ethernet controller
                vendor: Realtek Semiconductor Co., Ltd.
                physical id: 0
                bus info: pci@0000:03:00.0
                logical name: eth0
                version: 02
                serial: 00:26:9e:8d:2c:bb
                size: 100MB/s
                capacity: 100MB/s
                width: 64 bits
                clock: 33MHz
                capabilities: pm msi pciexpress msix vpd bus_master cap_list rom ethernet physical tp mii 10bt 10bt-fd 100bt 100bt-fd autonegotiation
                configuration: autonegotiation=on broadcast=yes driver=r8169 driverversion=2.3LK-NAPI duplex=full ip=192.168.1.175 latency=0 link=yes multicast=yes port=MII speed=100MB/s
                resources: irq:27 ioport:2000(size=256) memory:90010000-90010fff(prefetchable) memory:90000000-9000ffff(prefetchable) memory:90020000-9002ffff(prefetchable)
        *-storage
             description: SATA controller
             product: SB700/SB800 SATA Controller [AHCI mode]
             vendor: ATI Technologies Inc
             physical id: 11
             bus info: pci@0000:00:11.0
             logical name: scsi0
             logical name: scsi1
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: storage pm bus_master cap_list emulated
             configuration: driver=ahci latency=64
             resources: irq:22 ioport:4038(size=8) ioport:404c(size=4) ioport:4030(size=8) ioport:4048(size=4) ioport:4010(size=16) memory:90408000-904083ff
           *-disk
                description: ATA Disk
                product: TOSHIBA MK2555GS
                vendor: Toshiba
                physical id: 0
                bus info: scsi@0:0.0.0
                logical name: /dev/sda
                version: FG00
                serial: X97BFS8BS
                size: 232GiB (250GB)
                capabilities: partitioned partitioned:dos
                configuration: ansiversion=5 signature=0004dab1
              *-volume:0
                   description: EXT4 volume
                   vendor: Linux
                   physical id: 1
                   bus info: scsi@0:0.0.0,1
                   logical name: /dev/sda1
                   logical name: /
                   version: 1.0
                   serial: 2aa602b2-9cab-4686-9f9e-37437e63b55f
                   size: 227GiB
                   capacity: 227GiB
                   capabilities: primary bootable journaled extended_attributes large_files huge_files dir_nlink extents ext4 ext2 initialized
                   configuration: created=2010-06-04 13:35:07 filesystem=ext4 lastmountpoint=/~ï¿½ï¿½ï¿½0ï¿½ï¿½uï¿½ï¿½ï¿½ï¿½ï¿½pï¿½ï¿½ï¿½u^ ï¿½U/ï¿½dï¿½ï¿½ï¿½~!ï¿½ï¿½hï¿½ï¿½ï¿½hï¿½ï¿½ï¿½0ï¿½Ì¾ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½a modified=2010-06-05 05:59:36 mount.fstype=ext4 mount.options=rw,relatime,errors=remount-ro,barrier=1,data=ordered mounted=2010-06-06 10:36:59 state=mounted
              *-volume:1
                   description: Extended partition
                   physical id: 2
                   bus info: scsi@0:0.0.0,2
                   logical name: /dev/sda2
                   size: 5146MiB
                   capacity: 5146MiB
                   capabilities: primary extended partitioned partitioned:extended
                 *-logicalvolume
                      description: Linux swap / Solaris partition
                      physical id: 5
                      logical name: /dev/sda5
                      capacity: 5146MiB
                      capabilities: nofs
           *-cdrom
                description: DVD-RAM writer
                product: CDDVDW TS-L633M
                vendor: hp
                physical id: 1
                bus info: scsi@1:0.0.0
                logical name: /dev/cdrom
                logical name: /dev/cdrw
                logical name: /dev/dvd
                logical name: /dev/dvdrw
                logical name: /dev/scd0
                logical name: /dev/sr0
                version: 0301
                capabilities: removable audio cd-r cd-rw dvd dvd-r dvd-ram
                configuration: ansiversion=5 status=nodisc
        *-usb:0
             description: USB Controller
             product: SB700/SB800 USB OHCI0 Controller
             vendor: ATI Technologies Inc
             physical id: 12
             bus info: pci@0000:00:12.0
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: bus_master
             configuration: driver=ohci_hcd latency=64
             resources: irq:16 memory:90407000-90407fff
        *-usb:1
             description: USB Controller
             product: SB700 USB OHCI1 Controller
             vendor: ATI Technologies Inc
             physical id: 12.1
             bus info: pci@0000:00:12.1
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: bus_master
             configuration: driver=ohci_hcd latency=64
             resources: irq:16 memory:90406000-90406fff
        *-usb:2
             description: USB Controller
             product: SB700/SB800 USB EHCI Controller
             vendor: ATI Technologies Inc
             physical id: 12.2
             bus info: pci@0000:00:12.2
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: pm debug bus_master cap_list
             configuration: driver=ehci_hcd latency=64
             resources: irq:17 memory:90408500-904085ff
        *-usb:3
             description: USB Controller
             product: SB700/SB800 USB OHCI0 Controller
             vendor: ATI Technologies Inc
             physical id: 13
             bus info: pci@0000:00:13.0
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: bus_master
             configuration: driver=ohci_hcd latency=64
             resources: irq:18 memory:90405000-90405fff
        *-usb:4
             description: USB Controller
             product: SB700 USB OHCI1 Controller
             vendor: ATI Technologies Inc
             physical id: 13.1
             bus info: pci@0000:00:13.1
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: bus_master
             configuration: driver=ohci_hcd latency=64
             resources: irq:18 memory:90404000-90404fff
        *-usb:5
             description: USB Controller
             product: SB700/SB800 USB EHCI Controller
             vendor: ATI Technologies Inc
             physical id: 13.2
             bus info: pci@0000:00:13.2
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: pm debug bus_master cap_list
             configuration: driver=ehci_hcd latency=64
             resources: irq:19 memory:90408400-904084ff
        *-serial UNCLAIMED
             description: SMBus
             product: SBx00 SMBus Controller
             vendor: ATI Technologies Inc
             physical id: 14
             bus info: pci@0000:00:14.0
             version: 3c
             width: 32 bits
             clock: 66MHz
             capabilities: ht cap_list
             configuration: latency=0
        *-multimedia
             description: Audio device
             product: SBx00 Azalia (Intel HDA)
             vendor: ATI Technologies Inc
             physical id: 14.2
             bus info: pci@0000:00:14.2
             version: 00
             width: 64 bits
             clock: 33MHz
             capabilities: pm bus_master cap_list
             configuration: driver=HDA Intel latency=64
             resources: irq:16 memory:90400000-90403fff
        *-isa
             description: ISA bridge
             product: SB700/SB800 LPC host controller
             vendor: ATI Technologies Inc
             physical id: 14.3
             bus info: pci@0000:00:14.3
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: isa bus_master
             configuration: latency=0
        *-pci:3
             description: PCI bridge
             product: SBx00 PCI to PCI Bridge
             vendor: ATI Technologies Inc
             physical id: 14.4
             bus info: pci@0000:00:14.4
             version: 00
             width: 32 bits
             clock: 66MHz
             capabilities: pci bus_master
     *-pci:1
          description: Host bridge
          product: K10 [Opteron, Athlon64, Sempron] HyperTransport Configuration
          vendor: Advanced Micro Devices [AMD]
          physical id: 101
          bus info: pci@0000:00:18.0
          version: 00
          width: 32 bits
          clock: 33MHz
     *-pci:2
          description: Host bridge
          product: K10 [Opteron, Athlon64, Sempron] Address Map
          vendor: Advanced Micro Devices [AMD]
          physical id: 102
          bus info: pci@0000:00:18.1
          version: 00
          width: 32 bits
          clock: 33MHz
     *-pci:3
          description: Host bridge
          product: K10 [Opteron, Athlon64, Sempron] DRAM Controller
          vendor: Advanced Micro Devices [AMD]
          physical id: 103
          bus info: pci@0000:00:18.2
          version: 00
          width: 32 bits
          clock: 33MHz
     *-pci:4
          description: Host bridge
          product: K10 [Opteron, Athlon64, Sempron] Miscellaneous Control
          vendor: Advanced Micro Devices [AMD]
          physical id: 104
          bus info: pci@0000:00:18.3
          version: 00
          width: 32 bits
          clock: 33MHz
     *-pci:5
          description: Host bridge
          product: K10 [Opteron, Athlon64, Sempron] Link Control
          vendor: Advanced Micro Devices [AMD]
          physical id: 105
          bus info: pci@0000:00:18.4
          version: 00
          width: 32 bits
          clock: 33MHz
  *-battery
       product: EV06047
       vendor: CPT-U22F
       physical id: 1
       version: Unknown
       serial: Unknown
       slot: Primary
       capacity: 48840mWh
       configuration: voltage=11.1V

```