# FanNetworking

This base layer delivers the "Ubuntu fan" that is an extension of the network
tunnel driver in the Linux kernel.

Containers enable dense virtualization, it is easy to run hundreds or thousands
of containers on a single host machine. All of these containers need an IP
address and one solution is to use the fan.

The fan is a mapping between a smaller network address space (typically a /16
network) and a larger one (typically a /8), which assigns subnets from the
larger one to IP addresses on the smaller one, and enables automatic and simple
tunnelling and routing between systems on the larger address space.

The fan trades access to one user-selected /8 (potentially external) address
range for an expanded pool of addresses to be used by containers or virutal
machines. Fan does this by mapping the addresses in a way that can be computed,
rather than one that requires maintenance of distributed state.

For more information go to the [Ubuntu wiki page about Fan
networking](https://wiki.ubuntu.com/FanNetworking)

# Usage

This is designed to be a layer that can be built in to charms for docker or LXD. Just add this layer to your `layer.yaml` and build it into your solution.

    charm build -s xenial

> The fan technology is planned to be in the 16.04 (xenial release) of Ubuntu.

# States

The fan layer makes use of the reactive framework by setting states when
important events occur. The fan layer sets the following states that other
layers can consume:

**fan.installed** - Indicates the fan technology is installed and ready to be
configured.

**fan.configured** - Indicates the fan has been configured and is ready to
route traffic.

# Configuration

This layer exposes a number of configuration options:

**overlay** - The overlay network cidr to use for fan. An overlay network is a
computer network built on top of other networks. Nodes in the overlay network
are thought of connected by virtual links.

**underlay** - The underlay network cidr to use for fan. The underlay network
is the network addresses that are given to the containers by the host.


# Contact Information

The fan was conceived by Mark Shuttleworth and John Meinel, and implemented by
Jay Vosburgh and Andy Whitcroft.

## Upstream Project Name

- [Ubuntu Fan Wiki page](https://wiki.ubuntu.com/FanNetworking)
- [Introducing the Fan](https://insights.ubuntu.com/2015/06/24/introducing-the-fan-simpler-container-networking/)
- [Container to Container networking](http://blog.dustinkirkland.com/2015/06/the-bits-have-hit-fan.html)
