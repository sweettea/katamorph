# katamorph
A tool to recover from a wholly full device with COW (copy-on-write) semantics without permanently adding storage, even when freeing space on that device requires writing to it. 

For instance, consider the situation where you have a COW device (e.g. dm-snapshot or dm-vdo) under a filesystem (e.g. xfs), and you accidentally fill the device and don't have additional storage to permanently dedicate to it. In order to delete files from the filesystem, those deletions must be journaled, which requires space on the device, posing a problem. 

This tool helps you recover from such a situation, using some free space elsewhere on the system (default to /tmp) temporarily, along with clever use of dm snapshots, to temporarily provide space, allowing you to delete files or otherwise free space in a complex stack.

Dependencies
---
This tool requires interacting with device-mapper in the kernel, which usually requires root. 

- device-mapper kernel and userspace tools
- [dmpy](https://github.com/bmr-cymru/dmpy)

Known limitations
---
The tool is not currently safe to interrupt after it has begun committing data.

Roadmap
---
The tool is currently at v0.0.

- v0.1 seeks to be feature-compatible with [vdorecover](https://github.com/jakszewa/vdorecover)
- v0.2 will feature greater user-friendliness, allowing the specification of more different forms of the full device's name and being able to automatically find a filesystem atop the specified device to remount and run fstrim on
- v0.3 will feature better checkpointing during the recovery process, allowing interruption and resumption at any point.
- v1.0 might feature a GUI? 
