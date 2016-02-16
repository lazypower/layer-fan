from charms import layer
from charms.reactive import when, when_not, set_state
from charmhelpers.core.hookenv import status_set, config
from charmhelpers.fetch import apt_install

from shlex import split
from subprocess import check_call


@when_not('fan.installed')
def install_fan_modules():
    '''Installs the fan networking modules from the archive.'''
    pkgs = ['ubuntu-fan']
    apt_install(pkgs, fatal=True)
    set_state('fan.installed')


@when('fan.installed')
def configure_fan():
    '''Configure the fan settings when the values change.'''
    options = config()
    if options.changed('overlay') or options.changed('underlay'):
        # Load all the options for the fan layer.
        layer_options = layer.options('fan')
        fan_type = layer_options['fan-type']
        if fan_type in ['lxd', 'docker']:
            enable_fan(fan_type, options)
            status_set('active', '{0} fan network configured'.format(fan_type))
            set_state('fan.configured')


def enable_fan(fan_type, options):
    '''Configure the fan by type and with the current configuration options
    removing the old configuration if it exists.'''
    previous_overlay = options.previous('overlay')
    previous_underlay = options.previous('underlay')
    if previous_overlay and previous_underlay:
        cmd = 'fanatic disable-{0} {1} {2}'.format(fan_type, previous_overlay,
                                                   previous_underlay)
        print(cmd)
        check_call(split(cmd))
    overlay = options('overlay')
    underlay = options('underlay')
    if overlay and underlay:
        cmd = 'fanatic enable-{0} {1} {2}'.format(fan_type, overlay, underlay)
        print(cmd)
        check_call(split(cmd))
