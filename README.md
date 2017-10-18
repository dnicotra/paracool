# paracool

paracool is a live GNU\Linux distribution based on Debian that allows to build an MPI cluster over an existing network.

It is in early developing state. No prealpha/alpha/beta version are avaiable in this repository. I'm going to keep this repo updated with my last "working" developing version.

## Building

If you want to build this early stage of the project, just install Debian Live and clone the repo. Then
```
lb clean --purge
lb config
lb build
```
It will produce an iso-hybrid bootable image. I can't guarantee anything!
