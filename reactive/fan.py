from charms import layer
from charms.reactive import when, when_not, remove_state, set_state
from charmhelpers.core.hookenv import config, status_set
from charmhelpers.fetch import apt_install

from shlex import split
from subprocess import check_call


@when_not('fan.installed')
def install_fan_modules():
    '''Installs the fan networking modules from the archive.'''
    pkgs = ['ubuntu-fan']
    apt_install(pkgs, fatal=True)
    set_state('fan.installed')


@when('fan.installed', 'docker.installed')
@when_not('fan.configured')
def configure_docker():
    '''Configure docker for fan.'''
    enable_fan('docker', config())
    set_state('fan.configured')


@when('fan.installed', 'lxd.installed')
@when_not('fan.configured')
def configure_lxd():
    '''Configure lxd for fan.'''
    enable_fan('lxd', config())
    set_state('fan.configured')


@when('fan.configured')
def config_changed():
    '''When the config options change, unconfigure old settings.'''
    options = {k: config(k) for k in ['overlay', 'underlay']}
    if data_changed('fan.config', options):
        remove_state('fan.configured')


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
    overlay = options['overlay']
    underlay = options['underlay']
    if overlay and underlay:
        cmd = 'fanatic enable-{0} {1} {2}'.format(fan_type, overlay, underlay)
        print(cmd)
        check_call(split(cmd))
