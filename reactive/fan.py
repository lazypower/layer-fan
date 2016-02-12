from charms.reactive import when, when_not, set_state
from charmhelpers.core.hookenv import status_set, config
from charmhelpers.fetch import apt_install

from shlex import split
from subprocess import check_call


@when_not('fan.installed')
def install_fan_modules():
    ''' Installs the fan networking modules from ARCHIVE '''
    pkgs = ['ubuntu-fan']
    apt_install(pkgs, fatal=True)
    set_state('fan.installed')

@when('fan.installed')
def configure_fan_overlay():
    '''Configure the fan settings when the values change.'''
    cfg = config()
    if cfg.changed('overlay') or cfg.changed('underlay'):
        overlay = config('overlay')
        underlay = config('underlay')
        # When the values are not empty strings.
        if overlay and underlay:
            # fanatic configure and deconfgiure are meant to be interactive.
            # Call fanatic enable-fan or enable-docker to run non-interactively.
            cmd = "fanatic enable-docker {0} {1}".format(overlay, underlay)
        else:
            cmd = "fanctl down -e"
        print(cmd)
        check_call(split(cmd))

        status_set('active', 'Fan network configured to: {}'.format(cmd))
    set_state('fan.configured')
    # do something with fan.configured state later.
