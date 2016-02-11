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
    cfg = config()
    if cfg.changed('overlay') or cfg.changed('underlay'):
        # caveate - this breaks if you juju unset the values
        cmd = "fanatic configure {0} {1}".format(config('overlay'),
                                                 config('underlay'))
        check_call(split(cmd))

    status_set('active', 'Configured fan networking with: {}'.format(cmd))
    set_state('fan.configured')
    # do something with that later
